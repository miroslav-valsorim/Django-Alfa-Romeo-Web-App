#!/bin/bash
# Version1.3 deployment order
# Run from the repo root: bash kubernetes/Version1.3/commands.sh

set -e

K8S_DIR="kubernetes/Version1.3"

# 1. Namespace first
kubectl apply -f $K8S_DIR/namespace.yml

# 2. Config and secrets
kubectl apply -f $K8S_DIR/configmap.yml
kubectl apply -f $K8S_DIR/secret.yml

# 3. Storage
kubectl apply -f $K8S_DIR/postgres-pv.yml
kubectl apply -f $K8S_DIR/postgres-pvc.yml
kubectl apply -f $K8S_DIR/django-pv.yml
kubectl apply -f $K8S_DIR/django-pvc.yml

# 4. Database
kubectl apply -f $K8S_DIR/postgres-statefulset.yml
kubectl apply -f $K8S_DIR/postgres-service.yml
echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=alfa-romeo-db -n alfa-romeo --timeout=120s

# 5. Run migrations (must complete before app starts)
kubectl apply -f $K8S_DIR/migrate-job.yml
echo "Waiting for migrations to complete..."
kubectl wait --for=condition=complete job/django-migrate -n alfa-romeo --timeout=120s

# 6. Redis
kubectl apply -f $K8S_DIR/redis-deployment.yml
kubectl apply -f $K8S_DIR/redis-service.yml

# 7. App
kubectl apply -f $K8S_DIR/django-deployment.yml
kubectl apply -f $K8S_DIR/django-service.yml

# 8. Scaling and reliability
kubectl apply -f $K8S_DIR/hpa.yml
kubectl apply -f $K8S_DIR/poddisruptionbudget.yml
kubectl apply -f $K8S_DIR/networkpolicy.yml
kubectl apply -f $K8S_DIR/ingress.yml

echo ""
echo "Deployment complete. Check status with:"
echo "  kubectl get all -n alfa-romeo"
