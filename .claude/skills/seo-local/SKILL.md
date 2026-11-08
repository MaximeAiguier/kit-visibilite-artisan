---
name: seo-local
description: Référencement local du site généré par le kit (pages métier et zone, titres, descriptions, liens entre pages, textes des réalisations). Utiliser quand le gérant dit « être mieux trouvé sur Google », « je n'apparais pas quand on tape maçon + ma ville », « améliorer mon référencement », « faire des pages par ville », « mon site n'est pas trouvé ».
---

# Référencement local (SEO local = être trouvé sur Google dans sa zone, sans payer)

Lis la section 5 du profil (« Décision ») :
- **Site du kit** : tu travailles dans `entreprise/site-contenu.json` puis `outils/generer_site.py`.
- **Site actuel conservé** : mêmes règles, mais tu commences par un **état des lieux** de ses pages publiques (ouvre-les si ton outil peut lire une page web ; sinon demande au gérant le texte ou une capture de l'accueil et des pages de services). Pour chaque page, relève : titre de l'onglet, titre principal, présence du métier et de la ville, numéro cliquable, lien vers le contact. Puis prépare une **fiche de modifications** page par page (titre de page, description, titre principal, paragraphe à ajouter), textes définitifs et validés, que le gérant colle lui-même dans son outil (WordPress, Wix…, d'après l'aide officielle de l'outil) ou envoie à son prestataire (`modeles/messages/modifications-site-prestataire.md`). Ne demande jamais les identifiants du site.
- **Pas de site** : propose d'abord le skill site-creation.

En complément, la **fiche Google** (skill fiche-google) et les **avis** (skill avis-clients) comptent souvent plus que le site pour Google Maps : rappelle-le en une phrase si le gérant ne les a pas encore faits.

## Ce qu'on fait

1. **Une page par métier** (déjà créée par site-creation) : titre de page = « <Métier> à <commune principale> | <Nom commercial> » (60 caractères environ maximum) ; description (environ 155 caractères) = ce qu'on fait + zone + invitation à demander un devis.
2. **Pages de zone : seulement quelques-unes, et utiles.** Une page « <Métier> à <Commune> » n'est créée que si :
   - la commune est dans la zone réelle du profil ;
   - le gérant y a **réellement** fait des chantiers (au moins une réalisation ou une information concrète donnée par lui) ;
   - on peut écrire un texte **différent** des autres pages (chantiers faits là-bas, particularités locales données par le gérant).
   Maximum conseillé : 3 à 6 pages de zone au total. **Jamais** de dizaines de pages copiées-collées en changeant le nom de la ville : Google les considère comme du contenu trompeur et peut pénaliser tout le site.
3. **Liens entre les pages** (maillage interne) : chaque réalisation renvoie vers la page de son métier et, si elle existe, vers la page de sa commune ; chaque page métier montre ses dernières réalisations ; l'accueil renvoie vers toutes les pages métier. Le générateur le fait automatiquement à partir des champs `metier` et `commune` des réalisations.
4. **Textes des réalisations** : titre parlant (« Réfection de toiture en ardoise à Saint-Martin » plutôt que « Chantier 12 »), 80 à 200 mots, décrits avec les mots du gérant ; texte alternatif des photos (« Façade après ravalement, enduit gratté, maison des années 70 »).
5. **Titres de pages et descriptions** : uniques pour chaque page. Le générateur signale les doublons.

## Méthode

1. Lis le profil (zone, chantiers prioritaires) et `entreprise/site-contenu.json`.
2. Propose une liste courte : pages métier à améliorer, 0 à 3 pages de zone à créer, réalisations dont le texte est trop court. Explique en une phrase pourquoi.
3. Pour toute page de zone : demande au gérant 2 ou 3 informations réelles (chantiers faits, type de maisons, contraintes locales). Sans information réelle → pas de page.
4. Rédige, mets à jour `entreprise/site-contenu.json` (champs `titre_seo`, `description_seo`, tableau `pages_zones`), lance `python3 outils/generer_site.py`, montre les changements en langage simple, demande validation.
5. Le gérant remet le site en ligne (étapes dans site-creation, partie « Mettre à jour le site en ligne »).
6. Après mise en ligne, et une seule fois : guide l'ajout du site à Google Search Console (search.google.com/search-console → « + Ajouter une propriété » → type « Préfixe de l'URL » → méthode de validation « Balise HTML » : le gérant colle la balise ici ; c'est une information publique ; tu l'ajoutes dans `suivi.google_site_verification`, puis on régénère et remet en ligne) puis l'envoi du plan du site : « Sitemaps » → « Ajouter un sitemap » → `sitemap.xml` → « Envoyer » (état attendu : « Opération effectuée »).

## Mesure

Pas de promesse de position. Au bilan mensuel, on regarde : demandes `google-recherche` et `google-maps` dans le journal, et (si Search Console est en place) le nombre de clics du mois que le gérant lit dans « Performances ».
