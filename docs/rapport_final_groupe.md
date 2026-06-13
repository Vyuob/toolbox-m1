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

- **Renseignement passif (OSINT)** : fuites publiques, profils sociaux, documents indexés, mentions de credentials → couvert par `passive_recon` (Google Dorks, 3 catégories : Mot-clé, Réseaux sociaux, Domaine).
- **Enumération et reconnaissance active** : exposition réseau, DNS, ports ouverts, versions vulnérables → couverte par `recon`.
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
| S7 | Rebranding ToolboxV8 + finalisation rapport v1 | Première version du présent document |
| S8 | Module Reconnaissance passive (OSINT) | `passive_recon.py`, 18 templates de Google Dorks (Mot-clé, Réseaux sociaux, Domaine), cible en champ libre, ouverture multi-onglets |
| S9 | Sécurité réseau & DevOps | Caddy HTTPS reverse proxy (cert auto), CI/CD GitHub Actions + GitLab CI (lint/test/build), SSLyze pré-check TCP avec fallback IPv4/IPv6 |
| S10 | Démos validées end-to-end + cibles vulnérables intégrées | Conteneur `pentest_target` (SSH faible pour Hydra), conteneur `pentest_zap` (daemon API), refonte `web_scan.py` (polling + récupération alertes), SQLmap dump ciblé, validations cibles assouplies, palette PDF/HTML alignée |

### 3.3 Répartition des tâches

Documentée dans le backlog interne. Chaque membre a contribué à la fois au développement, aux tests et à la documentation (principe d'appropriation partagée).

---

## 4. Solution technique

### 4.1 Architecture globale

Trois services applicatifs **FastAPI/Celery** + une stack de supports, tous **conteneurisés** (Docker Compose) :

```
Navigateur ── 443 (HTTPS) ── Caddy ─┐
              80  → 301      reverse│
              proxy TLS             ▼
                              ┌── web (FastAPI, Jinja2) ─┬─ pages /login /dashboard /modules /reports /siem
                              │                          └─ proxy /api/* ── 8000 ── api (FastAPI)
                              │                                              ├─ PostgreSQL
                              │                                              └─ Redis ── worker (Celery + Kali)
                              │                                                             ├─ /tmp/wordlists (volume partagé)
                              │                                                             └─→ services cibles internes :
                              │                                                                  • zap:8080  (OWASP ZAP daemon API)
                              │                                                                  • target:2222 (SSH faible pour Hydra)
                              │
ELK (Elasticsearch + Logstash + Kibana)   MinIO (rapports S3)   Snort 3 (IDS, règles préparées)
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
| Reverse proxy TLS | Caddy 2 (`caddy:2-alpine`) | HTTPS auto via CA interne, config 3 lignes, basculement Let's Encrypt en 1 ligne pour la prod |
| CI/CD | GitHub Actions + GitLab CI (parallèle) | Lint → tests pytest avec PG/Redis → build Docker, à chaque push |
| Scanner web | OWASP ZAP 2.17 daemon (`zaproxy/zap-stable`) | API REST sur :8080, intégré au compose, polling + récupération auto des alertes |
| Cible vulnérable | `linuxserver/openssh-server` (`pentest_target`) | SSH faible `pentest_user:toor` sur :2222, démos Hydra réutilisables |
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
- `/dashboard` — KPIs + jobs récents + rapports récents + raccourcis vers les 5 modules
- `/modules` — 5 cartes (**passive_recon**, recon, scan, exploit, web_scan) avec config dynamique par outil ; passive_recon mis en première position car c'est l'étape la plus en amont d'un pentest (OSINT avant toute interaction réseau)
- `/reports` — liste + génération (toujours PDF)
- `/siem` — graphiques Chart.js sur Elasticsearch

Composants clés du frontend :

- **Chips de profils** (`profileBlock` JS) pour Nikto, SSLyze, SQLmap, MSF, ZAP, Nmap NSE
- **Catalogue de dorks** (passive_recon) : 18 templates répartis en 3 catégories (Mot-clé, Réseaux sociaux, Domaine) avec sélection multiple par checkbox + zone de dorks personnalisés `{target}`
- **Modale wordlist** pour Hydra + John : 3 boutons (fichier / manuelle / rockyou.txt)
- **Polling Celery** (3 s) pour la progression temps réel avec barre et logs
- **Validation de cible adaptative** : validation stricte IP/domaine/URL pour les modules réseau, désactivée pour passive_recon (champ libre type "nom de personne", "marque", "sujet") et pour John the Ripper (hash)

### 4.6 CI/CD — pipelines automatisés

Deux pipelines en parallèle, déclenchés à chaque `git push` et chaque pull/merge request :

| Plateforme | Fichier | Statut |
|-----------|---------|--------|
| **GitHub Actions** | [.github/workflows/ci.yml](../.github/workflows/ci.yml) | Actif (repo principal sur GitHub) |
| **GitLab CI** | [.gitlab-ci.yml](../.gitlab-ci.yml) | Présent (compatibilité — push miroir GitLab via [scripts/push_gitlab.sh](../scripts/push_gitlab.sh)) |

Les deux pipelines exécutent **les mêmes trois étapes** :

```
┌───────┐    ┌─────────────────────┐    ┌──────────────────────┐
│ lint  │ →  │ test                │ →  │ build Docker         │
│ ruff  │    │ pytest + PG + Redis │    │ api + worker (Kali)  │
└───────┘    └─────────────────────┘    └──────────────────────┘
```

**Stage 1 — Lint (ruff)** : analyse statique du code Python, en mode `--output-format=github` pour annoter directement les pull requests sur GitHub.

**Stage 2 — Tests** : pytest avec services Postgres 16 et Redis 7 en parallèle (équivalent à la stack `docker-compose` minimale). Variables d'environnement injectées :

```yaml
env:
  DATABASE_URL: postgresql://pentest:pentest@localhost:5432/pentestdb
  REDIS_URL: redis://localhost:6379/0
  SECRET_KEY: ci-test-secret-key-not-used-in-prod
  FERNET_KEY: M0F5T3JuZXRLZXlGb3JDSVRlc3RPbmx5MzJiPT0=
```

**Stage 3 — Build Docker** : build des deux images (`docker/Dockerfile` pour api/web, `docker/Dockerfile.celery` pour le worker Kali) avec cache GitHub Actions (`type=gha`) pour accélérer les builds suivants. Pas de push registry tant que le sprint 8 n'est pas validé (perspective).

**Justification GitHub Actions + GitLab CI** : le cahier des charges mentionne explicitement « CI/CD (GitLab) ». Le repo principal étant hébergé sur GitHub, GitHub Actions est le pipeline actif. Le `.gitlab-ci.yml` est conservé pour rester conforme à la lettre du cahier et permettre un futur mirroring sur GitLab sans réécriture.

### 4.7 Rapport PDF

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
| **passive_recon** | Google / Bing / DuckDuckGo dorks | Catalogue 18 dorks (Mot-clé : PDF, Office, CV, leaks, credentials — Réseaux sociaux : LinkedIn, GitHub, Twitter, Reddit, Facebook, Pastebin — Domaine : pages indexées, sous-domaines, admin, login, secrets…) + dorks personnalisés |
| recon | Nmap, DNS, whois, WhatWeb | Nmap : Quick/Standard/Full TCP/Stealth |
| scan | Nmap `--script=vuln`, Nikto, SSLyze | Nmap NSE : Quick/Standard/Full/Safe — Nikto : Quick/Standard/Full/Evasion — SSLyze : Cert/Standard/Full (avec pré-check TCP IPv4/IPv6 + détection cible sans HTTPS) |
| exploit | SQLmap, Hydra, John jumbo, Metasploit | SQLmap : Quick/Standard/Aggressive/Dump — MSF : Handler/EternalBlue/PortScan/SMB |
| web_scan | OWASP ZAP (Spider + Active, daemon API intégré au compose), Gobuster, Dependency-Check | ZAP Spider : Quick/Standard/Deep avec récupération des URLs découvertes — ZAP Active : Quick/OWASP/Full avec polling jusqu'à 100% + récupération des alertes agrégées par sévérité — Gobuster : Quick/Standard/Full sur wordlists dirb |
| post_exploit | (documentaire) | — |

Détails des profils → [docs/modules.md](modules.md).

#### 5.1.bis Focus passive_recon (OSINT)

Le module **passive_recon** ([backend/app/modules/offensive/passive_recon.py](../backend/app/modules/offensive/passive_recon.py)) génère des **Google Dorks prêts à exécuter** sans aucun trafic vers la cible (recherche **100 % passive**). Trois catégories :

| Catégorie | Cas d'usage | Exemples de dorks |
|----------|-------------|-------------------|
| **Mot-clé** | Cible libre (nom, marque, sujet) | `"{target}" filetype:pdf`, `intitle:"{target}"`, `"{target}" ("leaked" \| "leak" \| "dump")` |
| **Réseaux sociaux** | Profils & présence | `"{target}" site:linkedin.com`, `site:github.com`, `site:reddit.com`, `site:pastebin.com` |
| **Domaine** | Cible = domaine ou IP | `site:{target}`, `site:*.{target} -www`, `site:{target} (inurl:admin \| inurl:wp-admin)`, `intext:"@{target}"` |

Le frontend permet de **cocher / décocher** chaque dork puis d'ouvrir tous les résultats en multi-onglets (un par dork). Le rapport PDF liste les requêtes générées et les URLs cliquables.

### 5.2 Défensifs

- **SIEM ELK** *(déployé)* : Elasticsearch + Logstash + Kibana opérationnels, indexation automatique des résultats de scans dans `pentest-logs-*`. Pipeline Logstash [siem/elk/logstash.conf](../siem/elk/logstash.conf) prêt à parser des alertes Snort (input `file` sur `/var/log/snort/alert` + filtre grok dédié).
- **IDS Snort 3** *(règles préparées, conteneur non déployé)* : 9 règles personnalisées écrites dans [siem/snort/local.rules](../siem/snort/local.rules) : scan Nmap SYN, brute-force SSH (5/60s), brute-force HTTP Basic, SQLi (`UNION SELECT`), XSS, Directory Traversal, signature Nikto, signature SQLmap, Log4Shell (CVE-2021-44228). Le conteneur Snort lui-même n'est **pas** dans `docker-compose.yml` actuel — déploiement repoussé pour contourner les contraintes de mode promiscuous sous Docker Desktop Windows/WSL2 (cf. §10.2).
- **Response active** *(module fonctionnel, déclenchement manuel)* ([backend/app/modules/defensive/response.py](../backend/app/modules/defensive/response.py)) — voir §5.4 et §8.4
- **Forensic** (bonus) : ClamAV + VirusTotal API v3

### 5.4 Module Response — pare-feu & remédiation

Le module `ResponseModule` expose 4 actions de remédiation, journalisées systématiquement dans le SIEM :

| Action | Méthode | Implémentation |
|--------|---------|----------------|
| **Blocage IP** | `block_ip(ip, reason)` | `iptables -A INPUT -s <ip> -j DROP` dans le conteneur worker Kali |
| **Déblocage IP** | `unblock_ip(ip)` | `iptables -D INPUT -s <ip> -j DROP` |
| **Isolation hôte** | `isolate_host(ip)` | Hook prévu pour intégration hyperviseur (vSphere/Proxmox/AWS Security Group) |
| **Alerte SIEM** | `send_alert(message, severity)` | Indexation immédiate dans Elasticsearch (`response_action` / `alert`) |

**Mode dégradé** : si `iptables` n'est pas disponible (cas d'un dev local Windows pur sans namespace réseau privilégié), `block_ip` retourne `{"status": "simulated"}` au lieu de planter. L'action est tout de même journalisée dans le SIEM pour traçabilité. Le worker Kali, lui, dispose de `iptables` nativement.

**Journalisation systématique** : chaque appel `block_ip`/`isolate_host`/`send_alert` est indexé dans Elasticsearch avant l'action elle-même → traçabilité même si la commande système échoue.

**État actuel** : le module est fonctionnel et invocable depuis le worker Celery ou un script admin. L'exposition API REST (`POST /api/defensive/response/block-ip`) est en backlog pour automatiser la chaîne complète (cf. §10.3).

### 5.3 Upload de wordlists (spécifique Hydra / John)

Nouvel endpoint `POST /api/modules/wordlist` (multipart). Fichier stocké dans un volume Docker partagé `/tmp/wordlists` accessible aux deux services `api` et `worker`. Utilisable comme `user_file`, `pass_file` ou `wordlist_file` dans le lancement du scan.

---

## 6. Tests et résultats — KPIs

### 6.1 Environnement de test

- **Hôte** : Windows 11 + Docker Desktop (WSL2)
- **Cibles publiques autorisées** (sites Acunetix volontairement vulnérables) :
  - `testasp.vulnweb.com` (ASP / IIS / MSSQL) — SQLmap, ZAP, Gobuster
  - `scanme.nmap.org` — Nmap NSE, Nikto, recon
  - `badssl.com` — SSLyze (audit TLS complet)
- **Cibles locales intégrées au compose** (réutilisables soutenance) :
  - `pentest_target` — conteneur SSH avec credentials faibles (`pentest_user:toor` sur port 2222) pour Hydra
  - `db` — PostgreSQL (peut servir de cible Hydra mode `postgres`)
- **Hash de démo** : MD5 raw + SHA512crypt style `/etc/shadow` pour John the Ripper
- **Jeux de tests** : ≈ 50 scans enchaînés couvrant les 5 modules

### 6.2 KPI temps d'exécution

| Étape manuelle (avant) | Avec ToolboxV8 | Gain |
|------------------------|----------------|------|
| Recon + scan (15-20 min) | 3-5 min (Quick) | **~ 75 %** |
| Rapport rédigé (1-2 h) | 2 s (PDF auto) | **~ 99 %** |
| Brute-force SSH (config manuelle) | 1 clic | **~ 90 %** |

✅ **Objectif cahier des charges (≥ 40 %) atteint largement**.

### 6.3 KPI vulnérabilités détectées (mesures réelles end-to-end)

| Test | Cible | Résultat mesuré |
|------|-------|-----------------|
| SQLmap Quick | testasp.vulnweb.com/showforum.asp?id=0 | **3 types d'injection** détectés (boolean-based blind, stacked queries, time-based blind), MSSQL 2014 + IIS 8.5 fingerprintés en ~5 min |
| SQLmap Dump | même cible | Énumération de **7 bases de données** (acufo, acuse, master, model, msdb, tempd) + tentatives sur 8 tables sensibles |
| Hydra SSH | `pentest_target:2222` | **Cracké `pentest_user:toor` en 1 seconde** avec wordlist 5 mots |
| John MD5 | hash `21232f297a57a5a743894a0e4a801fc3` | **Cracké "admin" en 0 seconde** (format raw-md5, wordlist 5 mots) |
| ZAP Spider | testasp.vulnweb.com | URLs découvertes via crawl récursif, scanId tracké |
| **ZAP Active Quick** | testasp.vulnweb.com | **105 alertes** sur 14 types uniques en 55s (Medium : CSP / Anti-clickjacking / Anti-CSRF ; Low : leaks Server/X-Powered-By ; Informational : User Agent Fuzzer / XSS potentielles) |
| Gobuster Quick | testasp.vulnweb.com | 13 chemins cachés découverts (`/_vti_pvt`, `/cgi-bin`, `/templates/`, `/aspnet_client`, etc.) |
| SSLyze Standard | badssl.com:443 | Audit TLS complet : certificat, chaîne, toutes versions TLS, cipher suites, headers de sécurité |
| Nmap NSE Quick | scanme.nmap.org | Détection ports + scripts vuln (port 22 SSH, port 80 HTTP, port 443 filtré) |
| Nikto Quick | scanme.nmap.org:80 | Apache 2.4.7 fingerprinté + 9 findings (headers manquants, mod_negotiation, etc.) |
| passive_recon | "etudiant" + "League of Legends" | 18 dorks générés sur 3 catégories (Mot-clé / Réseaux sociaux / Domaine), ouverture multi-onglets fonctionnelle |

✅ **Couverture : 5 modules sur 5 démontrés avec des rapports PDF produits**.

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
- **HTTPS via reverse proxy Caddy 2** (image officielle `caddy:2-alpine`) — voir §7.6

### 7.6 HTTPS avec Caddy (reverse proxy)

**Choix** : Caddy plutôt que Nginx ou Traefik, pour trois raisons :

1. **Configuration minimaliste** : 3 lignes de Caddyfile vs ~30 lignes de Nginx pour le même résultat ([docker/caddy/Caddyfile](../docker/caddy/Caddyfile))
2. **Gestion TLS automatique** : Caddy embarque sa propre CA interne (`tls internal`) qui génère et renouvelle les certificats sans intervention. En production, basculer sur Let's Encrypt = remplacer `internal` par le domaine
3. **Surface d'erreur réduite** : pas de génération manuelle de cert OpenSSL, pas de permissions à gérer

**Architecture du proxy** :

```
Navigateur ── 443 (HTTPS) ── Caddy ── (réseau Docker interne) ── web:3000 (HTTP)
              80 (HTTP)  ── Caddy ── 301 redirect → 443
```

**Caddyfile** (essentiel) :

```caddy
:443 {
    tls internal
    reverse_proxy web:3000 {
        header_up X-Forwarded-Proto https
        header_up X-Real-IP {remote_host}
    }
    encode gzip
}

:80 {
    redir https://{host}{uri} permanent
}
```

**Service Docker Compose** :

```yaml
caddy:
  image: caddy:2-alpine
  container_name: pentest_caddy
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./caddy/Caddyfile:/etc/caddy/Caddyfile:ro
    - caddy_data:/data       # stocke la CA + les certs générés
    - caddy_config:/config
  depends_on:
    - web
```

**Confiance du navigateur (dev local)** : Caddy crée une CA racine auto-signée dans `caddy_data:/data/caddy/pki/authorities/local/root.crt`. Pour éviter le warning navigateur, on importe cette racine dans le trust store du système une fois :

```powershell
# Windows
docker cp pentest_caddy:/data/caddy/pki/authorities/local/root.crt .
certutil -user -addstore "ROOT" root.crt
```

```bash
# Linux
docker cp pentest_caddy:/data/caddy/pki/authorities/local/root.crt /tmp/
sudo cp /tmp/root.crt /usr/local/share/ca-certificates/caddy-local.crt
sudo update-ca-certificates
```

Après cet import, `https://localhost` affiche un cadenas vert classique.

**En production** : un seul changement dans le Caddyfile pour passer en Let's Encrypt :

```caddy
mondomaine.fr {     # remplacer :443 par le vrai domaine
    reverse_proxy web:3000
}
```

Caddy obtient et renouvelle automatiquement le certificat via ACME (HTTP-01 ou TLS-ALPN-01).

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

### 7.7 Politiques de sécurité

Synthèse des règles applicables au système ToolboxV8, formalisées pour répondre aux exigences du cadre pédagogique (§VII.3) :

#### 7.7.1 Politique de mots de passe

| Règle | Valeur |
|-------|--------|
| Algorithme de stockage | **bcrypt** (salage intégré, coût par défaut 12) |
| Longueur minimale (à l'inscription) | 8 caractères |
| Mots de passe en clair | **Jamais** stockés, **jamais** loggés (les mots de passe ne sont jamais sérialisés dans `AuditLog`) |
| Rotation admin | Recommandée tous les 90 jours en production (mot de passe par défaut `admin/admin123` à changer dès le 1er login) |

#### 7.7.2 Politique d'authentification & session

| Règle | Valeur |
|-------|--------|
| Mécanisme | JWT **HS256** signé avec `SECRET_KEY` (32 octets aléatoires, généré par `start.sh`/`start.ps1` au 1er démarrage) |
| Durée de vie du token | **60 minutes** (`ACCESS_TOKEN_EXPIRE_MINUTES`) |
| Stockage côté client | **Cookie HttpOnly + SameSite=Lax + Secure auto en HTTPS** (jamais en `localStorage`) |
| Endpoint API direct | `POST /api/auth/token` toujours disponible pour clients externes (Bearer token) |
| Renouvellement | Re-login après expiration (pas de refresh token — choix volontaire pour réduire la surface) |

#### 7.7.3 Politique d'autorisation (RBAC)

Trois rôles hiérarchiques définis dans [backend/app/core/auth.py](../backend/app/core/auth.py) :

| Rôle | Droits |
|------|--------|
| `admin` | Toutes actions : créer/modifier/supprimer utilisateurs, lancer scans, générer rapports, consulter logs |
| `analyst` | Lancer scans, consulter résultats, générer rapports — **pas** de gestion utilisateurs |
| `reader` | Consultation seule des rapports et logs — **pas** de lancement de scan |

Vérification systématique via les dépendances FastAPI `require_admin` / `require_analyst` à chaque endpoint sensible.

#### 7.7.4 Politique de journalisation (audit)

| Règle | Détail |
|-------|--------|
| Table | `audit_logs` ([backend/app/models/scan.py](../backend/app/models/scan.py)) |
| Champs | `user_id`, `action`, `ip_address`, `timestamp`, `details` (JSONB) |
| Actions tracées | Login (succès/échec), lancement de scan, génération de rapport, suppression de job, modification utilisateur |
| Rétention recommandée | **6 mois minimum** (conformité ANSSI), purge automatique au-delà (cron à mettre en place en production) |
| Indexation SIEM | Tous les résultats de scan également indexés dans Elasticsearch (`pentest-logs-*`) pour corrélation |
| Inviolabilité | Logs en append-only (pas de `UPDATE`/`DELETE` via l'API), accès SQL réservé à l'admin DB |

#### 7.7.5 Politique de gestion des secrets

| Secret | Stockage | Rotation |
|--------|----------|----------|
| `SECRET_KEY` (JWT) | Variable d'environnement `.env` (hors git, dans `.gitignore`) | À régénérer en cas de fuite : `openssl rand -hex 32` puis redémarrage de l'API |
| `FERNET_KEY` | Variable d'environnement `.env` | Rotation = re-chiffrement des secrets stockés (procédure manuelle documentée) |
| `POSTGRES_PASSWORD` | Variable d'environnement `.env` | À changer en production (par défaut `pentest/pentest` réservé au dev) |
| `VIRUSTOTAL_API_KEY` | Variable d'environnement `.env` | Régénération via le compte VirusTotal |
| Mots de passe utilisateurs | DB PostgreSQL, **hashés bcrypt** | À l'initiative de l'utilisateur |
| Cookies de session | Chiffrés (JWT signé), HttpOnly | Expiration 60 min |

Aucun secret en clair dans le code source, le repo ou les logs (validation manuelle au commit + `.gitignore` strict sur `.env`, `*.key`, `*.pem`, `*.crt`).

#### 7.7.6 Politique d'utilisation éthique

| Règle | Mise en œuvre |
|-------|---------------|
| Cibles autorisées uniquement | Bandeau d'avertissement dans l'UI (`/modules`) et en pied de chaque rapport PDF |
| Pas de scan agressif sans validation | Profils "Quick" par défaut, "Full" nécessite un clic explicite |
| Traçabilité | Chaque scan est attribué à un utilisateur via `audit_logs` |
| Conformité RGPD | Aucune donnée personnelle de tiers stockée, suppression sur demande possible (`DELETE /api/modules/jobs/{id}`) |

#### 7.7.7 Politique de mise à jour & dépendances

| Composant | Source | Fréquence cible |
|-----------|--------|-----------------|
| Images Docker (api, web) | `python:3.11-slim-bookworm` | Mensuelle (build CI re-tire l'image base) |
| Image worker | `kalilinux/kali-rolling` | Hebdomadaire (Kali rolling pousse en continu) |
| Dépendances Python | `pyproject.toml` + `poetry.lock` | Lock file commit, `poetry update` audité par PR |
| CVE des dépendances | À surveiller via `pip-audit` ou GitHub Dependabot (recommandé pour la production) |

---

## 8. SIEM et supervision

### 8.1 Pipeline ELK

État actuel — ce qui tourne réellement et ce qui est préparé pour la suite :

```
[Déployé et fonctionnel]
Résultat de scan (ScanModule) ──► index Elasticsearch pentest-logs-* ──► Kibana / page /siem
Actions ResponseModule (block_ip, alert) ──► index pentest-logs-*

[Préparé, en attente du conteneur Snort]
Alertes Snort (/var/log/snort/alert) ──► Logstash (config prête) ──► Elasticsearch
```

Pourquoi Snort n'est pas déployé : son mode IDS nécessite des privilèges réseau (`cap_add: NET_ADMIN`, accès en mode promiscuous à l'interface) qui demandent une configuration spécifique sous Docker Desktop Windows + WSL2 (l'environnement principal de l'équipe). Le déploiement a été repoussé pour ne pas bloquer le reste du projet — les **règles, la config Logstash et le pipeline d'ingestion sont prêts**, il ne reste qu'à ajouter le service au compose en environnement Linux ou via une VM Kali dédiée.

### 8.2 Règles Snort personnalisées (préparées)

Fichier [siem/snort/local.rules](../siem/snort/local.rules) — 9 règles écrites, prêtes à charger dès que le conteneur Snort sera déployé :

- Scan Nmap SYN sur plusieurs ports (sid 9000001)
- Brute-force SSH (5 tentatives / 60 s — sid 9000002)
- Brute-force HTTP Basic Auth (10 tentatives / 30 s — sid 9000003)
- SQL Injection `UNION SELECT` (sid 9000004)
- XSS `<script>` (sid 9000005)
- Directory Traversal `../` (sid 9000006)
- Signature User-Agent Nikto (sid 9000007)
- Signature User-Agent sqlmap (sid 9000008)
- Log4Shell `${jndi:` (CVE-2021-44228 — sid 9000009)

### 8.3 Dashboard `/siem`

Page Jinja2 + Chart.js qui interroge `/api/defensive/overview` (agrégations Elasticsearch) :

- Nombre d'alertes par jour
- Top 10 IPs sources
- Événements récents par catégorie
- Graphiques : barres + camemberts + timeline

### 8.4 Pipeline Détection → Réponse (SOAR léger)

> **Note d'état** : ce diagramme décrit l'**architecture cible** du pipeline défensif. Les briques **ELK + ResponseModule + AuditLog sont opérationnelles** ; le maillon **Snort est préparé** (règles + config Logstash) mais le conteneur Snort n'est pas dans le `docker-compose.yml` actuel (cf. §8.1 et §10.2). Le schéma reste pédagogiquement valide et démontre la chaîne complète une fois Snort déployé sur un hôte Linux.

Chaînage des composants défensifs pour réagir à une attaque :

```
       ATTAQUANT
           │
           ▼  (paquet réseau / requête HTTP)
   ┌───────────────┐
   │   Snort 3     │  ──── alerte (regle local.rules sid:90000xx)
   └───────────────┘                              │
                                                  ▼
                                          ┌──────────────┐
                                          │   Logstash   │
                                          └──────────────┘
                                                  │
                                                  ▼
                                       ┌──────────────────┐
                                       │  Elasticsearch   │
                                       │ pentest-alerts-* │
                                       └──────────────────┘
                                                  │
                                  ┌───────────────┴───────────────┐
                                  ▼                               ▼
                          ┌──────────────┐              ┌────────────────────┐
                          │  /siem (UI)  │              │  ResponseModule    │
                          │  Analyst SOC │              │  block_ip(...)     │
                          └──────────────┘              │  isolate_host(...) │
                                  │                     │  send_alert(...)   │
                                  │ (decision)          └────────────────────┘
                                  └──────► triggers ────────────┘
                                                                 │
                                                                 ▼
                                                       ┌──────────────────┐
                                                       │ iptables DROP    │
                                                       │ + log audit_logs │
                                                       │ + index SIEM     │
                                                       └──────────────────┘
```

**Exemple concret** :

1. Attaquant lance `sqlmap -u http://cible.local/page?id=1` depuis 192.168.1.50
2. Snort détecte la signature `User-Agent: sqlmap` → règle sid 9000008 → alerte
3. Logstash ingère l'alerte → indexée dans `pentest-alerts-*`
4. Le dashboard `/siem` affiche la nouvelle alerte (refresh 10s)
5. L'analyste SOC appelle (via console ou futur endpoint REST) :
   `ResponseModule().block_ip("192.168.1.50", reason="sqlmap_detected")`
6. **3 effets en cascade** :
   - Indexation préalable dans Elasticsearch (`response_action`)
   - Exécution de `iptables -A INPUT -s 192.168.1.50 -j DROP`
   - Trace dans `audit_logs` PostgreSQL
7. L'attaquant ne peut plus joindre la cible.

**Composants concrets de la chaîne** :

| Maillon | Implémentation | Fichier |
|---------|----------------|---------|
| Détection | Snort 3 + 9 règles | [siem/snort/local.rules](../siem/snort/local.rules) |
| Transport | Logstash pipeline | [siem/elk/logstash.conf](../siem/elk/logstash.conf) |
| Stockage | Elasticsearch 8.13 | conteneur `pentest_elasticsearch` |
| Visualisation | Kibana + page `/siem` | [frontend/templates/siem.html](../frontend/templates/siem.html) |
| Action firewall | `iptables` via `ResponseModule` | [backend/app/modules/defensive/response.py](../backend/app/modules/defensive/response.py) |
| Traçabilité | `AuditLog` + index SIEM | [backend/app/models/scan.py](../backend/app/models/scan.py) |

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
| **SSLyze plante en silence sur cible sans HTTPS** (ex : `scanme.nmap.org:443`) | Le binaire retournait juste "connection error" noyé dans son output ; le rapport affichait du vide | Ajout d'un **pré-check TCP** (5 s) avant lancement : si port 443 non joignable → erreur claire en français avec liste de cibles de test (badssl.com, github.com…). Détection complémentaire des `tlsv1 alert` dans le stdout pour reformater l'erreur |
| **SSLyze : `[Errno 101] Network is unreachable`** dans le conteneur worker | `socket.create_connection()` tentait IPv6 (résolu par `getaddrinfo`) sans fallback IPv4 propre, et le réseau Docker n'a pas de route v6 | Réimplémentation avec `getaddrinfo` + tri **IPv4 d'abord, IPv6 en fallback** + boucle de connexion explicite — message d'erreur final pertinent (timeout / refused / unreachable) |
| **Caddy `ERR_SSL_PROTOCOL_ERROR`** au premier démarrage | Caddyfile écrit `:443 { tls internal }` sans nom d'hôte → Caddy ne savait pas pour quel CN générer le cert serveur (handshake renvoyait `tlsv1 alert internal error`) | Remplacement de `:443` par `localhost` dans le Caddyfile → cert serveur généré au bon nom, validation client OK |
| **Reconnaissance passive : "Format invalide"** sur cible type "etudiant" ou "League of Legends" | Validation cible front+back imposait IP / domaine / URL strict | Bypass de validation pour `passive_recon` (front [modules.html](../frontend/templates/modules.html), back [modules.py](../backend/app/api/routes/modules.py)) — sur le même modèle que John (hash) |
| **Hydra : "Format invalide"** sur cible `target` (nom de service Docker) | Même validation qui exige un domaine avec TLD | Bypass étendu au mode `hydra` (cible peut être un hostname interne Docker comme `target`, `db`, etc.) |
| **Hydra : pas de cible réutilisable** pour les démos | Pas de service vulnérable dans le compose | Ajout du conteneur `pentest_target` (`linuxserver/openssh-server` avec `pentest_user:toor` sur :2222). Réutilisable à chaque démarrage de la stack et à la soutenance. Note : `USER_NAME=root` refusé par l'image (user existant), fallback sur `pentest_user` |
| **ZAP Active "scan terminé en 2s"** alors qu'il devait durer 5 min | Le module faisait du "fire and forget" : appel à `/JSON/ascan/action/scan/` puis retour immédiat avec le `scan_id`, **sans attendre la fin ni récupérer les alertes** | Refonte `_zap_scan()` avec polling automatique (toutes les 5s jusqu'à 100% ou timeout 8 min) + récupération des alertes via `/JSON/core/view/alerts/`, agrégation par (nom, sévérité), tri par criticité OWASP, top 50 dans le rapport |
| **ZAP `400 Bad Request` sur Active scan Quick** | Profil référençait `scanPolicyName=XSS-SQLi` qui n'existe pas par défaut dans ZAP | Suppression des policies custom inexistantes ; `Quick` et `OWASP` utilisent la default policy implicite, `Full` la référence explicitement (`Default Policy` existe toujours) |
| **PDF rapport : pages 2+ "vides" pour blocs longs** (SQLmap dump) | `ParagraphStyle` avec `textColor=#f8fafc` (presque blanc) sur `backColor=#0f172a` (sombre) ; ReportLab ne re-dessine **pas** `backColor` sur les pages d'overflow → texte blanc sur fond blanc = invisible | Inversion de la palette : texte sombre (`#1e293b`) sur fond clair (`#f8fafc`) + bordure subtile (`#cbd5e1`), garanti lisible même sur les overflows. Style HTML report aligné pour cohérence visualiseur / téléchargement |
| **PDF non régénéré après modification du générateur** | Le générateur PDF tourne dans le **worker** Celery (via `tasks.generate_report`), pas dans l'API. Un rebuild de l'API seul n'avait aucun effet | Rebuilder systématiquement `worker` après toute modification de `reporting/generator.py` |

---

## 10. Conclusion et perspectives

### 10.1 Objectifs atteints

- [x] Toolbox fonctionnelle couvrant **reconnaissance passive (OSINT)**, reconnaissance active, scan de vulnérabilités, exploitation, analyse web et post-exploitation documentaire
- [x] **5 modules offensifs** + 4 modules défensifs (SIEM, IDS, response, forensic)
- [x] **Démos end-to-end validées** sur les 5 modules avec rapports PDF produits (cf. §6.3)
- [x] Réduction du temps de pentest bien au-delà des 40 % visés (≈ 75 % sur recon+scan, ≈ 99 % sur la rédaction de rapport)
- [x] Interface utilisable par un analyste sans code (profils par chips, upload fichiers, catalogue de dorks)
- [x] Reporting PDF standardisé, charte professionnelle, sortie CLI lisible, lisibilité garantie sur les pages d'overflow
- [x] Intégration Docker Compose simple : `./scripts/start.sh` — stack complète y compris **cibles vulnérables intégrées** (`pentest_target` SSH, `zap` daemon API)
- [x] Sécurisation : JWT + cookie HttpOnly + RBAC + Fernet + audit logs + **HTTPS** (Caddy reverse proxy)
- [x] **CI/CD** : GitHub Actions + GitLab CI (lint, tests, build Docker) à chaque push
- [x] **ZAP Active scan** opérationnel avec polling + récupération automatique des alertes (preuve : 105 alertes sur testasp.vulnweb.com dans le rapport)

### 10.2 Limites actuelles

- **Conteneur Snort non déployé** : les 9 règles personnalisées et la config Logstash sont écrites et testables sur un Snort installé manuellement, mais le service Snort n'est **pas** intégré au `docker-compose.yml`. Raison : le mode IDS Snort nécessite `cap_add: NET_ADMIN` + accès promiscuous à une interface réseau, ce qui demande une configuration spécifique sous Docker Desktop Windows/WSL2 (l'environnement principal de l'équipe). Déploiement reporté à la phase d'évolution (cf. §10.3), réalisable rapidement sur un hôte Linux ou dans une VM Kali dédiée.
- **Metasploit** : `msfrpcd` n'est pas démarré automatiquement dans le worker. Le module `_metasploit()` est codé et invocable via `pymetasploit3`, mais nécessite (a) une installation manuelle de la dépendance Python et (b) le lancement du démon RPC en parallèle. Documentation §10.3 pour le sidecar préconfiguré.
- En dev local, le certificat Caddy nécessite un import manuel de la CA racine (one-shot par poste) — en prod cette étape disparaît (Let's Encrypt)
- **Réponse active semi-automatisée** : `ResponseModule` est fonctionnel mais son déclenchement reste manuel (depuis console ou futur endpoint REST). Pas encore de SOAR end-to-end (cf. §10.3)
- **SQLmap dump sur cible distante lente** : le profil Dump est volontairement bridé (5 lignes max, threads=10, technique boolean-based) pour rester sous 15 min. Sur testasp.vulnweb.com (time-based blind imposé par le WAF), même bridé l'extraction de lignes ne réussit pas systématiquement — limite intrinsèque à l'injection blind sur cible distante

### 10.3 Perspectives d'évolution

| Évolution | Impact |
|-----------|--------|
| **Service Snort dans docker-compose** (hôte Linux ou VM Kali dédiée) | Active le pipeline IDS end-to-end : les 9 règles existantes commencent à produire des alertes consommées par Logstash → Elasticsearch → `/siem` |
| Sidecar `msfrpcd` préconfiguré + `pymetasploit3` dans le worker | Automatisation complète Metasploit (le seul outil offensif encore non démontrable end-to-end depuis l'UI) |
| Intégration SecLists | 1000+ wordlists prêtes à l'emploi |
| Push d'image sur registry (CI déjà active, build prêt) | Distribution versionnée des images Docker |
| **Endpoint REST `POST /api/defensive/response/block-ip`** | Boucler la chaîne SOAR : alerte Snort → règle de corrélation Elasticsearch → trigger HTTP → blocage iptables automatique |
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
| Sécurisation de l'outil | §7 (auth, RBAC, Fernet, audit logs, HTTPS via Caddy) |
| Conteneurisation + CI/CD GitLab | Docker Compose v2 + .gitlab-ci.yml + .github/workflows/ci.yml |
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
│   │   ├── modules/offensive/  ← passive_recon, recon, scan, exploit, web_scan, post_exploit
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
│   ├── docker-compose.yml
│   └── caddy/Caddyfile         ← reverse proxy HTTPS
├── .github/workflows/ci.yml   ← pipeline CI GitHub Actions
├── .gitlab-ci.yml             ← pipeline CI GitLab (miroir)
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

# Rebuild un service (api, web ou worker — le worker Kali est le plus long)
docker compose -f docker/docker-compose.yml up -d --build worker

# Logs live
docker compose -f docker/docker-compose.yml logs -f worker caddy

# Statut des conteneurs
docker compose -f docker/docker-compose.yml ps

# Accès aux interfaces
#   HTTPS  : https://localhost            (port 443, via Caddy reverse proxy)
#   HTTP   : http://localhost:3000        (port 3000, direct au service web — dev)
#   API    : https://localhost/api/docs   (Swagger)
#   Kibana : http://localhost:5601
#   MinIO  : http://localhost:9001

# Importer la CA Caddy dans Windows pour éviter le warning navigateur
docker cp pentest_caddy:/data/caddy/pki/authorities/local/root.crt .
certutil -user -addstore "ROOT" root.crt

# Lancer un scan passive_recon via curl
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token -d 'username=admin&password=admin' | jq -r .access_token)
curl -X POST http://localhost:8000/api/modules/launch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"module":"passive_recon","target":"example.com","options":{"engine":"google","dorks":["site","admin","emails","social_linkedin"]}}'
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
