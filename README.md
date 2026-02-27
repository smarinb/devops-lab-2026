# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Production-style DevOps laboratory built in public.

This repository documents my transition toward a production-focused DevOps / Cloud Engineering profile by incrementally evolving real infrastructure systems: containerization, CI/CD automation, Kubernetes release management, autoscaling tuning, resiliency validation, workload hardening, observability, and Infrastructure as Code.

---

# 🧱 Architecture Overview

Current stack:

- FastAPI backend
- Docker
- GitHub Actions (self-hosted runner in WSL)
- GitHub Container Registry (GHCR, SHA-tagged images)
- k3d multi-node Kubernetes cluster (1 control plane tainted + 2 workers)
- Traefik Ingress Controller
- Helm (release lifecycle management)
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

The repository separates:

- Application layer
- Packaging layer
- Kubernetes configuration
- Infrastructure as Code (evolving)
- Automation workflows

---

# 🚀 CI/CD Workflow

Every push to `main` triggers:

git push  
→ GitHub Actions (self-hosted runner)  
→ Build Docker image  
→ Tag image with commit SHA  
→ Push image to GHCR  
→ helm upgrade --install  
→ Rolling update in Kubernetes  

Images are immutable and versioned by commit SHA.

This enables:

- Safe rollbacks  
- Full traceability  
- Deterministic deployments  

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

node-role.kubernetes.io/control-plane=true:NoSchedule

Workloads are scheduled only on worker nodes.

---

# 📦 Helm Release Management

Helm chart located under:

helm/

Key capabilities:

- Parameterized image repository & tag
- RollingUpdate strategy (maxUnavailable: 0, maxSurge: 1)
- Resource requests calibration
- Liveness & readiness probes
- Horizontal Pod Autoscaler
- PodDisruptionBudget
- Graceful shutdown support
- Versioned upgrades & rollback capability

---

# 📈 Horizontal Pod Autoscaler — Validated Behavior

Autoscaling behavior validated under sustained CPU pressure.

Key findings:

- HPA scales on relative utilization (usage / request), not absolute CPU.
- Poorly calibrated requests block autoscaling.
- CPU limits can distort scaling signals via throttling.
- Runtime concurrency (Uvicorn workers) directly impacts scaling behavior.
- Scale-up is aggressive.
- Scale-down is conservative (stabilization window ≈ 300s).

Control loop validated:

desiredReplicas = currentReplicas × (currentCPU / targetCPU)

Observed:

✔ Progressive scale-up under pressure  
✔ Stabilized scale-down  
✔ No flapping  
✔ Observability-driven validation  

---

# 🛡 Resiliency Validation

Simulated worker failure:

docker stop k3d-devops-lab-agent-1

Observed:

- Node → NotReady
- Pods → Unknown
- ReplicaSet recreated pods on healthy node
- Service availability maintained

Self-healing validated.

---

# 🔐 Workload Security Hardening

SecurityContext applied:

- runAsNonRoot: true
- runAsUser: 1000
- allowPrivilegeEscalation: false
- readOnlyRootFilesystem: true
- capabilities: drop ALL

Validated non-root container execution.

---

# 📊 Observability

kube-prometheus-stack installed to validate:

- CPU per pod
- Requests vs usage correlation
- Throttling visibility
- HPA behavior in real time
- Node failure impact

Monitoring used as validation tool, not decoration.

---

# 🧠 Engineering Concepts Demonstrated

- Immutable image versioning (SHA tagging)
- Zero-downtime rolling updates
- Resource right-sizing
- CPU throttling mechanics
- HPA control loop behavior
- Stabilization windows
- Runtime concurrency impact
- PodDisruptionBudget enforcement
- Node taints & scheduling isolation
- ReplicaSet self-healing
- Observability-first validation
- CI/CD gating
- Progressive Infrastructure-as-Code adoption

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
- [ ] Advanced HPA behavior policies
- [ ] Terraform-driven full environment reproducibility
- [ ] GitOps (ArgoCD)
- [ ] Cloud deployment (AWS)

---

# 🎯 Goal

Build and document production-style DevOps systems publicly to demonstrate:

- Infrastructure maturity
- Automation depth
- Cloud-native design principles
- Platform engineering mindset
- Observability-driven operations
- Infrastructure as Code proficiency

Building in public.  
System by system.  
Control loop by control loop.
