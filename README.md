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

## 📈 Horizontal Pod Autoscaler (Validated Under Load)

Configuration:

- minReplicas: 2  
- maxReplicas: 6  
- targetCPUUtilizationPercentage: 60  
- CPU request: 100m  
- CPU limit: 250m  

### Load Test Scenario

CPU-intensive process executed inside container:

yes > /dev/null

Observed behavior:

- CPU usage reached ~246m  
- CPU Requests % peaked at ~246%  
- CPU throttling reached ~98%  
- HPA triggered scale-up  
- Additional replicas created  
- Load redistributed  
- CPU normalized after load stopped  

Scaling formula validated:

desiredReplicas = currentReplicas × (currentCPU / targetCPU)

---

## 🛡 Resiliency Validation

### Node Failure Simulation (Hard Crash)

Simulated worker failure:

docker stop k3d-devops-lab-agent-1

Observed behavior:

- Node transitioned to NotReady  
- Pods entered Unknown state  
- ReplicaSet recreated pods on healthy node  
- Service availability maintained  

Validated self-healing without manual intervention.

---

## 🔐 Workload Security Hardening

SecurityContext applied:

- runAsNonRoot: true  
- runAsUser: 1000  
- allowPrivilegeEscalation: false  
- readOnlyRootFilesystem: true  
- capabilities: drop ALL  

Validated container runs without root privileges.

---

## 📊 Observability Stack

Installed:

kube-prometheus-stack

Includes:

- Prometheus  
- Grafana  
- Node Exporter  
- kube-state-metrics  
- Alertmanager  

Validated:

- CPU per pod visualization  
- Requests vs Limits correlation  
- CPU throttling visibility  
- Autoscaling behavior in real time  

---

## 🧠 Engineering Concepts Demonstrated

- Immutable image versioning (SHA tags)  
- Rolling updates without downtime  
- Resource-bound containers  
- CPU throttling behavior  
- Horizontal Pod Autoscaler logic  
- metrics-server integration  
- PodDisruptionBudget enforcement  
- Node taints & scheduling control  
- ReplicaSet self-healing  
- Node failure recovery  
- Workload hardening (least privilege)  
- Observability-driven validation  

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
- [x] Observability stack (Prometheus + Grafana)  
- [ ] Autoscaling tuning & advanced scaling strategies  
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
