# Script vidéo soutenance — ToolboxV8 (15-20 minutes · 25 slides)

> **Format imposé** (Cadre §VI.2) : screencast + **prise de parole de chaque membre**, **nom affiché** à l'écran pour chaque intervenant, structure **besoin → solution → démonstration**, durée **15-20 min**, export `.mp4`.
>
> **Répartition des voix** (rôles du cahier des charges §VI / slide 2) :
> - **Ayoub** — Architecte & Back-end / Sécurité → slides intro, archi, stack, sécurité, défensif. Démos : **Hydra, John** + **SIEM en direct**.
> - **Abdallah** — Intégration offensive & Qualité → périmètre, modules, KPIs, limites. Démos : **SQLmap, ZAP, Gobuster**.
> - **Titouan** — Interface & Reporting → problème, objectifs, roadmap, conclusion. Démos : **OSINT, Rapport PDF**.
>
> ✅ Chacun présente au moins 2 démos. Les 3 voix se partagent les 25 slides.
>
> **Les démos sont des VIDÉOS PRÉPARÉES** intégrées dans la présentation (dossier `videos/`), pas du live.
> L'intervenant **lance la vidéo de sa slide** et commente par-dessus / autour.

---

## AVANT L'ENREGISTREMENT (pré-production)

1. **Enregistrer les 7 vidéos de démo à l'avance** (cf. `videos/README.txt`) en faisant tourner la vraie stack (`./scripts/start.ps1`), puis les déposer dans `presentation-toolbox/videos/` avec les bons noms et décommenter les balises `<video>`.
2. Ouvrir `index.html` dans le navigateur, passer en **plein écran** (touche `F`).
3. Vérifier que chaque slide de démo lit bien sa vidéo (clic sur la vidéo = lecture).
4. Chaque intervenant répète son texte ; on enregistre la voix en commentant les vidéos.
5. Cacher tout mot de passe / token visible dans les vidéos de démo (re-tourner si besoin).

---

# ACTE 1 — LE BESOIN (~3 min)

### Slide 1 — Page de garde (~20 sec)

**Ayoub** :
> Bonjour à tous. Nous vous présentons **ToolboxV8**, notre projet de fin de Mastère Cybersécurité, promotion 2025-2026 : une plateforme web qui automatise les étapes d'un test d'intrusion. Je suis **Ayoub**, en charge de l'architecture back-end et de la sécurisation de l'outil. À mes côtés, **Abdallah**, qui pilote l'intégration des outils offensifs et la qualité, et **Titouan**, responsable de l'interface et du reporting.

### Slide 2 — Équipe (~30 sec)

**Ayoub** :
> Notre équipe se répartit sur trois axes complémentaires : l'**architecture back-end et la sécurité** de mon côté, l'**intégration des outils offensifs et la qualité** pour Abdallah, et l'**interface et le reporting** pour Titouan. Chacun a son périmètre principal, mais nous avons tous mis les mains dans tous les modules — c'est indispensable pour la cohérence du produit. Je laisse Abdallah présenter le contexte.

### Slide 3 — Le contexte client (~45 sec)

**Abdallah** :
> Notre client est une société spécialisée en **cybersécurité offensive** : elle réalise des tests d'intrusion pour des entreprises privées et des institutions publiques. Son problème est double. D'abord, ses pentests reposent sur des **manipulations manuelles**, donc longs — souvent plusieurs heures pour un audit basique. Ensuite, le résultat est **hétérogène selon l'analyste** : deux intervenants lancent le même outil mais ne rendent pas le même rapport. Le client y perd du temps, et de la crédibilité face à ses propres clients. Je passe la parole à Titouan pour le détail des douleurs.

### Slide 4 — Le problème à résoudre (~45 sec)

**Titouan** :
> Nous avons identifié **5 douleurs concrètes** : le temps perdu en commandes répétitives, l'absence de standardisation entre analystes, des rapports souvent illisibles écrits à la main, l'impossibilité pour un analyste junior de lancer un pentest sans connaître par cœur des dizaines d'outils en ligne de commande, et enfin aucune traçabilité claire des actions menées. Notre objectif : transformer ces 5 douleurs en 5 réponses concrètes dans une seule plateforme web.

### Slide 5 — Objectifs du cahier des charges (~45 sec)

**Titouan** :
> Le cahier des charges fixe **5 objectifs mesurables**. Le plus important : **réduire d'au moins 40 % le temps** de réalisation d'un pentest. Les autres : standardiser les pratiques, proposer une interface utilisable par un analyste qui n'est pas développeur, fournir des rapports lisibles et exploitables, et permettre une intégration simple dans l'écosystème du client. Comme vous le verrez, nous avons non seulement atteint ces objectifs, mais **largement dépassé** la cible de temps : 75 % de gain sur recon + scan, et près de 100 % sur la rédaction de rapport.

---

# ACTE 2 — LA SOLUTION (~4 min)

### Slide 6 — Périmètre fonctionnel (~50 sec)

**Abdallah** :
> ToolboxV8 couvre les **5 grandes étapes** d'un test d'intrusion. D'abord la **reconnaissance passive** — l'OSINT — on cherche tout ce qu'on peut trouver sans toucher à la cible. Ensuite la **reconnaissance active** : Nmap, DNS, fingerprinting. Puis le **scan de vulnérabilités** avec Nikto et SSLyze. L'**exploitation** avec SQLmap, Hydra et John the Ripper. Et enfin l'**analyse web** avec OWASP ZAP et Gobuster. On a aussi un **volet défensif** : un SIEM ELK opérationnel, des règles Snort et un module de réponse iptables — j'y reviendrai en toute transparence.

### Slide 7 — Organisation & méthodologie (~45 sec)

**Ayoub** :
> Côté organisation : nous avons travaillé à trois sur **six mois**, découpés en **quatre grandes phases** plutôt qu'en sprints rigides. Phase 1, le **socle** : architecture Docker, authentification, base de données. Phase 2, l'**offensif** : les cinq outils d'attaque. Phase 3, le **défensif** : SIEM, règles Snort, module de réponse. Phase 4, le **reporting** et les finitions. On se coordonnait **sur Teams et Discord, à l'oral, quand c'était nécessaire**. Le code est sur **GitHub avec un miroir GitLab** ; une version stable protégée, le travail en cours sur des branches, et chaque outil **testé sur une cible réelle** avant d'être intégré. Je continue sur l'architecture technique.

### Slide 8 — Architecture globale (~55 sec)

**Ayoub** :
> ToolboxV8 est une stack **100 % dockerisée**, en briques isolées. À l'extérieur, un reverse proxy **Caddy** qui gère le HTTPS. Derrière, on a séparé volontairement l'**interface** et le **moteur (l'API)** en deux services FastAPI. Pourquoi ? D'abord pour la **sécurité** : le cookie de session est posé par le service web seul, jamais exposé directement par l'API. Ensuite pour l'**intégration** : l'API reste accessible aux outils du client — un script ou la CI peut l'appeler sans passer par le formulaire web. Un **exécuteur Celery sur image Kali** lance les scans avec tous les outils préinstallés. Côté infra : PostgreSQL pour les données, Redis pour la file de tâches, MinIO pour les fichiers, et ELK pour la surveillance.

### Slide 9 — Stack technique (~45 sec)

**Ayoub** :
> Rien d'exotique, tout est standard et maintenable. Back-end : Python 3.11, FastAPI, SQLAlchemy, Celery. Front : Jinja2 et JavaScript vanilla — pas de framework lourd. Données : PostgreSQL 16, Redis 7, MinIO. Le worker tourne sur **Kali Rolling** — Nmap, Nikto, SQLmap, Hydra, John jumbo qui supporte 304 formats de hash, SSLyze. Pour le HTTPS, **Caddy** : trois lignes de configuration, certificat auto-généré, et bascule vers Let's Encrypt en une ligne pour la production. Côté CI/CD, **GitHub Actions + GitLab CI** — le dépôt est sur GitHub mais on respecte le cahier qui demande GitLab. Je passe la main à Abdallah pour les modules et les premières démos.

### Slide 10 — Les modules (~40 sec)

**Abdallah** :
> Voici le cœur du produit : **5 modules offensifs et 4 défensifs**. Le principe est simple — chaque outil expose des **profils par boutons** : Quick, Standard, Full. L'analyste ne tape plus aucune commande, il choisit son intensité d'un clic. Et chaque outil a un **interrupteur indépendant** : dans le module Scan, je peux activer Nikto sans lancer SSLyze, et les outils désactivés n'apparaissent pas dans le rapport. **Zéro ligne de commande à connaître.** Passons aux démonstrations.

---

# ACTE 3 — LA DÉMONSTRATION (~11 min 15)

### Slide 11 — DÉMO 1 : Reconnaissance passive OSINT (~1 min 15)

**Titouan** : *[lance la vidéo de démo de la slide]*
> Premier module : la **reconnaissance passive**. Imaginons qu'un client comme **Nike** nous mandate pour un audit OSINT — qu'est-ce qu'on trouve publiquement sur leur marque, sans envoyer un seul paquet à leurs serveurs ? Je tape simplement « Nike » dans le champ cible : pas besoin de domaine, le champ est libre. Je coche les catégories **Mot-clé** et **Réseaux sociaux** : ça génère automatiquement **12 dorks Google ciblés** — des recherches de PDF, CV publics, mentions sur LinkedIn, GitHub, Twitter, Reddit, Facebook, Pastebin, mais aussi des dorks plus offensifs : recherche de **fuites** (« leaked », « breach », « dump ») et de **mentions de credentials**. Je clique Lancer, et la toolbox **ouvre automatiquement un onglet Google par dork**. Le rapport PDF liste les 12 requêtes générées. Tout est **100% passif** : zéro paquet envoyé à Nike, on interroge uniquement Google qui restitue ce qui est déjà indexé publiquement — conformité RGPD garantie.

### Slide 11 bis — DÉMO 2 : Reconnaissance active (~45 sec)

**Ayoub** : *[lance la vidéo de démo de la slide]*
> Après l'OSINT, on touche au réseau de la cible — mais toujours en mode autorisé. Cible : **scanme.nmap.org**, le serveur officiel du projet Nmap mis en ligne pour qu'on puisse s'entraîner légalement. Profil **Quick** — un coup d'œil rapide. La toolbox enchaîne **trois outils** en parallèle : **Nmap** repère les ports ouverts et identifie les services, **Whois** récupère le propriétaire du domaine, et **WhatWeb** fingerprinte les technos web. Résultat en quelques secondes : ports **22 SSH** et **80 HTTP** ouverts, identification d'**Apache** côté web, propriétaire du domaine résolu. Tout est consolidé dans le rapport PDF en une seule page — la cartographie de la cible est faite.

### Slide 11 ter — DÉMO 3 : Scan de vulnérabilités (~45 sec)

**Titouan** : *[lance la vidéo de démo de la slide]*
> Une fois la surface identifiée, on passe au **scan de vulnérabilités**. Même cible scanme.nmap.org, port 80. J'active **Nikto** en profil Quick et je désactive SSLyze — scanme n'a pas de HTTPS donc pas besoin d'audit TLS. Nikto bombarde le serveur de **plusieurs milliers de requêtes** de tests : recherche de fichiers exposés, headers de sécurité manquants, anciennes versions exploitables. Résultat : **Apache fingerprinté**, plusieurs **headers de sécurité manquants** (X-Content-Type-Options, Strict-Transport-Security), `mod_negotiation` activé — un vecteur d'énumération connu. C'est exactement ce qu'un audit client doit produire : des findings concrets, classés et directement actionnables par l'équipe sécurité.

### Slide 12 — DÉMO 4 : SQLmap, injection SQL (~1 min 15)

**Abdallah** : *[lance la vidéo de démo de la slide]*
> On passe à l'**exploitation**. Cible légalement autorisée : `testasp.vulnweb.com`, un site volontairement vulnérable d'Acunetix. Outil : **SQLmap**, profil Quick. Pendant que ça tourne, un mot sur la sécurité de l'outil : **tous les scans sont tracés** dans une table d'audit. Si le client a un contrôle, on produit la liste exhaustive des scans, qui les a lancés et sur quelle cible. Résultat : SQLmap confirme la vulnérabilité avec **deux types d'injection** — boolean-based blind et time-based blind. Base de données identifiée : **Microsoft SQL Server 2014**. Stack web : **ASP, ASP.NET, IIS 8.5**. Le tout exporté en PDF en un clic.

### Slide 13 — DÉMO 5 : Hydra, brute-force SSH (~1 min)

**Ayoub** : *[lance la vidéo de démo de la slide]*
> Démo suivante : **Hydra**, le cassage d'identifiants. Pour rester légal, j'ai déployé une **cible interne dans notre stack** — un serveur SSH volontairement faible, isolé sur le réseau Docker, que j'ai monté côté back-end. Cible : `target`, port 2222. Une liste de cinq mots de passe dont le bon. Sur la vidéo : **cracké en une seconde** — `pentest_user : toor`. Imaginez la même chose sur une vraie cible avec la wordlist rockyou et ses 14 millions d'entrées : un compte faible tombe en quelques minutes. C'est exactement le risque qu'on aide le client à mesurer.

### Slide 14 — DÉMO 6 : John the Ripper, cassage de hash (~50 sec)

**Ayoub** : *[lance la vidéo de démo de la slide]*
> Deuxième outil de mon côté : **John the Ripper**. Cas d'usage : on a récupéré un hash après une compromission. Sur la vidéo, je colle un hash MD5 — celui du mot « admin » — au format raw-md5. **0 seconde** : John retrouve le mot de passe d'origine. Notre version supporte **304 formats** : bcrypt, sha512crypt des `/etc/shadow` Linux, NTLM Windows, coffres KeePass, archives ZIP… Je rends la parole à Abdallah pour l'analyse web.

### Slide 15 — DÉMO 7 : OWASP ZAP, scan web (~1 min 15)

**Abdallah** : *[lance la vidéo de démo de la slide]*
> Cinquième module : **OWASP ZAP**, notre scanner web. On l'a intégré directement dans la stack Docker — rien à installer à part. Cible : `testasp.vulnweb.com`, Active scan. Ce que fait le module est subtil : il **lance le scan**, **interroge l'API de ZAP toutes les 5 secondes** jusqu'à la fin, puis **récupère automatiquement les alertes**. Résultat sur la vidéo : **105 alertes, 14 types uniques**, en 55 secondes. En Medium : absence de Content Security Policy, pas de protection anti-clickjacking, pas d'anti-CSRF. En Low : fuites de versions serveur. C'est directement exploitable par l'équipe sécurité du client.

### Slide 16 — DÉMO 8 : Gobuster, pages cachées (~45 sec)

**Abdallah** : *[lance la vidéo de démo de la slide]*
> Toujours en analyse web : **Gobuster**, qui débusque les pages cachées d'un site. Même cible, profil Quick. Sur la vidéo, il trouve un dossier `_vti_pvt` — une vieille interface FrontPage Microsoft, indicateur d'une configuration à patcher — ainsi que `/cgi-bin`, `/templates`, `/aspnet_client`. Chaque chemin découvert apparaît dans le rapport avec son code HTTP. Voilà nos **5 modules offensifs** démontrés. Je rends la parole à Ayoub pour la sécurité et le défensif.

### Slide 17 — Sécurité de la toolbox (~45 sec)

**Ayoub** :
> Un outil de pentest est une cible de choix, donc **ToolboxV8 se protège elle-même**. L'authentification se fait par **jeton signé (JWT)**, dans un cookie HttpOnly. Les mots de passe sont stockés en **bcrypt**, jamais en clair. Les autorisations suivent un **RBAC à 3 rôles** : admin, analyste, lecture seule — vérifié à chaque action. Les secrets sont chiffrés en **Fernet**, et toute la communication passe en **HTTPS**. Enfin, un **journal d'audit horodaté** garde la trace de toutes les actions sensibles. C'est formalisé dans une section dédiée du rapport — 7 politiques, de l'accès au chiffrement.

### Slide 18 — Module défensif & pipeline de réponse (~50 sec)

**Ayoub** : *[montre le dashboard /siem — capture ou court extrait]*
> Côté défensif, soyons transparents sur ce qui tourne et ce qui est préparé. **Ce qui tourne** : un **SIEM ELK opérationnel** — Elasticsearch, Logstash, Kibana — qui indexe nos scans et nos événements. Voici notre tableau de bord `/siem` : événements récents, volumétrie. **Ce qui est préparé** : on a écrit **9 règles Snort** — détection de scan Nmap, brute-force SSH, injection SQL, XSS, Log4Shell — et un module de réponse capable de **bloquer une IP via iptables**. En toute honnêteté : le conteneur Snort n'est pas encore branché dans le compose, et le blocage iptables est aujourd'hui **simulé** tant qu'on n'est pas sur un hôte Linux. C'est la chaîne défensive **visée**, et c'est en tête de notre roadmap.

### Slide 19 — DÉMO SIEM : tableau de bord en direct (~50 sec)

**Ayoub** : *[bascule en direct sur `https://localhost/siem`]*
> Et justement, voici la partie qui **tourne déjà** : notre tableau de bord **SIEM**, en direct. Avant l'enregistrement, j'ai lancé plusieurs scans — le dashboard les agrège automatiquement. En haut, l'**état de la stack ELK** : Elasticsearch, Logstash, Kibana, plus MinIO, Redis et PostgreSQL, tous surveillés en temps réel. En dessous : le nombre de scans sur 24 heures, le taux de réussite, la **timeline** des scans par heure, la répartition par module et le top des cibles. Chaque action sensible est aussi indexée dans Elasticsearch et consultable dans **Kibana** — y compris une **réponse active** comme un blocage d'IP. C'est notre brique concrète de **détection et réponse**. Je passe la parole à Titouan pour le reporting.

### Slide 20 — DÉMO 9 : Le rapport PDF (~1 min)

**Titouan** : *[lance la vidéo de démo de la slide]*
> Tous les scans que mes collègues ont lancés produisent automatiquement un **rapport PDF structuré**. Sur la vidéo : page de couverture, **synthèse exécutive** en encart pour le CODIR du client, statistiques, déroulé technique par outil avec la commande exécutée et la sortie console brute, tableau de synthèse, recommandations et annexes. On a soigné la lisibilité — palette douce, blocs de code lisibles jusque sur les pages de débordement. Le tout généré en **2 secondes** depuis l'interface : c'est notre 99 % de gain sur la rédaction.

---

# ACTE 4 — BILAN (~3 min)

### Slide 21 — KPIs atteints (~45 sec)

**Titouan** :
> Bilan chiffré. Sur **recon + scan**, on passe de 15-20 minutes manuelles à 3-5 minutes en profil Quick : **75 % de gain**. Sur la **rédaction de rapport**, de 1-2 heures à 2 secondes : **99 % de gain**. L'objectif des 40 % du cahier des charges est donc **largement dépassé**. Côté qualité, **0 commande à apprendre** côté analyste, et **0 crash sur 50 scans enchaînés** lors de nos tests de stabilité.

### Slide 22 — Limites assumées (~45 sec)

**Abdallah** :
> Restons honnêtes — c'est notre rôle qualité. Trois limites documentées. **Metasploit** : intégré, mais son moteur doit être démarré à la main, pas encore industrialisé. **Snort** : les 9 règles sont écrites, mais le conteneur ne tourne pas sur notre PC de test sous Windows — il faut un vrai serveur Linux. Et l'**extraction de données** massive est volontairement bridée à 5 lignes par table : c'est une contrainte intrinsèque de l'injection en aveugle, pas un défaut de notre code. Tout est documenté, tout est défendable.

### Slide 23 — Perspectives d'évolution (~30 sec)

**Titouan** :
> Pour la suite : démarrer **Metasploit** automatiquement, déployer **Snort** sur un hôte Linux dédié, brancher le **blocage automatique** d'une IP depuis l'API, intégrer **SecLists** pour des listes plus complètes, et à plus long terme un **module IA / Machine Learning** pour trier automatiquement les failles par dangerosité, ainsi qu'une connexion **SSO** pour s'intégrer à l'écosystème de l'entreprise.

### Slide 24 — Récap & impact (~30 sec)

**Ayoub** :
> En résumé : **5 modules offensifs + 4 défensifs**, **12 outils** intégrés, **6 mois** de développement en 4 phases, une **CI/CD** à chaque push, du **HTTPS** en standard, et un produit qui démontre concrètement les **75 % de gain de temps** promis au client. Le tout **100 % dockerisé**, déployable en une commande, entièrement sur notre dépôt et documenté.

### Slide 25 — Conclusion & remerciements (~20 sec)

**Titouan** *(puis un mot de chacun)* :
> Merci à notre tuteur de Mastère et à l'équipe pédagogique pour l'accompagnement sur ces six mois. Le code, la documentation, le rapport technique et le guide pratique sont sur notre GitHub. Nous sommes à votre disposition pour vos questions. Merci à tous les trois — Ayoub, Abdallah, Titouan — et merci pour votre attention.

---

## INDICATIONS TECHNIQUES POUR L'ENREGISTREMENT

- **Vidéos de démo** : enregistrées à l'avance (OBS Studio), déposées dans `videos/`, intégrées dans les slides. L'orateur commente par-dessus.
- **Voix off** : enregistrer en 3 blocs (un par membre) puis monter, c'est plus simple qu'une prise unique.
- **Résolution** : 1920×1080, 30 fps, ~6 Mbps.
- **Nom à l'écran** : ajouter en post-production un bandeau bas avec le nom de l'intervenant qui parle (exigence Cadre §VI.2). Le bas de slide affiche déjà le nom via la barre de navigation.
- **Plein écran** : lancer la présentation avec la touche `F` ; avancer avec `→` (chaque clic révèle d'abord les encarts, puis change de slide).

## CONTRÔLE QUALITÉ AVANT EXPORT

- [ ] Durée **15-20 min** (idéalement 18)
- [ ] **Les 3 membres parlent** (Ayoub, Abdallah, Titouan)
- [ ] **Chaque membre présente au moins 2 démos** (Ayoub : Hydra + John + SIEM live · Abdallah : SQLmap + ZAP + Gobuster · Titouan : OSINT + Rapport)
- [ ] **Nom de chaque intervenant affiché** quand il parle
- [ ] Les **7 vidéos de démo** se lancent et sont nettes
- [ ] Au moins une démonstration **défensive** (dashboard `/siem`) — exigence « détection & réponse »
- [ ] Le **rapport PDF** est montré
- [ ] Aucun mot de passe / token / clé visible à l'écran
- [ ] Volume audio homogène entre les 3 voix
- [ ] Export `.mp4`, nom au format `PE-2526_<codepromo>_NomPrenom.mp4` (Cadre §VI.2)
