# Documentation ToolboxV8

Bienvenue dans la documentation complète de **ToolboxV8**, la toolbox automatisée de tests d'intrusion développée dans le cadre du Mastère Cybersécurité 2025/2026.

---

## 📌 Documents autoritaires (à jour — juin 2026)

Ces deux documents sont la **source de vérité** sur l'état réel du projet :

| Document | Description |
|----------|-------------|
| 📘 **[rapport_final_groupe.md](rapport_final_groupe.md)** | Rapport technique complet : architecture, modules, KPIs réels, REX, politiques de sécurité, conclusion. **Document principal à lire.** |
| 📋 **[guide_test_outils.txt](guide_test_outils.txt)** | Guide pratique : configs validées pour chaque outil avec cibles, profils et résultats attendus. **Pour reproduire les démos.** |
| 📝 [rapport_individuel_template.md](rapport_individuel_template.md) | Template pour les rapports individuels |

---

## 📂 Documents de référence (snapshot avril/juin 2026)

Ces documents sont des **références techniques pointues** sur des aspects précis. Ils datent du sprint S7 (avant l'ajout de passive_recon, Caddy HTTPS, ZAP daemon intégré, cible vulnérable target et CI/CD). En cas de divergence, **le rapport final fait foi**.

| Document | Description | Statut |
|----------|-------------|--------|
| [architecture.md](architecture.md) | Architecture (split api/web, flux d'auth, orchestration Celery) | ⚠️ Snapshot — Caddy/ZAP/target non décrits |
| [installation.md](installation.md) | Guide d'installation pas à pas | ⚠️ Snapshot — étape HTTPS/CA non décrite |
| [usage.md](usage.md) | Guide d'utilisation de l'interface et de l'API | ⚠️ Snapshot — module passive_recon non décrit |
| [modules.md](modules.md) | Description détaillée de chaque module et de ses profils | ⚠️ Snapshot — 4 modules listés (passive_recon manque) |
| [api.md](api.md) | Référence complète de l'API REST | À jour pour les endpoints existants |
| [securite.md](securite.md) | Authentification, RBAC, chiffrement, conformité | ⚠️ Snapshot — HTTPS Caddy non décrit |
| [livrables.md](livrables.md) | Livrables pédagogiques et correspondance cadre | ⚠️ Snapshot |

> 💡 **Pour le détail à jour**, voir [rapport_final_groupe.md](rapport_final_groupe.md) :
> - §1.4 équipe — §3.2 sprints (S1→S10) — §4 solution technique
> - §5 modules pentest (5 offensifs + 4 défensifs) — §6 KPIs réels mesurés
> - §7 sécurité (incluant §7.6 Caddy HTTPS et §7.7 politiques) — §8 SIEM
> - §9 REX — §10 conclusion et limites — §11 annexes

---

## Vue d'ensemble

ToolboxV8 est une plateforme web modulaire qui automatise les étapes d'un pentest :

```
OSINT → Reconnaissance → Scan de vulnérabilités → Exploitation → Scan Web/API
  ↑                                                                    ↓
SIEM ←──────────── Visualisation Elasticsearch ──────────────────────  ┘
  ↓
Snort (IDS — règles préparées)
  ↓
Response (iptables, isolation)
```

Le parcours utilisateur tient en 3 clics : **choisir le module → saisir la cible → cliquer sur Lancer**. Le rapport PDF est généré automatiquement et reprend la sortie CLI de chaque outil.

### Technologies principales

- **Backend** : Python 3.11 + FastAPI (2 services : api + web) + Celery
- **Frontend** : Jinja2 + HTML/CSS vanilla + Lucide icons
- **Base de données** : PostgreSQL 16
- **File de tâches** : Redis 7 + Celery 5
- **SIEM** : ELK Stack (Elasticsearch 8.13 + Logstash + Kibana)
- **IDS** : Snort 3 (règles préparées, conteneur non déployé — cf. §10.2)
- **Stockage** : MinIO (S3-compatible)
- **Worker pentest** : Kali Linux Rolling (image officielle, multi-stage build)
- **Reverse proxy TLS** : Caddy 2 (HTTPS auto via CA interne)
- **Scanner web** : OWASP ZAP 2.17 (daemon API intégré au compose)
- **Cible vulnérable** : conteneur SSH faible (`pentest_target` — démos Hydra)
- **Reporting** : ReportLab (PDF) + Jinja2 (HTML optionnel)
- **CI/CD** : GitHub Actions + GitLab CI (lint → tests → build Docker)
- **Conteneurisation** : Docker + Docker Compose

### Liens rapides

- **Interface web HTTPS** (recommandé) : `https://localhost`
- **Interface web HTTP** (fallback dev) : `http://localhost:3000`
- **API Swagger** (clients externes) : `http://localhost:8000/api/docs`
- **Kibana** (explorer brut des logs SIEM) : `http://localhost:5601`
- **MinIO Console** (stockage des rapports) : `http://localhost:9001`
