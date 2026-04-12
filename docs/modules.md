# Modules PentestBox – Référence

## Modules Offensifs

### 1. Reconnaissance (`recon`)

**Fichier** : `backend/app/modules/offensive/recon.py`

**Outils intégrés** :
- `nmap` – Scan de ports, détection OS et services (`-sV -O`)
- `whois` – Informations sur le domaine/IP
- Résolution DNS native Python

**Options** :

| Option | Type | Défaut | Description |
|--------|------|--------|-------------|
| `nmap_args` | string | `-sV -O --top-ports 1000` | Arguments Nmap |
| `whois` | bool | `false` | Activer le lookup whois |

**Résultat** :
```json
{
  "target": "192.168.1.1",
  "dns": {"resolved_ip": "192.168.1.1", "all_ips": ["192.168.1.1"]},
  "nmap": {"raw_xml": "..."},
  "whois": "..."
}
```

---

### 2. Scan de Vulnérabilités (`scan`)

**Fichier** : `backend/app/modules/offensive/scan.py`

**Outils intégrés** :
- `nmap --script=vuln` – Scripts NSE de détection de vulnérabilités
- `nikto` – Audit serveur web (headers, fichiers exposés, CVE)
- `sslyze` – Audit TLS/SSL (ciphers, certificats, HSTS)

**Options** :

| Option | Type | Défaut | Description |
|--------|------|--------|-------------|
| `nikto` | bool | `true` | Activer Nikto |
| `sslyze` | bool | `false` | Activer SSLyze |
| `port` | int/string | – | Port spécifique |

---

### 3. Exploitation (`exploit`)

**Fichier** : `backend/app/modules/offensive/exploit.py`

**Outils intégrés** :
- `sqlmap` – Injection SQL automatisée
- `hydra` – Brute-force (SSH, FTP, HTTP, etc.)
- `Metasploit` via `pymetasploit3` (MSFRPC)

**Options selon le mode** :

| Mode | Options |
|------|---------|
| `sqlmap` | `level (1-5)`, `risk (1-3)` |
| `hydra` | `service`, `userlist`, `passlist` |
| `msf` | `exploit`, `msf_host`, `msf_port`, `msf_password`, `msf_options` |

> **Avertissement** : Ce module ne doit être utilisé que sur des cibles autorisées.

---

### 4. Scan Web/API (`web_scan`)

**Fichier** : `backend/app/modules/offensive/web_scan.py`

**Outils intégrés** :
- `OWASP ZAP` via API REST (spider + active scan)
- `dependency-check` – Détection de composants vulnérables

**Options** :

| Option | Type | Défaut | Description |
|--------|------|--------|-------------|
| `zap` | bool | `true` | Activer ZAP |
| `scan_type` | string | `spider` | `spider` ou `active` |
| `zap_url` | string | `http://localhost:8080` | URL de l'instance ZAP |
| `dep_check` | bool | `false` | Activer Dependency-Check |

---

### 5. Post-Exploitation (`post_exploit`)

**Fichier** : `backend/app/modules/offensive/post_exploit.py`

Actions :
- `enumerate` : liste des commandes d'énumération locale (users, processes, sudo, SUID)
- `persistence_check` : vérification des mécanismes de persistance (cron, rc.local, systemd)

---

## Modules Défensifs

### 6. SIEM (`siem`)

**Fichier** : `backend/app/modules/defensive/siem.py`

Interface avec Elasticsearch :
- `index_event(type, data)` : indexe un événement
- `search_events(query)` : recherche full-text
- `get_recent_alerts()` : dernières alertes

Tous les résultats de scan sont automatiquement indexés dans `pentest-logs-*`.

---

### 7. IDS (`ids`)

**Fichier** : `backend/app/modules/defensive/ids.py`

Parse les alertes Snort depuis `/var/log/snort/alert`.

- `parse_alerts()` : retourne la liste des alertes structurées
- `get_stats()` : statistiques par classification

Règles Snort incluses :
- Détection scan Nmap SYN
- Bruteforce SSH et HTTP Basic Auth
- SQL Injection
- XSS
- Directory Traversal

---

### 8. Réponse Active (`response`)

**Fichier** : `backend/app/modules/defensive/response.py`

Actions :
- `block_ip(ip, reason)` : règle iptables DROP
- `unblock_ip(ip)` : suppression de la règle
- `isolate_host(ip)` : isolation réseau (à connecter à l'hyperviseur)
- `send_alert(message, severity)` : alerte dans le SIEM

---

### 9. Forensique (`forensic`) – Bonus

**Fichier** : `backend/app/modules/defensive/forensic.py`

Outils :
- `ClamAV` – Antivirus open-source
- `VirusTotal API v3` – Analyse multi-moteurs

Méthodes :
- `scan_file(path)` : analyse un fichier avec ClamAV et VirusTotal
- `get_vt_result(analysis_id)` : récupère les résultats VirusTotal
