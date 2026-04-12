# Todo – PentestBox

Suivi des taches en cours, a faire et terminees.
Mettre a jour ce fichier apres chaque session de travail.

---

## Sprint 1 – Architecture de base ✅

- [x] Structure complete du projet (dossiers + fichiers)
- [x] Backend FastAPI avec config, securite, auth, DB
- [x] Modeles SQLAlchemy : User, ScanJob, Report, AuditLog
- [x] Taches Celery : recon, scan, exploit, web_scan, report
- [x] Routes API : auth, modules, reports, dashboard
- [x] Stack Docker Compose complete
- [x] Configuration ELK Stack + Snort
- [x] Frontend : base, login, dashboard, report templates
- [x] Design System CSS dark mode
- [x] Documentation complete (7 fichiers dans docs/)
- [x] Scripts start.sh et push_gitlab.sh
- [x] .claude/changelog.md et .claude/todo.md

---

## Sprint 2 – Pages frontend + routes defensives ✅

- [x] Page **Modules** (`frontend/templates/modules.html`)
- [x] Page **Rapports** (`frontend/templates/reports.html`)
- [x] Page **SIEM** (`frontend/templates/siem.html`)
- [x] Routes defensives (`backend/app/api/routes/defensive.py`)
- [x] Routes pages HTML (`backend/app/api/routes/pages.py`)
- [x] Scripts PowerShell (`scripts/start.ps1`, `scripts/push_gitlab.ps1`)
- [x] CSS et JS supplementaires (`app.css`, `app.js`)
- [x] Depot pousse sur GitHub : https://github.com/Vyuob/toolbox-m1

---

## Sprint 3 – Migrations et tests 🔄

- [ ] Initialiser Alembic pour les migrations DB
  ```bash
  cd backend
  alembic init alembic
  alembic revision --autogenerate -m "initial"
  alembic upgrade head
  ```
- [ ] Completer les tests unitaires (`backend/tests/`)
  - [ ] Test CRUD User
  - [ ] Test lancement module + polling job
  - [ ] Test generation rapport
- [ ] Ajouter `pytest-asyncio` pour tests async
- [ ] Configurer CI/CD GitHub Actions (`.github/workflows/ci.yml`)

---

## Sprint 4 – Interface et UX 🔄

- [ ] Formulaire de lancement modules avec options dynamiques
- [ ] Affichage resultats en temps reel (polling JS)
- [ ] Liste des rapports avec filtres
- [ ] Previsualisation HTML inline des rapports
- [ ] Ameliorer le template de rapport PDF
  - Graphiques Matplotlib (ports ouverts, severites)
  - Logo + mise en page professionnelle

---

## Sprint 5 – Defense et SIEM 🔄

- [ ] Dashboard Kibana preconfigure (export JSON a importer)
  - Vue chronologique des scans
  - Alertes Snort par classification
  - Top 10 cibles scannees
- [ ] Endpoint API pour les alertes IDS
  - `GET /api/defensive/alerts` -> alertes Snort recentes
  - `GET /api/defensive/siem/search?q=...` -> recherche ELK
- [ ] Interface reponse active
  - Formulaire de blocage/deblocage IP

---

## Sprint 6 – Securite et production 🔄

- [ ] Activer HTTPS (Nginx reverse proxy dans docker-compose)
- [ ] Rate limiting sur `/api/auth/token` (5 tentatives/min)
- [ ] Endpoint suppression compte RGPD
- [ ] Rotation des tokens JWT (refresh token)
- [ ] Scan des dependances Python (`pip-audit`)
- [ ] Tests de penetration sur l'outil lui-meme

---

## Sprint 7 – Module Forensique (Bonus) 🔄

- [ ] Endpoint upload fichier suspect
  - `POST /api/forensic/scan` (multipart/form-data)
- [ ] Integration Cuckoo Sandbox (optionnel)
- [ ] Rapport forensique dedie

---

## Livrables pedagogiques 📋

- [ ] **Video MVP** (15-20 min)
  - [ ] Preparer la VM cible (Metasploitable2 ou DVWA)
  - [ ] Preparer le script de demo
  - [ ] Enregistrer (OBS Studio recommande)
  - [ ] Exporter en `.mp4`
  - [ ] Nommer : `PE-2526_codepromo_NomPrenom.mp4`

- [ ] **Document technique final**
  - [ ] Rediger rendu groupe (PDF)
  - [ ] Chaque membre redige son rendu individuel
  - [ ] Creer le ZIP final : `PE_2526_codepromo_noms.zip`

---

## Bugs connus / Points d'attention

| Probleme | Priorite | Assigne a |
|----------|----------|-----------|
| Importer les modules dans celery sans circular import | Haute | Etudiant 1 |
| WeasyPrint necessite des dependances systeme (Cairo, Pango) | Moyenne | Etudiant 1 |
| Snort non inclus dans docker-compose (a ajouter) | Moyenne | Etudiant 2 |
| HTTPS non active en dev (ok) mais obligatoire en prod | Haute | Etudiant 1 |
