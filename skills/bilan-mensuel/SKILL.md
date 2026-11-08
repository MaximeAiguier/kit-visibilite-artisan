---
name: bilan-mensuel
description: Bilan du mois en 15 minutes qui enchaîne l'analyse des pubs, l'état des avis, les réalisations ajoutées et le test de visibilité IA, et produit un rapport d'une page rapports/AAAA-MM.md. Utiliser quand le gérant dit « faire mon bilan du mois », « on fait le point », « où j'en suis ? », « combien de devis ce mois-ci ? », « le rapport du mois ».
---

# Bilan mensuel (15 minutes maximum côté gérant)

Annonce le déroulé : « 4 petites étapes, environ 15 minutes. On peut s'arrêter à tout moment. »

Mois analysé = **le mois précédent complet** (sauf si le gérant précise).

## Étape 1 — Mettre le journal des devis à jour (3 min)

1. Liste les demandes du mois dans `entreprise/journal-devis.csv`. Demande : « Ai-je oublié des demandes ? » (ajoute-les, avec leur source).
2. Liste les devis « en attente » de plus de 30 jours, tous mois confondus : « Signé, perdu ou toujours en attente ? » (+ montant si signé).

## Étape 2 — Pubs (5 min)

Suis le skill **pubs-analyse** (exports, calculs avec `python3 outils/bilan.py --mois AAAA-MM`, 3 actions maximum). Pas de pubs : saute, et ne garde que les demandes par source.

## Étape 3 — Avis et réalisations (2 min)

1. « Combien d'avis et quelle note voyez-vous sur votre fiche Google aujourd'hui ? »
2. Réalisations ajoutées ce mois : compte les dossiers de `entreprise/realisations/` dont le nom commence par le mois (ou ajoutés ce mois d'après le journal des actions).

## Étape 4 — Test IA (3 min)

Fais faire le test des 3 questions du skill **visibilite-ia** (partie 5). Si le gérant manque de temps, fais-le passer au mois suivant (le noter).

## Rapport

1. Relance `python3 outils/bilan.py --mois AAAA-MM --rapport` en ajoutant les informations des étapes 3 et 4 (options `--avis-nombre`, `--avis-note`, `--test-ia "oui,non,non"`, `--realisations N`) : il écrit `rapports/AAAA-MM.md` à partir de `modeles/rapports/bilan-mensuel.md`, avec les chiffres du mois et du mois précédent.
2. Complète **à la main** dans le rapport généré les deux parties marquées par le programme :
   - « Ce qui a été fait ce mois-ci » : d'après `entreprise/journal-actions.md` (3 à 6 lignes) ;
   - « Les 3 actions du mois prochain » : classées par impact, chacune avec ce qu'on fait, pourquoi, et comment on saura si ça a marché. Elles viennent de l'analyse des pubs, des avis (« demander un avis aux 3 derniers clients »), du site ou de la fiche Google.
3. Le rapport doit tenir sur **une page** (environ 40 lignes). Garde les limites d'attribution écrites par le programme.
4. Lance `python3 outils/verifier_publication.py rapports/AAAA-MM.md` (aucun texte provisoire ne doit rester).
5. Présente le rapport au gérant en 5 lignes dans la conversation (le fichier contient le reste).
6. Journal des actions : « Bilan AAAA-MM fait », avec le relevé d'avis et le test IA.

Si Python n'est pas disponible : remplis toi-même le modèle `modeles/rapports/bilan-mensuel.md` en montrant les calculs.

## Rappel mensuel

Propose une seule fois (puis note la réponse dans le profil) : « Voulez-vous un rappel le 2 de chaque mois ? » — Si ton outil sait créer une tâche planifiée, propose de la créer (avec accord). Sinon, guide le gérant pour créer un rappel récurrent dans l'agenda de son téléphone : « Bilan marketing — ouvrir l'assistant et dire "bilan du mois" ».
