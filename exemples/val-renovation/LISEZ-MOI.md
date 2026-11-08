# Cas de test — Val Rénovation (entreprise fictive)

**Dossier de test uniquement. Toutes les données sont fictives** : entreprise, prénom, adresse, communes, téléphone (numéro réservé à la fiction), e-mail (domaine réservé `.invalid`), site (`.example`), chiffres. Le cas s'inspire d'un premier testeur réel, anonymisé avant publication.

Dans `entreprise/profil.md`, « RÉEL » marque ce qui, dans le cas d'origine, venait du site public ou d'un appel (métiers, site WordPress fait par un prestataire, pubs Google sans suivi, page Facebook) ; « SIMULATION » marque les réponses inventées pour tester le kit de bout en bout (zone, priorités, journal des devis, exports Google Ads).

Le fichier `entreprise/site-contenu.json` porte `"_simulation": true` : le générateur refuse toujours d'en faire un site publiable.

Ce que contient le test :
- `entreprise/profil.md` : profil après un onboarding simulé.
- `entreprise/site-contenu.json` → `entreprise/site-apercu/` : site généré en mode aperçu (blocages attendus : mentions légales incomplètes, 0 réalisation sur 3, données simulées).
- `entreprise/journal-devis.csv` + `entreprise/exports/2026-09-*.csv`, `2026-10-*.csv` : données d'exemple pour le bilan.
- `rapports/2026-10.md` : bilan mensuel produit par le kit.
- `entreprise/brouillons/` : exemples de textes produits (annonce, demande d'avis, message au prestataire).
