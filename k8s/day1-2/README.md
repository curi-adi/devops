# Kubernetes Day 1-2 Assignment
**Topics:** Pods · Deployments · Services · ECR · Image Pull Secrets · Debugging

---

## Prerequisites

| Tool | Check |
|---|---|
| Docker Desktop (running) | `docker info` |
| kind | `kind version` |
| kubectl | `kubectl version --client` |
| AWS CLI (configured) | `aws sts get-caller-identity` |

---

## Quick Start — Run Everything

```bash
cd k8s/day1-2
bash setup.sh
```

The script walks through all 6 parts interactively, pausing at port-forward steps.

---

## Step-by-Step Reference

### Setup — Create kind cluster
```bash
kind create cluster --name bootcamp
kubectl cluster-info --context kind-bootcamp
```

---

### Part 1 — Pods
```bash
kubectl apply -f manifests/01-nginx-pod.yaml
kubectl get pods
kubectl describe pod nginx
```

**Concepts:** Pods are the smallest unit in Kubernetes. A pod wraps one or more containers.
`kubectl create` is imperative (one-shot); `kubectl apply` is declarative (idempotent, works from YAML).

---

### Part 2 — Deployments + Self-Healing
```bash
kubectl apply -f manifests/02-nginx-deployment.yaml
kubectl get pods -l app=nginx

# Delete one pod — Kubernetes will recreate it automatically
kubectl delete pod <pod-name>
kubectl get pods -l app=nginx   # new pod appears
```

**Concepts:** A Deployment maintains a desired replica count. If a pod dies, the ReplicaSet controller creates a replacement immediately.

---

### Part 3 — Services + Port-Forward
```bash
kubectl apply -f manifests/03-nginx-service.yaml
kubectl get svc nginx-service

# In a separate terminal:
kubectl port-forward svc/nginx-service 8080:8080
# Open: http://localhost:8080
```

**Service types comparison:**
| Type | Accessible from |
|---|---|
| ClusterIP (default) | Inside cluster only |
| NodePort | Node IP + a port (30000–32767) |
| LoadBalancer | External cloud LB (AWS/GCP/Azure) |

---

### Part 4 — Build & Push to ECR
```bash
# Create ECR repo
aws ecr create-repository --repository-name kind-static-app --region ap-south-1

# Build image
docker build -t kindapp ./simpleapp

# Tag for ECR
docker tag kindapp YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/kind-static-app:1.0

# Auth + push
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin \
    YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/kind-static-app:1.0
```

---

### Part 5 — Image Pull Secret + Deploy Flask App
```bash
# Create k8s secret so the cluster can pull from private ECR
kubectl create secret docker-registry ecr-secret \
  --docker-server=YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region ap-south-1) \
  --namespace=default

# Deploy the Flask app and its service
kubectl apply -f manifests/04-flask-deployment.yaml
kubectl apply -f manifests/05-flask-service.yaml
kubectl get pods -l app=flask-app

# Port-forward to test
kubectl port-forward svc/flask-service 5000:5000
# Open: http://localhost:5000 — shows pod hostname
# Delete a pod and refresh to see hostname change (self-healing proof!)
```

**Why ECR tokens expire:** ECR auth tokens are valid for 12 hours. The secret stores the current token — you'll need to refresh it periodically in production (use a CronJob or IRSA for this).

---

### Part 6 — Pod Debugging
```bash
# Exec into a running container
kubectl exec -it <flask-pod-name> -- /bin/sh

# Inside the pod:
hostname                    # pod name
env                         # environment variables
wget -qO- localhost:5000    # hit the app from inside
```

---

### Bonus — Inspect the ECR Secret
```bash
# See the base64-encoded docker config stored in the secret
kubectl get secret ecr-secret -o jsonpath='{.data.\.dockerconfigjson}' \
  | base64 --decode | python3 -m json.tool
```

The decoded JSON contains your ECR server URL, username (AWS), and the auth token as base64.

---

## File Structure

```
day1-2/
├── manifests/
│   ├── 01-nginx-pod.yaml          # Part 1
│   ├── 02-nginx-deployment.yaml   # Part 2
│   ├── 03-nginx-service.yaml      # Part 3
│   ├── 04-flask-deployment.yaml   # Part 5 — uses ECR image + secret
│   └── 05-flask-service.yaml      # Part 5
├── simpleapp/
│   ├── app.py                     # Flask app (shows pod hostname/IP)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/index.html
├── setup.sh                       # Runs the full assignment end-to-end
└── README.md
```

---

## Cleanup
```bash
# Delete cluster (removes everything)
kind delete cluster --name bootcamp

# Delete ECR repo (if you want to remove AWS resources)
aws ecr delete-repository --repository-name kind-static-app \
  --region ap-south-1 --force
```
