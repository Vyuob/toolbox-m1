# Architecture Technique – PentestBox

## Diagramme général

```
┌─────────────────────────────────────────────────────────────────┐
│                         NAVIGATEUR                               │
│            http://localhost:8000/api/dashboard/                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API FastAPI (port 8000)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐             │
│  │  /api/auth  │  │ /api/modules │  │/api/reports│             │
│  └─────────────┘  └──────────────┘  └────────────┘             │
│  ┌─────────────────────────────────────────────────┐            │
│  │              /api/dashboard                       │            │
│  └─────────────────────────────────────────────────┘            │
└──────┬──────────────────┬──────────────────────────────────────┘
       │                  │
       ▼                  ▼
┌────────────┐    ┌───────────────┐    ┌──────────────────────────┐
│ PostgreSQL  │    │ Redis (Queue) │    │    Celery Worker(s)       │
│  (données) │    │  (Celery +    │◄──►│  - recon, scan, exploit  │
│            │    │   sessions)   │    │  - web_scan, reporting   │
└────────────┘    └───────────────┘    └──────────────────────────┘
                                                │
              ┌─────────────────────────────────┤
              ▼                                 ▼
┌──────────────────────────┐      ┌────────────────────────┐
│  ELK Stack (SIEM)         │      │     MinIO (Storage)     │
│  ┌────────────────────┐  │      │  Rapports PDF/HTML/CSV  │
│  │   Elasticsearch    │  │      └────────────────────────┘
│  ├────────────────────┤  │
│  │     Logstash       │  │
│  ├────────────────────┤  │
│  │      Kibana        │  │
│  └────────────────────┘  │
└──────────────────────────┘
              ▲
              │ alertes
┌─────────────┴──────────────┐
│         Snort IDS           │
│  surveillance réseau        │
└────────────────────────────┘
```

## Composants

### Backend (FastAPI)

| Fichier | Rôle |
|---------|------|
| `app/main.py` | Point d'entrée, middlewares CORS/TrustedHost |
| `app/core/config.py` | Configuration via variables d'environnement |
| `app/core/security.py` | JWT, bcrypt, Fernet |
| `app/core/auth.py` | Dépendances FastAPI (auth + RBAC) |
| `app/core/database.py` | SQLAlchemy engine + session |
| `app/models/` | ORM : User, ScanJob, Report, AuditLog |
| `app/api/routes/` | Routes REST : auth, modules, reports, dashboard |
| `app/modules/offensive/` | Recon, Scan, Exploit, WebScan, PostExploit |
| `app/modules/defensive/` | SIEM, IDS, Response, Forensic |
| `app/tasks/` | Tâches Celery asynchrones |
| `app/reporting/` | Génération PDF/HTML/CSV |

### Modèle de données

```
User (id, username, email, hashed_pwd, role, is_active, created_at, last_login)
  │
  ├─► ScanJob (id, task_id, module, target, options, status, result, created_by, created_at)
  │
  ├─► Report  (id, title, scan_job_id, format, file_path, created_by, created_at)
  │
  └─► AuditLog (id, user_id, action, detail, ip_address, timestamp)
```

### RBAC (Rôles)

| Rôle | Droits |
|------|--------|
| `admin` | Tout (gestion users, tous les modules, tous les rapports) |
| `analyst` | Lancer des scans, générer des rapports, voir les dashboards |
| `reader` | Consultation uniquement (jobs, rapports propres) |

### Flux d'une attaque/détection

```
1. Analyst → POST /api/modules/launch {module: "scan", target: "192.168.1.1"}
2. API → crée ScanJob en DB → envoie tâche Celery
3. Celery → exécute Nmap/Nikto → résultat en DB
4. ScanModule → indexe les événements dans Elasticsearch
5. Snort → détecte l'activité réseau → alerte dans /var/log/snort/alert
6. Logstash → ingère les alertes → Elasticsearch
7. Kibana → visualisation temps réel
8. ResponseModule → peut bloquer IP automatiquement
9. Analyst → POST /api/reports/generate → rapport PDF dans MinIO
```

## Sécurité

- Authentification JWT Bearer (expiration configurable)
- Chiffrement des données sensibles avec Fernet (AES-128-CBC)
- HTTPS via reverse proxy (Nginx/Traefik en production)
- Audit log horodaté pour toutes les actions
- CORS et TrustedHost middleware activés

## Évolutivité

- Architecture plugin : ajouter un module = créer un fichier dans `modules/offensive/` ou `modules/defensive/` et enregistrer la tâche Celery
- API documentée Swagger accessible sur `/api/docs`
- Scalabilité horizontale : plusieurs workers Celery possibles
