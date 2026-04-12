# Todo – PentestBox

Suivi des tâches en cours, à faire et terminées.
Mettre à jour ce fichier après chaque session de travail.

---

## Sprint 1 – Architecture de base ✅

- [x] Structure complète du projet (dossiers + fichiers)
- [x] Backend FastAPI avec config, sécurité, auth, DB
- [x] Modèles SQLAlchemy : User, ScanJob, Report, AuditLog
- [x] Tâches Celery : recon, scan, exploit, web_scan, report
- [x] Routes API : auth, modules, reports, dashboard
- [x] Stack Docker Compose complète
- [x] Configuration ELK Stack + Snort
- [x] Frontend : base, login, dashboard, report templates
- [x] Design System CSS dark mode
- [x] Documentation complète (7 fichiers dans docs/)
- [x] Scripts start.sh et push_gitlab.sh
- [x] .claude/changelog.md et .claude/todo.md

---

## Sprint 2 – Migrations et tests 🔄

- [ ] Initialiser Alembic pour les migrations DB
  ```bash
  cd backend
  alembic init alembic
  alembic revision --autogenerate -m "initial"
  alembic upgrade head
  ```
- [ ] Compléter les tests unitaires (`backend/tests/`)
  - [ ] Test CRUD User
  - [ ] Test lancement module + polling job
  - [ ] Test génération rapport
- [ ] Ajouter `pytest-asyncio` pour tests async
- [ ] Configurer CI/CD GitLab (`.gitlab-ci.yml`)

---

## Sprint 3 – Interface et UX 🔄

- [ ] Page **Modules** (`frontend/templates/modules.html`)
  - Formulaire de lancement avec options dynamiques
  - Affichage résultats en temps réel (polling JS)
- [ ] Page **Rapports** (`frontend/templates/reports.html`)
  - Liste des rapports avec filtres
  - Prévisualisation HTML inline
- [ ] Améliorer le template de rapport PDF
  - Graphiques Matplotlib (ports ouverts, sévérités)
  - Logo + mise en page professionnelle

---

## Sprint 4 – Défense et SIEM 🔄

- [ ] Dashboard Kibana préconfiguré (export JSON à importer)
  - Vue chronologique des scans
  - Alertes Snort par classification
  - Top 10 cibles scannées
- [ ] Endpoint API pour les alertes IDS
  - `GET /api/defensive/alerts` → alertes Snort récentes
  - `GET /api/defensive/siem/search?q=...` → recherche ELK
- [ ] Interface réponse active
  - Formulaire de blocage/déblocage IP

---

## Sprint 5 – Sécurité et production 🔄

- [ ] Activer HTTPS (Nginx reverse proxy dans docker-compose)
- [ ] Rate limiting sur `/api/auth/token` (5 tentatives/min)
- [ ] Endpoint suppression compte RGPD
- [ ] Rotation des tokens JWT (refresh token)
- [ ] Scan des dépendances Python (`pip-audit`)
- [ ] Tests de pénétration sur l'outil lui-même

---

## Sprint 6 – Module Forensique (Bonus) 🔄

- [ ] Endpoint upload fichier suspect
  - `POST /api/forensic/scan` (multipart/form-data)
- [ ] Intégration Cuckoo Sandbox (optionnel)
- [ ] Rapport forensique dédié

---

## Livrables pédagogiques 📋

- [ ] **Vidéo MVP** (15-20 min)
  - [ ] Préparer la VM cible (Metasploitable2 ou DVWA)
  - [ ] Préparer le script de démo
  - [ ] Enregistrer (OBS Studio recommandé)
  - [ ] Exporter en `.mp4`
  - [ ] Nommer : `PE-2526_codepromo_NomPrenom.mp4`

- [ ] **Document technique final**
  - [ ] Rédiger rendu groupe (PDF)
  - [ ] Chaque membre rédige son rendu individuel
  - [ ] Créer le ZIP final : `PE_2526_codepromo_noms.zip`

---

## Bugs connus / Points d'attention

| Problème | Priorité | Assigné à |
|----------|----------|-----------|
| Importer les modules dans celery sans circular import | Haute | Étudiant 1 |
| WeasyPrint nécessite des dépendances système (Cairo, Pango) | Moyenne | Étudiant 1 |
| Snort non inclus dans docker-compose (à ajouter) | Moyenne | Étudiant 2 |
| HTTPS non activé en dev (ok) mais obligatoire en prod | Haute | Étudiant 1 |
