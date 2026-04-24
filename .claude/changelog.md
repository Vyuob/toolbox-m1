# Changelog – PentestBox

Toutes les modifications notables du projet sont documentees ici.
Format : `[version] – date – description`

---

## [1.2.1] – 2026-04-24 – Création automatique du compte admin côté Linux/macOS

### Corrige
- `scripts/start.sh` : ajoute la fonction `ensure_admin()` qui crée automatiquement le compte admin (`admin` / `admin123`) après démarrage de la stack. Auparavant seul `start.ps1` (Windows) créait le compte, provoquant une erreur "ID ou mot de passe incorrect" pour tout utilisateur Linux/macOS après un clone frais (DB vide).
- La fonction vérifie d'abord via `POST /api/auth/token` si le compte existe ; ne le crée que si absent.

### Documentation
- `docs/installation.md` : précise que le compte admin est créé automatiquement par les scripts de démarrage, aligne les identifiants documentés (`admin` / `admin123`, anciennement `Admin1234!` incohérent avec le script).

---

## [1.2.0] – 2026-04-24 – Stabilisation modules Recon et Scan

### Corrige

#### Reconnaissance (`recon`)
- Ajoute `-Pn` dans les 4 presets Nmap UI et le défaut backend. Les cibles derrière un pare-feu qui bloque ICMP (Windows Defender, gateways WSL/Hyper-V) peuvent maintenant être scannées.
- Whois : retombe automatiquement sur le domaine racine si le registry rejette le sous-domaine (`scanme.nmap.org` → `nmap.org`, plus de "Malformed request").
- Filtre les blocs `==NEXT SERVICE FINGERPRINT==` (dumps d'octets bruts pour services inconnus) de la sortie nmap — gain typique ~90 % sur la taille des rapports.

#### Scan de vulnérabilités (`scan`)
- Toggle **Activer Nmap NSE** désormais exposé dans l'UI (auparavant toujours actif, non désactivable).
- Nmap NSE propose 4 profils : Quick (`--script=default`), Standard (`--script=vuln`), Full (`--script=vuln,exploit,auth`), Safe (`--script=safe`).
- Timeout Nmap NSE porté à 20 min (était 10 min).
- Nikto : timeout adapté par profil — Quick 10 min, Standard 30 min, Full 60 min, Evasion 15 min (évite les coupures prématurées).
- SSLyze modernisé : `--regular` remplacé par `--mozilla_config intermediate` + scans individuels (sslyze ≥ 5.x, l'argument `--regular` a été retiré).
- Champ `port` pré-rempli avec `80,443` (était un placeholder grisé non envoyé au backend, provoquant des scans sur 1000 ports et des timeouts).

#### Rapport (`reporting/generator.py`)
- Les outils désactivés (dict vide côté backend) n'apparaissent plus dans le PDF/HTML.
- Badge "Erreur" dans le tableau synthétique quand l'outil renvoie stderr sans sortie utile (au lieu de "Collecté" trompeur).

#### Frontend (`modules.html`)
- `collectOptions()` lit maintenant aussi les `<textarea>` (auparavant seuls `input`/`select` étaient lus → les args Nmap du textarea n'étaient jamais envoyés au backend, qui tombait sur son défaut).
- Pré-remplissage du champ port avec `80,443` dans le module Scan.
- Presets SSLyze frontend alignés avec sslyze 6.x.

### Ajoute
- `_strip_nmap_fingerprints()` helper partagé entre `recon.py` et `scan.py`.
- Constante `_NMAP_VULN_PROFILES` (profils NSE) et `_NIKTO_PROFILES` enrichie d'un champ `timeout` par profil.

### Documentation
- `docs/modules.md` : sections Recon et Scan réécrites avec les nouveaux profils et comportements.
- `docs/usage.md` : table des options clés mise à jour, liste des chips par module.

---

## [1.1.0] – 2026-04-12 – Pages frontend + routes defensives + GitHub

### Ajoute

#### Backend
- `backend/app/api/routes/defensive.py` – Routes SIEM mini-dashboard (metriques, etat services, series temporelles)
- `backend/app/api/routes/pages.py` – Routes de rendu HTML (redirection racine, pages Jinja2)

#### Frontend
- `frontend/templates/modules.html` – Page Modules (lancement et suivi des scans)
- `frontend/templates/reports.html` – Page Rapports (liste et consultation)
- `frontend/templates/siem.html` – Page SIEM (dashboard defensif)
- `frontend/static/css/app.css` – Styles supplementaires de l'application
- `frontend/static/js/app.js` – Logique JS supplementaire de l'application

#### Scripts
- `scripts/start.ps1` – Script PowerShell de lancement (dev/prod/stop/logs/status/rebuild)
- `scripts/push_gitlab.ps1` – Script PowerShell pour init Git + push

#### Outils
- `pentest_rapport_generator/` – Generateur de rapports pentest standalone (HTML/JS)

### Modifie
- Migration du depot de GitLab vers **GitHub** : https://github.com/Vyuob/toolbox-m1

---

## [1.0.0] – 2026-04-09 – Initialisation complete du projet

### Ajoute

#### Backend
- `backend/app/main.py` – Application FastAPI avec middlewares CORS et TrustedHost
- `backend/app/core/config.py` – Configuration centralisee via Pydantic Settings + `.env`
- `backend/app/core/security.py` – JWT (HS256), bcrypt, Fernet
- `backend/app/core/auth.py` – Dependances FastAPI : `get_current_user`, `require_role`, `require_admin`, `require_analyst`
- `backend/app/core/database.py` – SQLAlchemy engine + `get_db()`
- `backend/app/models/user.py` – Modele `User` (id, username, email, hashed_pwd, role, is_active)
- `backend/app/models/scan.py` – Modeles `ScanJob`, `Report`, `AuditLog`
- `backend/app/api/routes/auth.py` – Routes : `/token`, `/register`, `/me`
- `backend/app/api/routes/modules.py` – Routes : liste modules, lancement, suivi jobs
- `backend/app/api/routes/reports.py` – Routes : generation, liste, telechargement
- `backend/app/api/routes/dashboard.py` – Route dashboard HTML + stats JSON
- `backend/app/tasks/celery_app.py` – Instance Celery configuree
- `backend/app/tasks/scan_tasks.py` – Taches async : recon, scan, exploit, web_scan
- `backend/app/tasks/report_tasks.py` – Tache async : generation rapport
- `backend/app/modules/offensive/recon.py` – DNS + Nmap + whois
- `backend/app/modules/offensive/scan.py` – Nmap NSE + Nikto + SSLyze
- `backend/app/modules/offensive/exploit.py` – SQLmap + Hydra + Metasploit
- `backend/app/modules/offensive/web_scan.py` – OWASP ZAP + Dependency-Check
- `backend/app/modules/offensive/post_exploit.py` – Enumeration + verification persistance
- `backend/app/modules/defensive/siem.py` – Integration Elasticsearch (index/search/alerts)
- `backend/app/modules/defensive/ids.py` – Parser alertes Snort
- `backend/app/modules/defensive/response.py` – Blocage IP iptables + alertes SIEM
- `backend/app/modules/defensive/forensic.py` – ClamAV + VirusTotal API
- `backend/app/reporting/generator.py` – Generation PDF (WeasyPrint), HTML, CSV + upload MinIO
- `backend/tests/test_api.py` – Tests d'integration de base

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
- `docker/docker-compose.yml` – Stack complete : API, worker, PostgreSQL, Redis, MinIO, ELK, Kibana

#### SIEM
- `siem/elk/logstash.conf` – Pipeline Logstash (beats + Snort + Docker -> Elasticsearch)
- `siem/elk/elasticsearch.yml` – Configuration Elasticsearch single-node
- `siem/snort/snort.conf` – Configuration Snort 3
- `siem/snort/local.rules` – Regles custom : scan Nmap, bruteforce SSH/HTTP, SQLi, XSS, traversal

#### Documentation
- `docs/README.md` – Index de la documentation
- `docs/architecture.md` – Architecture technique complete avec diagrammes
- `docs/installation.md` – Guide d'installation Docker et local
- `docs/usage.md` – Guide d'utilisation interface + API
- `docs/modules.md` – Reference de chaque module
- `docs/api.md` – Reference API REST complete
- `docs/securite.md` – Securite, RBAC, conformite RGPD
- `docs/livrables.md` – Livrables pedagogiques + grille d'evaluation

#### Scripts
- `scripts/start.sh` – Lancement de la stack (dev/prod/stop/logs/status)
- `scripts/push_gitlab.sh` – Init Git + push sur GitLab

#### Racine
- `.env.example` – Template de configuration
- `.gitignore` – Exclusions Git
- `README.md` – Presentation du projet
- `backend/pyproject.toml` – Dependances Poetry

---

## A venir

- [ ] Alembic (migrations DB)
- [ ] Endpoint de suppression de compte (RGPD)
- [ ] Rate limiting (`slowapi`)
- [ ] Module IAM avance (MFA, SSO)
- [ ] Pipeline CI/CD GitHub Actions
- [ ] Tests unitaires complementaires
- [ ] Dashboard Kibana preconfigure (export JSON)
