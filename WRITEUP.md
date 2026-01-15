# Short Write-Up (Template)

## Process (Steps + Design decisions)
1. **App stack**: FastAPI + Jinja2 for the UI, SQLAlchemy for persistence.
   - Chosen for simplicity and production realism (structured logging, health checks, metrics).
2. **Persistence**: Postgres in Docker, app uses `DATABASE_URL`.
   - Shows last 5 submissions ordered by timestamp.
3. **Containerization**:
   - `Dockerfile` uses `python:3.12-slim`, runs as non-root user.
   - `docker-compose.yml` runs app + db + Prometheus + Grafana.
4. **Monitoring**:
   - App exposes `/metrics` using `prometheus_client`.
   - Prometheus scrapes the app service, Grafana is pre-provisioned with a datasource + a small dashboard.
5. **CI/CD**:
   - GitHub Actions runs lint (ruff) + tests (pytest).
   - Builds the Docker image.
   - Deploy job SSHes into the server, clones/pulls the repo, applies Terraform, then runs `docker compose up -d --build`.
6. **Infrastructure as Code (Terraform)**:
   - Terraform uses the Docker provider to create external Docker network + volumes.
   - Compose references these as `external: true` to prove the infra can be recreated from code.

## Findings (What worked / what was tricky)
- Docker Compose healthchecks are critical so the app doesn't start before Postgres is ready.
- Deploying with GitHub Actions over SSH is straightforward, but depends on correct SSH key setup and network reachability.

## Learnings / Improvements (If more time)
- Add migrations (Alembic) rather than `Base.metadata.create_all()`.
- Add authentication (e.g., OAuth or SSO) and CSRF protection if the app had user sessions.
- Use a proper image registry (GHCR) with immutable tags and `docker compose pull`.
- Add alerting (Prometheus Alertmanager) and logs aggregation (Loki/ELK).
- Hardening: add seccomp/apparmor profiles and run with read-only filesystem where possible.

## Security measures (3–5)
1. **Secrets management**: never commit secrets; use GitHub Secrets + server-side `.env` or a secrets manager.
2. **Least privilege**: run the app as non-root; drop Linux capabilities; avoid privileged containers.
3. **Network segmentation**: expose only required ports; keep DB private to the Docker network; restrict SSH by firewall + IP allowlist.
4. **Supply-chain hardening**: pin image versions, enable Dependabot, scan images (Trivy/Grype), sign images (cosign).
5. **Access control**: restrict GitHub deploy permissions; use deploy keys; enforce branch protection and required checks.

## Compliance considerations
- **GDPR/POPIA** (if collecting personal data): data minimization, lawful basis, retention policy, right-to-erasure.
- **ISO 27001**: access controls, change management, audit logging, incident response runbooks.
- **CIS Benchmarks**: harden OS and Docker daemon, patching, least privilege, logging, and secure configuration baselines.
