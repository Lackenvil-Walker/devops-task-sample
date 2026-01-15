# DevOps Candidate Assignment — Reference Implementation

## What this repo contains
- **FastAPI web app** with a form + persistence (Postgres) and shows last 5 submissions.
- **Dockerfile** for the app + **docker-compose.yml** for app + Postgres + Prometheus + Grafana.
- **GitHub Actions** CI/CD:
  - lint + tests
  - Docker build
  - deploy to your Ubuntu server over SSH and run `docker compose up -d --build`
- **Terraform (Docker provider)** to provision a Docker network + volumes used by Compose.
- **Monitoring** via Prometheus scraping `/metrics` and Grafana pre-provisioned with a simple dashboard.

## Local run
```bash
docker compose up -d --build
# app:       http://localhost:8000
# prometheus http://localhost:9090
# grafana    http://localhost:3000 (admin/admin_change_me)
```

## Server bootstrap (Ubuntu)
Run once on your remote server:
```bash
bash scripts/server-bootstrap.sh
```

## Terraform (on the server)
```bash
cd infra/terraform
terraform init
terraform apply
```

## GitHub Actions secrets you must set
In GitHub → Settings → Secrets and variables → Actions → New repository secret

- `SSH_HOST` (e.g. 192.168.1.50)
- `SSH_USER` (e.g. ubuntu)
- `SSH_PORT` (e.g. 22)
- `SSH_PRIVATE_KEY` (private key contents)
- `APP_DIR` (e.g. /opt/devops-task)
- `REPO_SSH_URL` (repo SSH clone URL, e.g. git@github.com:you/devops-task.git)

> If your server can't access GitHub over SSH, switch to HTTPS clone and use a PAT, or add the deploy key to your repo.

## Quick verification
- `GET /healthz` should return `ok`
- `GET /metrics` should show Prometheus metrics including `http_requests_total`
