# Kubernetes Flask App Deployment with PostgreSQL

## Overview
This project demonstrates deploying a **Flask web application** with a **PostgreSQL database** inside a **Minikube-managed Kubernetes cluster**. The Flask app connects to the PostgreSQL database and is exposed using Kubernetes services.

## Project Structure
```
k8s-flask-app/
│── manifests/
│   │── deployment/
│   │   │── flask-deployment.yaml
│   │   │── postgres-deployment.yaml
│   │── service/
│   │   │── flask-service.yaml
│   │   │── postgres-service.yaml
│   │── configmap/
│   │   │── postgres-configmap.yaml
│   │── secret/
│   │   │── postgres-secret.yaml
│── app/
│   │── Dockerfile
│   │── requirements.txt
│   │── app.py
│── README.md
│── submission/
│   │── snapshot-deployment.png
│   │── snapshot-kubectl-get-all.png
│   │── scaling-test.png
```

## Prerequisites
Before deploying, ensure you have the following installed:
- **Minikube** (for running Kubernetes locally)
- **kubectl** (for managing Kubernetes resources)
- **Docker** (for building container images)

## Setup Steps
### 1. Start Minikube
```sh
minikube start
```

### 2. Configure Minikube Docker Environment
Since we are using Minikube's internal registry, run:
```sh
minikube -p minikube docker-env | Invoke-Expression  # For PowerShell
```

### 3. Build the Flask App Docker Image
```sh
docker build -t my-flask-app:latest ./app
```
Verify the image exists:
```sh
docker images | grep my-flask-app
```

### 4. Deploy PostgreSQL Database
Apply the database manifests:
```sh
kubectl apply -f manifests/configmap/postgres-configmap.yaml
kubectl apply -f manifests/secret/postgres-secret.yaml
kubectl apply -f manifests/deployment/postgres-deployment.yaml
kubectl apply -f manifests/service/postgres-service.yaml
```

### 5. Deploy Flask Application
Modify `flask-deployment.yaml` to use the **local image**:
```yaml
containers:
  - name: flask-app
    image: my-flask-app:latest
    imagePullPolicy: Never
```
Apply the deployment:
```sh
kubectl apply -f manifests/deployment/flask-deployment.yaml
kubectl apply -f manifests/service/flask-service.yaml
```

### 6. Verify Deployments
Check if the pods are running:
```sh
kubectl get pods
```
Expected output:
```
NAME                          READY   STATUS    RESTARTS   AGE
flask-app-xxxxx              1/1     Running   0          2m
postgres-xxxxx               1/1     Running   0          3m
```

If a pod is stuck in **ErrImagePull** or **ImagePullBackOff**, troubleshoot with:
```sh
kubectl describe pod <flask-app-pod-name>
kubectl logs <flask-app-pod-name>
```

### 7. Access the Flask Application
Expose the service:
```sh
minikube service flask-service
```
This will open the Flask app in your browser.

To get the Minikube service URL manually:
```sh
minikube service flask-service --url
```

### 8. Test Database Connectivity
Enter the Flask pod:
```sh
kubectl exec -it $(kubectl get pod -l app=flask -o jsonpath="{.items[0].metadata.name}") -- bash
```
Test PostgreSQL connection:
```python
import psycopg2
conn = psycopg2.connect(host="postgres-service", database="mydb", user="myuser", password="mypassword")
print("Connected Successfully")
```

### 9. Scale Flask Deployment
Increase Flask replicas:
```sh
kubectl scale deployment flask-app --replicas=3
kubectl get pods
```
Scale down:
```sh
kubectl scale deployment flask-app --replicas=1
```

### 10. Submission Requirements
Inside the `submission/` folder, provide:
- **`snapshot-deployment.png`** → Screenshot of deployed pods
- **`snapshot-kubectl-get-all.png`** → Screenshot of `kubectl get all`
- **`scaling-test.png`** → Screenshot of scaling up/down replicas

