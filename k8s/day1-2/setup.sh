#!/usr/bin/env bash
# K8s Day 1-2 Assignment — Aditya Shrivastava
# Run from: k8s/day1-2/
set -e

# Add kind to PATH (winget install location)
export PATH="$PATH:/c/Users/ankit/AppData/Local/Microsoft/WinGet/Packages/Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe"

AWS_ACCOUNT="${AWS_ACCOUNT:?Error: export AWS_ACCOUNT=<your-12-digit-account-id> before running}"
REGION="ap-south-1"
ECR_REPO="kind-static-app"
ECR_URL="${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO}"
CLUSTER_NAME="bootcamp"

# Change to the script's own directory so relative paths work
cd "$(dirname "$0")"

banner() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

echo "╔════════════════════════════════════════════════════╗"
echo "║    K8s Assignment — Aditya Shrivastava             ║"
echo "║    Pods · Deployments · Services · ECR · Secrets   ║"
echo "╚════════════════════════════════════════════════════╝"

# ────────────────────────────────────────────────────────────────────────
banner "SETUP: Create kind cluster"
# ────────────────────────────────────────────────────────────────────────
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  echo "  Cluster '${CLUSTER_NAME}' already exists — skipping create."
else
  kind create cluster --name "${CLUSTER_NAME}"
fi
kubectl cluster-info --context "kind-${CLUSTER_NAME}"

# ────────────────────────────────────────────────────────────────────────
banner "PART 1: Pods"
# ────────────────────────────────────────────────────────────────────────
echo "  Applying nginx pod manifest..."
kubectl apply -f manifests/01-nginx-pod.yaml

echo "  Waiting for pod to be Ready..."
kubectl wait --for=condition=Ready pod/nginx --timeout=60s

echo ""
kubectl get pod nginx -o wide
echo ""
echo "  Try: kubectl describe pod nginx"

# ────────────────────────────────────────────────────────────────────────
banner "PART 2: Deployments + Self-Healing Demo"
# ────────────────────────────────────────────────────────────────────────
kubectl apply -f manifests/02-nginx-deployment.yaml

echo "  Waiting for deployment (3 replicas)..."
kubectl wait --for=condition=available deployment/nginx-deployment --timeout=90s

echo ""
kubectl get pods -l app=nginx -o wide
echo ""

# Self-healing demo
POD_TO_DELETE=$(kubectl get pods -l app=nginx -o jsonpath='{.items[0].metadata.name}')
echo "  ── Self-healing demo ──"
echo "  Deleting pod: ${POD_TO_DELETE}"
kubectl delete pod "${POD_TO_DELETE}"

echo "  Pausing 8 seconds for Kubernetes to recreate..."
sleep 8

echo "  Pods after deletion (Kubernetes recreated one):"
kubectl get pods -l app=nginx -o wide

# ────────────────────────────────────────────────────────────────────────
banner "PART 3: Services"
# ────────────────────────────────────────────────────────────────────────
kubectl apply -f manifests/03-nginx-service.yaml
kubectl get svc nginx-service

echo ""
echo "  ✋ MANUAL — open a NEW terminal and run:"
echo "     kubectl port-forward svc/nginx-service 8080:8080"
echo "     Then open: http://localhost:8080"
echo ""
read -rp "  Press ENTER once you've tested nginx in the browser..."

# ────────────────────────────────────────────────────────────────────────
banner "PART 4: ECR — Build & Push"
# ────────────────────────────────────────────────────────────────────────
echo "  Creating ECR repository (no-op if exists)..."
aws ecr create-repository \
  --repository-name "${ECR_REPO}" \
  --region "${REGION}" 2>/dev/null \
  && echo "  Created: ${ECR_REPO}" \
  || echo "  Repository already exists — continuing."

echo ""
echo "  Building Docker image..."
docker build -t kindapp ./simpleapp

echo ""
echo "  Tagging for ECR..."
docker tag kindapp "${ECR_URL}:1.0"

echo ""
echo "  Authenticating Docker with ECR..."
aws ecr get-login-password --region "${REGION}" \
  | docker login --username AWS --password-stdin \
    "${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"

echo ""
echo "  Pushing image to ECR..."
docker push "${ECR_URL}:1.0"
echo ""
echo "  Pushed: ${ECR_URL}:1.0"

# ────────────────────────────────────────────────────────────────────────
banner "PART 5: Image Pull Secret + Deploy Flask App"
# ────────────────────────────────────────────────────────────────────────
echo "  Creating ECR secret in the cluster..."
# Using --dry-run + apply makes this idempotent (safe to re-run)
kubectl create secret docker-registry ecr-secret \
  --docker-server="${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com" \
  --docker-username=AWS \
  --docker-password="$(aws ecr get-login-password --region "${REGION}")" \
  --namespace=default \
  --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "  Deploying Flask app from ECR..."
kubectl apply -f manifests/04-flask-deployment.yaml
kubectl apply -f manifests/05-flask-service.yaml

echo "  Waiting for flask-app pods to be ready..."
kubectl wait --for=condition=available deployment/flask-app --timeout=120s

echo ""
kubectl get pods -l app=flask-app -o wide
echo ""
kubectl get svc flask-service

echo ""
echo "  ✋ MANUAL — open a NEW terminal and run:"
echo "     kubectl port-forward svc/flask-service 5000:5000"
echo "     Then open: http://localhost:5000"
echo "     (You'll see the pod hostname — delete a pod and refresh to see it change!)"
echo ""
read -rp "  Press ENTER once you've tested the Flask app..."

# ────────────────────────────────────────────────────────────────────────
banner "PART 6: Pod Debugging"
# ────────────────────────────────────────────────────────────────────────
FLASK_POD=$(kubectl get pods -l app=flask-app -o jsonpath='{.items[0].metadata.name}')
echo "  ✋ MANUAL — exec into a pod:"
echo "     kubectl exec -it ${FLASK_POD} -- /bin/sh"
echo ""
echo "  Inside the pod, try:"
echo "     hostname          # shows pod name"
echo "     env               # env vars"
echo "     wget -qO- localhost:5000   # hit the app internally"
echo ""
read -rp "  Press ENTER once you've done the exec..."

# ────────────────────────────────────────────────────────────────────────
banner "BONUS: Inspect the ECR Secret (base64 decode)"
# ────────────────────────────────────────────────────────────────────────
echo "  Raw secret data:"
kubectl get secret ecr-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 --decode | python3 -m json.tool 2>/dev/null \
  || kubectl get secret ecr-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 --decode
echo ""
echo "  This JSON is what Kubernetes sends to ECR when pulling your image."

# ────────────────────────────────────────────────────────────────────────
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅  Assignment Complete!                          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "All running resources:"
kubectl get pods
echo ""
kubectl get svc
echo ""
echo "To tear down: kind delete cluster --name ${CLUSTER_NAME}"
