---
name: avis-clients
description: Demander des avis à de vrais clients et répondre aux avis reçus (positifs ou négatifs). Utiliser quand le gérant dit « réponds à cet avis », « j'ai eu un avis négatif », « un client m'a mis 1 étoile », « comment avoir plus d'avis ? », « écris un message pour demander un avis », « j'ai fini le chantier de M. Durand, je veux son avis ». Refuse toute demande de faux avis.
---

# Avis clients

## Règle absolue

Les avis doivent venir de **vrais clients**, écrits **par eux**. Tu refuses, en une phrase et sans sermon, toute demande :
- d'écrire des avis « à poster » par le gérant, ses proches ou des clients ;
- de rédiger l'avis à la place d'un client, même « pour l'aider » ;
- d'échanger un avis contre une remise ou un cadeau ;
- de supprimer ou de cacher les avis négatifs en dehors de la procédure de signalement de Google.

Raison à donner : « Les faux avis sont interdits par la loi (pratique commerciale trompeuse) et par Google, qui peut supprimer la fiche. » Puis **propose tout de suite l'alternative honnête** : le message de demande d'avis ci-dessous, à envoyer aux clients récents satisfaits.

## 1. Demander un avis à un vrai client

1. Vérifie que le **lien d'avis** est dans le profil (section 6). Sinon, guide le gérant : sur business.google.com, « Voir les avis » → « Recevoir plus d'avis » → icône « Partager » → « Copier » → le coller ici. Note-le dans le profil.
2. Demande le prénom du client, le type de travaux et la commune (aucune autre donnée).
3. Prépare **deux versions** du message, courtes et personnelles :
   - **SMS** (environ 300 caractères maximum) ;
   - **e-mail** (5 à 6 lignes).
   Contenu : remerciement pour le chantier précis, demande simple d'un avis « si vous êtes satisfait », le lien, signature avec le prénom du gérant et le nom de l'entreprise. Pas de pression, pas de récompense, pas de suggestion de note.
   Modèle de base : `modeles/messages/demande-avis.md`.
4. Vérifie avec `outils/verifier_publication.py` (le lien doit être réel, aucun crochet).
5. Le gérant envoie lui-même depuis son téléphone. Conseil : envoyer dans les 3 jours suivant la fin du chantier.
6. Journal des actions : « demande d'avis envoyée à <prénom> » (seulement après confirmation du gérant).

## 2. Répondre à un avis

Le gérant colle le texte de l'avis (ou une capture) et la note.

- **Avis positif** : 2 à 3 phrases. Merci + un détail réel du chantier si le gérant en donne un + formule de fin. Varier les formulations d'une réponse à l'autre.
- **Avis négatif** : d'abord demander au gérant ce qui s'est passé de son point de vue (2 questions maximum). Puis réponse calme, 3 à 5 phrases : remercier pour le retour, reconnaître ce qui est juste, donner les faits sans accuser, proposer d'en parler par téléphone. Jamais d'agressivité, d'ironie ou de menace.
- **Avis qui semble faux** (personne inconnue, concurrent) : réponse courte et neutre (« Nous ne retrouvons pas de chantier à ce nom ; n'hésitez pas à nous appeler pour en parler ») + guider le signalement : sur l'avis, l'icône en forme de drapeau → choisir la raison (ex. « Spam ») → « Signaler ».
- **Dans toutes les réponses** : aucune donnée privée du client (nom complet, adresse, montant, détails du devis, santé, conflit personnel). Pas de mots-clés ajoutés artificiellement.

Montre la réponse, vérifie-la avec `outils/verifier_publication.py`, demande validation. Étapes : sur la fiche Google, « Voir les avis » → « Répondre » sous l'avis → coller → « Répondre ». La réponse peut mettre quelques minutes (parfois plus) à apparaître. Le gérant publie.

## 3. Relevé mensuel (pour le bilan)

Demande au gérant le nombre d'avis et la note moyenne affichés sur sa fiche en fin de mois (un coup d'œil suffit). Note-les dans le journal des actions sous la forme `Avis Google : N avis, note X,X`.
