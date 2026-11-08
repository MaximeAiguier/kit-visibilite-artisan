---
name: pubs-analyse
description: Analyse mensuelle des pubs Google à partir de l'export Google Ads et du journal des devis. Utiliser quand le gérant demande « mes pubs marchent ? », « combien me coûte un devis ? », « analyse mes pubs », « j'ai exporté le rapport Google Ads », « je dépense trop en pub ? », « est-ce que je dois arrêter Google Ads ? ».
---

# Analyse des pubs (mensuelle, 10 minutes côté gérant)

## 1. Récupérer les exports (le gérant, sur ordinateur)

Demande les fichiers du **mois précédent complet**. Une étape par message :

1. Ouvrez ads.google.com.
2. En haut à droite, cliquez sur les dates et choisissez **« Le mois dernier »** (pas « 30 derniers jours »). Cliquez sur « Appliquer ».
3. Menu de gauche : « Campagnes » → « Campagnes ». En haut à droite du tableau, cliquez sur l'icône « Télécharger » (flèche vers le bas) → « .csv » (choisissez « .csv » simple plutôt que « Excel .csv » si les deux existent).
4. Menu de gauche : « Campagnes » → « Insights et rapports » → « Termes de recherche » (ce que les gens ont réellement tapé). Même icône « Télécharger » → « .csv ».
5. Facultatif si le gérant a 5 minutes de plus : « Campagnes » → « Insights et rapports » → « Date et emplacement de diffusion de vos annonces » → onglet « Zones géographiques correspondantes » (communes où les pubs ont été vues) ; puis, au même endroit, la vue par jour et heure (« Heure et jour »). Téléchargez en .csv.
6. Glissez les fichiers téléchargés dans le dossier `entreprise/exports/` (ou dites-moi où ils sont).

Si le gérant ne trouve pas un menu : demande une capture d'écran. Les noms changent régulièrement.

Toi : renomme les fichiers en `AAAA-MM-campagnes`, `AAAA-MM-termes`, `AAAA-MM-lieux`, `AAAA-MM-horaires` en gardant leur extension (`.csv`, `.xlsx` ou `.tsv` : les trois sont lus), sans modifier leur contenu. Le nom sert au programme à savoir de quel rapport il s'agit.

Pas d'accès à Google Ads ? Fais quand même l'analyse avec le journal seul et la dépense déclarée par le gérant (relevé bancaire / facture Google), en le signalant.

## 2. Calculer

Lance : `python3 outils/bilan.py --mois AAAA-MM`

Le programme lit les exports et `entreprise/journal-devis.csv`, et sort (format texte et `rapports/donnees-AAAA-MM.json`) :

- **Dépense** du mois (somme de la colonne Coût de l'export campagnes).
- **Demandes comptées par Google** (colonne Conversions).
- **Demandes venant des pubs selon le journal** : lignes du mois avec source `google-annonce`.
- **Coût par demande (pubs)** = dépense ÷ demandes `google-annonce` du journal. Donne aussi dépense ÷ conversions Google, à titre de comparaison.
- **Devis signés venant des pubs** et **chiffre d'affaires signé attribué** (somme des montants des lignes `google-annonce` au statut `signé`, quelle que soit la date de signature, pour les demandes du mois).
- Toutes les demandes du mois par source.
- Termes de recherche qui coûtent sans aucune demande ; communes hors zone ; jours/heures (si exports fournis).

Si Python n'est pas disponible : fais les mêmes calculs toi-même, en montrant le détail.

Vérifie les chiffres : additionne à la main 2 ou 3 valeurs pour t'assurer que le programme a bien lu l'export (séparateur, virgule décimale, ligne « Total »).

Si le programme affiche « ATTENTION … pas le mois entier : fichier écarté », la période de l'export est fausse : redonne l'étape 2 au gérant et fais refaire l'export. Ne calcule jamais un coût par demande avec un export qui ne couvre pas le mois.

## 3. Repérer ce qui ne va pas

À partir des chiffres et du profil (zone, chantiers prioritaires / à éviter) :

- **Termes de recherche qui dépensent sans demande** : surtout ceux sans rapport avec le métier ou avec un chantier « à éviter » (ex. « formation », « salaire », « emploi », « bricolage soi-même », « prix au m² gratuit »). La ligne « Autres termes de recherche » regroupe les recherches que Google ne détaille pas : elle ne peut pas être exclue, ne la propose jamais comme mot à exclure.
- **Communes hors zone** (comparées à la zone du profil).
- **Horaires** où la dépense part alors que personne ne répond (nuit, dimanche) — seulement si le gérant ne veut pas de demandes à ces moments.
- **Annonces faibles** : taux de clic très bas comparé aux autres annonces du compte.

## 4. Proposer au maximum 3 actions

Chaque action, en mots simples :

- **Ce qu'on change** (ex. « Exclure les recherches contenant "emploi" et "formation" »).
- **Pourquoi** (chiffre à l'appui : « 38 € dépensés ce mois, 0 demande »).
- **Comment le faire**, clic par clic (ex. pour un mot clé à exclure : « Campagnes » → « Audiences, mots clés et contenu » → « Mots clés de recherche » → onglet « Mots clés de recherche à exclure » → bouton « + » → choisir la campagne → taper le mot → « Enregistrer »).
- **Comment on saura le mois prochain si ça a marché** (ex. « la dépense sur ces recherches doit être à 0 € et le coût par demande baisser »).

Classe par impact estimé (d'abord ce qui fait économiser le plus ou concerne le plus de demandes). Pas plus de 3, même s'il y a d'autres idées : garde-les pour le mois suivant.

N'applique rien toi-même. Le gérant choisit et clique. Ne propose jamais d'augmenter le budget sans qu'il le demande ; s'il le demande, donne les chiffres et laisse-le décider.

## 5. Limites à écrire à chaque fois

- « L'origine des demandes est celle que les clients déclarent : elle peut être fausse ou imprécise. »
- « Avec moins de 10 demandes par mois, un client de plus ou de moins change beaucoup le résultat : regardez la tendance sur 3 mois. »
- « Google ne compte pas les visiteurs qui refusent les cookies ni les clients qui rappellent plus tard sur un autre numéro. »

## 6. Fin

Écris les 3 actions dans `entreprise/journal-actions.md` avec la mention « proposée » ; quand le gérant dit les avoir faites, ajoute une ligne « appliquée le AAAA-MM-JJ ».
