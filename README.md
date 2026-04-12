# PentestBox

**Toolbox automatisée de tests d'intrusion** – Mastère Cybersécurité 2025/2026

---

## Démarrage rapide

```bash
# 1. Cloner le projet
git clone https://gitlab.com/<votre-groupe>/toolbox-pentest.git
cd toolbox-pentest

# 2. Lancer la stack complète
./scripts/start.sh

# 3. Accéder à l'interface
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
| `siem` | Elasticsearch | Défensif |
| `ids` | Snort | Défensif |
| `response` | iptables | Défensif |
| `forensic` | ClamAV, VirusTotal | Défensif (bonus) |

## Documentation

Voir le dossier [docs/](docs/README.md) pour la documentation complète.

## Pousser sur GitLab

```bash
./scripts/push_gitlab.sh https://gitlab.com/votre-groupe/toolbox-pentest.git
```

## Équipe

- **Étudiant 1** – Architecte / Back-end
- **Étudiant 2** – Analyste / Forensique / QA
- **Étudiant 3** – Interface & Reporting

---

> Ce projet est réalisé dans un cadre pédagogique.
> Utilisation uniquement sur des systèmes autorisés.
