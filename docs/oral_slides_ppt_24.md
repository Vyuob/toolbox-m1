# Contenu pour PPT — ToolboxV8 soutenance (24 slides)

> **À donner à Gamma IA** : copier-coller cette structure, elle convertit directement en présentation.
> **Style recommandé** (à indiquer à Gamma) : professionnel, palette bleu nuit + orange accent, typo Inter ou Roboto, peu de texte par slide (les voix portent l'explication, les slides supportent visuellement).
> **Format** : 16:9, 24 slides, durée cible 20 min — soit ~50 sec / slide en moyenne.

---

## DIRECTIVES GLOBALES POUR GAMMA

```
Sujet : ToolboxV8 - toolbox automatisée de tests d'intrusion
Audience : jury Mastère Cybersécurité (mixte tech + business)
Ton : professionnel, sobre, factuel
Palette : bleu nuit (#1f3b82), accent orange (#fb923c), gris clair (#f1f5f9), blanc
Police : Inter / Roboto (sans-serif moderne)
Densité : peu de texte par slide, gros titres, schémas privilégiés
Logo : "ToolboxV8" en bandeau bas discret sur chaque slide
Footer : "Mastère Cybersécurité - Promotion 2025/2026"
```

---

## SLIDE 1 — Page de garde

**Titre** : ToolboxV8

**Sous-titre** : Toolbox automatisée de tests d'intrusion

**Visuel** : Logo ou icône bouclier + outils de pentest, centré

**Texte additionnel** :
- Mastère Cybersécurité — Promotion 2025/2026
- Soutenance — Vidéo MVP
- Ayoub · Abdallah · Titouan

---

## SLIDE 2 — Équipe

**Titre** : L'équipe

**Layout** : 3 colonnes (1 par membre)

**Contenu de chaque colonne** :
- Photo ou avatar
- Prénom
- Rôle principal
  - Membre 1 : Architecte & Back-end / Sécurité
  - Membre 2 : Intégration offensive & Qualité
  - Membre 3 : Interface & Reporting

**Note bas de slide** : "Chaque membre a contribué à tous les modules — principe d'appropriation partagée"

---

## SLIDE 3 — Le contexte client

**Titre** : Notre client

**Sous-titre** : Société de cybersécurité offensive

**Visuel** : Pictogrammes — bouclier, loupe, document — reliés par flèches

**Bullet points** :
- Réalise des pentests pour entreprises privées + institutions publiques
- Pratiques actuelles : **manipulations manuelles**
- Conséquences : pentest **long** (plusieurs heures) + résultats **hétérogènes** selon l'analyste
- Impact business : perte de temps + perte de crédibilité client

---

## SLIDE 4 — Le problème à résoudre

**Titre** : 5 douleurs identifiées

**Layout** : 5 cartes en grille (3 + 2)

**Cartes** :
1. ⏱️ **Temps perdu** en commandes répétitives
2. 🔀 **Hétérogénéité** entre analystes (résultats variables)
3. 📄 **Rapports illisibles** rédigés à la main
4. 🧑‍💻 **Barrière technique** — outils CLI inaccessibles aux juniors
5. 🔍 **Pas de traçabilité** claire des actions

**Message clé en bas** : "5 douleurs → 5 réponses dans une seule plateforme"

---

## SLIDE 5 — Objectifs du cahier des charges

**Titre** : 5 objectifs mesurables

**Layout** : tableau ou liste avec icônes

**Contenu** :
| Objectif | Cible |
|---|---|
| Réduire le temps d'un pentest | ≥ 40 % |
| Standardiser les pratiques | flux unique |
| Interface analyste-friendly | 0 compétence dev requise |
| Rapports exploitables | PDF + structurés |
| Intégration écosystème client | API REST + Docker |

**Encart en bas (highlight orange)** : "Objectif temps largement dépassé : 75 % sur recon+scan, 99 % sur la rédaction de rapport"

---

## SLIDE 6 — Périmètre fonctionnel

**Titre** : 5 phases d'un pentest, couvertes

**Visuel** : Pipeline horizontal avec 5 étapes connectées

**Étapes (de gauche à droite)** :
1. 🌐 **OSINT** (reconnaissance passive)
2. 🎯 **Recon active** (Nmap, DNS)
3. ⚠️ **Scan vulnérabilités** (Nikto, SSLyze)
4. 💥 **Exploitation** (SQLmap, Hydra, John)
5. 🔍 **Analyse Web/API** (ZAP, Gobuster)

**Encart en bas** : "+ volet défensif : SIEM ELK, règles Snort, response iptables"

---

## SLIDE 7 — Organisation & méthodologie

**Titre** : Méthodologie Agile · 10 sprints

**Layout** : timeline horizontale ou tableau condensé

**Contenu** :
- 📅 **Sprints de 2 semaines**, daily court à 3
- 📋 Backlog dans **Notion** (tickets : UX, intégration outil, bug, doc)
- 🔀 Git monorepo : `main` stable + branches `feat/*`
- ✅ Pull request + test sur cible Metasploitable2 obligatoire avant merge
- 🎯 **10 sprints livrés** : S1 squelette → S10 démos validées end-to-end

**Encart** : "Outils : Notion, GitHub, Docker Compose, VS Code"

---

## SLIDE 8 — Architecture globale

**Titre** : Architecture dockerisée

**Visuel** : Diagramme d'architecture (à dessiner par Gamma)

**Structure du diagramme** :
```
Navigateur
   ↓ HTTPS :443
Caddy (reverse proxy TLS)
   ↓
web (FastAPI + Jinja2 :3000) ────► api (FastAPI :8000)
                                       ↓
                                  PostgreSQL  Redis
                                                ↓
                                            worker (Celery + Kali)
                                                ↓
                                      Outils pentest + cibles internes :
                                       - zap:8080 (OWASP ZAP)
                                       - target:2222 (SSH faible)

Infrastructure : ELK (Elasticsearch + Logstash + Kibana), MinIO
```

**Note** : "Split api/web : isolation sécu + intégration externe préservée"

---

## SLIDE 9 — Stack technique

**Titre** : Stack technologique

**Layout** : 4 colonnes par catégorie

**Colonnes** :
| Backend | Frontend | Infrastructure | DevOps |
|---|---|---|---|
| Python 3.11 | Jinja2 | PostgreSQL 16 | Docker Compose |
| FastAPI | HTML/CSS vanilla | Redis 7 | Caddy 2 (HTTPS) |
| SQLAlchemy 2 | Lucide icons | MinIO (S3) | GitHub Actions |
| Celery 5 | Chart.js | Elasticsearch 8 | GitLab CI |
| ReportLab 4 | | Kali Rolling (worker) | |

**Encart** : "OWASP ZAP 2.17 + linuxserver/openssh-server intégrés au compose pour les démos"

---

## SLIDE 10 — Les 5 modules pentest

**Titre** : 5 modules offensifs · 4 modules défensifs

**Layout** : 2 colonnes — Offensifs / Défensifs

**Offensifs (gauche)** :
1. 🌐 **passive_recon** — Google Dorks (18 templates)
2. 🎯 **recon** — Nmap, DNS, whois, WhatWeb
3. ⚠️ **scan** — Nmap NSE, Nikto, SSLyze
4. 💥 **exploit** — SQLmap, Hydra, John (304 formats)
5. 🔍 **web_scan** — OWASP ZAP, Gobuster

**Défensifs (droite)** :
1. 📊 **siem** — Elasticsearch + Logstash + Kibana
2. 🛡️ **ids** — Snort 3 (règles préparées)
3. 🚫 **response** — iptables, isolation host
4. 🔬 **forensic** — ClamAV, VirusTotal API

**Encart en bas** : "Chaque outil = chips Quick/Standard/Full. Zéro CLI à connaître."

---

## SLIDE 11 — DÉMO 1 · Reconnaissance passive (OSINT)

**Titre** : 🌐 Démo : OSINT en 3 clics

**Layout** : capture d'écran + 3 puces

**Capture suggérée** : page Modules avec passive_recon sélectionné, champ "etudiant" rempli, dorks Mot-clé + Réseaux sociaux cochés

**Bullets** :
- Cible **en champ libre** (nom, marque, sujet) — pas besoin de domaine
- 18 dorks Google répartis en 3 catégories
- Ouverture multi-onglets automatique des résultats

**Encart** : "100% passif — zéro paquet vers la cible. Conformité RGPD."

---

## SLIDE 12 — DÉMO 2 · SQLmap (détection SQLi)

**Titre** : 💥 Démo : Injection SQL automatisée

**Layout** : capture d'écran + résultats

**Capture** : rapport PDF SQLmap montrant les 3 types d'injection

**Bullets résultats** :
- Cible : `testasp.vulnweb.com` (Acunetix, autorisé)
- **3 types d'injection détectés** : Boolean-based, Time-based, Stacked queries
- SGBD identifié : Microsoft SQL Server 2014
- Stack web : IIS 8.5, ASP.NET, Django

**Encart** : "Détection complète + payload exact en ~5 min — vs ~30 min en manuel"

---

## SLIDE 13 — DÉMO 3 · Hydra (brute-force SSH)

**Titre** : 💥 Démo : Brute-force credentials en 1 seconde

**Layout** : capture d'écran terminal Hydra + bullet points

**Capture** : extrait du rapport montrant la ligne `[2222][ssh] host: target login: pentest_user password: toor`

**Bullets** :
- Cible : conteneur `pentest_target` (SSH faible **interne** à la stack)
- Wordlist : 5 mots dont le bon
- **Cracké en 1 seconde** : `pentest_user:toor`
- Sur cible réelle + rockyou.txt (14M) : compte faible cracké en quelques minutes

**Encart** : "Démontre concrètement le risque des mots de passe faibles aux clients"

---

## SLIDE 14 — DÉMO 4 · John the Ripper (cassage de hash)

**Titre** : 💥 Démo : Cassage de hash instantané

**Layout** : capture rapport John + petit tableau

**Capture** : section CRACKED du rapport montrant "admin (?)"

**Bullets** :
- Hash MD5 : `21232f297a57a5a743894a0e4a801fc3`
- Format : raw-md5
- **Cracké en 0 seconde** : mot de passe = `admin`

**Tableau formats supportés (échantillon)** :
| Format | Usage |
|---|---|
| bcrypt | bases de données modernes |
| sha512crypt | /etc/shadow Linux |
| NTLM | Windows |
| KeePass | bases de mots de passe |
| ZIP | archives protégées |

**Encart** : "304 formats supportés par John jumbo"

---

## SLIDE 15 — DÉMO 5 · OWASP ZAP Active Scan

**Titre** : 🔍 Démo : Scan web automatisé

**Layout** : capture rapport ZAP + chiffres clés en gros

**Capture** : extrait montrant la liste des 14 types d'alertes triés par sévérité

**Chiffres en gros (encadrés colorés)** :
- **105 alertes** trouvées
- **14 types uniques**
- **55 secondes** d'exécution

**Sévérités (badges)** :
- 🟠 Medium : CSP missing, Anti-clickjacking, Anti-CSRF
- 🟡 Low : Server version leaks, X-Powered-By, X-Content-Type-Options
- ⚪ Info : User Agent Fuzzer, XSS potentielles

**Encart** : "Polling automatique de l'API ZAP jusqu'à fin du scan + récupération auto des alertes"

---

## SLIDE 16 — DÉMO 6 · Gobuster (chemins cachés)

**Titre** : 🔍 Démo : Découverte de surface d'attaque

**Layout** : capture liste de chemins + commentaire

**Capture** : extrait rapport avec les chemins découverts

**Bullets — chemins trouvés (échantillon)** :
- `/_vti_pvt` — admin FrontPage Microsoft (legacy, à patcher)
- `/cgi-bin`, `/cgi.bin` — répertoires CGI
- `/templates/`, `/aspnet_client/` — exposition fichiers structure
- `/robots.txt` — informations bots

**Encart** : "Scan en 30 sec — wordlist dirb common.txt"

---

## SLIDE 17 — Sécurité de la toolbox

**Titre** : 🔒 ToolboxV8 sécurise aussi ToolboxV8

**Layout** : 4 quadrants ou tableau condensé

**Quadrants** :
| Authentification | Autorisation |
|---|---|
| JWT HS256 + cookie HttpOnly | RBAC 3 rôles (admin/analyst/reader) |
| bcrypt pour mots de passe | Décorateurs FastAPI |

| Chiffrement | Traçabilité |
|---|---|
| Fernet pour secrets | AuditLog PostgreSQL append-only |
| HTTPS via Caddy | Tous événements indexés ELK |

**Encart** : "Section 7.7 du rapport — 7 sous-sections politiques de sécurité formalisées"

---

## SLIDE 18 — Pipeline défensif (SOAR léger)

**Titre** : 🛡️ Détection → Réponse

**Visuel** : diagramme horizontal

**Diagramme** :
```
ATTAQUANT → Snort (9 règles) → Logstash → Elasticsearch
                                              ↓
                              ┌───────────────┴────────────┐
                              ↓                            ↓
                      Dashboard /siem            ResponseModule.block_ip()
                      (analyst SOC)                        ↓
                                              iptables -A INPUT -s X -j DROP
                                              + audit log + index SIEM
```

**Bullets honnêteté** :
- ✅ ELK + ResponseModule **opérationnels**
- ⏳ Conteneur Snort **préparé** (cap_add NET_ADMIN sous WSL2 = limite §10.2)

---

## SLIDE 19 — DÉMO 7 · Rapport PDF automatique

**Titre** : 📄 Démo : Reporting professionnel en 2 secondes

**Layout** : 2 colonnes — mockup PDF + features

**Mockup PDF** : afficher 2-3 pages du rapport HTML/PDF

**Features (droite)** :
- ✅ Page de garde + synthèse exécutive (encart CODIR orange)
- ✅ Statistiques + déroulé technique par outil
- ✅ Sortie console brute préservée (copie/colle utilisable)
- ✅ Tableau synthétique + recommandations
- ✅ Palette slate, blocs code lisibles sur toutes les pages
- ✅ Génération en **2 secondes** depuis l'interface

---

## SLIDE 20 — KPIs atteints

**Titre** : 📊 Résultats chiffrés

**Layout** : 4 grosses tuiles avec chiffres impactants

**Tuiles (chiffres en très gros)** :
| 75% | 99% | 105 | 0 crash |
|---|---|---|---|
| Gain de temps recon+scan | Gain temps reporting | Vulnérabilités ZAP trouvées | sur 50 scans enchaînés |

**Bullets ergonomie** :
- ⏱️ Temps moyen pour lancer un pentest : **< 30 secondes** depuis l'UI
- 🎯 **0 commande CLI** à apprendre côté analyste

**Footer** : "Objectif cahier des charges (≥ 40 %) largement dépassé"

---

## SLIDE 21 — Limites assumées

**Titre** : ⚠️ Ce qu'on a documenté comme limite

**Layout** : 3 cartes

**Carte 1 — Metasploit** :
- Module codé, msfrpcd nécessite démarrage manuel
- Solution : sidecar préconfiguré (§10.3)

**Carte 2 — Snort déployé** :
- 9 règles écrites, pipeline Logstash prêt
- Conteneur pas dans le compose (mode IDS + WSL2)
- Solution : hôte Linux dédié

**Carte 3 — Dump SQL massif** :
- Profil bridé à 5 lignes / table
- Limite intrinsèque blind injection sur cible distante

**Footer** : "Documenté en §10.2 — défendable à l'oral"

---

## SLIDE 22 — Perspectives d'évolution

**Titre** : 🚀 Roadmap

**Layout** : liste à puces avec priorités

**Évolutions** :
1. 🔧 **Sidecar msfrpcd** préconfiguré → Metasploit end-to-end
2. 🛡️ **Service Snort** dans compose sur hôte Linux → pipeline IDS actif
3. 🔁 **Endpoint REST** `/api/defensive/response/block-ip` → SOAR auto
4. 📚 **Intégration SecLists** → wordlists exhaustives
5. 🤖 **Module IA/ML** → classification automatique criticité CVE
6. 🔐 **SSO OIDC** → intégration écosystème entreprise

---

## SLIDE 23 — Récap & impact

**Titre** : 🎯 ToolboxV8 en chiffres

**Layout** : grosses tuiles centrales

**Chiffres clés** :
- **5 modules offensifs** + 4 défensifs
- **12 outils** intégrés (Nmap, Nikto, SQLmap, Hydra, John, SSLyze, ZAP, Gobuster, ClamAV...)
- **10 sprints** sur 6 mois
- **CI/CD automatique** à chaque push (GitHub Actions + GitLab CI)
- **HTTPS** standard (Caddy auto-cert)

**Encart final** : "Stack 100 % dockerisée — déploiement en une commande"

---

## SLIDE 24 — Conclusion & Q&A

**Titre** : Merci pour votre attention

**Layout** : centré, peu dense

**Contenu** :
- 🙏 Merci à notre tuteur de Mastère et à l'équipe pédagogique
- 📂 Code & documentation : **github.com/Vyuob/toolbox-m1**
- 📋 Guide pratique de test des outils : `docs/guide_test_outils.txt`
- 📘 Rapport technique complet : `docs/rapport_final_groupe.md`
- ❓ **Place aux questions**

**Logos en bas** : Mastère Cybersécurité + GitHub

---

## CONSEILS DE STYLE POUR GAMMA IA

1. **Cohérence visuelle** : même palette / même typo / même position des éléments d'une slide à l'autre
2. **Lisibilité** : maximum 30 mots par slide (les voix portent le contenu)
3. **Pictogrammes** : utiliser les emojis ou icons proposés — ça aide la lecture rapide
4. **Captures d'écran** : si Gamma supporte, demander de générer des mockups d'interface ; sinon laisser des placeholders à remplir manuellement
5. **Animations** : éviter les transitions trop voyantes — préférer fade simple
6. **Footer commun** : "ToolboxV8 · Mastère Cybersécurité 2025/2026 · Slide X/24"
7. **Encarts highlights** : utiliser la couleur orange (#fb923c) pour les chiffres impactants ou messages clés

---

## CAPTURES D'ÉCRAN À PRÉPARER À L'AVANCE

Pour insérer dans les slides ou pendant la démo live :

| Slide | Capture à préparer |
|---|---|
| 11 | Page /modules avec passive_recon configuré (cible "etudiant") |
| 12 | Rapport PDF SQLmap montrant les 3 injection points |
| 13 | Rapport Hydra avec "pentest_user:toor" cracké |
| 14 | Rapport John avec "admin" cracked |
| 15 | Rapport ZAP avec les 14 types d'alertes |
| 16 | Rapport Gobuster avec les chemins découverts |
| 18 | Dashboard /siem avec graphs |
| 19 | Mockup PDF (couverture + page de déroulé technique) |

> Tous ces rapports existent déjà dans ton historique de scans — il suffit d'exporter en PDF et de prendre les screenshots.
