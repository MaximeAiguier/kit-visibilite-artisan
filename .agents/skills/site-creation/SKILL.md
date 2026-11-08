---
name: site-creation
description: Crée le nouveau site internet de l'entreprise (site simple, rapide sur mobile, sans abonnement technique) à partir du profil et des réalisations, puis guide sa mise en ligne par glisser-déposer et le branchement du nom de domaine. Utiliser quand le gérant dit « refaire mon site », « créer mon site », « mon site est vieux », « mettre le site en ligne », « publier le site », « brancher mon nom de domaine ».
---

# Création du site

Résultat : un site de fichiers simples (HTML/CSS, aucun serveur ni base de données) que le gérant met en ligne en glissant un dossier sur un hébergeur gratuit.

Pages : accueil, une page par métier, réalisations (+ une page par réalisation), à propos (avec FAQ), contact / demande de devis, mentions légales, politique de confidentialité. Plus `llms.txt`, `sitemap.xml`, `robots.txt`.

Priorités intégrées au gabarit (`modeles/site/`) : rapide sur mobile, **bouton d'appel toujours visible sur mobile**, formulaire de devis court avec « Comment nous avez-vous connu ? », photos de chantiers mises en avant, bandeau cookies (le suivi Google Ads n'est chargé qu'après accord du visiteur, comme l'exige la CNIL).

## 1. Rassembler les informations (le moins de questions possible)

Tout ce qui est déjà dans `entreprise/profil.md` n'est pas redemandé. Il faut en plus :

1. **Textes** : tu rédiges à partir du profil (présentation, une page par métier, à propos, FAQ). Le gérant relit. Aucune promesse, certification, chiffre ou délai non fourni (règle 3).
2. **Réalisations** : au moins **3** chantiers avec photos dans `entreprise/realisations/` (skill site-mise-a-jour). Moins de 3 : le site peut être préparé en aperçu, mais **la mise en ligne est bloquée** jusqu'à 3.
3. **Logo** : facultatif. Sans logo, le nom commercial est écrit en texte.
   **Réseaux sociaux** : s'ils ne sont pas dans le profil, demande l'adresse de la page Facebook / Instagram (lien en bas du site et dans la fiche d'identité lue par Google).
4. **Couleur principale** : proposer 3 couleurs simples (bleu foncé, vert, brique) ou celle du logo/véhicule.
5. **Informations légales** (section 8 du profil) — obligatoires pour les mentions légales : forme juridique et raison sociale, adresse, SIRET, immatriculation (artisan entrepreneur individuel : « RNE – SIREN … » ; société : « RCS Ville … » ; le « Répertoire des métiers / RM » n'existe plus depuis 2023), capital (société), TVA intracommunautaire (si assujetti), directeur de la publication, **médiateur de la consommation** et l'hébergeur. **Toute info légale manquante bloque la mise en ligne** ; le générateur la signale.
   - Hébergeur : le modèle contient déjà Netlify (nom, adresse, page de contact ; Netlify ne publie pas de téléphone, le générateur affiche alors un avertissement). Vérifie ces informations sur la page « legal » officielle de l'hébergeur et montre-les au gérant.
   - Médiateur : tout artisan qui travaille pour des particuliers doit en avoir un et l'afficher sur son site. Demande : « Êtes-vous inscrit auprès d'un médiateur de la consommation ? Son nom figure souvent sur vos devis, ou votre fédération (CAPEB, FFB…) ou votre comptable le connaît. » N'invente jamais un médiateur : s'il n'en a pas, dis-lui de s'inscrire auprès d'un médiateur de la liste officielle (economie.gouv.fr, « médiateurs de la consommation référencés ») et note-le comme blocage dans le profil.
   - Entrepreneur individuel (EI, micro-entrepreneur) : « EI » est ajouté après son nom automatiquement. S'il ne veut pas afficher son adresse personnelle, il peut indiquer une adresse de domiciliation (`legal.adresse_domiciliation`) ; sinon l'adresse de l'entreprise figure dans les mentions légales même si elle est masquée ailleurs (la loi le demande).
6. **Formulaire** : service retenu = **Formspree** (gratuit jusqu'à 50 demandes par mois, aucun serveur à gérer). Le gérant crée le formulaire, toi tu ne te connectes pas :
   1. Ouvrez formspree.io, cliquez sur « Get Started » et créez un compte avec l'e-mail **où vous voulez recevoir les demandes**. Ouvrez l'e-mail de vérification envoyé par Formspree et confirmez.
   2. En haut à gauche, cliquez sur « + Add New » → « New Form ». Nom : `Devis site` ; e-mail de réception : le vôtre. Cliquez sur « Create Form ».
   3. Onglet « Integration » : copiez l'adresse qui suit « Your form's endpoint is: » (elle commence par `https://formspree.io/f/`) et collez-la-moi. Ce n'est pas un mot de passe : elle est visible dans le site.
   4. Onglet « Settings » → « Spam protection » : vérifiez que **reCAPTCHA est désactivé** (sinon le formulaire du site ne peut pas envoyer). Le site a déjà sa propre protection contre les robots.
   Au-delà de 50 demandes par mois (offre gratuite), Formspree ne transmet plus les demandes par e-mail : elles restent dans un dossier « Over Limit » de son site, et il prévient par e-mail. Dites-le au gérant pour qu'il aille les lire. Si le gérant reçoit plus de 40 demandes par formulaire par mois, propose de passer à l'offre payante ou de changer de service.
7. **Délai de rappel** : demande « En combien de temps rappelez-vous un client qui a fait une demande ? ». S'il ne s'engage pas sur un délai, la confirmation dira seulement « Nous avons bien reçu votre demande et nous vous recontactons. »

## 2. Écrire `entreprise/site-contenu.json`

Pars de `modeles/site/site-contenu.exemple.json` (structure commentée dans `modeles/site/LISEZ-MOI.md`). Règles :
- Nom, adresse, téléphone : **recopiés exactement** du profil (une seule source dans le JSON ; le générateur les répète à l'identique sur toutes les pages).
- Champ absent = phrase absente. N'écris jamais de valeur provisoire.

## 3. Générer

`python3 outils/generer_site.py`

- Si tout est complet : le site est écrit dans `entreprise/site/` (dossier prêt à glisser).
- Sinon : un aperçu est écrit dans `entreprise/site-apercu/` et le programme liste ce qui bloque (ex. « SIRET manquant », « 2 réalisations sur 3 minimum »). Explique chaque blocage en une phrase et demande l'info manquante.
- Le programme refuse aussi tout texte provisoire, crochets, « à compléter », doublons de titres, JSON-LD illisible.

Montre le résultat au gérant : propose-lui d'ouvrir `entreprise/site-apercu/index.html` ou `entreprise/site/index.html` (double-clic) sur son ordinateur. Le formulaire ne fonctionne qu'une fois en ligne. Demande sa validation page par page (rapide : accueil, une page métier, contact).

## Remplacer un site existant

À lire seulement si le profil indique un site actuel (section 5). Si `Décision : garder`, ne crée pas de site : rappelle au gérant qu'on peut améliorer son site actuel (skills seo-local, site-mise-a-jour) et demande-lui s'il veut vraiment le remplacer. Note sa réponse dans « Décision ».

S'il veut le remplacer :
1. **Reprendre ce qui est bon** : ouvre les pages publiques de l'ancien site (ou demande-lui le texte / des captures). Reprends, **avec son accord**, les textes qu'il a écrits lui-même, ses photos de chantiers et les informations exactes (horaires, zone, services). Un texte écrit par une agence se réécrit plutôt qu'il ne se recopie.
2. **Garder les anciennes adresses** : relève les adresses des anciennes pages, dans l'ordre : le plan du site public (`/sitemap.xml`, ou `/wp-sitemap.xml` pour WordPress) si tu peux l'ouvrir ; sinon le gérant les copie depuis Google (taper `site:son-domaine.fr`) ou Search Console (« Pages »). Pour chaque ancienne page, choisis la page équivalente du nouveau site et ajoute-la dans `redirections` de `entreprise/site-contenu.json` : `{"de": "/ancienne-page/", "vers": "/plomberie.html"}`. Le générateur écrit le fichier `_redirects` (lu par Netlify et Cloudflare) : les visiteurs et Google qui arrivent par une ancienne adresse tombent sur la bonne page.
3. **Même nom de domaine** : la bascule se fait à la partie 5 (e-mails conservés, ancien site gardé jusqu'à vérification). Si le domaine appartient au prestataire, la récupération passe d'abord (H3).
4. **Après la bascule** : ouvre 2 ou 3 anciennes adresses pour vérifier qu'elles arrivent sur la bonne page.

## 4. Mise en ligne (le gérant, 10 minutes, par glisser-déposer)

Hébergeur retenu : **Netlify** (offre gratuite, mise en ligne par glisser-déposer « Netlify Drop »). Ne demande jamais ses identifiants.

**Première mise en ligne**
1. Ouvrez app.netlify.com/drop sur votre ordinateur.
2. Ouvrez votre dossier du kit, puis `entreprise`. Faites glisser le dossier **`site`** (pas un autre) dans la zone de la page Netlify.
3. Netlify affiche une adresse en `.netlify.app`. Cliquez dessus et vérifiez le site sur votre téléphone.
4. **Tout de suite** (le délai peut n'être que d'une heure) : cliquez sur le lien proposé pour **réclamer le site** (« Claim », se connecter ou créer un compte gratuit). Sans cela, le site est supprimé. S'il a disparu, recommencez à l'étape 1.
5. Envoyez une vraie demande de test via le formulaire (« TEST » dans le message) et vérifiez que l'e-mail arrive.

**Mettre à jour le site en ligne** (après chaque modification)
1. Connectez-vous sur app.netlify.com et ouvrez votre site.
2. Onglet « Deploys ». En bas de la page, une zone permet de glisser-déposer un dossier.
3. Glissez à nouveau le dossier `entreprise/site`. Attention : déposer sur app.netlify.com/drop créerait un **deuxième** site.

Si le glisser-déposer échoue ou paraît trop compliqué (hypothèse H5) : propose un autre hébergeur gratuit à glisser-déposer (Cloudflare : « Workers & Pages » → « Create application » → « Get started » → « Drag and drop your files » → nom du projet → « Deploy site » ; mises à jour : « Create a new deployment »), toujours guidé pas à pas. Ne jamais demander au gérant d'utiliser une ligne de commande.

## 5. Brancher le nom de domaine (ex. www.mon-entreprise.fr)

- Vérifie la section 5 du profil. **Si le gérant n'est pas propriétaire du nom de domaine (H3)** : la mise en ligne sur cette adresse est bloquée. Le site reste visible sur l'adresse `.netlify.app`. Prépare `modeles/messages/recuperer-nom-de-domaine.md` (code de transfert « AuthCode » / changement de titulaire) que le gérant envoie lui-même au prestataire.
- S'il est propriétaire : guide-le dans Netlify → « Domain management » → « Add a domain » → « Add a domain you already own » → taper le domaine → suivre les instructions affichées. Netlify indique les réglages à faire chez le registraire (OVH, Ionos, Gandi, etc.) : guide le gérant dans l'interface de son registraire, réglage par réglage, en lisant avec lui ce que Netlify affiche (ne recopie pas de valeurs de mémoire). Le changement prend de quelques minutes à 48 h.
- **Avant de basculer** : vérifie avec le gérant que l'ancien site n'héberge pas ses e-mails (ex. adresse @son-domaine). Si oui, ne touche qu'aux réglages « www » et « @ » du site, jamais aux réglages « MX » (e-mails).
- L'ancien site WordPress / prestataire : ne pas le supprimer tant que le nouveau n'est pas en ligne et vérifié.

## 6. Après la mise en ligne

1. Si des pubs Google tournent : changer l'adresse de destination des annonces vers la page d'accueil ou la page métier du nouveau site (étapes clic par clic) et faire le test de la partie B de pubs-mise-en-place.
2. Mettre l'adresse du site sur la fiche Google (skill fiche-google).
3. Journal des actions : date de mise en ligne, adresse, ce qui reste.
