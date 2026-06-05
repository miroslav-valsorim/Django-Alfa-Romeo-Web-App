#!/bin/bash

# =============================================================================
# Alfa Romeo Web App - Kubernetes Helper Commands
# =============================================================================
#
# FIRST TIME SETUP
# ----------------
# 1. Run deploy script (handles minikube start, addons, manifests):
#      Windows:  .\deploy.ps1
#      Linux:    ./deploy.sh
#
# 2. Run migrations (only needed on fresh cluster / after minikube delete):
#      kubectl exec -n alfa-romeo deployment/alfa-romeo-web -- python manage.py migrate
#
# 3. Create superuser:
#      kubectl exec -it <pod-name> -n alfa-romeo -- python manage.py createsuperuser
#
# =============================================================================
# DAILY WORKFLOW (after minikube stop / PC restart)
# -------------------------------------------------
# Minikube stop/start keeps all data and resources — no need to redeploy.
#
# 1. Start minikube (with host mount for persistent DB):
#      minikube start --cpus=4 --memory=4096 --driver=docker \
#        --mount --mount-string="$HOME/minikube-data:/mnt/data"
#
# 2. Start access (pick one):
#
#    Option A — Simple (no Ingress):
#      kubectl port-forward svc/alfa-romeo-web 8080:80 -n alfa-romeo
#      Open: http://localhost:8080
#
#    Option B — Via Ingress (hostname-based, like production):
#      kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
#      Open: http://alfa-romeo-web.local:8080
#      (requires 127.0.0.1 alfa-romeo-web.local in /etc/hosts or Windows hosts file)
#
# NOTE: After minikube delete, run deploy script again + repeat steps 2 and 3.
#       Data is safe on disk at ~/minikube-data/ even after minikube delete.
#
# =============================================================================
# USEFUL COMMANDS
# =============================================================================

echo "STATUS:"
echo "  kubectl get all -n alfa-romeo"
echo "  kubectl get pods -n alfa-romeo -w"
echo "  kubectl get hpa -n alfa-romeo"
echo ""
echo "LOGS:"
echo "  kubectl logs -f deployment/alfa-romeo-web -n alfa-romeo"
echo "  kubectl logs -f statefulset/alfa-romeo-db -n alfa-romeo"
echo "  kubectl logs <pod-name> -n alfa-romeo -c wait-for-db    # init container logs"
echo ""
echo "DATABASE:"
echo "  kubectl exec -it statefulset/alfa-romeo-db -n alfa-romeo -- psql -U hello_django -d alfa_romeo_db"
echo "  kubectl exec -n alfa-romeo deployment/alfa-romeo-web -- python manage.py migrate"
echo "  kubectl exec -n alfa-romeo deployment/alfa-romeo-web -- python manage.py createsuperuser"
echo ""
echo "SHELL ACCESS:"
echo "  kubectl exec -it deployment/alfa-romeo-web -n alfa-romeo -- /bin/sh"
echo ""
echo "RESTART / SCALE:"
echo "  kubectl rollout restart deployment/alfa-romeo-web -n alfa-romeo"
echo "  kubectl scale deployment/alfa-romeo-web --replicas=3 -n alfa-romeo"
echo ""
echo "STORAGE (DB lives on host at ~/minikube-data/postgres/):"
echo "  minikube ssh 'ls /mnt/data/postgres/postgres/'"
echo ""
echo "DEBUG:"
echo "  kubectl describe pod <pod-name> -n alfa-romeo"
echo "  kubectl get events -n alfa-romeo --sort-by=.metadata.creationTimestamp"
echo "  kubectl top pods -n alfa-romeo"