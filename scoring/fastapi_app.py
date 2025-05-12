apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
  labels:
    app: fastapi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi-container
          image: your-docker-image:latest
          ports:
            - containerPort: 80
# Removed volumeMounts section here
#      volumes section removed here