# ToolboxV8

**Toolbox automatisée de tests d'intrusion** – Mastère Cybersécurité 2025/2026

Plateforme web qui automatise les étapes d'un pentest (reconnaissance, scan, exploitation, analyse web) et produit des rapports PDF structurés, prêts à livrer au client. L'ergonomie est pensée pour un analyste, pas pour un développeur : un seul formulaire, un choix de profil, un clic.

---

## Démarrage rapide

```bash
# 1. Cloner le projet
git clone https://github.com/Vyuob/toolbox-m1.git
cd toolbox-m1

# 2. Copier la configuration
cp .env.example .env

# 3. Lancer la stack complète
./scripts/start.sh        # Linux / macOS
.\scripts\start.ps1       # Windows (PowerShell)

# 4. Ouvrir l'interface
open http://localhost:3000/login
```

Identifiants par défaut seedés : `admin` / `admin`.

---

## Interfaces disponibles

| Service | URL | Rôle |
|---------|-----|------|
| **Interface web** | http://localhost:3000 | Login, dashboard, modules, rapports, SIEM |
| **API Swagger** | http://localhost:8000/api/docs | Documentation REST pour clients externes |
| **MinIO Console** | http://localhost:9001 | Stockage S3 des rapports |
| **Elasticsearch** | http://localhost:9200 | Backend SIEM (logs) |

---

## Architecture

Stack **dockerisée** en 3 services applicatifs + infra :

```
Navigateur ──► web:3000 ──┬──► pages HTML (Jinja2, cookie HttpOnly)
                          └──► proxy /api/* ──► api:8000 ──► PostgreSQL
                                                         └─► Redis ──► worker (Kali Rolling)
                                                                            └─► outils pentest
```

- **web** (FastAPI, port 3000) : sert les pages HTML, gère l'auth via formulaire + cookie HttpOnly, proxifie `/api/*` vers l'API
- **api** (FastAPI, port 8000) : endpoints REST pur `/api/*`, reste disponible pour intégrations externes
- **worker** (Celery + Kali Rolling) : exécute les scans offensifs avec tous les outils préinstallés
- **db** PostgreSQL, **redis**, **minio**, **elasticsearch+logstash+kibana**, **snort**

---

## Modules pentest

| Module | Outils (préinstallés dans Kali) | Type |
|--------|---------------------------------|------|
| **recon** | Nmap, DNS (résolution), whois | Offensif |
| **scan** | Nmap NSE (--script=vuln), Nikto, SSLyze | Offensif |
| **exploit** | SQLmap, Hydra, John the Ripper (jumbo, 304 formats), Metasploit | Offensif |
| **web_scan** | OWASP ZAP (Spider + Active), Dependency-Check | Offensif |
| **siem** | Elasticsearch, Logstash, Kibana | Défensif |
| **ids** | Snort 3 | Défensif |
| **forensic** | ClamAV, VirusTotal API | Défensif (bonus) |

Chaque outil expose des **profils par chips** (Quick / Standard / Full / …) qui mappent vers la vraie ligne de commande — pas de textarea éditable à remplir. Le retour est la sortie CLI brute, rendue telle quelle dans le rapport PDF.

---

## Fonctionnalités clés

- **Auth par formulaire web** + cookie HttpOnly (signé JWT côté backend) ; `POST /api/auth/token` reste utilisable pour les clients externes
- **RBAC** à 3 rôles : `admin`, `analyst`, `reader`
- **Création auto du compte admin** (`admin` / `admin`) au premier démarrage via `start.sh` ou `start.ps1`
- **Profils chips** sur tous les modules offensifs — Nmap recon (Quick/Standard/Full TCP/Stealth), **Nmap NSE** (Quick/Standard/Full/Safe), Nikto (Quick/Standard/Full/Evasion), SSLyze (Cert/Standard/Full), SQLmap, Metasploit, ZAP
- **Toggles indépendants** dans le module Scan — Nmap NSE / Nikto / SSLyze activables séparément, les outils désactivés sont masqués du rapport
- **Timeouts adaptés** par profil Nikto (10/15/30/60 min) pour éviter les coupures sur cibles distantes
- **Filtre des dumps de fingerprints nmap** dans la sortie (gain ~90 % sur la taille des rapports)
- **Whois avec fallback** sur le domaine racine pour les sous-domaines
- **Upload de wordlists** personnelles via `POST /api/modules/wordlist` (volume partagé api↔worker) — utilisable par Hydra et John
- **Hydra** : 3 sources au choix pour users/passwords (fichier uploadé, liste manuelle dans une modale, rockyou.txt par défaut)
- **John the Ripper jumbo** : bcrypt, sha512crypt, NTLM, argon2, keepass, zip… (304 formats)
- **Rapport PDF** (ReportLab) : charte professionnelle (header bleu, encart CODIR orange, tableau synthétique), sortie CLI brute préservée par outil
- **SIEM** : collecte via Logstash, visualisation dans la page `/siem` (Chart.js)
- **IDS** : Snort 3 avec règles locales
- **Audit logs** : toute action sensible (login, lancement de scan, génération de rapport) tracée en base
- **Chiffrement Fernet** pour les secrets stockés

---

## Stack technique

- **Backend** : Python 3.11, FastAPI, SQLAlchemy, Celery, Pydantic v2
- **Frontend** : HTML/CSS/JS (Jinja2, Lucide icons, Chart.js — pas de framework JS)
- **Base de données** : PostgreSQL 16
- **File de tâches** : Redis 7 + Celery 5 (concurrency=4)
- **Stockage objet** : MinIO (S3-compatible)
- **SIEM** : Elasticsearch 8.13 + Logstash + Kibana
- **IDS** : Snort 3
- **Worker pentest** : **Kali Linux Rolling** (image officielle), build multi-stage
- **Conteneurisation** : Docker + Docker Compose v2
- **PDF** : ReportLab 4 (HTML optionnel via Jinja2)

---

## Documentation

Dossier [docs/](docs/README.md) :

- [Architecture](docs/architecture.md) — split api/web, flux d'auth, orchestration Celery
- [Installation](docs/installation.md) — prérequis, `.env`, commandes Docker
- [Utilisation](docs/usage.md) — parcours utilisateur, captures de l'UI
- [Modules](docs/modules.md) — détail de chaque outil, profils, options
- [API REST](docs/api.md) — référence des endpoints, exemples curl
- [Sécurité](docs/securite.md) — auth, RBAC, chiffrement, audit
- [Livrables](docs/livrables.md) — correspondance avec le cadre pédagogique

---

## Équipe

- **Étudiant 1** – Architecte / Back-end (FastAPI, Celery, Docker, sécurité)
- **Étudiant 2** – Intégration offensive / QA (modules pentest, tests, validation)
- **Étudiant 3** – Interface & Reporting (Jinja2, PDF ReportLab, UX)

---

> Projet réalisé dans un cadre pédagogique.
> **Utilisation uniquement sur des systèmes autorisés.**
