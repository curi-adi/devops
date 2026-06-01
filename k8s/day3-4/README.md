# Kubernetes Day 3-4 Assignments
**Aditya Shrivastava**

---

## Assignment 3 — Persistent Storage + StatefulSets

### Run
```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
bash setup3.sh
```

### What it covers

| Part | Topic |
|---|---|
| Setup | 4-node kind cluster (1 control-plane + 3 workers) |
| Part 1 | PVC — StorageClass → PersistentVolumeClaim → volumeMount |
| Part 2 | Postgres as **Deployment** (broken) — RWO PVC blocks scheduling on multiple nodes |
| Part 4 | Postgres as **StatefulSet** — stable names, per-pod storage, ordered init |
| Part 3 | Deploy DevOps Portal Flask app connecting to Postgres via secret |

### Key concept: Deployment vs StatefulSet

| | Deployment | StatefulSet |
|---|---|---|
| Pod names | Random hash | Stable: `postgres-0`, `postgres-1` |
| Storage | Shared PVC (broken for DBs) | Per-pod via `volumeClaimTemplates` |
| DNS | Service IP only | `postgres-0.postgres.svc.cluster.local` |
| Use for | Stateless apps | Databases, queues |

---

## Assignment 4 — Resource Management + HPA + Probes

### Run
```bash
# Must run after setup3.sh (needs the day3-4 cluster)
bash setup4.sh
```

### What it covers

| Part | Topic |
|---|---|
| Part 1 | CPU/memory `requests` and `limits` on containers |
| Part 2-3 | Install `metrics-server`, create HPA (min 1, max 6 replicas at 50% CPU) |
| Part 4-5 | Apache Bench load test inside cluster → watch HPA scale pods up |
| Part 6 | `startupProbe`, `readinessProbe`, `livenessProbe` on `/health` endpoint |

### Key concepts

**Resource requests vs limits:**
```
requests = scheduler placement hint (reserve this much)
limits   = hard cap (OOMKilled if memory exceeded)
```

**Probe types:**
```
startupProbe  → gives slow apps time to boot before other probes kick in
readinessProbe → removes pod from load balancer if unhealthy
livenessProbe  → restarts container if unhealthy
```

**HPA scale-down is conservative** — 5s stabilization + 50%/60s policy prevents flapping.

---

## File structure

```
day3-4/
├── kind-config.yaml                      # 4-node cluster config
├── manifests/
│   ├── db-as-deployment/                 # Part 2 — broken postgres
│   │   ├── 01-secret.yaml
│   │   ├── 02-pvc.yaml
│   │   ├── 03-deployment.yaml
│   │   └── 04-service.yaml
│   ├── db-as-statefulset/                # Part 4 — correct postgres
│   │   ├── 01-secret.yaml
│   │   ├── 02-statefulset.yaml
│   │   └── 03-service.yaml
│   └── app/
│       ├── 01-secret.yaml               # DB credentials
│       ├── 02-deployment-simple.yaml    # Assignment 3 — no limits/probes
│       ├── 03-deployment-resources.yaml # Assignment 4 — CPU/mem limits
│       ├── 04-deployment-probes.yaml    # Assignment 4 — health probes
│       └── 05-hpa.yaml                  # Assignment 4 — autoscaler
├── setup3.sh
├── setup4.sh
└── README.md
```

## Cleanup
```bash
kind delete cluster --name day3-4
aws ecr delete-repository --repository-name devops-portal --region ap-south-1 --force
```
