# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Hands-on DevOps lab simulating production-style workflows using containers, CI/CD automation and Kubernetes release management.

This repository documents my transition into a production-focused DevOps / Cloud Engineering profile by incrementally evolving real infrastructure systems.

---

## 🧱 Current Stack

- FastAPI backend  
- Docker & Docker Compose  
- GitHub Actions (self-hosted runner inside WSL)  
- GitHub Container Registry (GHCR)  
- k3d multi-node Kubernetes cluster (1 control plane + 2 workers)  
- Traefik Ingress Controller  
- Helm (release management & templating)

---

## 🔄 CI/CD Workflow (Current Phase)

Every push to `main` triggers:

```
git push
   ↓
GitHub Actions (self-hosted runner)
   ↓
Build Docker image
   ↓
Push image to GHCR
   ↓
kubectl apply (legacy phase)
```

Helm-based deployment:

```
helm upgrade --install devops-api ./devops-api-chart -n helm-lab
```

---

## ☸️ Kubernetes Architecture

Full request flow validated end-to-end:

```
Client
   ↓
k3d LoadBalancer (localhost:8081)
   ↓
Traefik (Ingress Controller)
   ↓
Ingress (host-based routing)
   ↓
ClusterIP Service
   ↓
Deployment (replicated pods)
```

---

## 📦 Helm Release Management (Current Phase)

Helm chart structure:

```
devops-api-chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

Key improvements over raw manifests:

- Parameterized image repository & tag
- Configurable replica count
- Proper liveness & readiness probes
- Separated containerPort and service.port
- Release versioning
- Upgrade capability
- Rollback capability
- Namespace isolation

Example commands:

```
helm install devops-api ./devops-api-chart -n helm-lab
helm upgrade devops-api ./devops-api-chart -n helm-lab
helm history devops-api -n helm-lab
helm rollback devops-api <revision> -n helm-lab
```

---

## 🏗 Namespaces

- `default` → Raw Kubernetes manifests (manual phase)
- `helm-lab` → Helm-managed release

This allows comparison between unmanaged resources and release-based lifecycle management.

---

## ▶️ Run Locally (Docker Phase)

```
docker compose up -d --build
```

Test:

```
curl http://localhost:8080/health
```

---

## ▶️ Kubernetes Manual Deployment (Legacy Phase)

```
kubectl apply -f k8s/
```

Test:

```
curl -H "Host: devops.local" http://localhost:8081/health
```

---

## ▶️ Kubernetes via Helm (Current Phase)

```
helm install devops-api ./devops-api-chart -n helm-lab
```

Port-forward test:

```
kubectl port-forward svc/devops-api-devops-api-chart 9000:8000 -n helm-lab
curl http://localhost:9000/health
```

---

## 📂 Project Structure

```
.
├── app/
├── docker-compose.yml
├── k8s/                 # Raw manifests (manual phase)
├── devops-api-chart/    # Helm chart (release-managed phase)
└── .github/workflows/
```

---

## ☸️ Roadmap

- [x] Containerized backend  
- [x] Automated CI pipeline  
- [x] Publish image to registry  
- [x] Deploy to local Kubernetes (k3d)  
- [x] Self-hosted CI/CD deployment  
- [x] Helm packaging & release management  
- [ ] Integrate Helm into CI/CD pipeline  
- [ ] Semantic image versioning  
- [ ] GitOps with ArgoCD  
- [ ] Terraform-based cloud deployment  
- [ ] Observability (Prometheus + Grafana)  

---

## 🎯 Goal

Build and document production-style DevOps systems publicly to demonstrate infrastructure maturity, automation depth, and platform engineering mindset.

---

Building in public.  
System by system.
