# Documentation PentestBox

Bienvenue dans la documentation complète de **PentestBox**, la toolbox automatisée de tests d'intrusion développée dans le cadre du Mastère Cybersécurité.

## Table des matières

| Document | Description |
|----------|-------------|
| [architecture.md](architecture.md) | Architecture technique complète |
| [installation.md](installation.md) | Guide d'installation pas à pas |
| [usage.md](usage.md) | Guide d'utilisation de l'interface et de l'API |
| [modules.md](modules.md) | Description détaillée de chaque module |
| [api.md](api.md) | Référence complète de l'API REST |
| [securite.md](securite.md) | Mesures de sécurité et conformité RGPD |
| [livrables.md](livrables.md) | Livrables pédagogiques et grille d'évaluation |

## Vue d'ensemble

PentestBox est une plateforme web modulaire permettant d'automatiser l'ensemble des étapes d'un pentest :

```
Reconnaissance → Scan → Exploitation → Post-exploitation
       ↑                                      ↓
    SIEM ←────────── Réponse Active ──────────┘
```

### Technologies principales

- **Backend** : Python 3.11 + FastAPI + Celery
- **Frontend** : Jinja2 + HTML/CSS vanilla
- **Base de données** : PostgreSQL + Redis
- **SIEM** : ELK Stack (Elasticsearch + Logstash + Kibana)
- **IDS** : Snort 3
- **Stockage** : MinIO
- **Conteneurisation** : Docker + Docker Compose

### Liens rapides

- Interface web : `http://localhost:8000/api/dashboard/`
- API Swagger : `http://localhost:8000/api/docs`
- Kibana : `http://localhost:5601`
- MinIO Console : `http://localhost:9001`
