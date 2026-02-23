# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Hands-on DevOps lab simulating production-style workflows using containers, CI/CD automation, Kubernetes release management, autoscaling, resiliency and workload hardening.

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

Example:

ghcr.io/smarinb/devops-lab-2026:<commit-sha>

---

## ☸️ Kubernetes Architecture

Validated request flow end-to-end:

Client  
→ k3d LoadBalancer  
→ Traefik  
→ Ingress  
→ ClusterIP Service  
→ Deployment (replicated pods)

Control-plane is tainted (`NoSchedule`) to simulate production behavior.

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

- Parameterized image repo & tag  
- RollingUpdate strategy (maxUnavailable: 0, maxSurge: 1)  
- Resource requests & limits  
- Liveness & readiness probes  
- Horizontal Pod Autoscaler  
- PodDisruptionBudget  
- Graceful shutdown support  
- Release versioning & rollback  

---

## 📈 Horizontal Pod Autoscaler (HPA)

CPU-based autoscaling:

- minReplicas: 2  
- maxReplicas: 6  
- targetCPUUtilizationPercentage: 60  

Validated behavior:

- 2 replicas  
- CPU spike above 120%  
- Automatic scale up to 4 replicas  
- Load removed  
- Automatic scale down to 2 replicas  

Scaling model:

desiredReplicas = currentReplicas × (currentCPU / targetCPU)

---

## 🛡 Resiliency & Availability

### PodDisruptionBudget

minAvailable: 1  

Ensures service remains available during node drain operations.

### Node Maintenance Simulation

- Tested cordon + drain  
- ReplicaSet re-schedules pods automatically  
- Availability maintained  

### Control-plane Hardening

Control-plane node tainted:

node-role.kubernetes.io/control-plane=true:NoSchedule  

Ensures workloads run only on worker nodes.

---

## 🔐 Workload Security Hardening

SecurityContext applied:

- runAsNonRoot: true  
- runAsUser: 1000  
- allowPrivilegeEscalation: false  
- readOnlyRootFilesystem: true  
- capabilities: drop ALL  

Validated workload runs without root privileges.

---

## 🧠 Engineering Concepts Demonstrated

- Immutable image versioning (SHA tags)  
- Rolling updates without downtime  
- Resource-bound containers  
- CPU-based autoscaling  
- metrics-server integration  
- PodDisruptionBudget  
- Node taints & scheduling control  
- Graceful termination behavior  
- Workload hardening (least privilege)  
- Multi-node scheduling behavior  
- Troubleshooting HPA & Helm templating issues  

---

## 🛣 Roadmap

- [x] Containerized backend  
- [x] Automated CI pipeline  
- [x] Deploy to multi-node Kubernetes  
- [x] Helm release lifecycle  
- [x] Resource requests & limits  
- [x] Horizontal Pod Autoscaler  
- [x] PodDisruptionBudget  
- [x] Control-plane isolation (taints)  
- [x] SecurityContext hardening  
- [ ] Observability stack (Prometheus + Grafana)  
- [ ] GitOps (ArgoCD)  
- [ ] Terraform-based cloud deployment  

---

## 🎯 Goal

Build and document production-style DevOps systems publicly to demonstrate:

- Infrastructure maturity  
- Automation depth  
- Cloud-native design principles  
- Platform engineering mindset  

---

Building in public.  
System by system.
