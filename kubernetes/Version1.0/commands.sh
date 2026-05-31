minikube status
minikube start --dry-run=true # start default driver and checks for other drivers available

minikube start --driver=virtualbox # failed Exiting due to HOST_VIRT_UNAVAILABLE: Failed to start host: creating host: create: precreate: This computer doesn't have VT-X/AMD-v enabled. Enabling it in the BIOS is mandatory
minikube start --no-vtx-check # fixed the error above

minikube start --driver=virtualbox --no-vtx-check # final command

kubectl cluster-info

kubectl apply -f postgres-pv.yml

kubectl apply -f postgres-pvc.yml

kubectl apply -f webapp-pv.yml

kubectl apply -f webapp-pvc.yml

kubectl apply -f configmap.yml

kubectl apply -f postgres-deployment.yml

kubectl get pods

kubectl get svc

kubectl apply -f django-deployment.yml

kubectl get pods

kubectl get svc

# Enter the WEB pod and run the migrations !!!
kubectl exec -it <django-pod-name> -- /bin/bash
python manage.py migrate
python manage.py collectstatic

kubectl port-forward svc/alfa-romeo-web 8000:8000

kubectl get pods

kubectl get pods --all-namespaces 
kubectl get pods -n default