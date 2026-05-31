# Health Checks

## Current setup

| Pod | Probe type | What it checks |
|---|---|---|
| PostgreSQL | `exec pg_isready` | DB is accepting connections on the right user/db |
| Django | `tcpSocket :8000` | Gunicorn port is open (process is alive) |

Django uses a TCP socket check — not an HTTP endpoint. The `/health/` app was removed
to keep the deployment simple. A TCP check is sufficient to detect a crashed Gunicorn process.

## Probe timings (django-deployment.yml)

**Readiness probe** (stops traffic to pod if failing):
- initialDelaySeconds: 30
- periodSeconds: 5
- timeoutSeconds: 3
- failureThreshold: 3 → pod marked unready after 15s of failures

**Liveness probe** (restarts pod if failing):
- initialDelaySeconds: 60
- periodSeconds: 10
- timeoutSeconds: 5
- failureThreshold: 3 → pod restarted after 30s of failures

## Checking probe status

```bash
# See probe results in pod description
kubectl describe pod <pod-name> -n alfa-romeo

# Watch pod readiness changes live
kubectl get pods -n alfa-romeo -w
```

## Troubleshooting CrashLoopBackOff

```bash
# Check what init container failed
kubectl logs <pod-name> -n alfa-romeo -c wait-for-db

# Check main container logs
kubectl logs <pod-name> -n alfa-romeo

# Check environment variables the pod sees
kubectl exec <pod-name> -n alfa-romeo -- env | grep DATABASE

# Test DB connectivity manually
kubectl exec <pod-name> -n alfa-romeo -- nc -zv alfa-romeo-db 5432
```

## Adding HTTP health checks in the future

If you want to restore HTTP-level probes:

1. Re-add `health_check` app to `INSTALLED_APPS` in `settings.py`
2. Re-add the URL include in `urls.py`:
   ```python
   path('health/', include('alfa_romeo_web.health_check.urls')),
   ```
3. Change probes in `django-deployment.yml` from `tcpSocket` back to:
   ```yaml
   livenessProbe:
     httpGet:
       path: /health/
       port: 8000
   readinessProbe:
     httpGet:
       path: /health/ready/
       port: 8000
   ```
4. Rebuild and push the image.
