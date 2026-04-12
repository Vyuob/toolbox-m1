# PentestBox

**Toolbox automatisee de tests d'intrusion** – Mastere Cybersecurite 2025/2026

---

## Demarrage rapide

```bash
# 1. Cloner le projet
git clone https://github.com/Vyuob/toolbox-m1.git
cd toolbox-m1

# 2. Copier la configuration
cp .env.example .env

# 3. Lancer la stack complete
# Linux / macOS
./scripts/start.sh

# Windows (PowerShell)
.\scripts\start.ps1

# 4. Acceder a l'interface
open http://localhost:8000/api/dashboard/
```

## Interfaces disponibles

| Service | URL |
|---------|-----|
| Dashboard / API | http://localhost:8000/api/dashboard/ |
| Swagger UI | http://localhost:8000/api/docs |
| Kibana (SIEM) | http://localhost:5601 |
| MinIO Console | http://localhost:9001 |

## Modules

| Module | Outils | Type |
|--------|--------|------|
| `recon` | Nmap, DNS, whois | Offensif |
| `scan` | Nmap NSE, Nikto, SSLyze | Offensif |
| `exploit` | SQLmap, Hydra, Metasploit | Offensif |
| `web_scan` | OWASP ZAP, Dependency-Check | Offensif |
| `siem` | Elasticsearch | Defensif |
| `ids` | Snort | Defensif |
| `response` | iptables | Defensif |
| `forensic` | ClamAV, VirusTotal | Defensif (bonus) |

## Stack technique

- **Backend** : Python 3.11, FastAPI, SQLAlchemy, Celery
- **Frontend** : HTML/CSS/JS (Jinja2 templates, dark mode)
- **Base de donnees** : PostgreSQL
- **File de taches** : Redis + Celery
- **Stockage** : MinIO (S3-compatible)
- **SIEM** : Elasticsearch + Logstash + Kibana (ELK)
- **IDS** : Snort 3
- **Conteneurisation** : Docker + Docker Compose

## Documentation

Voir le dossier [docs/](docs/README.md) pour la documentation complete :

- [Architecture](docs/architecture.md)
- [Installation](docs/installation.md)
- [Utilisation](docs/usage.md)
- [Modules](docs/modules.md)
- [API REST](docs/api.md)
- [Securite](docs/securite.md)
- [Livrables](docs/livrables.md)

## Depot GitHub

```bash
git remote add origin https://github.com/Vyuob/toolbox-m1.git
git push -u origin main
```

## Equipe

- **Etudiant 1** – Architecte / Back-end
- **Etudiant 2** – Analyste / Forensique / QA
- **Etudiant 3** – Interface & Reporting

---

> Ce projet est realise dans un cadre pedagogique.
> Utilisation uniquement sur des systemes autorises.
