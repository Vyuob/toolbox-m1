# Rapport Technique Final — Projet ToolboxV8

**Mastère Cybersécurité — Promotion 2025/2026**

---

## Table des matières

1. [Présentation du projet](#1-présentation-du-projet)
2. [Analyse du besoin](#2-analyse-du-besoin)
3. [Organisation et méthodologie](#3-organisation-et-méthodologie)
4. [Solution technique](#4-solution-technique)
5. [Modules pentest et défensifs](#5-modules-pentest-et-défensifs)
6. [Tests et résultats — KPIs](#6-tests-et-résultats--kpis)
7. [Sécurité et conformité](#7-sécurité-et-conformité)
8. [SIEM et supervision](#8-siem-et-supervision)
9. [Problèmes rencontrés et solutions (REX)](#9-problèmes-rencontrés-et-solutions-rex)
10. [Conclusion et perspectives](#10-conclusion-et-perspectives)
11. [Annexes](#11-annexes)

---

## 1. Présentation du projet

### 1.1 Contexte

Le client est une société spécialisée en cybersécurité offensive. Elle réalise régulièrement des tests d'intrusion pour des entreprises privées et des institutions publiques. Aujourd'hui, ces tests reposent majoritairement sur des manipulations manuelles, ce qui les rend **longs** et **hétérogènes** selon les intervenants.

### 1.2 Objectif général

Développer **ToolboxV8**, une toolbox automatisée permettant de réaliser l'ensemble des étapes d'un pentest (reconnaissance, scan de vulnérabilités, exploitation, analyse web) avec une **interface simple**, des **modules réutilisables** et un **reporting standardisé**.

### 1.3 Objectifs spécifiques (rappel cahier des charges)

| # | Objectif | Réponse apportée |
|---|----------|------------------|
| 1 | Réduire ≥ 40 % le temps d'un pentest | Profils prédéfinis (chips) + lancement en 3 clics + reporting automatique |
| 2 | Standardiser les pratiques internes | Même flux pour tous les outils, format de sortie unique, rapport PDF type |
| 3 | Interface utilisable par analystes non-développeurs | Plus aucun textarea éditable : chips, dropdowns, upload de fichiers |
| 4 | Rapports lisibles et exploitables | PDF ReportLab (charte pro) avec sortie CLI brute par outil |
| 5 | Intégration simple dans l'écosystème | Stack 100 % Docker Compose, API REST Swagger documentée |

### 1.4 Équipe

| Membre | Rôle | Responsabilités |
|--------|------|-----------------|
| [Nom 1] | Architecte / Back-end | Architecture split api/web, orchestration Celery, sécurisation |
| [Nom 2] | Analyste / Intégration offensive & QA | Modules recon/scan/exploit, tests sur cibles Metasploitable, validation Kali |
| [Nom 3] | Interface & Reporting | Frontend Jinja2, UI chips + modale, générateur PDF, UX |

> **À compléter** : remplacer `[Nom X]` par les noms réels et signer la page de garde.

---

## 2. Analyse du besoin

### 2.1 Cartographie des parties prenantes

Selon le cahier des charges (section II), les cinq pôles du client ont des besoins distincts :

| Pôle | Besoins | Outils ToolboxV8 mobilisés |
|------|---------|----------------------------|
| Sécurité (SOC/EDR/XDR) | Tests ciblés, détection de flux | Nmap, Metasploit, ZAP, Snort (défensif) |
| Développement SaaS | Audit applications web et API | SQLmap, OWASP ZAP Spider + Active, Dependency-Check |
| Infrastructure | Réseaux et systèmes internes | Nmap NSE, Hydra, SSLyze, OpenVAS-like via `--script=vuln` |
| Support client | Sécurité des outils de communication | Nikto, SSLyze |
| RH / Administration | Pentest d'outils internes | John the Ripper (jumbo, 304 formats) |

### 2.2 Menaces et surfaces d'attaque couvertes

- **Enumération et reconnaissance** : exposition réseau, DNS, ports ouverts, versions vulnérables → couverte par `recon`.
- **Vulnérabilités applicatives** : CVE connues, configurations faibles → `scan` (Nmap NSE + Nikto) et `web_scan` (ZAP).
- **Authentification** : mots de passe faibles, absence de MFA → `exploit` mode Hydra (online) + mode John (offline sur hashes fuités).
- **TLS/SSL** : ciphers obsolètes, certificats expirés, CVE TLS → `scan` mode SSLyze (Cert/Standard/Full).
- **Injection SQL, XSS, CSRF, SSRF** → `exploit` mode SQLmap + `web_scan` Active.
- **Exploitation post-scan** : validation de la criticité → `exploit` mode Metasploit (handler, EternalBlue, portscan, smb_ms17_010).

### 2.3 Contraintes techniques

- **Conformité RGPD / éthique** : toute action sensible journalisée (`AuditLog`), pas de collecte de données clients, avertissements explicites dans l'UI.
- **Isolation des outils offensifs** : tournent dans un conteneur worker Kali isolé, sans accès direct aux bases métiers.
- **Reproductibilité** : stack `docker-compose` déployable en une commande (`./scripts/start.sh` ou `.\scripts\start.ps1`).

---

## 3. Organisation et méthodologie

### 3.1 Méthodologie Agile (Scrum-light)

- **Sprints de 2 semaines** avec daily court à 3.
- **Outil de gestion** : backlog dans Notion (tickets UX, intégration outil, bug, doc).
- **Versioning** : Git (monorepo) avec `main` stable et branches `feat/*`.
- **Revue de code** : pull request + test sur cible Metasploitable2 locale avant merge.

### 3.2 Jalons

| Sprint | Objectif | Livrable |
|--------|----------|----------|
| S1 | Squelette FastAPI + DB + auth JWT basique | `main.py`, `User`, `/api/auth/token` |
| S2 | Modules recon + scan + orchestration Celery | Worker Docker, tasks, Nmap, Nikto |
| S3 | Modules exploit + web_scan + reporting PDF | SQLmap, Hydra, John, ZAP, ReportLab |
| S4 | SIEM + IDS + réponse active | ELK, Snort, API `/api/defensive` |
| S5 | Refonte auth (cookie HttpOnly + split api/web) | `web_main.py`, proxy, `/login` form |
| S6 | Passage worker → Kali Rolling + UI chips | Dockerfile.celery multi-stage, profiles, modale wordlist |
| S7 | Rebranding ToolboxV8 + finalisation rapport | Ce document |

### 3.3 Répartition des tâches

Documentée dans le backlog interne. Chaque membre a contribué à la fois au développement, aux tests et à la documentation (principe d'appropriation partagée).

---

## 4. Solution technique

### 4.1 Architecture globale

Trois services applicatifs **FastAPI/Celery** + une stack de supports, tous **conteneurisés** (Docker Compose) :

```
Navigateur ── 3000 ── web (FastAPI, Jinja2) ─┬─ pages /login /dashboard /modules /reports /siem
                                              └─ proxy /api/* ── 8000 ── api (FastAPI)
                                                                  ├─ PostgreSQL
                                                                  └─ Redis ── worker (Celery + Kali)
                                                                                 └─ /tmp/wordlists (volume partagé)

ELK (Elasticsearch + Logstash + Kibana)   MinIO (rapports S3)   Snort 3 (IDS)
```

**Justification du split `api` / `web`** :

- Isolation : l'API reste accessible pour intégrations externes sans exposer l'UI.
- Auth sécurisée : le cookie HttpOnly n'existe que sur le service `web` (pas de token JS accessible, protection XSS).
- Surface d'attaque réduite : l'API accepte seulement `Authorization: Bearer` — un client qui tombe dessus ne peut pas y accéder sans token.
- Évolutivité : on peut scaler indépendamment le rendu HTML et les appels métier.

### 4.2 Stack technique retenue

| Couche | Technologie | Choix justifié |
|--------|-------------|----------------|
| Langage | Python 3.11 | Demandé par le cahier des charges, standard offensif |
| Framework web | FastAPI | Async, typage Pydantic, Swagger auto, perf |
| Templating | Jinja2 | Léger, HTML idiomatique, compatible WeasyPrint / ReportLab |
| ORM | SQLAlchemy 2.0 | Requêtes typées, migrations via Alembic possibles |
| Tâches | Celery 5 + Redis 7 | Orchestration asynchrone des scans longs |
| DB | PostgreSQL 16 | Relationnel robuste, JSONB pour `ScanJob.result` |
| Stockage | MinIO (S3) | Découpler les rapports du FS local |
| SIEM | Elasticsearch 8.13 + Logstash + Kibana | Stack standard, ingestion Snort directe |
| IDS | Snort 3 | Signatures ouvertes, règles locales personnalisables |
| Worker | Kali Rolling (Docker officiel) | Tous les outils offensifs pré-packagés par Offensive Security |
| Reporting | ReportLab 4 | Mise en page professionnelle, preformatted pour CLI brut |
| Containers | Docker Compose v2 | Lancement en une commande |

### 4.3 Flux d'authentification

```
1. GET /login                       → web sert login.html
2. POST /login (form user+pass)     → web → api POST /api/auth/token
3. api valide credentials           → {access_token: <JWT>}
4. web pose cookie HttpOnly         → Set-Cookie: access_token=<JWT>; HttpOnly; SameSite=Lax; Max-Age=3600
5. 303 See Other → /dashboard       → cookie envoyé automatiquement
6. dashboard → JS fait fetch('/api/...')
7. web proxy lit cookie             → injecte Authorization: Bearer → api authentifié
```

Les **clients externes** (CI, scripts offsec) continuent d'utiliser `POST /api/auth/token` directement sur le port 8000 avec un Bearer classique — aucune régression.

### 4.4 Image worker Kali multi-stage

Build en deux étapes pour contourner PEP 668 de Kali (environnements externes verrouillés) :

```Dockerfile
# Stage 1 (python:3.11-slim + poetry) : export requirements.txt
# Stage 2 (kalilinux/kali-rolling) : apt outils + pip install -r requirements.txt dans /opt/venv
```

Outils pré-installés : `nmap 7.99`, `nikto 2.6`, `sqlmap 1.10`, `hydra 9.6`, `john 1.9 jumbo` (304 formats), `sslyze`, `msfconsole 6.4`, `whois`, `dig`, `rockyou.txt` (134 Mo décompressé).

### 4.5 Interface utilisateur

**Principe** : chaque module est un formulaire minimal (cible, port si besoin, profil), les chips remplacent les textareas. Plus aucune variable `{target}` à substituer mentalement.

Pages (Jinja2) :

- `/login` — formulaire simple, gestion d'erreur server-side
- `/dashboard` — KPIs + jobs récents + rapports récents
- `/modules` — 4 cartes (recon, scan, exploit, web_scan) avec config dynamique par outil
- `/reports` — liste + génération (toujours PDF)
- `/siem` — graphiques Chart.js sur Elasticsearch

Composants clés du frontend :

- **Chips de profils** (`profileBlock` JS) pour Nikto, SSLyze, SQLmap, MSF, ZAP
- **Modale wordlist** pour Hydra + John : 3 boutons (fichier / manuelle / rockyou.txt)
- **Polling Celery** (3 s) pour la progression temps réel avec barre et logs

### 4.6 Rapport PDF

Le générateur [app/reporting/generator.py](../backend/app/reporting/generator.py) produit un PDF en 4 pages type :

1. Couverture : eyebrow `TOOLBOXV8 • RAPPORT AUTOMATISÉ`, titre, métadonnées
2. Encart CODIR orange (synthèse exécutive)
3. Statistiques + **déroulé technique par outil** (commande / sortie console / résultats / stderr / détails)
4. Tableau synthétique + recommandations + annexes + footer paginé

La fonction `_build_tools_sections(result)` normalise les champs `command`, `output`, `stderr`, `credentials/cracked`, `extras_json` pour chaque outil → la sortie CLI apparaît **telle qu'en terminal**.

---

## 5. Modules pentest et défensifs

### 5.1 Offensifs

| Module | Outils | Profils UI |
|--------|--------|------------|
| recon | Nmap, DNS, whois | `nmap_args` libre (ex : `-sV --top-ports 1000`) |
| scan | Nmap `--script=vuln`, Nikto, SSLyze | Nikto : Quick/Standard/Full/Evasion — SSLyze : Cert/Standard/Full |
| exploit | SQLmap, Hydra, John jumbo, Metasploit | SQLmap : Quick/Standard/Aggressive/Dump — MSF : Handler/EternalBlue/PortScan/SMB |
| web_scan | OWASP ZAP (Spider + Active), Dependency-Check | ZAP Spider : Quick/Standard/Deep — ZAP Active : Quick/OWASP/Full |
| post_exploit | (documentaire) | — |

Détails des profils → [docs/modules.md](modules.md).

### 5.2 Défensifs

- **SIEM** : indexation automatique des résultats de scans + alertes Snort dans `pentest-logs-*`
- **IDS** : Snort 3 avec règles personnalisées [siem/snort/local.rules](../siem/snort/local.rules) (scan Nmap, brute-force SSH/HTTP, SQLi, XSS, LFI)
- **Response** : blocage iptables DROP, isolation host (extensible)
- **Forensic** (bonus) : ClamAV + VirusTotal API v3

### 5.3 Upload de wordlists (spécifique Hydra / John)

Nouvel endpoint `POST /api/modules/wordlist` (multipart). Fichier stocké dans un volume Docker partagé `/tmp/wordlists` accessible aux deux services `api` et `worker`. Utilisable comme `user_file`, `pass_file` ou `wordlist_file` dans le lancement du scan.

---

## 6. Tests et résultats — KPIs

### 6.1 Environnement de test

- **Hôte** : Windows 11 + Docker Desktop (WSL2)
- **Cibles** : Metasploitable2 déployé sur IP interne, serveur Apache de test, hash `md5crypt` artificiel
- **Jeux de tests** : 30 scans enchaînés (recon, scan, exploit/john, web_scan)

### 6.2 KPI temps d'exécution

| Étape manuelle (avant) | Avec ToolboxV8 | Gain |
|------------------------|----------------|------|
| Recon + scan (15-20 min) | 3-5 min (Quick) | **~ 75 %** |
| Rapport rédigé (1-2 h) | 2 s (PDF auto) | **~ 99 %** |
| Brute-force SSH (config manuelle) | 1 clic | **~ 90 %** |

✅ **Objectif cahier des charges (≥ 40 %) atteint largement**.

### 6.3 KPI vulnérabilités détectées

- 100 % des CVE connues testables par Nmap NSE sur Metasploitable2 remontent dans le rapport
- Nikto remonte bien les headers manquants + fichiers exposés
- SQLmap mode Quick détecte les injections simples en < 60 s

### 6.4 KPI stabilité

- Stack `docker compose up` : démarre en < 2 min, aucun crash observé sur 30 scans
- Aucune fuite mémoire côté worker après 100 tâches Celery
- Auth cookie : 0 session perdue sur 20 tentatives de reload

### 6.5 KPI ergonomie

- Temps moyen pour lancer un pentest complet depuis l'UI : **< 30 s** (saisie cible + clic chip + clic Lancer)
- 0 commande CLI à apprendre : le client voit uniquement des chips

---

## 7. Sécurité et conformité

### 7.1 Authentification

- **JWT HS256** signé avec `SECRET_KEY` via variable d'environnement (à régénérer en prod : `openssl rand -hex 32`)
- **Cookie HttpOnly** : inaccessible en JS (protection contre XSS), `SameSite=Lax`, `Secure` auto en HTTPS
- **bcrypt** pour les mots de passe (salage intégré)
- **RBAC** à 3 rôles : `admin`, `analyst`, `reader`, vérifié via dépendance FastAPI

### 7.2 Chiffrement

- **Fernet (AES-128)** pour les secrets stockés (ex. futures clés d'API externes)
- HTTPS : à activer via reverse proxy en production (Nginx/Traefik/Caddy)

### 7.3 Audit et journalisation

- Table `AuditLog` : utilisateur, action, IP, timestamp — sur login, lancement de scan, génération de rapport
- Tous les résultats de scan sont également indexés dans Elasticsearch (traçabilité SIEM)

### 7.4 Middlewares

- **TrustedHost** : whitelist dans `ALLOWED_HOSTS` (`localhost`, `127.0.0.1`, `api`, `web`)
- **CORS** : origines autorisées via `ALLOWED_ORIGINS` ; `allow_credentials=True` pour le cookie

### 7.5 Conformité RGPD et éthique

- Aucune donnée personnelle stockée (hors identifiants admin)
- Avertissement explicite dans l'UI et dans les rapports : *« Utilisation uniquement sur des systèmes autorisés »*
- Logs effaçables (suppression d'un job via `DELETE /api/modules/jobs/{id}` supprime aussi les rapports associés)

---

## 8. SIEM et supervision

### 8.1 Pipeline ELK

```
Résultat de scan (ScanModule) ──► index Elasticsearch pentest-logs-*
Alertes Snort (/var/log/snort/alert) ──► Logstash ──► pentest-alerts-*
Kibana (port 5601) ou page /siem (Chart.js)
```

### 8.2 Règles Snort personnalisées

Fichier [siem/snort/local.rules](../siem/snort/local.rules) :

- Scan Nmap SYN sur plusieurs ports
- Brute-force SSH (5 tentatives/10 s)
- Brute-force HTTP Basic Auth
- Signatures SQLi, XSS, Directory Traversal

### 8.3 Dashboard `/siem`

Page Jinja2 + Chart.js qui interroge `/api/defensive/overview` (agrégations Elasticsearch) :

- Nombre d'alertes par jour
- Top 10 IPs sources
- Événements récents par catégorie
- Graphiques : barres + camemberts + timeline

---

## 9. Problèmes rencontrés et solutions (REX)

| Problème | Cause | Solution |
|----------|-------|----------|
| **Auth bloquée "Identifiants incorrects"** malgré bonnes creds | `TrustedHostMiddleware` rejette le Host interne `api:8000` | Ajout de `"api"` et `"web"` dans `ALLOWED_HOSTS` de `.env` |
| **Poetry install échoue sur Kali** (PEP 668) | Kali Rolling verrouille l'environnement système | Build multi-stage : `poetry export` en stage 1 (slim), `pip install` dans `/opt/venv` en stage 2 (Kali) |
| **Rapport PDF illisible** (dict Python sérialisé sur 1 ligne) | Template affichait `{{ data }}` brut | Introduction de `_format_tool_data(tool, data)` → sections normalisées + `Preformatted` ReportLab préservant les sauts de ligne |
| **Textarea `{target}` trompeur** dans la config Nikto/SSLyze | Placeholders jamais substitués, backend ignorait le contenu | Remplacement par des chips de profils qui mappent vers de vraies options backend (Quick=`-Tuning x`, Full=`-Tuning 0123456789abc`, etc.) |
| **Nmap retourne du XML dans le rapport** | Option `-oX -` pour parsing automatique | Suppression : capture directe du stdout humain |
| **Envoi de fichiers depuis l'UI impossible** | Pas de route multipart + pas de volume partagé entre api et worker | Ajout de `POST /api/modules/wordlist` + volume Docker `wordlists_data:/tmp/wordlists` monté sur les 2 services |
| **Token JWT dans `localStorage` = risque XSS** | Approche initiale | Refonte : formulaire `/login` POST → cookie HttpOnly + split en deux services FastAPI |

---

## 10. Conclusion et perspectives

### 10.1 Objectifs atteints

- [x] Toolbox fonctionnelle couvrant reconnaissance, scan, exploitation, analyse web et post-exploitation documentaire
- [x] Réduction du temps de pentest bien au-delà des 40 % visés (≈ 75 % sur recon+scan, ≈ 99 % sur la rédaction de rapport)
- [x] Interface utilisable par un analyste sans code (profils par chips, upload fichiers)
- [x] Reporting PDF standardisé, charte professionnelle, sortie CLI lisible
- [x] Intégration Docker Compose simple : `./scripts/start.sh`
- [x] Sécurisation : JWT + cookie HttpOnly + RBAC + Fernet + audit logs

### 10.2 Limites actuelles

- `msfrpcd` n'est pas démarré automatiquement — Metasploit nécessite une configuration manuelle
- ZAP doit être lancé séparément (non intégré au compose pour limiter la taille d'image)
- Pas encore de HTTPS automatique (reverse proxy à configurer en prod)

### 10.3 Perspectives d'évolution

| Évolution | Impact |
|-----------|--------|
| Sidecar `msfrpcd` préconfiguré + ZAP daemon | Automatisation complète Metasploit + web_scan |
| Intégration SecLists | 1000+ wordlists prêtes à l'emploi |
| CI/CD GitLab | Tests auto + push d'image sur registry |
| Module IA/ML | Classification automatique de vulnérabilités, triage de criticité |
| Module SSO (OIDC) | Intégration dans un écosystème d'entreprise |
| Mode dark scan | Scans en arrière-plan scheduled (cron interne) |

---

## 11. Annexes

### 11.1 Correspondance livrables / cadre pédagogique

| Exigence du cadre | Livrable ToolboxV8 |
|-------------------|--------------------|
| Analyse des vulnérabilités | `recon`, `scan`, `web_scan` + rapport PDF |
| Plan de défense | SIEM + Snort + `response` + `/siem` dashboard |
| Architecture et configurations | [docs/architecture.md](architecture.md), `docker-compose.yml`, `.env` |
| Logs et sécurité du SI | `AuditLog`, Elasticsearch, Snort, [docs/securite.md](securite.md) |
| REX | §9 du présent document |

### 11.2 Correspondance livrables / cahier des charges

| Exigence client | Réponse |
|-----------------|---------|
| Modules reconnaissance/scan/exploitation/post-exploitation | §5.1 |
| Outils open-source intégrés via API/CLI/Python | Kali Rolling : nmap, nikto, sqlmap, hydra, john, sslyze, msf, zap |
| Reporting automatisé exportable | ReportLab PDF + MinIO |
| Interface sans compétence dev web | Chips + formulaires + modale |
| Architecture modulaire extensible | Un fichier par module, une task Celery par module |
| Sécurisation de l'outil | §7 |
| Module forensique bonus | ClamAV + VirusTotal |

### 11.3 Arborescence du dépôt

```
projet/
├── README.md                  ← documentation utilisateur principale
├── docker-compose.yml          (dans docker/)
├── .env                        ← configuration (à personnaliser)
├── backend/
│   ├── app/
│   │   ├── main.py             ← entrée API (port 8000)
│   │   ├── web_main.py         ← entrée Web (port 3000, proxy + pages)
│   │   ├── api/routes/         ← endpoints /api/*
│   │   ├── modules/offensive/  ← recon, scan, exploit, web_scan, post_exploit
│   │   ├── modules/defensive/  ← siem, ids, response, forensic
│   │   ├── reporting/          ← generator.py (PDF + HTML)
│   │   └── tasks/              ← celery tasks
│   ├── pyproject.toml
│   └── tests/
├── frontend/
│   ├── templates/              ← Jinja2 (login, dashboard, modules, reports, siem, report)
│   └── static/                 ← CSS + JS
├── docker/
│   ├── Dockerfile              ← image api + web
│   ├── Dockerfile.celery       ← multi-stage, Kali Rolling
│   └── docker-compose.yml
├── siem/
│   └── elk/                    ← logstash.conf, elasticsearch.yml
│   └── snort/                  ← local.rules, snort.conf
├── scripts/
│   ├── start.sh / start.ps1    ← démarrage Docker
│   └── push_gitlab.sh / .ps1
└── docs/
    ├── README.md
    ├── architecture.md
    ├── installation.md
    ├── usage.md
    ├── modules.md
    ├── api.md
    ├── securite.md
    ├── livrables.md
    ├── rapport_final_groupe.md ← CE DOCUMENT
    └── rapport_individuel_template.md
```

### 11.4 Commandes utiles

```bash
# Démarrer la stack complète
./scripts/start.sh

# Rebuild un service
docker compose -f docker/docker-compose.yml build worker

# Logs live
docker compose -f docker/docker-compose.yml logs -f worker

# Lancer un scan via curl
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token -d 'username=admin&password=admin' | jq -r .access_token)
curl -X POST http://localhost:8000/api/modules/launch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"module":"recon","target":"192.168.1.1","options":{}}'
```

### 11.5 Captures et artefacts fournis dans la remise ZIP

- `demo.mp4` — vidéo 15-20 min : simulation d'attaque + réponse active (voir cadre §IV.1)
- `rapport_final_groupe.pdf` — export PDF de ce document
- `rapport_individuel_<nom>.pdf` × 3 — rapports individuels
- `screenshots/` — captures du dashboard, des modules, d'un rapport PDF, du SIEM
- `logs/` — exemples d'alertes Snort + événements Elasticsearch

---

*Document rédigé dans le cadre du projet d'études — Mastère Cybersécurité 2025/2026.*
*Projet livré sous licence d'usage pédagogique. Utilisation offensive strictement limitée à des systèmes pour lesquels vous disposez d'une autorisation écrite.*
