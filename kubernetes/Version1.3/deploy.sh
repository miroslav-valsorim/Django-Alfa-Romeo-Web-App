#!/bin/bash
set -e

echo "=========================================="
echo "Alfa Romeo Web App - Minikube Deployment"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Preflight checks
print_step "Checking if Minikube is installed..."
if ! command -v minikube &>/dev/null; then
    print_error "Minikube is not installed or not in PATH"
    echo "Install from: https://minikube.sigs.k8s.io/"
    exit 1
fi
print_success "Minikube is installed"

print_step "Checking if kubectl is installed..."
if ! command -v kubectl &>/dev/null; then
    print_error "kubectl is not installed or not in PATH"
    echo "Install from: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi
print_success "kubectl is installed"

# Ensure host data directories exist for persistent volumes
DATA_ROOT="${HOME}/minikube-data"
mkdir -p "${DATA_ROOT}/postgres" "${DATA_ROOT}/django"
print_success "Host data directories ready at ${DATA_ROOT}"

# Check if minikube is running
MOUNT_STRING="${HOME}/minikube-data:/mnt/data"
print_step "Checking if Minikube is running..."
if ! minikube status | grep -q "Running"; then
    print_warning "Minikube is not running. Starting Minikube..."
    if minikube start --cpus=4 --memory=4096 --driver=docker --mount --mount-string="$MOUNT_STRING" 2>/dev/null; then
        print_success "Minikube started with Docker driver"
    else
        print_warning "Docker driver failed, trying VirtualBox..."
        print_warning "NOTE: VirtualBox driver does not support --mount. DB data will not persist on host."
        minikube start --cpus=4 --memory=4096 --driver=virtualbox
        print_success "Minikube started with VirtualBox driver"
    fi
else
    print_success "Minikube is already running"
fi

# Give the API server a moment to be fully ready after a fresh start
print_step "Waiting for Minikube to be fully ready (10 seconds)..."
sleep 10

# Enable required addons
print_step "Enabling Minikube addons..."
minikube addons enable ingress || print_warning "Ingress addon may already be enabled"
minikube addons enable metrics-server || print_warning "metrics-server addon may already be enabled"

# Set Docker environment to use Minikube's Docker daemon
print_step "Configuring Docker environment for Minikube..."
eval $(minikube docker-env)
print_success "Docker environment configured"

# Create namespace
print_step "Creating Kubernetes namespace..."
kubectl create namespace alfa-romeo || print_warning "Namespace may already exist"

# Apply manifests in order
print_step "Applying Kubernetes manifests..."

echo "  1. Applying ConfigMap..."
kubectl apply -f configmap.yml

echo "  2. Applying Secrets..."
kubectl apply -f secret.yml

echo "  3. Applying PostgreSQL PersistentVolumes and PersistentVolumeClaims..."
kubectl apply -f postgres-pv.yml
kubectl apply -f postgres-pvc.yml

echo "  4. Applying Django PersistentVolumes and PersistentVolumeClaims..."
kubectl apply -f django-pv.yml
kubectl apply -f django-pvc.yml

echo "  5. Applying PostgreSQL StatefulSet..."
kubectl apply -f postgres-statefulset.yml

echo "  6. Applying PostgreSQL Service..."
kubectl apply -f postgres-service.yml

echo "  7. Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=alfa-romeo-db -n alfa-romeo --timeout=300s || print_warning "PostgreSQL took longer to start"

echo "  8. Running database migrations (Job)..."
kubectl apply -f migrate-job.yml
echo "  Waiting for migrations to complete..."
kubectl wait --for=condition=complete job/django-migrate -n alfa-romeo --timeout=120s || print_warning "Migration job timed out. Check: kubectl logs job/django-migrate -n alfa-romeo"

echo "  9. Applying Redis Deployment..."
kubectl apply -f redis-deployment.yml

echo "  10. Applying Redis Service..."
kubectl apply -f redis-service.yml

echo "  11. Applying Django Deployment..."
kubectl apply -f django-deployment.yml

echo "  12. Applying Django Service..."
kubectl apply -f django-service.yml

echo "  13. Applying HPA (Horizontal Pod Autoscaler)..."
kubectl apply -f hpa.yml

echo "  14. Applying Pod Disruption Budget..."
kubectl apply -f poddisruptionbudget.yml

echo "  15. Applying Network Policy..."
kubectl apply -f networkpolicy.yml

echo "  16. Applying Ingress..."
kubectl apply -f ingress.yml

print_success "All manifests applied successfully"
echo ""

# Wait for Django to be ready
print_step "Waiting for Django deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/alfa-romeo-web -n alfa-romeo || print_warning "Django took longer to start"

print_success "Deployment complete!"
echo ""

# Display useful information
print_step "Getting deployment status..."
echo ""
kubectl get all -n alfa-romeo
echo ""

# Get the Minikube IP
MINIKUBE_IP=$(minikube ip)
print_step "Accessing your application..."
echo -e "${GREEN}Minikube IP: $MINIKUBE_IP${NC}"
echo -e "${GREEN}Service URL: http://$MINIKUBE_IP${NC}"
echo ""

# Show how to forward port
print_step "To access the application from your host:"
echo "  Option 1 - Direct port forward (simple):"
echo "    kubectl port-forward svc/alfa-romeo-web 8080:80 -n alfa-romeo"
echo "    Then open: http://localhost:8080"
echo ""
echo "  Option 2 - Via Ingress (hostname routing, like production):"
echo "    kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80"
echo "    Add to hosts file: 127.0.0.1  alfa-romeo-web.local"
echo "    Then open: http://alfa-romeo-web.local:8080"
echo ""

# Show how to access logs
print_step "To view application logs:"
echo "  kubectl logs -f deployment/alfa-romeo-web -n alfa-romeo"
echo ""

print_step "To check migration job logs:"
echo "  kubectl logs job/django-migrate -n alfa-romeo"
echo ""

# Show how to access database
print_step "To access PostgreSQL:"
echo "  kubectl exec -it statefulset/alfa-romeo-db -n alfa-romeo -- psql -U hello_django -d alfa_romeo_db"
echo ""

print_step "To ping Redis:"
echo "  kubectl exec -it deployment/redis -n alfa-romeo -- redis-cli ping"
echo ""

# Show scale options
print_step "To scale the deployment:"
echo "  kubectl scale deployment/alfa-romeo-web --replicas=3 -n alfa-romeo"
echo ""

print_success "Setup complete! Your application is ready."
