# Gabarit du site (pour l'assistant)

- `gabarit.html` : squelette commun à toutes les pages (variables `$nom`).
- `style.css` : mise en page, mobile d'abord, aucune police ni ressource externe.
- `site.js` : menu mobile, bandeau cookies, suivi Google Ads **après accord seulement**, envoi du formulaire à Formspree sans quitter la page.
- `site-contenu.exemple.json` : structure de `entreprise/site-contenu.json`. Marqué `_modele: true`, le générateur le refuse tel quel.

## Champs de `entreprise/site-contenu.json`

| Champ | Obligatoire | Notes |
|---|---|---|
| `entreprise.nom`, `telephone`, `email`, `adresse.rue/code_postal/ville` | oui | Recopiés exactement du profil. Répétés à l'identique sur toutes les pages. |
| `entreprise.afficher_adresse` | non | `false` si le gérant ne reçoit pas de clients à son adresse (seuls code postal et ville sont affichés). |
| `entreprise.zone.communes` | oui | Communes réellement desservies. `rayon_km` et `texte` facultatifs. |
| `entreprise.horaires`, `horaires_schema` | non | Jours en anglais dans `horaires_schema` (format schema.org : Monday…). |
| `entreprise.type_schema` | non | Voir `modeles/metiers.md`. Défaut `HomeAndConstructionBusiness`. |
| `entreprise.site_url` | non | Adresse définitive (https://…). Nécessaire pour le plan du site et les liens absolus. |
| `entreprise.logo` | non | Chemin relatif à `entreprise/`. Sans logo : nom en texte. |
| `legal.*` | pour publier | Forme, raison sociale, SIRET (14 chiffres), immatriculation (entrepreneur individuel artisan : « RNE – SIREN … » ; société : « RCS Ville … » ; jamais « RM », registre supprimé en 2023), directeur de publication, hébergeur (nom, adresse, téléphone — ou `contact` = page de contact s'il ne publie pas de téléphone, avec un avertissement), médiateur de la consommation (`mediateur.nom`, `mediateur.site`, obligatoire) ; capital pour les sociétés ; TVA ou `tva_non_applicable: true`. Pour un entrepreneur individuel (EI, micro-entrepreneur), « EI » est ajouté après le nom. Manquant = page non générée + mise en ligne bloquée. |
| `legal.adresse_domiciliation` | non | Adresse affichée dans les mentions légales si elle diffère de l'adresse de l'entreprise (société de domiciliation, local). |
| `legal.assurance` | non | Seulement avec attestation fournie. Champs : `assureur`, `coordonnees`, `contrat`, `zone_couverte`. |
| `redirections` | non | Seulement si on remplace un ancien site sur le même nom de domaine : `[{"de": "/ancienne-page/", "vers": "/plomberie.html"}]`. Écrit `_redirects` (redirection permanente). Une page « vers » inexistante est ignorée avec un avertissement. |
| `formulaire.endpoint` | pour publier | `https://formspree.io/f/…` fourni par le gérant. |
| `formulaire.delai_rappel` | non | Ex. « sous 48 heures ouvrées », uniquement si le gérant s'y engage. |
| `suivi.*` | non | Identifiant `AW-…` et libellés copiés par le gérant depuis Google Ads. Sans identifiant : ni bandeau cookies ni balise. |
| `accueil.titre`, `accueil.intro` | oui | `points_forts` : uniquement ce que le gérant affirme. |
| `metiers[]` | oui (≥1) | `slug` (minuscules, tirets), `nom`, `intro` obligatoires. |
| `realisations[]` | pour publier (≥3) | Photos dans `entreprise/realisations/<dossier>/`, `alt` obligatoire. `metier` = un `slug` de `metiers`. |
| `a_propos`, `faq[]` | non | Factuels, d'après les réponses du gérant. |
| `pages_zones[]` | non | 6 maximum, communes de la zone, texte différent pour chacune (voir skill seo-local). |
| `_simulation` | — | `true` pour des données de test : publication toujours bloquée. |

## Ce que le générateur refuse

Texte provisoire (crochets, accolades, « à compléter », « non renseigné », lorem, XXX, TODO…), titres de page en double, page de zone hors zone, plus de 6 pages de zone, photo introuvable ou sans description, bloc nom/adresse/téléphone différent d'une page à l'autre, données structurées illisibles.
