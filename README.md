# ToolboxV8

[![Version](https://img.shields.io/badge/version-1.2.2-blue.svg)](.claude/changelog.md)
[![Python](https://img.shields.io/badge/python-3.11-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-compose-2496ED.svg)](https://docs.docker.com/compose/)
[![Kali](https://img.shields.io/badge/worker-Kali_Rolling-557C94.svg)](https://www.kali.org/)
[![Status](https://img.shields.io/badge/status-stable-success.svg)](.claude/changelog.md)

**Toolbox automatisée de tests d'intrusion** — Mastère Cybersécurité 2025/2026

Plateforme web qui automatise les étapes d'un pentest (reconnaissance, scan de vulnérabilités, exploitation, audit web) et produit des rapports PDF prêts à livrer au client. **L'ergonomie est pensée pour un analyste, pas pour un développeur** : un seul formulaire, un choix de profil par chips, un clic.

---

## ✨ Quoi de neuf — v1.2.2 (mai 2026)

- 🎛 **Toggle Nmap NSE** : activable/désactivable indépendamment dans le module Scan, avec **4 profils** (Quick / Standard / Full / Safe).
- ⏱ **Timeouts dynamiques** par profil Nikto (10/15/30/60 min) — fini les coupures prématurées sur cibles distantes.
- 🔒 **SSLyze modernisé** : passage de l'argument `--regular` (obsolète) à `--mozilla_config intermediate` (sslyze ≥ 5.x).
- 🧹 **Filtre des fingerprints nmap** : les blocs `==NEXT SERVICE FINGERPRINT==` illisibles sont retirés de la sortie (gain ~90 % sur la taille des rapports).
- 🌐 **Whois résilient** : fallback automatique sur le domaine racine pour les sous-domaines (`scanme.nmap.org` → `nmap.org`).
- 👤 **Compte admin auto-créé** par `start.sh` et `start.ps1` après le premier démarrage (plus de "ID ou mdp incorrect" pour les nouveaux contributeurs).
- 🛡 **3 nouvelles règles Snort** : détection scan Nikto, détection scan sqlmap, détection injection Log4Shell (CVE-2021-44228).

➡ Détail complet dans [.claude/changelog.md](.claude/changelog.md).

---

## 🚀 Démarrage rapide

```bash
# 1. Cloner
git clone https://github.com/Vyuob/toolbox-m1.git
cd toolbox-m1

# 2. Copier la configuration
cp .env.example .env

# 3. Lancer la stack complète (build + démarrage + création auto admin)
./scripts/start.sh        # Linux / macOS
.\scripts\start.ps1       # Windows (PowerShell)

# 4. Ouvrir l'interface
open http://localhost:3000/login
```

> 🔑 **Identifiants par défaut** : `admin` / `admin123` (créés automatiquement au premier démarrage). Modifie-les en production.

---

## 🌐 Interfaces disponibles

| Service | URL | Rôle |
|---------|-----|------|
| **Interface web** | http://localhost:3000 | Login, dashboard, modules, rapports, SIEM |
| **API Swagger** | http://localhost:8000/api/docs | Documentation REST pour clients externes |
| **Kibana (SIEM brut)** | http://localhost:5601 | Exploration brute des logs Elasticsearch |
| **MinIO Console** | http://localhost:9001 | Stockage S3 des rapports (`minioadmin / minioadmin`) |
| **Elasticsearch** | http://localhost:9200 | Backend SIEM (logs) |

---

## 🏗 Architecture

Stack **dockerisée** en 3 services applicatifs + infra :

```
Navigateur ──► web:3000 ──┬──► pages HTML (Jinja2, cookie HttpOnly)
                          └──► proxy /api/* ──► api:8000 ──► PostgreSQL
                                                         └─► Redis ──► worker (Kali Rolling)
                                                                            └─► outils pentest
```

- **web** (FastAPI, port 3000) — sert les pages HTML, gère l'auth via formulaire + cookie HttpOnly, proxifie `/api/*` vers l'API
- **api** (FastAPI, port 8000) — endpoints REST pur `/api/*`, utilisable directement pour intégrations externes
- **worker** (Celery + Kali Rolling) — exécute les scans offensifs avec **tous les outils Kali préinstallés**
- **infra** — PostgreSQL 16, Redis 7, MinIO, Elasticsearch 8.13 + Logstash + Kibana, Snort 3

---

## 🛠 Modules pentest

| Module | Outils (préinstallés dans Kali) | Profils chips | Type |
|--------|--------------------------------|---------------|------|
| **recon** | Nmap, DNS (résolution), whois | Quick / Standard / Full TCP / Stealth | Offensif |
| **scan** | Nmap NSE, Nikto, SSLyze (toggles indépendants) | NSE: Quick/Standard/Full/Safe • Nikto: Quick/Standard/Full/Evasion • SSLyze: Cert/Standard/Full | Offensif |
| **exploit** | SQLmap, Hydra, John the Ripper (jumbo 304 formats), Metasploit | SQLmap: Quick/Standard/Aggressive/Dump • MSF: Handler/EternalBlue/PortScan/SMB | Offensif |
| **web_scan** | OWASP ZAP (Spider + Active), Dependency-Check | ZAP Spider: Quick/Standard/Deep • ZAP Active: Quick/OWASP/Full | Offensif |
| **siem** | Elasticsearch, Logstash, Kibana | — | Défensif |
| **ids** | Snort 3 (avec règles locales : Nmap, Nikto, sqlmap, Log4Shell, SQLi, XSS, traversal, brute-force) | — | Défensif |
| **forensic** | ClamAV, VirusTotal API | — | Défensif (bonus) |

> Le retour de chaque outil est la **sortie CLI brute**, rendue telle quelle dans le rapport PDF (un analyste reconnaît ses outils).

---

## ⭐ Fonctionnalités clés

### Sécurité applicative
- 🔐 **Auth par formulaire web** + cookie HttpOnly (signé JWT côté backend) ; `POST /api/auth/token` reste utilisable pour les clients externes (Bearer token)
- 🛡 **RBAC** à 3 rôles : `admin`, `analyst`, `reader`
- 📜 **Audit logs** : toute action sensible (login, lancement de scan, génération de rapport, blocage IP) tracée en base
- 🔑 **Chiffrement Fernet** pour les secrets stockés
- 👤 **Création auto du compte admin** au premier démarrage (Windows et Linux/macOS)

### UX & ergonomie
- 🎛 **Profils chips** sur tous les modules offensifs — pas de ligne de commande à éditer
- 🔄 **Toggles indépendants** dans le module Scan — désactiver Nikto/SSLyze/NSE séparément
- 🎯 Le rapport **masque les outils désactivés** (plus de sections vides "Aucune donnée")
- 🚦 Le badge **"Erreur"** s'affiche correctement quand un outil retourne stderr sans sortie utile

### Robustesse des modules
- ⏱ **Timeouts adaptés** par profil Nikto (10 → 60 min)
- 🧹 **Filtre des dumps de fingerprints nmap** dans la sortie (`==NEXT SERVICE FINGERPRINT==`)
- 🌐 **Whois avec fallback** sur le domaine racine pour les sous-domaines
- 🔒 **SSLyze ≥ 5.x** : `--mozilla_config intermediate` au lieu de `--regular` (retiré de l'outil)

### Outillage avancé
- 📤 **Upload de wordlists** via `POST /api/modules/wordlist` (volume partagé api↔worker) — utilisable par Hydra et John
- 🔓 **Hydra** : 3 sources au choix pour users/passwords (fichier uploadé, liste manuelle dans une modale, rockyou.txt par défaut)
- 🔨 **John the Ripper jumbo** : bcrypt, sha512crypt, NTLM, argon2, keepass, zip… (304 formats)

### Reporting
- 📄 **Rapport PDF** (ReportLab) : charte professionnelle (header bleu, encart CODIR orange, tableau synthétique), sortie CLI brute préservée par outil
- 🌐 **Rendu HTML** également disponible (pour pré-visualisation web)

### Visibilité
- 📊 **SIEM** : collecte via Logstash, visualisation dans la page `/siem` (Chart.js)
- 🚨 **IDS** : Snort 3 avec 9 règles locales (scan, brute-force, SQLi, XSS, traversal, Nikto, sqlmap, Log4Shell)

---

## 🧰 Stack technique

| Couche | Technologie |
|---|---|
| Backend | Python 3.11, FastAPI, SQLAlchemy, Celery 5, Pydantic v2 |
| Frontend | Jinja2 + HTML/CSS/JS vanilla, Lucide icons, Chart.js |
| Base de données | PostgreSQL 16 |
| File de tâches | Redis 7 + Celery (concurrency=4) |
| Stockage objet | MinIO (S3-compatible) |
| SIEM | Elasticsearch 8.13 + Logstash + Kibana |
| IDS | Snort 3 |
| Worker pentest | **Kali Linux Rolling** (image officielle), build multi-stage |
| Conteneurisation | Docker + Docker Compose v2 |
| Reporting | ReportLab 4 (PDF) + Jinja2 (HTML optionnel) |

---

## 📚 Documentation

Dossier [docs/](docs/README.md) :

- 📐 [Architecture](docs/architecture.md) — split api/web, flux d'auth, orchestration Celery
- ⚙ [Installation](docs/installation.md) — prérequis, `.env`, commandes Docker
- 🖥 [Utilisation](docs/usage.md) — parcours utilisateur, captures de l'UI
- 🛠 [Modules](docs/modules.md) — détail de chaque outil, profils, options
- 🌐 [API REST](docs/api.md) — référence des endpoints, exemples curl
- 🔐 [Sécurité](docs/securite.md) — auth, RBAC, chiffrement, audit
- 🎓 [Livrables](docs/livrables.md) — correspondance avec le cadre pédagogique
- 📜 [Changelog](.claude/changelog.md) — historique des versions

---

## 👥 Équipe

- **Étudiant 1** – Architecte / Back-end (FastAPI, Celery, Docker, sécurité)
- **Étudiant 2** – Intégration offensive / QA (modules pentest, tests, validation)
- **Étudiant 3** – Interface & Reporting (Jinja2, PDF ReportLab, UX)

---

> ⚠ **Projet réalisé dans un cadre pédagogique.**
> Utilisation uniquement sur des **systèmes pour lesquels vous avez une autorisation écrite explicite**.
> Le scan non autorisé d'un système tiers est puni par l'article 323-1 du Code pénal français (jusqu'à 3 ans d'emprisonnement et 100 000 € d'amende).
