# Kubernetes Local Deployment - Minikube (Version 1.3)

Django + PostgreSQL + Redis on Minikube with a dedicated migrations Job and automated Docker image publishing.

## What's inside

- Namespace isolation (`alfa-romeo`)
- Secrets separate from ConfigMap
- PostgreSQL as StatefulSet with health probes
- Gunicorn (4 workers) — not runserver
- 2 replicas + RollingUpdate strategy
- HorizontalPodAutoscaler (2–5 replicas, CPU/memory based)
- PodDisruptionBudget
- NetworkPolicy
- Nginx Ingress
- **Persistent DB storage mounted from Windows host** — survives `minikube delete`
- **Migrations run as a dedicated K8s Job** — no more racing replicas
- **Redis deployed and ready** — infrastructure in place for caching and async tasks

---

## What changed from Version1.2

| Area | Version 1.2 | Version 1.3 |
|---|---|---|
| **Migrations** | Run inside app container on startup — 2 replicas race each other | Dedicated `migrate-job.yml` runs once, completes, then app starts |
| **Redis** | Not present | Redis 7 Alpine deployed (`redis-deployment.yml` + `redis-service.yml`) |
| **ConfigMap** | 9 vars | 10 vars — added `REDIS_URL: redis://redis:6379/1` |
| **Deploy order** | No enforced ordering between migrations and app pods | `commands.sh` waits for migrate Job to complete before applying Deployment |
| **Docker image CI** | No image push pipeline | `docker-publish.yml` workflow pushes `:latest` + `:<git-sha>` tags after CI passes |

### Health check detail

| Pod | Type | What it checks |
|---|---|---|
| PostgreSQL | `exec pg_isready` | Postgres is accepting connections on the right DB and user |
| Django liveness | `httpGet /health/live/` | Gunicorn is alive and responding |
| Django readiness | `httpGet /health/ready/` | Gunicorn is alive AND database is reachable |

---

## Prerequisites

- Minikube installed
- kubectl installed
- Docker Desktop installed and **running**
- 4 GB RAM and 4 CPUs available

---

## First Time Setup

### 1. Deploy everything

```powershell
# Windows
.\deploy.ps1

# Linux/macOS
./deploy.sh
```

The script:
- Creates `C:\Users\<you>\minikube-data\` folders on your host
- Starts Minikube with `--mount` so DB data persists on your disk
- Enables ingress + metrics-server addons
- Applies all manifests in order
- Waits for PostgreSQL and Django to be ready

### 2. Migrations

Migrations now run automatically as a K8s Job before the app Deployment starts (handled by `commands.sh`). You no longer need to run them manually.

To check the Job status:
```powershell
kubectl get jobs -n alfa-romeo
kubectl logs job/django-migrate -n alfa-romeo
```

The Job cleans itself up 5 minutes after completion (`ttlSecondsAfterFinished: 300`).

### 3. Create superuser

```powershell
kubectl exec -it <pod-name> -n alfa-romeo -- python manage.py createsuperuser
# Get pod name: kubectl get pods -n alfa-romeo
```

---

## Accessing the App

### Option A — Simple (no Ingress)
```powershell
kubectl port-forward svc/alfa-romeo-web 8080:80 -n alfa-romeo
```
Open: **http://localhost:8080**

### Option B — Via Ingress (hostname routing, like production)
```powershell
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
```
Add to hosts file (`C:\Windows\System32\drivers\etc\hosts`) as **Administrator**:
```
127.0.0.1  alfa-romeo-web.local
```
Open: **http://alfa-romeo-web.local:8080**

> **Why port 8080 and not 80?**
> Port 80 requires admin rights on Windows to bind locally.
> The Ingress inside the cluster still works on port 80 — the 8080 is only on your local machine side.

> **Why not just use `minikube tunnel`?**
> `minikube tunnel` helps LoadBalancer services get an IP, but the Ingress controller
> is bound to the Minikube node IP (192.168.49.x) which is not reachable from Windows
> with the Docker driver. Port-forwarding to ingress-nginx is the correct workaround.

---

## Daily Workflow

`minikube stop` / `minikube start` keeps all pods and data — **no need to redeploy**.

```powershell
# Resume after stop or PC restart
minikube start

# Then start access (pick Option A or B above)
kubectl port-forward svc/alfa-romeo-web 8080:80 -n alfa-romeo
```

After `minikube delete` → run `deploy.ps1` again, then re-run migrations and create superuser.
DB data on `C:\Users\<you>\minikube-data\postgres\` is safe even after `minikube delete`.

---

## Data Persistence

```
C:\Users\<user>\minikube-data\
  ├── postgres\    ← PostgreSQL data files (survives minikube delete)
  └── django\      ← Media files uploaded by users
```

Mounted into Minikube at `/mnt/data/` via `--mount-string` on `minikube start`.
The PersistentVolumes use `hostPath: /mnt/data/postgres` which maps to this folder.

---

## Environment / Debug Mode

Controlled by `DEBUG` in `configmap.yml`:

| `DEBUG` | Database | Static files | Media storage |
|---|---|---|---|
| `True` (local k8s) | PostgreSQL (from configmap) | Whitenoise from image | Local filesystem (PVC) |
| `False` (production) | PostgreSQL | Whitenoise compressed | Cloudinary |

`DEBUG=True` is set in `configmap.yml` for local Minikube — no Cloudinary credentials needed.

---

## File Reference

| File | Purpose |
|---|---|
| `namespace.yml` | `alfa-romeo` namespace |
| `configmap.yml` | Non-secret env vars (DEBUG, DB host, etc.) |
| `secret.yml` | DB credentials, Django SECRET_KEY — **never commit real values** |
| `secret.example.yml` | Template to copy from |
| `postgres-statefulset.yml` | PostgreSQL with health probes and resource limits |
| `postgres-service.yml` | Headless service for DB |
| `postgres-pv.yml` / `postgres-pvc.yml` | DB persistent storage |
| `migrate-job.yml` | One-shot Job that runs `manage.py migrate` — waits for DB, cleans up after 5 min |
| `django-deployment.yml` | Gunicorn app, 2 replicas, wait-for-db init container |
| `django-service.yml` | LoadBalancer service |
| `django-pv.yml` / `django-pvc.yml` | Media file storage |
| `redis-deployment.yml` | Redis 7 Alpine — no persistence (in-memory only for local use) |
| `redis-service.yml` | ClusterIP on port 6379, reachable at `redis://redis:6379` inside the cluster |
| `ingress.yml` | Nginx ingress, routes `alfa-romeo-web.local` |
| `hpa.yml` | Autoscale 2–5 pods on CPU/memory |
| `poddisruptionbudget.yml` | Min 1 pod available during updates |
| `networkpolicy.yml` | Restricts pod-to-pod traffic |
| `deploy.ps1` | Windows deployment script |
| `deploy.sh` | Linux/macOS deployment script |
| `cleanup.sh` | Delete all cluster resources |
| `commands-helper.sh` | Quick reference for common kubectl commands |

## Cleanup

```powershell
.\cleanup.sh
# or
kubectl delete namespace alfa-romeo
```
