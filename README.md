# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Production-style DevOps laboratory built in public.

This repository documents my transition toward a production-focused DevOps / Cloud Engineering profile by incrementally evolving real infrastructure systems: containerization, CI/CD automation, Kubernetes release management, autoscaling tuning, resiliency validation, workload hardening, observability, and Infrastructure as Code.

---

# 🧱 Architecture Overview

Current stack:

- FastAPI backend
- Docker & GitHub Container Registry (GHCR)
- GitHub Actions (self-hosted runner in WSL)
- **ArgoCD (GitOps Engine)** 🐙
- k3d multi-node Kubernetes cluster (1 control plane tainted + 2 workers)
- Traefik Ingress Controller
- Helm (declarative packaging layer)
- Horizontal Pod Autoscaler (CPU-based, tuned)
- PodDisruptionBudget
- metrics-server
- kube-prometheus-stack (Prometheus + Grafana)
- Hardened SecurityContext
- Infrastructure-as-Code evolution (Terraform in progress)

---

# 📂 Repository Structure

lab-devops-2026/
├── app/                     # FastAPI application
├── helm/                    # Helm chart (packaging layer)
├── k8s/                     # Raw Kubernetes manifests (HPA, PDB, etc.)
├── infra/                   # Infrastructure as Code & operational scripts
├── nginx/                   # Reverse proxy configuration
├── .github/                 # CI workflows
├── docker-compose.yml       # Local development environment
└── README.md

---

# 🚀 CI/CD & GitOps Workflow

The repository has evolved to a **Declarative GitOps model**:

**git push** → **GitHub Actions**: Build Docker image & Tag with commit SHA  
→ **GHCR**: Push immutable image  
→ **ArgoCD**: Automated reconciliation loop  
→ **Kubernetes**: Rolling update & Self-healing  

This enables:
- **Decoupled Deployments**: CI only builds; ArgoCD ensures the cluster state matches Git.
- **Full Traceability**: Every cluster change is backed by a Git commit.
- **Drift Detection**: Automated reversion of manual `kubectl` overrides.

---

# ☸️ Kubernetes Architecture

Validated request flow:

Client
→ k3d LoadBalancer
→ Traefik
→ Ingress
→ ClusterIP Service
→ Deployment (replicated pods)

Control-plane node is tainted:
`node-role.kubernetes.io/control-plane=true:NoSchedule`

---

# 📦 Helm Release Management

Helm chart located under `helm/`. Key capabilities:

- Parameterized image repository & SHA tagging
- RollingUpdate strategy (maxUnavailable: 0, maxSurge: 1)
- Resource requests calibration
- Liveness & readiness probes
- Horizontal Pod Autoscaler & PodDisruptionBudget integration

---

# 📈 Horizontal Pod Autoscaler — Validated Behavior

Autoscaling behavior validated under sustained CPU pressure.

Key findings:
- HPA scales on relative utilization (usage / request).
- CPU limits managed to avoid throttling during scaling signals.
- **Observed**: Aggressive scale-up, conservative scale-down (300s window).

Control loop validated:
`desiredReplicas = currentReplicas × (currentCPU / targetCPU)`

---

# 🛡 Resiliency Validation

Simulated worker failure (`docker stop k3d-devops-lab-agent-1`):

- **ArgoCD Detection**: Identified drift in desired vs actual state.
- **Recovery**: ReplicaSet recreated pods on healthy node automatically.
- **Availability**: Service maintained via Traefik during failover.

---

# 🔐 Workload Security Hardening

SecurityContext applied:
- runAsNonRoot: true | runAsUser: 1000
- allowPrivilegeEscalation: false
- readOnlyRootFilesystem: true
- capabilities: drop ALL

---

# 📊 Observability

kube-prometheus-stack installed to validate:
- CPU/Memory per pod & Throttling visibility.
- HPA behavior in real time via Grafana.
- Monitoring used as validation tool, not decoration.

---

# 🧠 Engineering Concepts Demonstrated

- **GitOps Continuous Delivery** (ArgoCD)
- **Immutable image versioning** (SHA tagging)
- **Zero-downtime rolling updates**
- **Drift detection & Self-healing**
- **Resource right-sizing** & HPA control loops
- **Observability-first validation**
- **Infrastructure-as-Code proficiency**

---

# 🛣 Roadmap

- [x] Containerized backend
- [x] Automated CI pipeline
- [x] Multi-node Kubernetes deployment
- [x] Helm release lifecycle
- [x] Advanced HPA tuning
- [x] Observability stack
- [x] Workload hardening
- [x] Resiliency validation
- [x] **GitOps Implementation (ArgoCD)**
- [ ] Advanced HPA behavior policies
- [ ] Terraform-driven full environment reproducibility (In Progress)
- [ ] Cloud deployment (AWS)

---

# 🎯 Goal

Build and document production-style DevOps systems publicly to demonstrate:
Infrastructure maturity, automation depth, and a platform engineering mindset.

**Building in public. System by system. Control loop by control loop.**
