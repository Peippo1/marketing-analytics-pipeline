

# 🚀 Kubernetes Deployment Guide

This file documents how to deploy the Marketing Analytics Pipeline using Kubernetes.

---

## 🧱 Components

The following components are containerized and deployed:

- **FastAPI**: Serves customer data
- **Streamlit**: Hosts the interactive dashboard
- **MySQL**: Hosted externally (e.g., Railway)
- **Airflow**: Optional orchestration layer
- **MLflow**: Optional for model tracking

---

## 🐳 Docker Images

Build local Docker images before deployment:

```bash
docker build -t marketing-analytics-app .
docker build -f Dockerfile.fastapi -t fastapi-app .
```

---

## ☸️ Minikube Setup

1. Start Minikube:
   ```bash
   minikube start
   ```

2. Load local images into Minikube:
   ```bash
   minikube image load marketing-analytics-app:latest
   minikube image load fastapi-app:latest
   ```

---

## 🗂 Deployments

Apply Kubernetes deployments and services:

```bash
kubectl apply -f k8s/streamlit-deployment.yaml
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/streamlit-service.yaml
kubectl apply -f k8s/fastapi-service.yaml
```

---

## 🌐 Ingress Setup

1. Install NGINX Ingress Controller (via Helm):
   ```bash
   brew install helm
   helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
   helm repo update
   helm install ingress-nginx ingress-nginx/ingress-nginx --namespace default
   ```

2. Update `/etc/hosts`:
   ```
   127.0.0.1 streamlit.local
   127.0.0.1 fastapi.local
   ```

3. Apply the ingress:
   ```bash
   kubectl apply -f k8s/ingress.yaml
   ```

---

## 🌍 Access Services

### ✅ Option 1: Port Forwarding

Use port forwarding for reliable local access:

```bash
# Streamlit
kubectl port-forward service/streamlit-service 8501:8501
# FastAPI
kubectl port-forward service/fastapi-service 8000:8000
```

Access:
- [http://localhost:8501](http://localhost:8501)
- [http://localhost:8000/customers](http://localhost:8000/customers)

### 🌐 Option 2: Ingress + Custom DNS

If DNS resolution is set up:

- [http://streamlit.local](http://streamlit.local)
- [http://fastapi.local](http://fastapi.local)

Note: On macOS, you may need to flush the DNS cache or switch to `.test` domains.

---

## 🧼 Cleanup

To delete resources:
```bash
kubectl delete -f k8s/
```

To stop Minikube:
```bash
minikube stop
```