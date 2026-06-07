# Script vidéo soutenance — ToolboxV8 (20 minutes)

> Format : 3 voix (Voix 1, Voix 2, Voix 3) — assigner librement à Ayoub, Abdallah, Titouan
> Démos : LIVE (partage d'écran réel) — la stack doit tourner pendant l'enregistrement (`./scripts/start.ps1` lancé à l'avance)
> Ton : technique + business (gain client + impl. technique)
> Total : ~20 min, ~6 min 40 par voix
>
> **Avant l'enregistrement** :
> 1. Lancer `./scripts/start.ps1` (10 min de buffer pour que tout démarre)
> 2. Ouvrir `https://localhost/login` et se connecter avec admin/admin
> 3. Avoir ces onglets prêts : Dashboard, Modules, Rapports, SIEM
> 4. Vérifier que `pentest_target` et `pentest_zap` tournent (`docker ps`)
> 5. Tester rapidement que SQLmap, Hydra, ZAP répondent (pour ne pas se faire avoir en live)

---

## PARTIE 1 — INTRODUCTION & CONTEXTE (Voix 1, ~6 min 40)

### Slide 1 — Page de garde (~20 sec)

**Voix 1** :
> Bonjour à tous. Aujourd'hui nous vous présentons **ToolboxV8**, notre projet d'études de fin de Mastère Cybersécurité, promotion 2025-2026. C'est une plateforme web qui automatise les étapes d'un test d'intrusion. Avec moi, [Nom Voix 2] et [Nom Voix 3].

### Slide 2 — Équipe (~30 sec)

**Voix 1** :
> Notre équipe se répartit les responsabilités sur trois axes : l'architecture back-end et la sécurisation de l'outil, l'intégration des outils offensifs et la qualité des tests, et enfin l'interface utilisateur et le reporting. Chacun a son périmètre principal mais on a tous mis les mains dans tous les modules — c'est essentiel pour la cohérence du produit final.

### Slide 3 — Le contexte client (~50 sec)

**Voix 1** :
> Notre client est une société spécialisée en cybersécurité offensive. Concrètement, elle réalise des tests d'intrusion pour des entreprises privées et des institutions publiques. Aujourd'hui, son problème est **double** : ses pentests reposent sur des manipulations manuelles, donc ils sont **longs** — souvent plusieurs heures pour un audit basique. Et surtout, le résultat est **hétérogène selon l'intervenant** : deux analystes lancent le même outil mais ne sortent pas le même rapport. Le client perd du temps et de la crédibilité face à ses propres clients.

### Slide 4 — Le problème à résoudre (~50 sec)

**Voix 1** :
> Nous avons identifié 5 douleurs concrètes : le temps perdu en commandes répétitives, l'absence de standardisation entre analystes, des rapports parfois illisibles écrits à la main dans Word, l'impossibilité pour un analyste junior de lancer un pentest sans connaître par cœur 30 outils CLI, et enfin pas de traçabilité claire des actions menées. Notre objectif : transformer ces 5 douleurs en 5 réponses concrètes dans une seule plateforme web.

### Slide 5 — Objectifs du cahier des charges (~50 sec)

**Voix 1** :
> Le cahier des charges fixe 5 objectifs mesurables. Le plus important : **réduire d'au moins 40 pour cent le temps de réalisation d'un pentest**. Les autres : standardiser les pratiques, proposer une interface utilisable par un analyste pas développeur, fournir des rapports lisibles et exploitables, et permettre une intégration simple dans l'écosystème technique du client. Comme vous le verrez, on a non seulement atteint ces objectifs, mais on les a **largement dépassés** sur le temps — on parle de 75% de gain sur recon plus scan, et presque 100% sur la rédaction de rapport.

### Slide 6 — Périmètre fonctionnel (~50 sec)

**Voix 1** :
> ToolboxV8 couvre les 5 grandes phases d'un test d'intrusion. D'abord la **reconnaissance passive**, donc l'OSINT, on cherche tout ce qu'on peut trouver sans toucher à la cible. Ensuite la **reconnaissance active** : Nmap, DNS, fingerprinting. Puis le **scan de vulnérabilités** avec Nikto et SSLyze. L'**exploitation** avec SQLmap, Hydra, et John the Ripper. Et enfin l'**analyse web** avec OWASP ZAP et Gobuster. On a aussi un volet **défensif** : un SIEM ELK, des règles Snort, et un module de réponse active iptables.

### Slide 7 — Organisation & méthodologie (~50 sec)

**Voix 1** :
> Nous avons travaillé en méthodologie Agile, sprints de deux semaines. Au total **10 sprints** depuis le kick-off. Backlog géré dans Notion, versioning Git avec une branche main stable et des branches feat slash par fonctionnalité, revue de code obligatoire avant merge. Chaque sprint avait un livrable concret : le sprint 1 c'était l'auth, le sprint 5 c'était le passage en cookie HttpOnly, le sprint 8 c'était le module OSINT, le sprint 9 c'était HTTPS et la CI/CD. Je laisse maintenant [Voix 2] vous présenter l'architecture technique et nos premières démos.

---

## PARTIE 2 — ARCHITECTURE & DÉMOS OFFENSIVES (Voix 2, ~7 min)

### Slide 8 — Architecture globale (~1 min)

**Voix 2** :
> Merci [Voix 1]. Côté technique, ToolboxV8 est une stack 100% dockerisée. À l'extérieur : un reverse proxy **Caddy** qui termine le HTTPS — j'y reviens dans une seconde. Derrière, on a séparé volontairement l'API et le front en **deux services FastAPI distincts**. Pourquoi ? Pour deux raisons. Premièrement, sécurité : le cookie de session HttpOnly est posé par le service web seul, pas exposé à l'API. Deuxièmement, intégration : l'API reste accessible aux clients externes — un script offsec ou la CI peut faire un POST sur /api/auth/token sans passer par le formulaire HTML. Derrière, un worker Celery sur image **Kali Linux Rolling** exécute les scans avec tous les outils préinstallés. Côté infra : PostgreSQL, Redis, MinIO pour les rapports, ELK pour le SIEM.

### Slide 9 — Stack technique (~50 sec)

**Voix 2** :
> Côté backend, Python 3.11, FastAPI, SQLAlchemy, Celery. Front : Jinja2 et vanilla JavaScript — pas de framework lourd, ça reste léger et maintenable. Base de données PostgreSQL 16, file de tâches Redis 7, stockage objet MinIO. Le worker tourne sur Kali Rolling officiel — Nmap, Nikto, SQLmap, Hydra, John jumbo qui supporte 304 formats de hash, SSLyze, Metasploit. Pour le HTTPS on a choisi **Caddy** plutôt que Nginx — 3 lignes de config, certificat auto-signé généré automatiquement via sa CA interne, et basculement vers Let's Encrypt en une seule ligne pour la production. Pour la CI/CD on a mis en place **GitHub Actions ET GitLab CI** en parallèle — le repo est sur GitHub mais on respecte la lettre du cahier qui demande GitLab.

### Slide 10 — Les 5 modules offensifs (~40 sec)

**Voix 2** :
> Maintenant la partie qui fait le sel du produit : les 5 modules. Le principe est simple — chaque outil expose des **profils par boutons** : Quick, Standard, Full, Aggressive. L'analyste n'a plus à taper de commande, il choisit son intensité d'un clic. Et on a des **toggles indépendants** : dans le module Scan par exemple, je peux activer juste Nikto sans lancer SSLyze. Les outils désactivés n'apparaissent pas dans le rapport. Passons à la démo.

### Slide 11 — DÉMO 1 : Reconnaissance passive OSINT (~1 min 30)

**Voix 2** : *[bascule sur l'écran, ouvre https://localhost/modules]*
> Premier module : **Reconnaissance passive**. Imaginez que je suis un pentester et que le client me demande de vérifier ce qu'on peut trouver publiquement sur sa marque. Je tape simplement "etudiant" — pas besoin de domaine, on accepte le champ libre. Je choisis le moteur Google. Je coche les catégories "Mot-clé" et "Réseaux sociaux" — vous voyez, on a préparé 18 dorks Google : recherche LinkedIn, GitHub, recherche de leaks, de CV, de credentials. Je clique sur Lancer.
>
> *[lance le scan, attend 2-3 sec, montre le résultat]*
>
> Et voilà — la toolbox ouvre automatiquement les onglets Google pour chaque dork sélectionné. Le rapport PDF généré liste les requêtes utilisées. C'est la phase passive — **zéro paquet envoyé à la cible**, conformité RGPD garantie.

### Slide 12 — DÉMO 2 : SQLmap (détection SQLi) (~1 min 30)

**Voix 2** : *[bascule sur module Exploitation]*
> Maintenant on passe à l'**exploitation**. Cible légalement autorisée : `testasp.vulnweb.com`, c'est un site volontairement vulnérable proposé par Acunetix. URL avec un paramètre injectable. Outil : SQLmap. Profil Quick.
>
> *[lance le scan, indique pendant que ça tourne]*
>
> Pendant que SQLmap teste, un mot sur la sécurité de l'outil lui-même : tous les scans sont **tracés dans une table audit_logs** PostgreSQL. Si demain le client a un audit, on peut produire la liste exhaustive de tous les scans, qui les a lancés, et sur quelle cible. C'est essentiel pour la conformité.
>
> *[au résultat]*
>
> Et voilà : **3 types d'injection détectés** — boolean-based blind, time-based, stacked queries. SGBD identifié comme Microsoft SQL Server 2014. Stack web : IIS 8.5, ASP.NET, Django. Tout est dans le rapport PDF en un clic.

### Slide 13 — DÉMO 3 : Hydra (brute-force SSH) (~1 min 15)

**Voix 2** : *[reste dans module Exploitation]*
> Démo suivante : **Hydra**, brute-force credentials. Pour respecter la légalité, on a déployé un **conteneur cible interne** dans notre stack — un serveur SSH volontairement faible. Cible : `target` sur le port 2222. Service ssh. Liste d'utilisateurs : juste "pentest_user". Liste de mots de passe : cinq mots dont le bon.
>
> *[lance, attend 2 secondes]*
>
> **Cracké en 1 seconde**. Le rapport vous montre : login pentest_user, password toor. Imaginez la même opération sur une cible réelle avec un mot de passe faible et la wordlist rockyou.txt — 14 millions d'entrées — le compte tombe en quelques minutes. C'est exactement le risque qu'on aide nos clients à mesurer.

### Slide 14 — DÉMO 4 : John the Ripper (cassage de hash) (~50 sec)

**Voix 2** :
> Dernier outil offensif de cette partie : **John the Ripper**. Cas d'usage : imaginez qu'on a récupéré un hash après une compromission. Je colle un hash MD5 — c'est le hash du mot "admin". Format raw-md5. Wordlist : cinq mots dont admin.
>
> *[lance, instantané]*
>
> **0 seconde**. John identifie "admin" comme étant le mot de passe original. Notre version supporte 304 formats : bcrypt, sha512crypt, NTLM Windows, KeePass, ZIP... Je passe la parole à [Voix 3] pour la partie web et l'aspect défensif.

---

## PARTIE 3 — WEB SCAN, DÉFENSIF, REPORTING & CONCLUSION (Voix 3, ~6 min 20)

### Slide 15 — DÉMO 5 : ZAP Active Scan (~1 min 30)

**Voix 3** : *[partage l'écran, va sur module Web/API]*
> Merci [Voix 2]. Cinquième et dernier module offensif : **OWASP ZAP**. C'est notre scanner web. On a intégré le démon ZAP directement dans notre stack Docker — pas besoin de l'installer à part. Cible : toujours `testasp.vulnweb.com`. Type Active scan, profil Quick.
>
> *[lance, indique pendant que ça tourne ~1 min]*
>
> Le module fait quelque chose de subtil : il **lance le scan ZAP**, puis **polle l'API toutes les 5 secondes** jusqu'à ce que ZAP termine, puis **récupère automatiquement les alertes**. C'était l'une des évolutions du sprint 10 — avant, le module rendait juste la main au bout de 2 secondes sans attendre les résultats.
>
> *[au résultat]*
>
> Et voilà le résultat : **105 alertes**, **14 types uniques**. Triés par sévérité : en Medium on a l'absence de Content Security Policy, le manque de header anti-clickjacking, l'absence d'anti-CSRF. En Low : les fuites de versions serveur et X-Powered-By. C'est directement actionable pour l'équipe sécurité du client.

### Slide 16 — DÉMO 6 : Gobuster (chemins cachés) (~45 sec)

**Voix 3** :
> Toujours dans web scan : **Gobuster**, bruteforce de chemins HTTP. Même cible, profil Quick.
>
> *[lance, ~30 sec]*
>
> Trouvé : un dossier `_vti_pvt` qui est une vieille interface FrontPage Microsoft — c'est un indicateur de configuration legacy à patcher. Aussi `/cgi-bin`, `/templates`, `/aspnet_client`. Tous les chemins découverts apparaissent dans le rapport avec leur code HTTP. Voilà nos 5 modules offensifs validés en live.

### Slide 17 — Sécurité de la toolbox elle-même (~50 sec)

**Voix 3** :
> Important : **la toolbox elle-même est sécurisée**. JWT signé en HS256, cookie HttpOnly avec SameSite Lax — protégé contre les XSS. RBAC à 3 rôles : admin, analyst, reader. Les mots de passe sont stockés en bcrypt — jamais en clair. Les secrets sont chiffrés en Fernet. Et comme dit tout à l'heure : audit logs sur toutes les actions sensibles. On a documenté tout ça dans une **section 7.7 Politiques de sécurité** du rapport, qui couvre 7 sous-sections : mots de passe, authentification, autorisation, journalisation, secrets, éthique, mise à jour.

### Slide 18 — Module défensif & pipeline de réponse (~50 sec)

**Voix 3** : *[ouvre la page /siem]*
> Côté défensif : on a un **SIEM ELK complet** qui indexe en temps réel tous les scans et tous les événements. Voici notre dashboard `/siem` : nombre d'alertes par jour, top IPs sources, événements récents. Sous le capot : Elasticsearch 8.13, Logstash, Kibana. On a aussi écrit **9 règles Snort personnalisées** — détection scan Nmap SYN, brute-force SSH, SQLi, XSS, Log4Shell. Et un module Response qui peut **bloquer une IP via iptables** à la volée. Une honnêteté : le conteneur Snort lui-même n'est pas dans le compose actuel — c'est documenté dans nos limites parce que le mode IDS exige `cap_add NET_ADMIN` compliqué sous Docker Desktop Windows.

### Slide 19 — DÉMO 7 : Le rapport PDF (~1 min)

**Voix 3** : *[ouvre Rapports et clique sur Générer pour un job récent]*
> Tous les scans que [Voix 2] et moi avons lancés produisent automatiquement un **rapport PDF structuré**. Le voici : page de couverture, synthèse exécutive en encart orange — pour le CODIR du client — statistiques, déroulé technique par outil avec la commande exécutée et la sortie console brute, tableau synthétique, recommandations, annexes. On a soigné la **palette graphique** — couleurs slate douces, blocs de code avec bordure subtile, garantie de lisibilité y compris sur les pages d'overflow où ReportLab a tendance à perdre les couleurs de fond. Tout ça en 2 secondes de génération.

### Slide 20 — KPIs atteints (~45 sec)

**Voix 3** :
> Bilan chiffré : sur **recon + scan**, on est passé de **15-20 minutes manuelles à 3-5 minutes** en profil Quick — **75% de gain**. Sur la rédaction de rapport, **de 1-2 heures à 2 secondes** — **99% de gain**. Sur le brute-force SSH : **de la config manuelle à 1 clic**. L'objectif des 40% du cahier des charges est largement dépassé. Côté qualité : **100% des CVE testables sur notre environnement de démo remontent dans le rapport**. Côté stabilité : 50 scans enchaînés sans crash.

### Slide 21 — Limites assumées (~45 sec)

**Voix 3** :
> Restons honnêtes. On a documenté nos limites en section 10.2 du rapport. Trois limites principales : **Metasploit** est codé et invocable, mais nécessite un démarrage manuel du démon msfrpcd — pas industrialisé. **Snort** : les règles sont écrites, le pipeline Logstash est prêt, mais le conteneur n'est pas dans le compose pour les raisons techniques évoquées. Et le **dump SQL massif** sur cible distante reste bridé volontairement à 5 lignes par table — c'est une contrainte intrinsèque de l'injection blind, pas un bug de notre code. Tout est documenté, tout est défendable.

### Slide 22 — Perspectives d'évolution (~30 sec)

**Voix 3** :
> Pour la suite : sidecar msfrpcd préconfiguré, déploiement Snort sur hôte Linux dédié, endpoint REST pour automatiser la chaîne SOAR détection → blocage iptables, intégration SecLists pour des wordlists plus complètes, et à plus long terme un module IA/ML pour la classification automatique de criticité des vulnérabilités trouvées.

### Slide 23 — Récap & impact (~30 sec)

**Voix 3** :
> En résumé : 5 modules offensifs + 4 modules défensifs, 12 outils intégrés, 10 sprints, une CI/CD à chaque push, HTTPS en standard, et un produit qui démontre concrètement les **75% de gain de temps** promis au client. Le projet est entièrement sur GitHub, publié, documenté, démontrable à tout moment.

### Slide 24 — Conclusion et remerciements (~20 sec)

**Voix 3** :
> Merci à notre tuteur de Mastère et à l'équipe pédagogique pour l'accompagnement sur ces 6 mois. Le code, la documentation, le rapport technique et le guide pratique sont disponibles sur notre GitHub. Nous sommes à votre disposition pour vos questions. Merci pour votre attention.

---

## INDICATIONS TECHNIQUES POUR L'ENREGISTREMENT

- **Logiciel** : OBS Studio (gratuit) — Screen Capture + Audio Input Capture sur chaque micro
- **Résolution** : 1920×1080, 30 fps, débit ~6 Mbps
- **Affichage du nom** : ajouter en post-prod un bandeau bas avec le nom de l'intervenant qui parle (cf. exigence cadre §VI.2)
- **Pré-prod** : faire un test technique de 5 min la veille pour vérifier le son, la latence, la stabilité de Docker
- **Découpage suggéré** : enregistrer en 3 blocs (un par voix) puis monter — plus simple que de tout faire en une prise
- **Sauvegarde** : enregistrer aussi en local sur chaque PC qui parle au cas où

## CONTRÔLE QUALITÉ AVANT EXPORT

- [ ] Durée 18-20 min exactement
- [ ] Les 3 voix parlent toutes
- [ ] Le nom de chaque intervenant est affiché à l'écran quand il parle
- [ ] Les 5 démos sont visibles et fonctionnent
- [ ] Au moins une démo défensive (dashboard /siem)
- [ ] Le rapport PDF est montré au moins une fois
- [ ] Pas de mot de passe / token / clé API visible à l'écran (cachez le .env si on le voit)
- [ ] Audio cohérent en volume entre les 3 voix
- [ ] Export `.mp4`, nom du fichier au format `PE-2526_<codepromo>_NomPrenom.mp4` (cf. cadre §VI.2)
