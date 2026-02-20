# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Hands-on DevOps lab simulating production-style workflows using containers, CI/CD automation and Kubernetes-based architecture.

This repository documents my transition into a production-focused DevOps / Cloud Engineering profile by building real systems end-to-end and evolving them incrementally.

---

## 🧱 Current Stack

- FastAPI backend  
- Nginx reverse proxy (Docker phase)  
- Docker & Docker Compose  
- GitHub Actions (CI pipeline)  
- GitHub Container Registry (GHCR)  
- k3d multi-node Kubernetes cluster (1 control plane + 2 workers)  
- Traefik Ingress Controller  
- Self-hosted GitHub Actions runner (running inside WSL)  

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
kubectl apply
   ↓
kubectl rollout restart
   ↓
Pods recreated automatically
```

Published image:

```
ghcr.io/smarinb/devops-lab-2026:latest
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
Ingress (host-based routing: devops.local)
   ↓
ClusterIP Service
   ↓
Deployment (2 replicas)
   ↓
FastAPI Pods
```

Key concepts implemented:

- Multi-node cluster simulation  
- Host-based routing with Ingress  
- Rolling updates  
- Automated pod recreation  
- End-to-end request validation  
- CI-triggered deployment  

---

## ▶️ Run Locally (Docker Phase)

```
docker compose up -d --build
```

Test endpoints:

```
curl http://localhost:8080
curl http://localhost:8080/health
```

---

## ▶️ Deploy to Kubernetes (Manual Mode)

```
kubectl apply -f k8s/
```

Test Ingress routing:

```
curl -H "Host: devops.local" http://localhost:8081/health
```

---

## 📂 Project Structure

```
.
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── .github/workflows/
    └── ci.yml
```

---

## ☸️ Roadmap

- [x] Containerized backend  
- [x] Reverse proxy setup  
- [x] Automated CI pipeline  
- [x] Publish image to registry  
- [x] Deploy to local Kubernetes (k3d)  
- [x] Self-hosted CI/CD deployment  
- [ ] Helm packaging  
- [ ] GitOps with ArgoCD  
- [ ] Terraform-based cloud deployment  
- [ ] Observability (Prometheus + Grafana)  

---

## 🎯 Goal

Build and document production-style DevOps systems publicly to strengthen real-world cloud engineering skills and demonstrate infrastructure maturity.

---

## 📌 Key Focus Areas

- Automation  
- Infrastructure reproducibility  
- CI/CD lifecycle  
- Kubernetes networking fundamentals  
- Incremental system evolution  
- Platform engineering mindset  

---

## 📝 Notes

This is an evolving lab designed to simulate real-world DevOps environments step by step.

Each phase builds on the previous one:

Containers → CI → Kubernetes → Helm → GitOps → Cloud Infrastructure.

Building in public.
