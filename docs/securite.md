# Sécurité & Conformité – PentestBox

## 1. Authentification et autorisation

### JWT (JSON Web Tokens)
- Algorithme : **HS256**
- Expiration configurable (`ACCESS_TOKEN_EXPIRE_MINUTES`, défaut 60 min)
- Stockage côté client uniquement (pas de session serveur)
- Revocation possible via blacklist Redis (à implémenter en production)

### RBAC (Role-Based Access Control)
| Rôle | Permissions |
|------|------------|
| `admin` | Tout accès, gestion des utilisateurs |
| `analyst` | Lancer des scans, générer des rapports |
| `reader` | Lecture seule de ses propres données |

### Mots de passe
- Hachage : **bcrypt** (coût adaptatif, résistant aux attaques par dictionnaire)
- Politique minimale recommandée : 12 caractères, majuscule + chiffre + symbole

---

## 2. Chiffrement

### Données en transit
- HTTPS obligatoire en production (reverse proxy Nginx/Traefik + Let's Encrypt)
- HSTS activé : `Strict-Transport-Security: max-age=31536000`

### Données au repos
- Chiffrement des données sensibles avec **Fernet** (AES-128-CBC + HMAC-SHA256)
- Clé générée via `cryptography.fernet.Fernet.generate_key()`
- Stocker la clé dans un gestionnaire de secrets (HashiCorp Vault, AWS SSM) en production

---

## 3. Protection de l'API

### Middlewares actifs
- `TrustedHostMiddleware` : rejette les requêtes avec Host header invalide
- `CORSMiddleware` : origines autorisées configurables
- Rate limiting recommandé (à ajouter via `slowapi` ou reverse proxy)

### Injection
- Toutes les entrées utilisateur validées via **Pydantic**
- Requêtes SQL via **SQLAlchemy ORM** (pas de SQL brut)
- Échappement automatique dans les templates Jinja2 (`autoescape=True`)

### Dépendances
- Scan régulier avec `safety check` ou `pip-audit`
- Dependency-Check (OWASP) intégré comme module

---

## 4. Audit et journalisation

### Audit Log
Toutes les actions sensibles sont enregistrées dans la table `audit_logs` :
- Connexion / déconnexion
- Lancement de modules
- Génération de rapports
- Erreurs d'authentification

### SIEM (ELK Stack)
- Tous les événements de scan indexés dans Elasticsearch
- Alertes IDS (Snort) ingérées via Logstash
- Rétention des logs : 90 jours (configurable dans ILM Elasticsearch)

---

## 5. Conformité RGPD

| Exigence RGPD | Implémentation |
|---------------|----------------|
| Minimisation des données | Seules les données nécessaires sont collectées |
| Droit à l'effacement | Endpoint de suppression de compte à implémenter |
| Sécurité des traitements | Chiffrement, RBAC, audit log |
| Journaux d'accès | AuditLog horodaté avec IP |
| Consentement | Réservé à des cibles autorisées (contrat de prestation) |

> **Important** : PentestBox ne doit être utilisé que dans le cadre de tests d'intrusion autorisés par écrit par le propriétaire de la cible.

---

## 6. Cadre légal

- Utilisation soumise à la loi n°88-19 du 5 janvier 1988 (CNIL) et au RGPD
- Chaque test doit faire l'objet d'une **lettre de mission signée**
- Les résultats doivent être traités comme **confidentiel**
- Interdiction d'utilisation sur des systèmes non autorisés

---

## 7. Recommandations pour la production

- [ ] Activer HTTPS (Nginx + Let's Encrypt)
- [ ] Remplacer les mots de passe par défaut (PostgreSQL, MinIO, Kibana)
- [ ] Utiliser HashiCorp Vault pour les secrets
- [ ] Activer l'authentification Elasticsearch (`xpack.security.enabled: true`)
- [ ] Configurer les sauvegardes PostgreSQL (pg_dump) + MinIO
- [ ] Mettre en place un WAF devant l'API
- [ ] Activer le rate limiting sur les endpoints d'auth
- [ ] Scanner régulièrement les dépendances Python
