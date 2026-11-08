---
name: visibilite-ia
description: Rendre l'entreprise compréhensible et citable par les assistants IA (ChatGPT, Gemini, Claude, Perplexité…) — données structurées, page À propos et FAQ factuelles, fichier llms.txt, cohérence nom/adresse/téléphone, test mensuel. Utiliser quand le gérant dit « est-ce que ChatGPT me connaît ? », « être cité par les IA », « être recommandé par ChatGPT », « on m'a dit de faire un llms.txt », « vérifier que mes infos sont partout pareilles ».
---

# Visibilité dans les assistants IA

Les assistants IA s'appuient sur ce qu'ils trouvent sur le web : le site, la fiche Google, les annuaires, les avis. Il n'existe aucune méthode garantie pour y apparaître ; on rend simplement les informations **claires, factuelles et identiques partout**. Dis-le au gérant sans promettre de résultat.

## 1. Fiche d'identité cachée dans le site (données structurées)

Le générateur ajoute automatiquement à chaque page un bloc de « données structurées » (format JSON-LD, vocabulaire schema.org) : nom, téléphone, e-mail, adresse, zone desservie, métiers, site, page Facebook. Il est rempli depuis `entreprise/site-contenu.json`.

À vérifier avec le gérant :
- le type d'entreprise (`entreprise.type_schema`) correspond au métier : voir `modeles/metiers.md` (ex. `Plumber`, `Electrician`, `RoofingContractor`, `GeneralContractor`, `HousePainter`) ; par défaut `HomeAndConstructionBusiness` ;
- les informations sont **les mêmes que sur la fiche Google** (nom, adresse, téléphone, horaires).

**Site actuel conservé** (section 5 du profil) : prépare le bloc JSON-LD avec les mêmes informations (même format que celui du générateur), vérifie qu'il est lisible, et fais-le ajouter dans l'en-tête de toutes les pages : par le gérant si son outil le permet (fonction « code personnalisé » ou équivalent, d'après l'aide officielle de l'outil), sinon par le prestataire (`modeles/messages/modifications-site-prestataire.md`). Le fichier `llms.txt` n'est utile que si l'outil permet d'ajouter un fichier à la racine du site ; sinon, passe.

Après mise en ligne, test (le gérant clique) : ouvrir search.google.com/test/rich-results, coller l'adresse du site, « Tester l'URL ». Il doit voir un élément détecté sans erreur. Tu peux aussi valider localement : `python3 outils/generer_site.py` contrôle que le JSON-LD est lisible.

## 2. Page « À propos » et FAQ factuelles

- **À propos** : qui (prénom du gérant si d'accord), depuis quand (seulement si donné), métiers, zone, façon de travailler — dans les mots du gérant.
- **FAQ** : 5 à 8 questions que les clients posent vraiment. Demande au gérant : « Quelles questions vos clients vous posent-ils le plus souvent au téléphone ? » Réponses courtes et factuelles, tirées de ses réponses. Exemples de questions : « Intervenez-vous à <commune> ? », « Faites-vous les petits chantiers ? », « Comment se passe un devis ? », « Quels délais ? » (seulement si le gérant donne une réponse réelle).
- Pas de question dont la réponse serait inventée. Pas de prix si le gérant n'en donne pas.

Mets à jour `a_propos` et `faq` dans `entreprise/site-contenu.json`. La FAQ est aussi décrite dans les données structurées (type FAQPage) par le générateur.

## 3. Fichier llms.txt

Le générateur crée `llms.txt` à la racine du site : un résumé en texte simple (nom, métiers, zone, contact, liens vers les pages principales et la FAQ). C'est une convention proposée, pas une norme officielle : utile et sans risque, mais rien ne garantit qu'un assistant le lise. Relis-le avec le gérant.

## 4. Même nom, même adresse, même téléphone partout

Liste de contrôle guidée (le gérant vérifie, toi tu notes) — le modèle est `modeles/rapports/controle-coherence.md`. Copie-le dans `entreprise/controle-coherence.md` à la première utilisation :

| Endroit | Nom identique ? | Adresse identique ? | Téléphone identique ? | Site indiqué ? |
|---|---|---|---|---|
| Site du kit | | | | |
| Fiche Google | | | | |
| Page Facebook | | | | |
| Instagram | | | | |
| Pages Jaunes / annuaires connus | | | | |
| Plateformes de mise en relation utilisées | | | | |
| Ancien site (si encore en ligne) | | | | |

Pour chaque « non » : donne au gérant les étapes pour corriger lui-même (ou le message à envoyer à la plateforme).

## 5. Test mensuel (2 minutes, pendant le bilan)

Le gérant pose ces 3 questions à l'assistant IA de son choix (ChatGPT, Gemini, etc.), **sur son téléphone, dans une nouvelle conversation** :

1. « Quel <métier principal> recommandes-tu près de <commune principale> ? »
2. « Je cherche une entreprise pour <chantier prioritaire> à <commune proche>. Qui contacter ? »
3. « Que sais-tu de <nom commercial> à <commune> ? »

Il répond pour chaque question : apparaît / n'apparaît pas / infos fausses. Note dans `entreprise/journal-actions.md` :
`- AAAA-MM-JJ — Test IA (<assistant utilisé>) — Q1 : oui/non, Q2 : oui/non, Q3 : oui/non/infos fausses (lesquelles)`

Si des informations fausses apparaissent : vérifier la cohérence (point 4) et la fiche Google, qui sont les sources les plus probables. Les résultats varient d'une fois à l'autre : on regarde la tendance sur plusieurs mois.
