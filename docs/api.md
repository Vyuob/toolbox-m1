# Référence API REST – ToolboxV8

> Documentation Swagger interactive : `http://localhost:8000/api/docs`

## Authentification

Toutes les routes (sauf `/health` et `/api/auth/token`) nécessitent un JWT.

L'API accepte **deux méthodes** d'authentification équivalentes :

- En-tête HTTP `Authorization: Bearer <access_token>` (clients externes, scripts, CI)
- Cookie `access_token=<jwt>` (utilisé automatiquement par le service **web** sur le port 3000, posé en `HttpOnly` lors du login)

```
Authorization: Bearer <access_token>
```

---

## Auth `/api/auth`

### POST `/api/auth/token`
Obtenir un token JWT.

**Body** (form-data) :
```
username=admin
password=Admin1234!
```

**Réponse 200** :
```json
{"access_token": "eyJ...", "token_type": "bearer"}
```

---

### POST `/api/auth/register`
Créer un compte utilisateur.

**Body** (JSON) :
```json
{
  "username": "alice",
  "email": "alice@pentest.local",
  "password": "SecurePass1!",
  "role": "analyst"
}
```

**Réponse 201** :
```json
{"id": 2, "username": "alice", "email": "alice@pentest.local", "role": "analyst", "is_active": true}
```

---

### GET `/api/auth/me`
Profil de l'utilisateur connecté.

**Réponse 200** :
```json
{"id": 1, "username": "admin", "email": "admin@pentest.local", "role": "admin", "is_active": true}
```

---

## Modules `/api/modules`

### GET `/api/modules/`
Lister les modules disponibles.

**Réponse 200** :
```json
{
  "modules": [
    {"name": "recon",    "description": "Reconnaissance OSINT & Nmap"},
    {"name": "scan",     "description": "Scan de vulnérabilités"},
    {"name": "exploit",  "description": "Exploitation"},
    {"name": "web_scan", "description": "Analyse Web/API"}
  ]
}
```

---

### POST `/api/modules/launch`
Lancer un module. Rôle requis : `analyst` ou `admin`.

**Body** :
```json
{
  "module": "recon",
  "target": "192.168.1.100",
  "options": {
    "whois": true,
    "nmap_args": "-sV -T4 --top-ports 100"
  }
}
```

**Réponse 202** :
```json
{
  "id": 5,
  "task_id": "a1b2c3d4-...",
  "module": "recon",
  "target": "192.168.1.100",
  "status": "pending"
}
```

---

### GET `/api/modules/jobs`
Lister ses jobs.

### GET `/api/modules/jobs/{job_id}`
Détail d'un job avec état Celery en temps réel.

---

### POST `/api/modules/wordlist`
Uploader une wordlist custom (utilisable ensuite par les modules **Hydra** et **John**). Rôle requis : `analyst` ou `admin`.

Le fichier est stocké dans le volume Docker partagé `wordlists_data` (monté sur `/tmp/wordlists` côté `api` et côté `worker`).

**Requête** : `multipart/form-data`

| Champ | Type | Description |
|-------|------|-------------|
| `file` | file | Fichier texte (un mot par ligne) |

**Exemple curl** :
```bash
curl -X POST http://localhost:8000/api/modules/wordlist \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./passwords.txt"
```

**Réponse 201** :
```json
{
  "path": "/tmp/wordlists/passwords.txt",
  "filename": "passwords.txt",
  "size": 10240,
  "lines": 1337
}
```

Le champ `path` renvoyé peut être passé aux modules Hydra / John comme wordlist source.

---

## Rapports `/api/reports`

### POST `/api/reports/generate`
Générer un rapport. Rôle requis : `analyst` ou `admin`.

**Body** :
```json
{
  "scan_job_id": 5,
  "title": "Audit réseau – 2025",
  "format": "pdf"
}
```

**Réponse 202** :
```json
{"task_id": "...", "message": "Génération du rapport lancée"}
```

---

### GET `/api/reports/`
Lister ses rapports.

### GET `/api/reports/{id}/download`
Télécharger un rapport (PDF, HTML ou CSV).

---

## Dashboard `/api/dashboard`

### GET `/api/dashboard/`
Retourne la page HTML du dashboard (Jinja2).

### GET `/api/dashboard/stats`
KPIs JSON pour le dashboard.

**Réponse 200** :
```json
{
  "total_jobs": 12,
  "done_jobs": 10,
  "error_jobs": 1,
  "total_reports": 7
}
```

---

## Codes d'erreur

| Code | Description |
|------|-------------|
| 400 | Données invalides (module inconnu, email déjà pris…) |
| 401 | Token absent ou expiré |
| 403 | Rôle insuffisant |
| 404 | Ressource introuvable |
| 422 | Erreur de validation Pydantic |
| 500 | Erreur interne serveur |
