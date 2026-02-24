# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Hands-on DevOps lab simulating production-style workflows using containers, CI/CD automation, Kubernetes release management, autoscaling, resiliency, workload hardening and observability.

This repository documents my transition toward a production-focused DevOps / Cloud Engineering profile by incrementally evolving real infrastructure systems in public.

---

## 🧱 Current Stack

- FastAPI backend
- Docker
- GitHub Actions (self-hosted runner inside WSL)
- GitHub Container Registry (GHCR)
- k3d multi-node Kubernetes cluster (1 control plane + 2 workers)
- Traefik Ingress Controller
- Helm (release lifecycle management)
- Horizontal Pod Autoscaler (CPU-based)
- PodDisruptionBudget
- metrics-server
- kube-prometheus-stack (Prometheus + Grafana)
- Hardened SecurityContext

---

## 🔄 CI/CD Workflow

Every push to `main` triggers:

git push  
→ GitHub Actions (self-hosted runner)  
→ Build Docker image  
→ Tag image with commit SHA  
→ Push image to GHCR  
→ helm upgrade --install  
→ Rolling update in Kubernetes  

Images are immutable and versioned by commit SHA.

---

## ☸️ Kubernetes Architecture

Validated request flow end-to-end:

Client  
→ k3d LoadBalancer  
→ Traefik  
→ Ingress  
→ ClusterIP Service  
→ Deployment (replicated pods)

Control-plane node is tainted:

node-role.kubernetes.io/control-plane=true:NoSchedule

Workloads run only on worker nodes.

---

## 📦 Helm Release Management

Helm chart structure:

devops-api-chart/  
├── Chart.yaml  
├── values.yaml  
└── templates/  
    ├── deployment.yaml  
    ├── service.yaml  
    ├── ingress.yaml  
    ├── hpa.yaml  
    └── pdb.yaml  

Key capabilities:

- Parameterized image repository & tag
- RollingUpdate strategy (maxUnavailable: 0, maxSurge: 1)
- Resource requests & limits
- Liveness & readiness probes
- Horizontal Pod Autoscaler
- PodDisruptionBudget
- Graceful shutdown support
- Release versioning & rollback

---

# 📈 Horizontal Pod Autoscaler — Learning Evolution

## Phase 1 — Basic CPU Scaling

Initial configuration:

- minReplicas: 2
- maxReplicas: 6
- targetCPUUtilizationPercentage: 60
- CPU request: 100m
- CPU limit: 250m

Load generated via:

yes > /dev/null

Observed:

- CPU reached ~246m
- Utilization peaked ~246%
- CPU throttling ~98%
- HPA scaled up correctly
- Replicas redistributed load
- Scale-down occurred after load stopped

Validated formula:

desiredReplicas = currentReplicas × (currentCPU / targetCPU)

---

## Phase 2 — Removing CPU Limits

Objective:

- Eliminate artificial throttling
- Allow pods to use full node CPU capacity
- Validate real consumption behavior

Changes:

- Removed cpu limits
- Increased request to 200m

Result:

- No more CFS throttling
- Pods able to consume full core
- HPA behavior cleaner

Key learning:

CPU limits can distort autoscaling signals.

---

## Phase 3 — Runtime Concurrency Impact

Issue discovered:

- Single-worker Uvicorn prevented real parallel CPU usage.
- Multiple clients did not generate real CPU pressure.

Fix:

- Enabled 4 workers in Uvicorn.

Result:

- True CPU-bound parallelism
- Concurrency visible at pod level
- HPA received valid sustained metrics

Key learning:

Autoscaling depends on application concurrency model.

---

## Phase 4 — Requests Calibration (Critical Insight)

Observation:

CPU consumption ≈ 15m  
CPU request = 200m  

Utilization:

15m / 200m ≈ 7%

→ HPA never scaled.

Adjustment:

cpu request reduced to 20m.

Now:

15m / 20m ≈ 75%

Observed behavior:

- cpu: 58%/60% → replicas 4
- cpu: 76%/60% → replicas 5
- cpu: 85%/60% → replicas 6

HPA scaled progressively under sustained pressure.

Key learning:

HPA scales on relative utilization (usage / request), not absolute CPU.

Poorly calibrated requests block autoscaling.

---

## Phase 5 — Scale-Down Stabilization

After deleting load generators:

Observed:

- CPU dropped below target
- Replicas did not drop immediately
- Gradual reduction: 6 → 5 → 4 → 3 → 2

Explanation:

HPA scale-down stabilization window (~300s) prevents flapping.

Key learning:

Scale-up is aggressive.  
Scale-down is conservative by design.

---

## 📊 Autoscaling Behavior Fully Validated

✔ Scale-up under sustained pressure  
✔ Scale-down stabilization  
✔ Impact of requests on scaling decisions  
✔ Runtime concurrency influence  
✔ Removal of throttling artifacts  
✔ CI/CD blocking faulty rollouts  
✔ ReplicaSet self-healing  
✔ Observability-driven validation  

---

## 🛡 Resiliency Validation

Simulated worker failure:

docker stop k3d-devops-lab-agent-1

Observed:

- Node → NotReady
- Pods → Unknown
- ReplicaSet recreated pods on healthy node
- Service availability maintained

Self-healing validated.

---

## 🔐 Workload Security Hardening

SecurityContext applied:

- runAsNonRoot: true
- runAsUser: 1000
- allowPrivilegeEscalation: false
- readOnlyRootFilesystem: true
- capabilities: drop ALL

Validated non-root container execution.

---

## 📊 Observability Stack

Installed:

kube-prometheus-stack

Validated:

- CPU per pod
- Requests vs limits correlation
- Throttling visibility
- HPA behavior in real time
- Node failure impact analysis

---

## 🧠 Engineering Concepts Demonstrated

- Immutable image versioning (SHA tags)
- Zero-downtime rolling updates
- Resource right-sizing
- CPU throttling mechanics
- HPA control loop behavior
- Stabilization windows
- Concurrency impact on scaling
- PodDisruptionBudget enforcement
- Node taints & scheduling control
- ReplicaSet self-healing
- Observability-first validation
- Production-style CI/CD gating

---

## 🛣 Roadmap

- [x] Containerized backend
- [x] Automated CI pipeline
- [x] Deploy to multi-node Kubernetes
- [x] Helm release lifecycle
- [x] Resource requests & limits
- [x] Horizontal Pod Autoscaler
- [x] Autoscaling tuning (advanced)
- [x] PodDisruptionBudget
- [x] Control-plane isolation
- [x] SecurityContext hardening
- [x] Observability stack
- [ ] Advanced HPA behavior tuning
- [ ] GitOps (ArgoCD)
- [ ] Terraform-based cloud deployment

---

## 🎯 Goal

Build and document production-style DevOps systems publicly to demonstrate:

- Infrastructure maturity
- Automation depth
- Cloud-native design principles
- Platform engineering mindset
- Observability-driven operations

---

Building in public.  
System by system.  
Control loop by control loop.
