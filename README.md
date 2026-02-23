# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Hands-on DevOps lab simulating production-style workflows using containers, CI/CD automation, Kubernetes release management and autoscaling.

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
- metrics-server  

---

## 🔄 CI/CD Workflow (Current Phase)

Every push to `main` triggers:

git push  
→ GitHub Actions (self-hosted runner)  
→ Build Docker image  
→ Tag image with commit SHA  
→ Push image to GHCR  
→ helm upgrade --install  
→ Rolling update in Kubernetes  

Images are versioned using immutable commit SHA tags instead of `latest`.

Example:

ghcr.io/smarinb/devops-lab-2026:<commit-sha>

---

## ☸️ Kubernetes Architecture

Validated request flow end-to-end:

Client  
→ k3d LoadBalancer (localhost:8081)  
→ Traefik (Ingress Controller)  
→ Ingress (host-based routing)  
→ ClusterIP Service  
→ Deployment (replicated pods)

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
    └── hpa.yaml  

Key features:

- Parameterized image repository & tag  
- SHA-based image deployment  
- RollingUpdate strategy (maxUnavailable: 0, maxSurge: 1)  
- Resource requests & limits defined  
- Liveness & readiness probes  
- Horizontal Pod Autoscaler  
- Release versioning  
- Upgrade & rollback capability  
- Namespace isolation  

Example commands:

helm upgrade --install devops-api ./devops-api-chart -n helm-lab  
helm history devops-api -n helm-lab  
helm rollback devops-api <revision> -n helm-lab  

---

## ⚙️ Resource Management

CPU and memory boundaries are explicitly defined:

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 250m
    memory: 256Mi

Requests are required for HPA to calculate CPU utilization percentage.

---

## 📈 Horizontal Pod Autoscaler (HPA)

CPU-based autoscaling enabled using autoscaling/v2.

Configuration:

- minReplicas: 2  
- maxReplicas: 6  
- targetCPUUtilizationPercentage: 60  

Under load testing:

- 2 replicas  
- CPU spike above 120%  
- Automatic scale up to 4 replicas  
- Load removed  
- Automatic stabilization and scale down to 2 replicas  

HPA calculation model:

desiredReplicas = currentReplicas × (currentCPU / targetCPU)

---

## 🏗 Namespaces

- default → Raw manifests (legacy/manual phase)  
- helm-lab → Helm-managed release (current phase)  

This separation allows comparison between unmanaged and release-managed lifecycle strategies.

---

## ▶️ Local Development (Docker Phase)

docker build -t devops-api .  
docker run -p 8080:8000 devops-api  

Test:

curl http://localhost:8080/health  

---

## ▶️ Kubernetes Deployment via Helm

helm upgrade --install devops-api ./devops-api-chart -n helm-lab  

Port-forward test:

kubectl port-forward svc/devops-api-devops-api-chart 9000:8000 -n helm-lab  
curl http://localhost:9000/health  

Check autoscaling:

kubectl get hpa -n helm-lab  
kubectl get pods -n helm-lab  
kubectl top pods -n helm-lab  

---

## 📂 Project Structure

.  
├── app/  
├── k8s/                    # Raw manifests (legacy phase)  
├── devops-api-chart/       # Helm-managed deployment  
├── .github/workflows/      # CI/CD automation  
└── README.md  

---

## 🧠 Engineering Concepts Demonstrated

- Immutable image versioning (SHA tags)  
- Rolling updates without downtime  
- Resource-bound containers  
- CPU-based autoscaling  
- metrics-server integration  
- Helm release lifecycle management  
- Multi-node cluster scheduling  
- Troubleshooting HPA metrics issues  
- Namespace isolation strategies  

---

## 🛣 Roadmap

- [x] Containerized backend  
- [x] Automated CI pipeline  
- [x] Publish image to registry  
- [x] Deploy to local Kubernetes (k3d)  
- [x] Self-hosted CI/CD deployment  
- [x] Helm packaging & release management  
- [x] Resource requests & limits  
- [x] Horizontal Pod Autoscaler  
- [ ] PodDisruptionBudget  
- [ ] Graceful shutdown handling  
- [ ] GitOps with ArgoCD  
- [ ] Terraform-based cloud deployment  
- [ ] Observability stack (Prometheus + Grafana)  

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
