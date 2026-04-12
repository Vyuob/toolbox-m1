# Changelog – PentestBox

Toutes les modifications notables du projet sont documentées ici.
Format : `[version] – date – description`

---

## [1.0.0] – 2026-04-09 – Initialisation complète du projet

### Ajouté

#### Backend
- `backend/app/main.py` – Application FastAPI avec middlewares CORS et TrustedHost
- `backend/app/core/config.py` – Configuration centralisée via Pydantic Settings + `.env`
- `backend/app/core/security.py` – JWT (HS256), bcrypt, Fernet
- `backend/app/core/auth.py` – Dépendances FastAPI : `get_current_user`, `require_role`, `require_admin`, `require_analyst`
- `backend/app/core/database.py` – SQLAlchemy engine + `get_db()`
- `backend/app/models/user.py` – Modèle `User` (id, username, email, hashed_pwd, role, is_active)
- `backend/app/models/scan.py` – Modèles `ScanJob`, `Report`, `AuditLog`
- `backend/app/api/routes/auth.py` – Routes : `/token`, `/register`, `/me`
- `backend/app/api/routes/modules.py` – Routes : liste modules, lancement, suivi jobs
- `backend/app/api/routes/reports.py` – Routes : génération, liste, téléchargement
- `backend/app/api/routes/dashboard.py` – Route dashboard HTML + stats JSON
- `backend/app/tasks/celery_app.py` – Instance Celery configurée
- `backend/app/tasks/scan_tasks.py` – Tâches async : recon, scan, exploit, web_scan
- `backend/app/tasks/report_tasks.py` – Tâche async : génération rapport
- `backend/app/modules/offensive/recon.py` – DNS + Nmap + whois
- `backend/app/modules/offensive/scan.py` – Nmap NSE + Nikto + SSLyze
- `backend/app/modules/offensive/exploit.py` – SQLmap + Hydra + Metasploit
- `backend/app/modules/offensive/web_scan.py` – OWASP ZAP + Dependency-Check
- `backend/app/modules/offensive/post_exploit.py` – Enumération + vérification persistance
- `backend/app/modules/defensive/siem.py` – Intégration Elasticsearch (index/search/alerts)
- `backend/app/modules/defensive/ids.py` – Parser alertes Snort
- `backend/app/modules/defensive/response.py` – Blocage IP iptables + alertes SIEM
- `backend/app/modules/defensive/forensic.py` – ClamAV + VirusTotal API
- `backend/app/reporting/generator.py` – Génération PDF (WeasyPrint), HTML, CSV + upload MinIO
- `backend/tests/test_api.py` – Tests d'intégration de base

#### Frontend
- `frontend/templates/base.html` – Layout principal avec sidebar
- `frontend/templates/login.html` – Page de connexion
- `frontend/templates/dashboard.html` – Dashboard KPIs + jobs + rapports
- `frontend/templates/report.html` – Template rapport PDF/HTML
- `frontend/static/css/main.css` – Design System dark mode complet
- `frontend/static/js/main.js` – Helpers JS : auth, fetch API, polling, toast

#### Docker
- `docker/Dockerfile` – Image API FastAPI
- `docker/Dockerfile.celery` – Image worker Celery
- `docker/docker-compose.yml` – Stack complète : API, worker, PostgreSQL, Redis, MinIO, ELK, Kibana

#### SIEM
- `siem/elk/logstash.conf` – Pipeline Logstash (beats + Snort + Docker → Elasticsearch)
- `siem/elk/elasticsearch.yml` – Configuration Elasticsearch single-node
- `siem/snort/snort.conf` – Configuration Snort 3
- `siem/snort/local.rules` – Règles custom : scan Nmap, bruteforce SSH/HTTP, SQLi, XSS, traversal

#### Documentation
- `docs/README.md` – Index de la documentation
- `docs/architecture.md` – Architecture technique complète avec diagrammes
- `docs/installation.md` – Guide d'installation Docker et local
- `docs/usage.md` – Guide d'utilisation interface + API
- `docs/modules.md` – Référence de chaque module
- `docs/api.md` – Référence API REST complète
- `docs/securite.md` – Sécurité, RBAC, conformité RGPD
- `docs/livrables.md` – Livrables pédagogiques + grille d'évaluation

#### Scripts
- `scripts/start.sh` – Lancement de la stack (dev/prod/stop/logs/status)
- `scripts/push_gitlab.sh` – Init Git + push sur GitLab

#### Racine
- `.env.example` – Template de configuration
- `.gitignore` – Exclusions Git
- `README.md` – Présentation du projet
- `backend/pyproject.toml` – Dépendances Poetry

---

## À venir

- [ ] Alembic (migrations DB)
- [ ] Endpoint de suppression de compte (RGPD)
- [ ] Rate limiting (`slowapi`)
- [ ] Module IAM avancé (MFA, SSO)
- [ ] Pipeline GitLab CI/CD
- [ ] Tests unitaires complémentaires
- [ ] Dashboard Kibana préconfiguré (export JSON)
