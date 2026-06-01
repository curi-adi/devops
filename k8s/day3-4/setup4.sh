#!/usr/bin/env bash
# Assignment 4 — Resource Limits, HPA, Load Testing, Health Probes
# Assumes Assignment 3 (setup3.sh) has been run — cluster day3-4 must be up
set -e

export PATH="$PATH:/c/Users/ankit/AppData/Local/Microsoft/WinGet/Packages/Kubernetes.kind_Microsoft.Winget.Source_8wekyb3d8bbwe"

CLUSTER_NAME="day3-4"

cd "$(dirname "$0")"

banner() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

echo "╔════════════════════════════════════════════════════╗"
echo "║  Assignment 4 — Resources · HPA · Probes           ║"
echo "║  Aditya Shrivastava                                ║"
echo "╚════════════════════════════════════════════════════╝"

# Verify cluster is running
if ! kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  echo "ERROR: Cluster '${CLUSTER_NAME}' not found. Run setup3.sh first."
  exit 1
fi
kubectl config use-context "kind-${CLUSTER_NAME}"
echo "  Using cluster: ${CLUSTER_NAME}"

# ── Part 1: Resource limits ──────────────────────────────────────────────
banner "PART 1: CPU & Memory Requests/Limits"
echo "  Applying deployment WITH resource limits..."
kubectl apply -f manifests/app/03-deployment-resources.yaml
kubectl wait --for=condition=available deployment/devops-portal-resources --timeout=120s

echo ""
echo "  Pod resource requests:"
kubectl get pod -l app=devops-portal,variant=resources -o jsonpath='{range .items[*]}{.metadata.name}{"\n  CPU req: "}{.spec.containers[0].resources.requests.cpu}{"\n  Mem req: "}{.spec.containers[0].resources.requests.memory}{"\n"}{end}'
echo ""
echo "  Lesson:"
echo "    requests = what scheduler uses for placement"
echo "    limits   = hard cap (OOMKilled if memory exceeded, throttled if CPU)"

# ── Part 2-3: Metrics server + HPA ──────────────────────────────────────
banner "PART 2: Install metrics-server"
echo "  Applying metrics-server with kubelet-insecure-tls patch for kind..."
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl patch deployment metrics-server -n kube-system \
  --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

echo "  Waiting for metrics-server to be ready (30s)..."
kubectl wait --for=condition=available deployment/metrics-server -n kube-system --timeout=90s
sleep 15

echo ""
echo "  Test metrics-server:"
kubectl top nodes
echo ""
kubectl top pods

banner "PART 3: Horizontal Pod Autoscaler"
kubectl apply -f manifests/app/05-hpa.yaml
echo ""
echo "  HPA status:"
kubectl get hpa devops-portal-hpa
echo ""
echo "  Targets show CURRENT/TARGET CPU & memory utilization"

# ── Part 4-5: Load test ──────────────────────────────────────────────────
banner "PART 4-5: Load Test — watch HPA scale up"
echo "  Starting load generator inside cluster (Apache Bench)..."
echo "  100,000 requests, 200 concurrent — targeting devops-portal-resources:8000"
echo ""

# Run load test in background pod
kubectl run load-test \
  --image=httpd:alpine \
  --restart=Never \
  --rm \
  --pod-running-timeout=60s \
  -- ab -n 100000 -c 200 http://devops-portal-resources:8000/ &

LOAD_PID=$!

echo "  Load test running. Watching HPA scale-up (Ctrl+C to stop watching)..."
echo "  Run in another terminal: kubectl get hpa devops-portal-hpa -w"
echo ""
for i in {1..6}; do
  sleep 20
  echo "  --- ${i}0s ---"
  kubectl get hpa devops-portal-hpa
  kubectl get pods -l app=devops-portal,variant=resources
done

wait $LOAD_PID 2>/dev/null || true

echo ""
echo "  Load test done. Watching scale-down (conservative — takes ~60s)..."
sleep 70
kubectl get hpa devops-portal-hpa
kubectl get pods -l app=devops-portal,variant=resources

# ── Part 6: Health probes ────────────────────────────────────────────────
banner "PART 6: Startup · Readiness · Liveness Probes"
kubectl apply -f manifests/app/04-deployment-probes.yaml
kubectl wait --for=condition=available deployment/devops-portal-probes --timeout=120s

echo ""
kubectl get pods -l app=devops-portal,variant=probes
echo ""
echo "  Probe types:"
echo "    startupProbe  — gives app time to boot (12 × 5s = 60s window)"
echo "    readinessProbe — removes pod from LB if /health fails"
echo "    livenessProbe  — restarts container if /health fails"
echo ""
echo "  Check probe config on a pod:"
PROBE_POD=$(kubectl get pods -l app=devops-portal,variant=probes -o jsonpath='{.items[0].metadata.name}')
kubectl describe pod "$PROBE_POD" | grep -A 8 "Liveness\|Readiness\|Startup"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅  Assignment 4 Complete!                        ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "Final state:"
kubectl get pods
echo ""
kubectl get hpa
echo ""
echo "Tear down: kind delete cluster --name ${CLUSTER_NAME}"
