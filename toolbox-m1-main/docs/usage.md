# Guide d'Utilisation – ToolboxV8

## 1. Connexion

Accéder à : `http://localhost:3000/dashboard` (redirige vers `/login` si non authentifié).

Se connecter avec vos identifiants via le formulaire du service **web**. Celui-ci effectue `POST /login` qui appelle en interne `POST /api/auth/token` et **pose le JWT dans un cookie `HttpOnly`** (`access_token=...`).

> Le cookie HttpOnly n'est **pas** accessible en JavaScript côté navigateur : c'est volontairement plus sûr que l'ancien stockage en `localStorage`, car cela bloque l'exfiltration en cas de faille XSS.

Pour les **clients externes** (scripts, CI, Postman…), il reste toujours possible de récupérer un JWT classique avec `POST /api/auth/token` et de l'envoyer via l'en-tête `Authorization: Bearer <token>`.

---

## 2. Dashboard

Le dashboard affiche :

- **KPIs** : nombre de scans totaux, terminés, en erreur, rapports générés
- **Derniers jobs** : liste des 10 dernières tâches avec statut en temps réel
- **Derniers rapports** : accès direct au téléchargement

---

## 3. Lancer un module

### Via l'interface

1. Aller sur **Modules** dans la barre latérale
2. Sélectionner le module voulu
3. Renseigner la cible (IP, domaine ou URL)
4. Configurer les options avancées si nécessaire
5. Cliquer sur **Lancer**

Le job s'exécute en arrière-plan. Son statut se met à jour automatiquement.

### Profils par chips

Les modules offensifs proposent des **profils prédéfinis sous forme de chips**, plus besoin d'éditer la ligne de commande :

- **Nmap (Reconnaissance)** : Quick / Standard / Full TCP / Stealth — tous incluent `-Pn` par défaut pour scanner les hosts qui bloquent ICMP.
- **Nmap NSE (Scan Vulnérabilités)** : Quick / Standard / Full / Safe
- **Nikto** : Quick / Standard / Full / Evasion — timeout adapté par profil (10 à 60 min)
- **SSLyze** : Cert / Standard / Full — `--regular` obsolète remplacé par `--mozilla_config intermediate` (sslyze ≥ 5.x)
- **SQLmap** : Quick / Standard / Aggressive / Dump
- **MSF (Metasploit)** : Handler / EternalBlue / PortScan / SMB
- **ZAP Spider** : Quick / Standard / Deep
- **ZAP Active** : Quick / OWASP / Full

Il suffit de cliquer sur la chip correspondante pour charger les bons paramètres.

### Wordlists custom (Hydra / John)

Les modules **Hydra** et **John** acceptent 3 sources de wordlist au choix :

1. Un **fichier uploadé** via `POST /api/modules/wordlist` (stocké dans le volume partagé `wordlists_data`)
2. Une **liste manuelle** (saisie dans l'UI, un mot par ligne)
3. La **rockyou.txt** préinstallée dans l'image worker Kali

### Via l'API

```bash
# Obtenir un token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token \
  -d "username=admin&password=Admin1234!" | jq -r .access_token)

# Lancer une reconnaissance
curl -X POST http://localhost:8000/api/modules/launch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"module": "recon", "target": "192.168.1.1", "options": {"whois": true}}'
```

---

## 4. Modules disponibles

| Module | Cible | Options clés |
|--------|-------|-------------|
| `recon` | IP, domaine | `whois: true`, `nmap_args` (défaut `-sV -O -Pn --top-ports 1000`) |
| `scan` | IP, domaine | `nmap_vuln: true`, `nikto: true`, `sslyze: true`, `port` (défaut `"80,443"`), `nmap_vuln_profile`, `nikto_profile`, `sslyze_profile` |
| `exploit` | URL/IP | `mode: sqlmap\|hydra\|msf\|john` |
| `web_scan` | URL | `zap: true`, `scan_type: spider\|active` |

---

## 5. Suivre un job

```bash
# Lister ses jobs
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/modules/jobs

# Détail d'un job (résultat + état Celery)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/modules/jobs/1
```

---

## 6. Générer un rapport

```bash
# Générer un rapport PDF depuis un job terminé (ReportLab)
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"scan_job_id": 1, "title": "Rapport audit 192.168.1.1", "format": "pdf"}'

# Télécharger
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/reports/1/download -o rapport.pdf
```

> Les rapports sont générés en **PDF** via **ReportLab**.

---

## 7. SIEM – Kibana

1. Accéder à `http://localhost:5601`
2. Aller dans **Discover**
3. Créer un index pattern : `pentest-logs-*`
4. Visualiser les événements de scan, alertes IDS, actions de réponse

Dashboards recommandés à créer :
- Vue chronologique des scans
- Alertes Snort par classification
- Actions de réponse (blocages IP)

---

## 8. Réponse active

```bash
# Bloquer une IP suspecte
curl -X POST http://localhost:8000/api/modules/launch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"module": "response", "target": "10.0.0.5", "options": {"action": "block_ip", "reason": "bruteforce SSH détecté"}}'
```

---

## 9. Forensique (bonus)

```bash
# Scanner un fichier suspect
curl -X POST http://localhost:8000/api/modules/launch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"module": "forensic", "target": "/uploads/fichier_suspect.exe", "options": {}}'
```
