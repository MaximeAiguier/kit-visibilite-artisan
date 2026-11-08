---
name: pubs-annonces
description: Rédige ou réécrit des annonces Google Ads (annonces de recherche) à partir du profil et des réalisations, avec plusieurs variantes à tester. Utiliser quand le gérant dit « améliore mes annonces », « écris-moi une pub », « mes annonces sont nulles », « change le texte de ma pub », « je veux plus de demandes pour les rénovations de façade ».
---

# Annonces Google

## Limites en vigueur (vérifiées dans l'aide Google Ads « À propos des annonces responsives sur le Réseau de Recherche », novembre 2026)

- Titres : 3 minimum, **15 maximum**, **30 caractères** chacun (espaces compris).
- Descriptions : 2 minimum, **4 maximum**, **90 caractères** chacune.
- Chemins d'URL affichés : 2 champs de **15 caractères** chacun.
- Google mélange titres et descriptions automatiquement : chaque titre doit avoir du sens seul, dans n'importe quel ordre.

Si le gérant signale un message d'erreur de longueur, compte à nouveau et raccourcis.

## Sources autorisées

Uniquement : `entreprise/profil.md` (métiers, zone, chantiers prioritaires, ce qui différencie — sans les éléments marqués « non publié tant que pas de preuve »), `entreprise/realisations/*/fiche.md`, et ce que le gérant dit pendant la session.

Interdit sans preuve fournie : « n°1 », « meilleur », « garantie décennale », labels (RGE, Qualibat…), « devis en 24 h », « intervention rapide », prix, remises, « X ans d'expérience », « Y chantiers réalisés », avis / notes. Si le gérant veut l'un de ces éléments, demande la preuve ou le chiffre exact, note-le dans le profil, puis utilise-le.

Pas de fausse urgence (« offre limitée », « plus que 2 places »).

## Méthode

1. Demande quelle campagne / quel type de chantier est visé (proposer les chantiers prioritaires du profil). Si une annonce existe déjà, demande au gérant de copier-coller ses titres et descriptions actuels (ou une capture).
2. Rédige **15 titres** répartis ainsi : métier + commune principale (3–4), chantier précis (3–4), ce qui différencie selon le gérant (2–3), appel à l'action simple (2–3 : « Demandez votre devis », « Appelez-nous »), nom de l'entreprise (1).
3. Rédige **4 descriptions** : une centrée chantier, une centrée zone, une centrée façon de travailler (selon le gérant), une centrée prise de contact.
4. Propose 2 chemins d'URL (ex. `facade` / `le-mans`).
5. Écris l'annonce dans `entreprise/brouillons/annonce-AAAA-MM-JJ.txt`, une ligne par élément préfixée `T:` (titre), `D:` (description) ou `P:` (chemin), puis lance `python3 outils/verifier_annonce.py` sur ce fichier : il compte les caractères et signale tout dépassement. Corrige jusqu'à « OK ». Affiche ensuite le tout dans un tableau avec le nombre de caractères de chaque ligne.
6. Lance aussi `python3 outils/verifier_publication.py` sur ce fichier. Corrige si besoin.
7. Demande validation. Ensuite seulement, donne les étapes clic par clic pour coller les textes :
   « Campagnes » → « Annonces » → cliquer sur l'annonce existante → « Modifier » (ou « + » → « Annonce responsive sur le Réseau de Recherche ») → coller titre par titre → « Enregistrer ».
8. Conseille de **garder l'ancienne annonce active** à côté pendant un mois pour comparer (si elle existe), sauf si elle contient une promesse fausse.
9. Note dans `entreprise/journal-actions.md` : date, campagne, « nouvelle annonce publiée par le gérant » (seulement après qu'il a confirmé).

## Variantes pour tester

Si le gérant veut tester deux angles (ex. « rapidité de réponse » vs « soin du travail »), crée 2 annonces dans le même groupe, chacune avec un angle dominant. Au bilan suivant, compare le taux de clic et les demandes ; avec peu de volume, attendre 2 mois avant de conclure.
