# Rapport Technique Final — Projet PentestBox
## Mastere Cyberscurite — Promotion 2025

---

## Table des matieres

1. [Presentation du projet](#1-presentation-du-projet)
2. [Analyse du besoin](#2-analyse-du-besoin)
3. [Organisation et methodologie](#3-organisation-et-methodologie)
4. [Solution technique](#4-solution-technique)
5. [Tests et resultats](#5-tests-et-resultats)
6. [Problemes rencontres et solutions](#6-problemes-rencontres-et-solutions)
7. [Securite et conformite](#7-securite-et-conformite)
8. [SIEM et supervision](#8-siem-et-supervision)
9. [Annexes](#9-annexes)

---

## 1. Presentation du projet

### 1.1 Contexte

Le client est une societe specialisee en cybersecurite offensive, realisant des tests d'intrusion pour des entreprises privees et des institutions publiques. Ces tests reposent majoritairement sur des manipulations manuelles, ce qui les rend longs et heterogenes selon les intervenants.

### 1.2 Objectif general

Developper une **toolbox automatisee** — PentestBox — permettant de realiser l'ensemble des etapes d'un pentest avec une interface simple, des modules reutilisables et un reporting standardise.

### 1.3 Objectifs specifiques

- Reduire d'au moins 40% le temps de realisation d'un pentest
- Standardiser les pratiques internes
- Proposer une interface exploitable par des profils analystes
- Renforcer la qualite et la lisibilite des rapports
- Permettre une integration simple dans l'ecosysteme technique du client

### 1.4 Equipe

| Membre | Role | Responsabilites |
|--------|------|-----------------|
| [Nom 1] | Architecte / Dev Back-end | Architecture, orchestration, integration outils, securisation |
| [Nom 2] | Analyste / QA | Integration des outils de scan, tests, validation |
| [Nom 3] | Interface & Reporting | Interface web, generation des rapports, dashboards |

> **A COMPLETER** : Remplacer [Nom X] par les noms reels des membres de l'equipe.

---

## 2. Analyse du besoin

### 2.1 Enjeux par pole

| Pole | Besoins specifiques | Outils integres dans PentestBox |
|------|--------------------|---------------------------------|
| Securite (SOC, EDR, XDR) | Tests cibles sur les systemes de detection | Nmap, OWASP ZAP |
| Developpement SaaS | Tests d'applications web et API | SQLmap, Dependency-Check |
| Infrastructure | Evaluation des systemes internes et reseaux | Nmap NSE, Hydra, SSLyze |
| Support client | Tests de securite des outils de communication | Nikto, SSLyze |

### 2.2 Menaces identifiees

- **DDoS** : surcharge des services exposes
- **Injection SQL** : compromission des bases de donnees
- **Phishing / Credential stuffing** : vol d'identifiants
- **RCE (Remote Code Execution)** : execution de code a distance via vulnerabilites non patchees
- **Man-in-the-Middle** : interception sur configurations TLS faibles

### 2.3 Fonctionnalites attendues (cahier des charges)

1. Modules automatises couvrant toutes les etapes du pentest
2. Integration d'outils open-source via API, CLI ou bibliotheques Python
3. Reporting automatise exportable (PDF, HTML, CSV)
4. Interface simple et intuitive
5. Architecture modulaire permettant l'ajout de modules
6. Securisation de l'outil (authentification, chiffrement, logging)
7. Module forensique pour l'analyse post-compromission (bonus)

---

## 3. Organisation et methodologie

### 3.1 Methodologie

Methode **Agile Scrum** adaptee avec des sprints de 2 semaines :

| Sprint | Objectif | Duree |
|--------|----------|-------|
| S1 | Architecture, Docker, auth JWT, modeles de donnees | 2 semaines |
| S2 | Modules offensifs (recon, scan, exploit, web_scan) | 2 semaines |
| S3 | Interface web, dashboard, SIEM interne | 2 semaines |
| S4 | Modules defensifs (ELK, Snort, reponse active) | 2 semaines |
| S5 | Reporting PDF/HTML/CSV, securisation HTTPS | 2 semaines |
| S6 | Tests, documentation, video MVP, corrections | 2 semaines |

### 3.2 Outils de gestion

- **Git / GitLab** : versionning du code et CI/CD
- **Docker / Docker Compose** : conteneurisation et orchestration
- **VS Code** : IDE principal
- **Postman / Swagger** : tests API

### 3.3 Arborescence du projet

```
projet/
  backend/           # API FastAPI + modules Python
    app/
      api/routes/    # Endpoints REST
      core/          # Config, auth, database, security
      models/        # Modeles SQLAlchemy
      modules/       # Modules offensifs et defensifs
      tasks/         # Taches Celery asynchrones
      reporting/     # Generateur de rapports
  frontend/          # Interface web
    templates/       # Pages HTML (Jinja2)
    static/css/      # Styles CSS
    static/js/       # JavaScript
  docker/            # Dockerfiles + docker-compose.yml
  siem/              # Config ELK Stack + Snort
  docs/              # Documentation technique
  scripts/           # Scripts de demarrage
```

---

## 4. Solution technique

### 4.1 Stack technologique

| Composant | Technologie | Justification |
|-----------|------------|---------------|
| Backend API | Python 3.11 + FastAPI | Performance async, documentation auto (Swagger) |
| Base de donnees | PostgreSQL 16 | Robuste, support JSON, transactions ACID |
| Cache / Broker | Redis 7 | Rapide, broker Celery, cache de sessions |
| Taches async | Celery 5.4 | Execution parallele des scans longs |
| Stockage fichiers | MinIO | Compatible S3, stockage des rapports |
| SIEM | Elasticsearch 8.13 + Logstash + Kibana | Analyse de logs, dashboards securite |
| IDS | Snort 3 | Detection d'intrusion reseau |
| Conteneurisation | Docker + Docker Compose | Deploiement reproductible, isolation |
| Frontend | HTML/CSS/JS + Jinja2 + Lucide Icons | Leger, pas de framework lourd |
| Graphiques | Chart.js 4 | Graphiques temps reel dans le SIEM |

### 4.2 Architecture systeme

```
                    +-------------------+
                    |   Navigateur Web  |
                    |  (HTML/CSS/JS)    |
                    +--------+----------+
                             |
                    +--------v----------+
                    |   FastAPI (API)   |
                    |   Port 8000       |
                    +--+-----+------+---+
                       |     |      |
              +--------+  +--+--+  +--------+
              |           |     |           |
     +--------v--+  +-----v-+  +--v-------+ +--v--------+
     | PostgreSQL |  | Redis |  | Celery   | | MinIO     |
     | (donnees)  |  | (cache|  | Workers  | | (fichiers)|
     +------------+  +-------+  +----+-----+ +-----------+
                                     |
                        +------------+-------------+
                        |            |             |
                   +----v----+  +---v----+  +-----v-----+
                   | Nmap    |  | SQLmap |  | Nikto     |
                   | Hydra   |  | ZAP    |  | SSLyze    |
                   +---------+  +--------+  +-----------+
                        
              +------------------------------------------+
              |        ELK Stack (SIEM)                  |
              | Elasticsearch + Logstash + Kibana        |
              +------------------------------------------+
```

### 4.3 Modele de donnees

| Table | Champs principaux | Description |
|-------|------------------|-------------|
| `users` | id, username, email, hashed_password, role, is_active | Utilisateurs avec RBAC |
| `scan_jobs` | id, task_id, module, target, options, status, result | Jobs de scan |
| `reports` | id, title, scan_job_id, format, file_path | Rapports generes |
| `audit_logs` | id, user_id, action, detail, ip_address, timestamp | Journalisation |

### 4.4 Modules implementes

#### Modules offensifs

| Module | Outils integres | Fonction |
|--------|----------------|----------|
| Reconnaissance | Nmap, DNS, Whois | Decouverte d'hotes, ports, services |
| Scan vulnerabilites | Nmap NSE, Nikto, SSLyze | Detection de failles connues |
| Exploitation | SQLmap, Hydra, Metasploit | Exploitation active des vulnerabilites |
| Web/API scan | OWASP ZAP, Dependency-Check | Audit securite web et dependances |

#### Modules defensifs

| Module | Outils integres | Fonction |
|--------|----------------|----------|
| SIEM | Elasticsearch, Logstash, Kibana | Collecte et analyse de logs |
| IDS | Snort 3 | Detection d'intrusion en temps reel |
| Reponse active | iptables, alertes | Blocage automatique d'IP |
| Forensique | ClamAV, VirusTotal API | Analyse post-compromission |

### 4.5 Interface web

L'interface PentestBox comprend 5 pages principales :

| Page | URL | Fonction |
|------|-----|----------|
| Login | `/login` | Authentification JWT |
| Dashboard | `/dashboard` | KPIs, jobs recents, lancement rapide |
| Modules | `/modules` | Lancement de scans avec presets configurables |
| Rapports | `/reports` | Generation, visualisation et telechargement |
| SIEM | `/siem` | Dashboard de securite temps reel, etat des services |

### 4.6 Reporting

Trois formats de rapports disponibles :
- **PDF** : genere via ReportLab, structure professionnelle (cover, synthese CODIR, resultats detailles, recommandations)
- **HTML** : visualisation inline dans le navigateur
- **CSV** : export tabulaire pour analyse Excel

---

## 5. Tests et resultats

### 5.1 Scenarios de test

| Scenario | Module | Cible | Resultat attendu |
|----------|--------|-------|-----------------|
| Scan reseau local | Reconnaissance | 192.168.x.x | Ports ouverts, services detectes |
| Audit web | Scan vulnerabilites | site-test.com | CVE detectees, headers manquants |
| Injection SQL | Exploitation (SQLmap) | URL avec parametre GET | Detection de l'injection |
| Brute-force SSH | Exploitation (Hydra) | IP avec SSH | Test de credentials |
| Crawl web | Web/API (ZAP Spider) | URL application | Cartographie des endpoints |
| Rapport PDF | Reporting | Job termine | PDF genere et telechargeable |

### 5.2 Resultats obtenus

> **A COMPLETER** : Inserer ici les captures d'ecran et resultats des tests realises.
> Exemples :
> - Screenshot du terminal CLI pendant un scan
> - Screenshot du dashboard SIEM avec les metriques
> - Screenshot d'un rapport PDF genere
> - Logs d'un scan de reconnaissance
> - Tableau recapitulatif des vulnerabilites trouvees

### 5.3 KPIs mesures

| KPI | Objectif | Resultat |
|-----|----------|----------|
| Temps d'execution (recon) | < 2 min | A MESURER |
| Temps d'execution (scan complet) | < 10 min | A MESURER |
| Taux de succes des scans | > 90% | Visible dans `/siem` |
| Nombre de modules fonctionnels | 8+ | 9 modules (5 off + 4 def) |

---

## 6. Problemes rencontres et solutions

| Probleme | Cause | Solution |
|----------|-------|----------|
| Nikto non disponible dans Debian | Package absent des repos Trixie/Bookworm | Installation via `git clone` depuis GitHub |
| WeasyPrint crash PDF | Incompatibilite pydyf/Pillow 12 | Remplacement par ReportLab (pur Python) |
| bcrypt Internal Server Error | passlib incompatible avec bcrypt >= 4.0 | Pin `bcrypt < 4.0.0` dans pyproject.toml |
| Email .local rejete | Pydantic email-validator rejette les TLD .local | Utilisation d'un email valide (.com) |
| Docker version warning | Cle `version` depreciee dans docker-compose | Suppression de la cle `version: "3.9"` |
| PowerShell encoding UTF-8 | Caracteres corrompus dans la console | `[Console]::OutputEncoding = UTF8` apres `param()` |
| FK violation a la suppression | Reports referencent scan_jobs | Suppression en cascade des reports lies |
| Celery result expire | AsyncResult vide apres expiration | Stockage des logs dans job.result en DB |

---

## 7. Securite et conformite

### 7.1 Authentification et autorisation

- **JWT (HS256)** : tokens avec expiration de 60 minutes
- **bcrypt** : hachage des mots de passe (12 rounds)
- **RBAC** : 3 roles (admin, analyst, reader)
- **Fernet (AES-128-CBC)** : chiffrement des donnees sensibles au repos

### 7.2 Protection de l'API

| Mesure | Implementation |
|--------|---------------|
| CORS | Origins restreintes |
| TrustedHost | Middleware de validation |
| Validation | Pydantic v2 sur tous les inputs |
| ORM | SQLAlchemy (prevention injection SQL) |
| Templates | Jinja2 autoescape (prevention XSS) |
| Audit | Toutes les actions sensibles loggees |

### 7.3 Conformite RGPD

- Minimisation des donnees collectees
- Droit a la suppression (endpoints de suppression jobs/rapports)
- Journalisation des acces (audit_logs)
- Chiffrement des donnees sensibles
- Pas de donnees personnelles dans les scans de test

---

## 8. SIEM et supervision

### 8.1 Stack ELK

- **Elasticsearch 8.13** : stockage et indexation des logs
- **Logstash** : ingestion et transformation des evenements
- **Kibana** : visualisation et dashboards

### 8.2 Dashboard SIEM interne (`/siem`)

Le dashboard SIEM integre offre :

- **Indicateur de sante global** : badge colore (vert/orange/rouge) avec description
- **6 metriques temps reel** : scans totaux, reussis, en cours, erreurs, activite 24h, taux de succes
- **Graphiques Chart.js** :
  - Timeline d'activite sur 24h (courbe)
  - Distribution par module (barres horizontales)
  - Repartition des statuts (donut)
- **Etat des services** : 6 cartes de sante (Elasticsearch, Kibana, Logstash, MinIO, Redis, PostgreSQL) avec latence en ms
- **Activite recente** : feed des 10 derniers evenements avec icones et couleurs par statut
- **Top 5 cibles** : classement avec barres de progression
- **Auto-refresh** : toutes les 5 secondes

### 8.3 Detection d'intrusion

- **Snort 3** : IDS reseau configure pour detecter les attaques courantes
- Integration des alertes dans le SIEM via Logstash

---

## 9. Annexes

### 9.1 Documentation technique

La documentation complete est disponible dans le dossier `docs/` :

| Document | Description |
|----------|------------|
| `README.md` | Vue d'ensemble du projet |
| `architecture.md` | Architecture technique detaillee |
| `installation.md` | Guide d'installation Docker et local |
| `usage.md` | Guide d'utilisation de l'interface |
| `modules.md` | Reference des modules offensifs et defensifs |
| `api.md` | Documentation API REST complete |
| `securite.md` | Mesures de securite et conformite RGPD |
| `livrables.md` | Grille d'evaluation et correspondance cours |

### 9.2 Acces et URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Application web | http://localhost:8000 | admin / admin123 |
| Swagger API | http://localhost:8000/api/docs | Token JWT |
| Kibana | http://localhost:5601 | - |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin |

### 9.3 Scripts de demarrage

```powershell
# Lancer tout le projet
.\scripts\start.ps1

# Arreter
.\scripts\start.ps1 -Mode stop

# Voir les logs
.\scripts\start.ps1 -Mode logs

# Etat des services
.\scripts\start.ps1 -Mode status

# Rebuild complet
.\scripts\start.ps1 -Mode rebuild
```

### 9.4 Correspondance livrables / cours

| Element PentestBox | Cours associes |
|-------------------|----------------|
| Modules offensifs (Nmap, SQLmap, Hydra) | Securite offensive, pentest |
| ELK Stack, dashboard SIEM | SIEM, DevSecOps |
| JWT, RBAC, chiffrement Fernet | IAM, cryptologie |
| Analyse de rapports, forensique | Forensique, Reverse Engineering |
| Docker, CI/CD, Poetry | DevSecOps, CI/CD |
| Documentation, gestion de projet | Management securite |

---

*Document genere dans le cadre du projet d'etudes — Mastere Cybersecurite 2025*
