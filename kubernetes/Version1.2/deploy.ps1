# Kubernetes Deployment Script for Minikube (PowerShell Version)
# Run with: powershell -ExecutionPolicy Bypass -File deploy.ps1

param(
    [switch]$NoColor = $false
)

# Color codes
$script:Colors = @{
    Green = if (-not $NoColor) { "`e[32m" } else { "" }
    Blue = if (-not $NoColor) { "`e[34m" } else { "" }
    Yellow = if (-not $NoColor) { "`e[33m" } else { "" }
    Red = if (-not $NoColor) { "`e[31m" } else { "" }
    Reset = if (-not $NoColor) { "`e[0m" } else { "" }
}

function Print-Step {
    param([string]$Message)
    Write-Host "$($script:Colors.Blue)[STEP]$($script:Colors.Reset) $Message"
}

function Print-Success {
    param([string]$Message)
    Write-Host "$($script:Colors.Green)[SUCCESS]$($script:Colors.Reset) $Message"
}

function Print-Warning {
    param([string]$Message)
    Write-Host "$($script:Colors.Yellow)[WARNING]$($script:Colors.Reset) $Message"
}

function Print-Error {
    param([string]$Message)
    Write-Host "$($script:Colors.Red)[ERROR]$($script:Colors.Reset) $Message"
}

# Header
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Alfa Romeo Web App - Minikube Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if minikube is installed
Print-Step "Checking if Minikube is installed..."
try {
    $minikubeVersion = minikube version 2>&1
    Print-Success "Minikube is installed: $minikubeVersion"
} catch {
    Print-Error "Minikube is not installed or not in PATH"
    Write-Host "Please install Minikube from: https://minikube.sigs.k8s.io/"
    exit 1
}

# Check if kubectl is installed
Print-Step "Checking if kubectl is installed..."
try {
    $kubectlVersion = kubectl version --client 2>&1
    Print-Success "kubectl is installed"
} catch {
    Print-Error "kubectl is not installed or not in PATH"
    Write-Host "Please install kubectl from: https://kubernetes.io/docs/tasks/tools/"
    exit 1
}

# Ensure host data directories exist for persistent volumes
$dataRoot = "$env:USERPROFILE\minikube-data"
New-Item -ItemType Directory -Force "$dataRoot\postgres" | Out-Null
New-Item -ItemType Directory -Force "$dataRoot\django"   | Out-Null
Print-Success "Host data directories ready at $dataRoot"

# Check if Minikube is running
Print-Step "Checking if Minikube is running..."
try {
    $status = minikube status --format='{{.Host}}'
    if ($status -eq "Running") {
        Print-Success "Minikube is already running"
    } else {
        Print-Warning "Minikube is not running. Starting Minikube..."
        $mountString = "$env:USERPROFILE\minikube-data:/mnt/data"
        Write-Host "Attempting with Docker driver (recommended)..."
        try {
            minikube start --cpus=4 --memory=4096 --driver=docker --mount --mount-string=$mountString 2>&1 | Out-Null
            Print-Success "Minikube started with Docker driver"
        } catch {
            Print-Warning "Docker driver failed, trying VirtualBox..."
            Print-Warning "NOTE: VirtualBox driver does not support --mount. DB data will not persist on host."
            try {
                minikube start --cpus=4 --memory=4096 --driver=virtualbox --no-vtx-check 2>&1 | Out-Null
                Print-Success "Minikube started with VirtualBox driver"
            } catch {
                Print-Error "Failed to start Minikube with both Docker and VirtualBox drivers"
                Print-Error "Error: $_"
                Write-Host ""
                Write-Host "Please ensure:"
                Write-Host "  1. Docker is installed and running, OR"
                Write-Host "  2. VirtualBox is installed and VT-X/AMD-v is enabled in BIOS"
                Write-Host ""
                exit 1
            }
        }
    }
} catch {
    $mountString = "$env:USERPROFILE\minikube-data:/mnt/data"
    Print-Warning "Could not determine Minikube status. Attempting to start..."
    try {
        Write-Host "Attempting with Docker driver (recommended)..."
        minikube start --cpus=4 --memory=4096 --driver=docker --mount --mount-string=$mountString 2>&1 | Out-Null
        Print-Success "Minikube started with Docker driver"
    } catch {
        Print-Warning "Docker driver failed, trying VirtualBox..."
        Print-Warning "NOTE: VirtualBox driver does not support --mount. DB data will not persist on host."
        minikube start --cpus=4 --memory=4096 --driver=virtualbox --no-vtx-check 2>&1 | Out-Null
        Print-Success "Minikube started with VirtualBox driver"
    }
}

# Wait for Minikube to be fully ready
Print-Step "Waiting for Minikube to be fully ready (10 seconds)..."
Start-Sleep -Seconds 10

# Enable required addons
Print-Step "Enabling Minikube addons..."
try {
    minikube addons enable ingress | Out-Null
    Print-Success "Ingress addon enabled"
} catch {
    Print-Warning "Ingress addon may already be enabled"
}
try {
    minikube addons enable metrics-server | Out-Null
    Print-Success "metrics-server addon enabled"
} catch {
    Print-Warning "metrics-server addon may already be enabled"
}

# Configure Docker environment
Print-Step "Configuring Docker environment for Minikube..."
$dockerEnv = minikube docker-env --shell=powershell
Invoke-Expression $dockerEnv
Print-Success "Docker environment configured"

# Create namespace
Print-Step "Creating Kubernetes namespace..."
try {
    kubectl create namespace alfa-romeo 2>&1 | Out-Null
    Print-Success "Namespace created"
} catch {
    Print-Warning "Namespace may already exist"
}

# Apply manifests in order
Print-Step "Applying Kubernetes manifests..."

$manifests = @(
    @{ file = "configmap.yml"; name = "ConfigMap" },
    @{ file = "secret.yml"; name = "Secrets" },
    @{ file = "postgres-pv.yml"; name = "PostgreSQL PersistentVolume" },
    @{ file = "postgres-pvc.yml"; name = "PostgreSQL PersistentVolumeClaim" },
    @{ file = "django-pv.yml"; name = "Django PersistentVolume" },
    @{ file = "django-pvc.yml"; name = "Django PersistentVolumeClaim" }
)

$count = 1
foreach ($manifest in $manifests) {
    Write-Host "  $count. Applying $($manifest.name)..."
    kubectl apply -f $manifest.file
    $count++
}

Write-Host "  $count. Applying PostgreSQL StatefulSet..."
kubectl apply -f postgres-statefulset.yml
$count++

Write-Host "  $count. Applying PostgreSQL Service..."
kubectl apply -f postgres-service.yml
$count++

Write-Host "  $count. Waiting for PostgreSQL to be ready..."
Write-Host "  (This may take 1-2 minutes...)"
try {
    kubectl wait --for=condition=ready pod -l app=alfa-romeo-db -n alfa-romeo --timeout=300s 2>&1 | Out-Null
    Print-Success "PostgreSQL is ready"
} catch {
    Print-Warning "PostgreSQL took longer to start, but deployment will continue"
}
$count++

Write-Host "  $count. Applying Django Deployment..."
kubectl apply -f django-deployment.yml
$count++

Write-Host "  $count. Applying Django Service..."
kubectl apply -f django-service.yml
$count++

Write-Host "  $count. Applying HPA (Horizontal Pod Autoscaler)..."
kubectl apply -f hpa.yml
$count++

Write-Host "  $count. Applying Pod Disruption Budget..."
kubectl apply -f poddisruptionbudget.yml
$count++

Write-Host "  $count. Applying Network Policy..."
kubectl apply -f networkpolicy.yml
$count++

Write-Host "  $count. Applying Ingress..."
kubectl apply -f ingress.yml

Print-Success "All manifests applied successfully"
Write-Host ""

# Wait for Django to be ready
Print-Step "Waiting for Django deployment to be ready..."
Write-Host "  (This may take 2-5 minutes for migrations...)"
try {
    kubectl wait --for=condition=available --timeout=600s deployment/alfa-romeo-web -n alfa-romeo 2>&1 | Out-Null
    Print-Success "Django deployment is ready"
} catch {
    Print-Warning "Django took longer to start. Check logs with:"
    Write-Host "  kubectl logs deployment/alfa-romeo-web -n alfa-romeo"
}

Print-Success "Deployment complete!"
Write-Host ""

# Display deployment status
Print-Step "Getting deployment status..."
Write-Host ""
kubectl get all -n alfa-romeo
Write-Host ""

# Get Minikube IP
Print-Step "Accessing your application..."
$minikubeIP = minikube ip
Write-Host "$($script:Colors.Green)Minikube IP: $minikubeIP$($script:Colors.Reset)"
Write-Host "$($script:Colors.Green)Service URL: http://$minikubeIP$($script:Colors.Reset)"
Write-Host ""

# Access instructions
Print-Step "To access the application from your host:"
Write-Host "  Option 1 - Direct port forward (simple):"
Write-Host "    kubectl port-forward svc/alfa-romeo-web 8080:80 -n alfa-romeo"
Write-Host "    Then open: http://localhost:8080"
Write-Host ""
Write-Host "  Option 2 - Via Ingress (hostname routing, like production):"
Write-Host "    kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80"
Write-Host "    Add to hosts file (as Admin): 127.0.0.1  alfa-romeo-web.local"
Write-Host "    Then open: http://alfa-romeo-web.local:8080"
Write-Host ""

# Useful commands
Print-Step "Useful commands:"
Write-Host "  View application logs:"
Write-Host "    kubectl logs -f deployment/alfa-romeo-web -n alfa-romeo"
Write-Host ""
Write-Host "  Access PostgreSQL:"
Write-Host "    kubectl exec -it statefulset/alfa-romeo-db -n alfa-romeo -- psql -U hello_django -d alfa_romeo_db"
Write-Host ""
Write-Host "  Scale the deployment:"
Write-Host "    kubectl scale deployment/alfa-romeo-web --replicas=3 -n alfa-romeo"
Write-Host ""
Write-Host "  Watch pods status:"
Write-Host "    kubectl get pods -n alfa-romeo -w"
Write-Host ""

Print-Success "Setup complete! Your application is ready."
