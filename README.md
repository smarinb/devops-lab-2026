# DevOps Lab 2026 🚀

![CI](https://github.com/smarinb/devops-lab-2026/actions/workflows/ci.yml/badge.svg)

Hands-on DevOps lab simulating production-style workflows using containers, CI/CD and Kubernetes-ready architecture.

This repository documents my journey transitioning into a production-focused DevOps profile.

---

## 🧱 Current Stack

- FastAPI backend  
- Nginx reverse proxy  
- Docker & Docker Compose  
- GitHub Actions (CI pipeline)  
- GitHub Container Registry (GHCR)  

---

## 🔄 CI/CD Workflow

Every push to `main` triggers:

    git push
       ↓
    GitHub Actions
       ↓
    Build Docker image
       ↓
    Push image to GHCR

Published image:

    ghcr.io/smarinb/devops-lab-2026:latest

---

## 🏗️ Architecture (Current Phase)

    Client Request
          ↓
        Nginx
          ↓
      FastAPI App
          ↓
      Docker Image
          ↓
      GitHub Actions
          ↓
      GHCR Registry

---

## ▶️ Run Locally

    docker compose up -d --build

Test endpoints:

    curl http://localhost:8080
    curl http://localhost:8080/health

---

## 📂 Project Structure

    .
    ├── app/
    │   ├── Dockerfile
    │   ├── main.py
    │   └── requirements.txt
    ├── nginx/
    │   └── nginx.conf
    ├── docker-compose.yml
    └── .github/workflows/
        └── ci.yml

---

## ☸️ Roadmap

- [x] Containerized backend  
- [x] Reverse proxy setup  
- [x] Automated CI pipeline  
- [x] Publish image to registry  
- [ ] Deploy to local Kubernetes (k3d)  
- [ ] Helm packaging  
- [ ] GitOps with ArgoCD  
- [ ] Terraform-based cloud deployment  
- [ ] Observability (Prometheus + Grafana)  

---

## 🎯 Goal

Build and document production-like DevOps systems publicly to strengthen practical cloud engineering skills.

---

## 📌 Key Focus Areas

- Automation  
- Infrastructure reproducibility  
- CI/CD best practices  
- Incremental system evolution  
- Cloud-native mindset  

---

## 📝 Notes

This is an evolving lab designed to simulate real-world DevOps environments step by step.

Building in public.

