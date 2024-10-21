minikube start --driver=virtualbox --no-vtx-check

kubectl cluster-info

kubectl apply -f postgres-pv.yml

kubectl apply -f postgres-pvc.yml

kubectl apply -f webapp-pv.yml

kubectl apply -f webapp-pvc.yml

kubectl apply -f configmap.yml

kubectl apply -f postgres-deployment.yml

kubectl get pods

kubectl apply -f alfa-db-service.yml

kubectl get svc

kubectl apply -f django-deployment.yml

kubectl get pods

kubectl apply -f alfa-service.yml

kubectl get svc

kubectl port-forward svc/alfa-romeo-web 8000:8000

kubectl get pods

# OR 2nd (shorter way)

# minikube start --driver=virtualbox --no-vtx-check

# will apply all yml files at once
# kubectl apply -f /path/to/your/yaml/directory/

# kubectl get pods

# kubectl get svc

# kubectl port-forward svc/alfa-romeo-web 8000:8000