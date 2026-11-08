---
name: pubs-nouveau-canal
description: Prépare un test encadré sur un nouveau canal de pub (Facebook / Instagram, autre) une fois le suivi en place. Utiliser quand le gérant dit « et Facebook ? », « essayer d'autres pubs », « faire de la pub sur Instagram », « tester un autre canal », « mon concurrent fait des pubs Facebook ».
---

# Tester un nouveau canal

## Publications gratuites (TikTok, Instagram, Facebook sans payer)

Si le gérant parle de **publier** sans payer (« montrer mes chantiers sur TikTok »), ce n'est pas un test de pub : pas de budget, pas de conditions. Réponds simplement :

- c'est possible et gratuit, mais cela demande du temps chaque semaine ; les demandes de devis qui en viennent restent rares pour un artisan local ;
- à chaque chantier terminé, le skill site-mise-a-jour prépare déjà un texte et des photos : le gérant peut les publier lui-même sur le réseau de son choix (pour TikTok, une courte vidéo avant / après filmée au téléphone) ;
- ajoute la valeur `autre` (note « TikTok ») au journal des devis quand un client dit venir de là.

Ne crée aucun compte et ne publie rien à sa place. Le reste de ce skill concerne la **pub payante**.

## Conditions avant de commencer

Vérifie dans les fichiers :

1. Le journal des devis est tenu depuis **au moins un mois complet** (`entreprise/journal-devis.csv` contient des demandes sur au moins un mois entier).
2. On connaît le **coût par demande Google** d'au moins un mois (un `rapports/AAAA-MM.md` existe), ou le gérant ne fait pas de pub Google (alors on compare au nombre de demandes habituel).
3. Au moins **3 réalisations avec photos** existent dans `entreprise/realisations/` (indispensables pour Facebook / Instagram).

Si une condition manque : explique laquelle en une phrase, et propose ce qu'il faut faire d'abord (ex. « Notez vos demandes pendant un mois, puis on testera Facebook avec de bons chiffres pour comparer »). N'insiste pas.

## Construire le test (avec le gérant)

1. **Canal** : par défaut Facebook + Instagram (même outil : Gestionnaire de publicités Meta), adapté aux photos avant / après. Autre canal possible si le gérant le demande ; applique la même méthode.
2. **Budget de test** : c'est le gérant qui le choisit. Aide-le avec un repère : « Pour avoir un résultat lisible, il faut viser au moins 3 à 5 demandes. Avec votre coût par demande Google de X €, cela fait environ Y € au total. » Ne jamais dépasser ce qu'il a fixé.
3. **Durée** : 4 semaines par défaut.
4. **Critère d'arrêt** (écrit avant de commencer) : par ex. « si après la moitié du budget il n'y a aucune demande, on arrête ».
5. **Critère de succès** : coût par demande Facebook ≤ coût par demande Google du dernier bilan (ou ≤ un montant fixé par le gérant), en ne comptant que les demandes notées `facebook` / `instagram` dans le journal.
6. **Zone** : uniquement les communes de la zone d'intervention.
7. **Contenu** : 2 visuels à partir des vraies photos de réalisations (avant / après), texte court tiré de la fiche du chantier. Aucune promesse non fournie. Vérifie les textes avec `outils/verifier_publication.py`.

Écris le plan du test dans `entreprise/journal-actions.md` (date de début, budget, durée, critères).

## Instructions de création (le gérant clique, tu ne lances rien)

Guide pas à pas, une étape par message, en demandant une capture si l'écran diffère :

1. Depuis la page Facebook de l'entreprise, ouvrir le « Gestionnaire de publicités » (business.facebook.com ou bouton « Promouvoir »). Si le gérant n'a pas de page professionnelle ou pas les droits d'administrateur : arrêter ici et expliquer comment les obtenir.
2. « + Créer » → objectif « Prospects » (ou « Trafic » vers la page devis du site si le site du kit est en ligne : le formulaire demande déjà la source).
3. Budget : « Budget total » = le montant choisi, dates de début et de fin.
4. Audience : lieux = communes de la zone (ou rayon autour de l'adresse). Ne pas cibler selon l'âge, le genre ou d'autres critères sensibles sans raison ; les règles Meta limitent de toute façon certains ciblages.
5. Publicité : importer les 2 visuels, coller le texte validé.
6. Relire l'aperçu ensemble. **Demander explicitement** : « Vous confirmez le lancement avec un budget total de X € du JJ/MM au JJ/MM ? » Le gérant clique lui-même sur « Publier ».

## Suivi et décision

- À mi-parcours (2 semaines) : le gérant regarde la dépense dans le Gestionnaire et tu comptes les demandes `facebook`/`instagram` du journal. Appliquer le critère d'arrêt si besoin.
- À la fin : compare au critère de succès dans le bilan mensuel. Trois issues possibles, présentées simplement : continuer, ajuster (un seul changement), arrêter.
- Rappelle les limites : petit volume, origine déclarée par le client.
