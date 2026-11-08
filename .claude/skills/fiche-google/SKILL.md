---
name: fiche-google
description: Audit guidé et textes de la fiche d'établissement Google (Google Maps), et publications à partir des réalisations. Utiliser quand le gérant dit « ma fiche Google », « je suis mal placé sur Google Maps », « change mes horaires sur Google », « écris la description de ma fiche », « publier sur ma fiche Google », « je n'ai pas de fiche Google ».
---

# Fiche Google (fiche d'établissement)

La fiche Google est ce qui apparaît sur Google Maps et à droite des résultats quand on cherche l'entreprise. Pour un artisan, c'est souvent la première source de demandes gratuites.

Tu ne te connectes jamais à la fiche : le gérant fait les modifications sur son téléphone ou son ordinateur, guidé par toi.

## 0. Accès

- Le gérant ouvre business.google.com, connecté au compte Google qui gère sa fiche (ou cherche le nom de son entreprise sur Google : s'il voit le bouton « Éditer la fiche », il a la main ; sur l'application Google Maps : « Établissement » → « Modifier le profil »).
- S'il ne l'a pas : la fiche a peut-être été créée par un prestataire. Deux voies, au choix du gérant :
  1. lui envoyer le message `modeles/messages/demande-acces-fiche-google.md` (aucun crochet restant, passé dans `outils/verifier_publication.py`), qu'il envoie lui-même ;
  2. la demande officielle : business.google.com/add → chercher l'entreprise → « Demander l'accès » → remplir le formulaire → « Envoyer ». Le propriétaire actuel a 3 jours pour répondre ; sans réponse, le gérant peut parfois valider lui-même depuis l'e-mail reçu (« Voir la demande »).
- Si la fiche n'existe pas : guide la création sur business.google.com/add. À la fin, « Valider » : Google choisit les méthodes proposées (téléphone ou SMS, e-mail, appel vidéo, vidéo enregistrée, carte postale avec un code sous 14 jours environ).
- Note l'état dans la section 6 du profil.

## 1. Audit en 10 points (le gérant regarde, répond « oui / non / je ne sais pas », ou envoie des captures)

1. **Nom** : exactement le nom commercial du profil (pas de mots-clés ou de ville ajoutés : c'est interdit par Google et peut faire suspendre la fiche).
2. **Catégorie principale** : celle qui correspond le mieux au métier principal (ex. « Maçon », « Plombier », « Paysagiste »).
3. **Catégories secondaires** : les autres métiers réels du profil, sans en rajouter.
4. **Adresse / zone desservie** : si le gérant ne reçoit pas de clients à son adresse, Google exige que l'adresse soit masquée (crayon à côté de « Adresse de l'établissement » → désactiver « Montrer l'adresse de l'établissement aux utilisateurs ») et seule la zone desservie affichée. Zone = communes du profil.
5. **Téléphone** : identique au profil, au site et aux réseaux (même format).
6. **Site web** : l'adresse du site (page d'accueil).
7. **Horaires** : ceux du profil.
8. **Description** : présente, factuelle, sans lien ni promesse.
9. **Services** : liste des prestations réelles avec une courte description.
10. **Photos** : au moins quelques photos de chantiers récents, logo ou photo de l'équipe / du véhicule si le gérant le souhaite.

Si une information change (horaires, téléphone…), applique la règle « Même information partout » de `AGENTS.md` : profil, site et fiche Google ensemble.

Résume en « ✅ bon / ⚠️ à corriger » et propose au maximum 3 corrections par session, la plus importante d'abord.

## 2. Rédiger les textes

- **Description** (750 caractères maximum, vérifie la limite dans l'interface si le gérant voit autre chose) : qui, quels métiers, quelle zone, quels types de chantiers, comment contacter. Uniquement des faits du profil. Pas d'URL, pas de prix ni de promotion.
- **Services** : un texte de 1 à 2 phrases par service (300 caractères maximum chacun).
- Fais vérifier par `outils/verifier_publication.py`, montre le texte, demande validation, puis donne les étapes :
  « Éditer la fiche » → « Description de l'établissement » → coller → « Enregistrer ». Pour les services : « Éditer services » → « Ajouter un service personnalisé » → coller → « Enregistrer ».
- Rappel : une modification peut être vérifiée par Google avant d'apparaître (quelques heures à quelques jours).

## 3. Publications (« posts ») à partir des réalisations

Quand une réalisation est ajoutée (skill site-mise-a-jour) ou sur demande :

- Texte de 2 à 4 phrases : quel travail, quelle commune, ce qui était particulier (d'après la fiche du chantier). Un appel simple : « Un projet similaire ? Appelez-nous », et si possible un bouton vers la page de la réalisation.
- 1 photo (la plus parlante, idéalement « après »).
- Jamais de nom du client, ni d'adresse précise, sans son accord écrit.
- Étapes : sur la fiche, « Posts » → « Ajouter un post » → type « Actualité » → photo → texte → bouton d'action facultatif (choisir le plus proche de « Appeler » ou « En savoir plus » avec le lien de la page) → « Publier ». Le gérant publie lui-même après validation.

## 4. Cohérence

Le nom, l'adresse et le téléphone doivent être **identiques partout** (fiche, site, Facebook, annuaires). Si le skill visibilite-ia a établi une liste de contrôle, utilise-la.

## 5. Fin

Ligne dans `entreprise/journal-actions.md` (corrections faites par le gérant, textes publiés, ce qui reste).
