VIDÉOS DE DÉMO — ToolboxV8
==========================

Place tes vidéos de démonstration dans CE dossier, avec EXACTEMENT ces noms :

  Slide 11  →  demo-osint.mp4      (Reconnaissance passive / OSINT)
  Slide 12  →  demo-sqlmap.mp4     (SQLmap — injection SQL)
  Slide 13  →  demo-hydra.mp4      (Hydra — brute-force SSH)
  Slide 14  →  demo-john.mp4       (John the Ripper — cassage de hash)
  Slide 15  →  demo-zap.mp4        (OWASP ZAP — scan web)
  Slide 16  →  demo-gobuster.mp4   (Gobuster — pages cachées)
  Slide 19  →  demo-rapport.mp4    (Génération du rapport PDF)


COMMENT ACTIVER UNE VIDÉO
-------------------------
1. Dépose le fichier .mp4 ici, avec le bon nom (voir liste ci-dessus).
2. Ouvre ../index.html dans un éditeur.
3. Sur la slide concernée, trouve le bloc <div class="video-slot"> et :
     - DÉCOMMENTE la ligne <video ...> (retire les <!--  et  -->)
     - SUPPRIME (ou laisse) le bloc <div class="vs-ph">…</div> qui est le placeholder.

   Exemple AVANT :
     <!-- <video controls preload="metadata" src="videos/demo-osint.mp4"></video> -->
     <div class="vs-ph"> … </div>

   Exemple APRÈS :
     <video controls preload="metadata" src="videos/demo-osint.mp4"></video>

   (Si tu laisses le placeholder, il sera simplement masqué par la vidéo.)


FORMAT CONSEILLÉ
----------------
- Conteneur : .mp4 (codec H.264 + audio AAC) — lu par tous les navigateurs.
- Résolution : 1280×720 ou 1920×1080 (la zone est en 16:9).
- Durée : 30 à 60 s par démo idéalement.
- Astuce : ajoute   poster="videos/demo-osint.jpg"   sur la balise <video>
  pour afficher une image d'aperçu avant lecture.

Dis-moi si tu préfères que je décommente directement les balises <video>
une fois tes fichiers déposés — je peux le faire en une passe.
