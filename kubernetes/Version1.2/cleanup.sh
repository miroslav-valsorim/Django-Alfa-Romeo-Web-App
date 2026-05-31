#!/bin/bash
set -e

echo "Cleaning up Minikube deployment..."

# Delete namespace (this will delete all resources in it)
kubectl delete namespace alfa-romeo --ignore-not-found=true

echo "Waiting for namespace to be deleted..."
sleep 5

echo "Cleanup complete. All resources have been removed."
