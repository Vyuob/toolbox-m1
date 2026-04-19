# Documentation ToolboxV8

Bienvenue dans la documentation complète de **ToolboxV8**, la toolbox automatisée de tests d'intrusion développée dans le cadre du Mastère Cybersécurité 2025/2026.

## Table des matières

| Document | Description |
|----------|-------------|
| [architecture.md](architecture.md) | Architecture (split api/web, flux d'auth, orchestration Celery) |
| [installation.md](installation.md) | Guide d'installation pas à pas |
| [usage.md](usage.md) | Guide d'utilisation de l'interface et de l'API |
| [modules.md](modules.md) | Description détaillée de chaque module et de ses profils |
| [api.md](api.md) | Référence complète de l'API REST |
| [securite.md](securite.md) | Authentification, RBAC, chiffrement, conformité |
| [livrables.md](livrables.md) | Livrables pédagogiques et correspondance cadre |

## Vue d'ensemble

ToolboxV8 est une plateforme web modulaire qui automatise les étapes d'un pentest :

```
Reconnaissance → Scan de vulnérabilités → Exploitation → Scan Web/API
       ↑                                                       ↓
    SIEM  ←───────── Visualisation Elasticsearch ──────────────┘
       ↓
  Snort (IDS)
```

Le parcours utilisateur tient en 3 clics : **choisir le module → saisir la cible → cliquer sur Lancer**. Le rapport PDF est généré automatiquement et reprend la sortie CLI de chaque outil.

### Technologies principales

- **Backend** : Python 3.11 + FastAPI (2 services : api + web) + Celery
- **Frontend** : Jinja2 + HTML/CSS vanilla + Lucide icons
- **Base de données** : PostgreSQL 16
- **File de tâches** : Redis 7 + Celery 5
- **SIEM** : ELK Stack (Elasticsearch 8.13 + Logstash + Kibana)
- **IDS** : Snort 3
- **Stockage** : MinIO (S3-compatible)
- **Worker pentest** : Kali Linux Rolling (image officielle, multi-stage build)
- **Reporting** : ReportLab (PDF) + Jinja2 (HTML optionnel)
- **Conteneurisation** : Docker + Docker Compose

### Liens rapides

- **Interface web** (point d'entrée utilisateur) : `http://localhost:3000/login`
- **API Swagger** (clients externes) : `http://localhost:8000/api/docs`
- **Kibana** (explorer brut des logs SIEM) : `http://localhost:5601`
- **MinIO Console** (stockage des rapports) : `http://localhost:9001`
