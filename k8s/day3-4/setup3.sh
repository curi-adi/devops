#!/usr/bin/env bash
# Assignment 3 — Persistent Storage, StatefulSets, Flask + Postgres
set -e

export PATH="$PATH:/c/Users/ankit/AppData/Local/Microsoft/WinGet/Packages/Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe"

AWS_ACCOUNT="768093818017"
REGION="ap-south-1"
CLUSTER_NAME="day3-4"

cd "$(dirname "$0")"

banner() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

echo "╔════════════════════════════════════════════════════╗"
echo "║  Assignment 3 — Storage · StatefulSets · Flask     ║"
echo "║  Aditya Shrivastava                                ║"
echo "╚════════════════════════════════════════════════════╝"

# ── Setup: 4-node cluster ────────────────────────────────────────────────
banner "SETUP: 4-node kind cluster (1 control-plane + 3 workers)"
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  echo "  Cluster '${CLUSTER_NAME}' already exists — skipping."
else
  kind create cluster --name "${CLUSTER_NAME}" --config kind-config.yaml
fi
kubectl cluster-info --context "kind-${CLUSTER_NAME}"
echo ""
echo "  Nodes:"
kubectl get nodes

# ── ECR secret (needed for app deployment) ───────────────────────────────
banner "SETUP: ECR Image Pull Secret"
# Create devops-portal repo if it doesn't exist
aws ecr create-repository --repository-name devops-portal --region "${REGION}" 2>/dev/null \
  && echo "  Created ECR repo: devops-portal" \
  || echo "  ECR repo already exists."

ECR_IMAGE="${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/devops-portal:latest"

# Check if image exists in ECR already
IMAGE_EXISTS=$(aws ecr describe-images \
  --repository-name devops-portal \
  --region "${REGION}" \
  --query 'length(imageDetails)' \
  --output text 2>/dev/null || echo "0")

if [ "${IMAGE_EXISTS}" = "0" ] || [ "${IMAGE_EXISTS}" = "None" ]; then
  echo "  ERROR: devops-portal image not found in ECR."
  echo "  Push the course app image to ECR first, then re-run this script:"
  echo "    docker pull <course-app-image>"
  echo "    docker tag <course-app-image> ${ECR_IMAGE}"
  echo "    aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"
  echo "    docker push ${ECR_IMAGE}"
  exit 1
fi
echo "  Image found in ECR: ${ECR_IMAGE}"

echo "  Creating ecr-secret in cluster..."
kubectl create secret docker-registry ecr-secret \
  --docker-server="${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com" \
  --docker-username=AWS \
  --docker-password="$(aws ecr get-login-password --region "${REGION}")" \
  --namespace=default \
  --dry-run=client -o yaml | kubectl apply -f -

# ── Part 1: PVC basics ───────────────────────────────────────────────────
banner "PART 1: PersistentVolumeClaim"
kubectl apply -f manifests/db-as-deployment/01-secret.yaml
kubectl apply -f manifests/db-as-deployment/02-pvc.yaml
echo ""
echo "  PVC status (should be Bound):"
sleep 3
kubectl get pvc postgres-data
echo ""
echo "  Storage chain: StorageClass → PVC → Pod volumeMount"
kubectl get storageclass

# ── Part 2: Postgres as Deployment (broken) ──────────────────────────────
banner "PART 2: Postgres as Deployment — intentionally broken"
kubectl apply -f manifests/db-as-deployment/03-deployment.yaml
kubectl apply -f manifests/db-as-deployment/04-service.yaml

echo "  Waiting 20 seconds to observe pod scheduling..."
sleep 20
echo ""
echo "  Pod status — notice some pods stuck in Pending (RWO PVC already mounted on another node):"
kubectl get pods -l app=postgres -o wide
echo ""
echo "  Describe the pending pod to see the error:"
PENDING=$(kubectl get pods -l app=postgres --field-selector=status.phase=Pending -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
if [ -n "$PENDING" ]; then
  kubectl describe pod "$PENDING" | grep -A5 "Events:"
fi
echo ""
echo "  Lesson: ReadWriteOnce PVC can only be mounted by ONE node."
echo "          A Deployment doesn't guarantee stable storage per pod."
echo ""
read -rp "  Press ENTER to continue to the fix (StatefulSet)..."

# ── Clean up broken deployment ───────────────────────────────────────────
echo "  Cleaning up broken deployment and PVC..."
kubectl delete deployment postgres --ignore-not-found
kubectl delete svc postgres --ignore-not-found
kubectl delete pvc postgres-data --ignore-not-found
sleep 5

# ── Part 4: Postgres as StatefulSet (correct) ────────────────────────────
banner "PART 4: Postgres as StatefulSet — the correct way"
kubectl apply -f manifests/db-as-statefulset/01-secret.yaml
kubectl apply -f manifests/db-as-statefulset/02-statefulset.yaml
kubectl apply -f manifests/db-as-statefulset/03-service.yaml

echo "  Waiting for postgres-0 to be ready..."
kubectl wait --for=condition=Ready pod/postgres-0 --timeout=120s

echo ""
echo "  Pods — notice stable name 'postgres-0' (not random hash):"
kubectl get pods -l app=postgres -o wide
echo ""
echo "  PVC — each replica gets its own (volumeClaimTemplate):"
kubectl get pvc
echo ""
echo "  Headless service — enables DNS: postgres-0.postgres.default.svc.cluster.local"
kubectl get svc postgres

# ── Part 3: Flask app (DevOps Portal) ────────────────────────────────────
banner "PART 3: Deploy Flask App (DevOps Portal)"
kubectl apply -f manifests/app/01-secret.yaml
kubectl apply -f manifests/app/02-deployment-simple.yaml

echo "  Waiting for devops-portal to be ready..."
kubectl wait --for=condition=available deployment/devops-portal-simple --timeout=120s

echo ""
kubectl get pods -l app=devops-portal
echo ""
kubectl get svc devops-portal-simple

echo ""
echo "  ✋ MANUAL — access the app via NodePort:"
echo "     The app runs on NodePort 30001."
echo "     Get your node IP: kubectl get nodes -o wide"
echo "     Then open: http://<node-ip>:30001"
echo ""
echo "  OR port-forward: kubectl port-forward svc/devops-portal-simple 8000:8000"
echo "     Then open: http://localhost:8000"
echo ""
read -rp "  Press ENTER once you've tested the app..."

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅  Assignment 3 Complete!                        ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "Running resources:"
kubectl get pods
echo ""
kubectl get svc
echo ""
echo "Run setup4.sh next for Assignment 4 (HPA, metrics, probes)"
