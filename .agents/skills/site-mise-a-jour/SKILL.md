---
name: site-mise-a-jour
description: Ajoute un chantier terminé au site (photos + texte), prépare les posts fiche Google et Facebook, et modifie les textes du site. Utiliser quand le gérant dit « j'ai fini un chantier », « voici des photos de mon dernier chantier », « ajoute ce chantier au site », « change mon numéro sur le site », « modifier mon site », « enlève cette photo ».
---

# Mise à jour du site

**Quel site ?** Lis la section 5 du profil (« Décision »). Si le gérant **garde son site actuel**, tout ce qui suit reste valable (photos, questions, texte, posts), mais au lieu de modifier `entreprise/site-contenu.json` et de régénérer :
1. Allège les photos (`python3 outils/reduire_photos.py`) et range-les dans `entreprise/realisations/<slug>/`.
2. Donne au gérant le texte final validé (titre, paragraphe, légendes des photos) et dis où le mettre (page « Réalisations » ou équivalent).
3. Il modifie lui-même : guide-le clic par clic d'après l'aide officielle de son outil (WordPress, Wix…), capture d'écran en cas de doute. Un prestataire modifie : prépare `modeles/messages/modifications-site-prestataire.md`. Règle « Site actuel du gérant » d'AGENTS.md.
4. Après la mise en ligne, ouvre la page publique (ou demande une capture) pour vérifier ; note dans le journal des actions.

## A. « J'ai fini un chantier » (10 minutes côté gérant)

1. **Photos** : demande 2 à 6 photos (avant / pendant / après si possible), prises en largeur, sans visage ni plaque d'immatriculation ni numéro de rue lisible. Le gérant les glisse dans la conversation ou dans `entreprise/realisations/`. S'il a des photos de clients reconnaissables ou de l'intérieur d'une maison, demande-lui s'il a l'accord du client.
2. **3 questions**, une à la fois :
   1. Quel type de travaux ? (ex. « ravalement de façade en enduit »)
   2. Dans quelle commune ?
   3. Qu'est-ce qui était difficile ou particulier sur ce chantier ?
   Facultatif, seulement s'il a le temps : mois de fin du chantier ; matériaux.
3. **Toi** :
   - Crée `entreprise/realisations/AAAA-MM-<type>-<commune>/` (minuscules, tirets, sans accents), déplace-y les photos renommées `01.jpg`, `02.jpg`… Lance ensuite `python3 outils/reduire_photos.py entreprise/realisations` : il réduit les photos de plus de 1 Mo à 1600 pixels (originaux gardés dans `originaux/`, qui n'est pas mis en ligne). S'il répond qu'aucun outil d'images n'est disponible, continue : le site reste publiable, juste plus lent sur mobile.
   - Écris `fiche.md` (modèle : `modeles/realisation-fiche.md`) avec les réponses **dans les mots du gérant**, et un texte de 80 à 200 mots pour le site. Pas de nom de client, pas de prix, pas de superlatif non fondé.
   - Rédige le texte alternatif de chaque photo (description factuelle).
   - Ajoute l'entrée dans `realisations` de `entreprise/site-contenu.json` (champs : `slug`, `titre`, `metier` (slug d'un métier existant), `commune`, `date` (AAAA-MM si connu), `texte`, `photos` [{`fichier`, `alt`}], `dossier`).
   - Lance `python3 outils/generer_site.py` et vérifie qu'il n'y a pas d'erreur.
4. **Prépare 2 posts** (après validation du texte de la réalisation) :
   - **Fiche Google** : 2 à 4 phrases + 1 photo + bouton vers la page de la réalisation (voir skill fiche-google, partie 3).
   - **Facebook** : 3 à 5 phrases, ton naturel, 1 à 4 photos (avant / après), commune, invitation à demander un devis avec le lien du site. 0 à 3 mots-dièse utiles au plus (#maçonnerie #<commune>).
   Passe les textes dans `outils/verifier_publication.py`. Montre-les, demande validation.
5. **Republication** : redonne les 3 étapes « Mettre à jour le site en ligne » du skill site-creation (glisser `entreprise/site` dans l'onglet « Deploys » de Netlify). Le gérant publie aussi les posts lui-même.
6. Propose, si le client était content : le message de demande d'avis (skill avis-clients).
7. Journal des actions : réalisation ajoutée + ce qui a été publié (après confirmation).

Si c'est la 3e réalisation et que le site n'était pas encore en ligne : dis-le, c'est le moment de la première mise en ligne.

## B. Modifier un texte ou une information

1. Demande ce qu'il faut changer, en une phrase.
2. Si c'est le **nom, l'adresse, le téléphone ou les horaires** : change-les aussi dans `entreprise/profil.md`, et rappelle de les changer **à l'identique** sur la fiche Google et Facebook (liste du skill visibilite-ia).
3. Modifie `entreprise/site-contenu.json`, régénère, montre la différence en mots simples (« Avant : … / Après : … »), demande validation, puis étapes de republication.
4. Retirer une photo ou une réalisation : supprime l'entrée dans le JSON (les fichiers photo peuvent rester dans le dossier du chantier), régénère.

Pour une demande de modification de mise en page plus large (couleurs, ordre des sections) : modifie `couleur` dans le JSON ; pour le reste, modifie les gabarits de `modeles/site/` avec prudence, régénère et vérifie l'affichage mobile.
