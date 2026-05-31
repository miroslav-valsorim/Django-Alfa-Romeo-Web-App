# Kubernetes Local Deployment - Minikube (Version 1.2)

Django + PostgreSQL on Minikube with persistent storage, Gunicorn, HPA, Ingress, and NetworkPolicy.

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

---

## What changed from Version1.1

| Area | Version 1.1 | Version 1.2 |
|---|---|---|
| **Namespace** | None (default) | `alfa-romeo` namespace |
| **Secrets** | Credentials in ConfigMap (plaintext) | Separate `secret.yml` |
| **ConfigMap** | 3 vars (DB creds only) | 9 vars — DEBUG, ALLOWED_HOSTS, DB config, SSL mode, static/media URLs |
| **PostgreSQL resource** | `Deployment` | `StatefulSet` — correct type for databases |
| **PostgreSQL image** | `postgres:latest` | `postgres:15-alpine` — pinned version, smaller |
| **PostgreSQL health checks** | None | `pg_isready` liveness + readiness probes |
| **PostgreSQL resources** | No limits | 256Mi–512Mi RAM, 250m–500m CPU |
| **Django replicas** | 1 | 2 + RollingUpdate strategy |
| **Django server** | `python manage.py runserver` | Gunicorn (4 workers, sync, max-requests 1000) |
| **Django health checks** | None | `httpGet /health/live/` (liveness) + `httpGet /health/ready/` (checks DB) |
| **Django resources** | No limits | 256Mi–512Mi RAM, 250m–500m CPU |
| **Django security context** | None | `runAsUser: 1000`, capabilities dropped |
| **Service type** | ClusterIP port 8000 | LoadBalancer port 80→8000 + session affinity |
| **Ingress** | None | Nginx ingress routing `alfa-romeo-web.local` |
| **Autoscaling** | None | HPA: 2–5 pods based on CPU (70%) / memory (80%) |
| **PodDisruptionBudget** | None | Min 1 pod available during updates |
| **NetworkPolicy** | None | Pod-to-pod traffic restrictions |
| **Storage size** | 1Gi, `storageClassName: manual` | 5Gi, `storageClassName: standard` |
| **Data persistence** | Inside Minikube container (lost on delete) | Mounted from Windows host (`C:\Users\<you>\minikube-data\`) |
| **Static files** | Not collected — served from source dirs | `collectstatic` runs at Docker build time, served by Whitenoise |
| **Media storage** | Always Cloudinary | Filesystem when `DEBUG=True`, Cloudinary when `DEBUG=False` |
| **Deploy scripts** | `commands.sh` (manual steps) | `deploy.ps1` / `deploy.sh` (fully automated) |

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

### 2. Run migrations (fresh cluster only)

```powershell
kubectl exec -n alfa-romeo deployment/alfa-romeo-web -- python manage.py migrate
```

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
| `django-deployment.yml` | Gunicorn app, 2 replicas, wait-for-db init container |
| `django-service.yml` | LoadBalancer service |
| `django-pv.yml` / `django-pvc.yml` | Media file storage |
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
