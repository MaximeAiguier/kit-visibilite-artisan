# Guides détaillés de l'assistant (version chat)

> Fichier généré par outils/synchroniser_skills.py — ne pas modifier à la main. À ajouter comme fichier du projet.
> Dans la version chat, « lance python3 outils/… » veut dire : fais le calcul ou le contrôle toi-même, en montrant le détail.


---

<!-- guide : avis-clients -->

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



---

<!-- guide : bilan-mensuel -->

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



---

<!-- guide : demarrage -->

---
name: demarrage
description: Démarrage du kit (questionnaire puis profil de l'entreprise). Utiliser quand le gérant dit « je veux commencer », « on démarre », « c'est la première fois », « configure le kit », « bonjour, je fais quoi ? », « reprendre le questionnaire », « modifier mon profil », ou quand entreprise/profil.md est vide ou incomplet. Pose d'abord 7 questions à choix en un seul message (réponse en une ligne), puis quelques blocs de questions groupées pour construire le profil de l'entreprise.
---

# Démarrage (15 minutes environ, une seule fois)

But : comprendre ce dont le gérant a besoin, remplir `entreprise/profil.md`, puis lui proposer un plan simple. Fonctionne pour tout métier.

**Environ 8 messages du gérant**, 10 à 15 minutes. Les questions sont **groupées** et presque toutes **à choix** : le gérant répond en une ligne ou en cliquant. Ce qui n'est pas indispensable au plan de départ est demandé plus tard, au moment où il sert (avis et réseaux sociaux : skills fiche-google, avis-clients et site-creation ; informations légales : site-creation).

## Règles de conduite

- **Un message = un bloc de questions** (pas une question à la fois). Attends la réponse avant le bloc suivant. Si une réponse manque ou n'est pas claire, redemande **seulement** celle-là.
- **Questions à choix** : 4 choix au maximum, repérés par des lettres (a, b, c, d). Le gérant peut répondre en une ligne, par exemple « 1c 2b 3b 4a » ; accepte aussi les phrases libres (« électricien, surtout des particuliers »).
- **Fenêtre de choix cliquables** : si ton outil en propose une (choix à cliquer avec une case « Autre »), utilise-la à la place de la liste écrite, en respectant ses limites (souvent 4 questions par fenêtre et 4 choix par question : fais alors 2 fenêtres pour l'étape 1). Sinon, écris le bloc en entier dans un seul message.
- Si une réponse contient déjà la réponse à une question suivante (ex. « je fais 150 € de Google Ads par une agence »), note-la et **ne repose pas** la question.
- Dès la première réponse, passe `Statut du profil` à `en cours`. Après chaque réponse, **écris-la immédiatement** dans `entreprise/profil.md` (remplace `(non renseigné)`). Ainsi, si la session s'arrête, on reprend où on en était.
- Reprise (statut `en cours`) : dis « On reprend là où on s'était arrêtés » et pose seulement les questions dont la réponse est encore `(non renseigné)`. Une réponse `inconnu` ne se repose pas.
- Le gérant peut répondre « je ne sais pas » ou « passer » : note `inconnu` et continue.
- Ne jamais inventer. Une estimation est notée « (estimation) ».
- Affiche une progression simple : « Étape 2 sur 3 ». Si on dépasse 20 minutes, propose de finir lors de la prochaine session.
- Accuse réception en quelques mots seulement (« C'est noté. »), sans commentaire long, puis envoie le bloc suivant.

## Étape 1 sur 3 — 7 questions à choix, en un seul message (environ 2 minutes)

Présente-toi en une phrase, puis envoie le bloc **tel quel** (même présentation, lettres comprises) :

« Je suis votre assistant pour vos pubs, votre site et votre visibilité sur Google. Pour commencer, 7 questions rapides : répondez en une ligne avec le numéro et la lettre, par exemple **1c 2b 3b 4a 5a 6b 7b**.

**1. Votre métier ?**
a. Maçonnerie, rénovation · b. Plomberie, chauffage · c. Électricité · d. Autre : écrivez-le

**2. Votre priorité n°1 pour les 3 prochains mois ?** (un seul choix)
a. Savoir ce que mes pubs me rapportent · b. Plus de demandes de devis · c. Des chantiers mieux choisis (moins de ceux qui ne m'intéressent pas) · d. Être mieux trouvé sur Google (site, Google Maps)

**3. Temps disponible pour ça, par mois ?**
a. Moins d'1 heure · b. 1 à 2 heures · c. 2 à 4 heures · d. Plus

**4. Vos clients vous trouvent surtout par…** (plusieurs lettres possibles)
a. Bouche-à-oreille · b. Google (pubs, Maps ou site) · c. Facebook, Instagram, annuaires · d. Je ne sais pas

**5. Vos clients sont surtout…**
a. Des particuliers · b. Des professionnels ou collectivités · c. Un mélange

**6. Votre planning en ce moment ?**
a. Plein, je veux surtout mieux choisir · b. Correct, mais je veux plus de demandes · c. Trop de creux

**7. Avec l'ordinateur, vous êtes…**
a. Peu à l'aise (je préfère le téléphone) · b. Ça va pour les choses simples · c. À l'aise »

- Q1 : remplace les exemples a/b/c par les métiers les plus probables si tu les connais déjà ; « d » ou une réponse libre = noter le métier écrit. Consulte ensuite `modeles/metiers.md` pour adapter la suite (exemples de chantiers, vocabulaire). Ne le cite pas au gérant.
- Q4 « b » : à l'étape 3, précise sans reposer la question (pubs, fiche ou site).
- Remplis la section « 1. Besoins et priorités » du profil. « Ce que j'ai déjà essayé » se remplit avec les réponses de l'étape 3.

## Étape 2 sur 3 — L'entreprise (3 messages, environ 5 minutes)

Réponses libres, mais groupées. Exemples de chantiers adaptés au métier (tirés de `modeles/metiers.md`).

**Message A — coordonnées** (le gérant peut répondre ligne par ligne) :
« Pour votre fiche et votre site :
– nom de l'entreprise (tel qu'il doit apparaître partout) et votre prénom ;
– téléphone à afficher, et e-mail où recevoir les demandes ;
– adresse de l'entreprise. Recevez-vous des clients à cette adresse ? a. Oui · b. Non, c'est seulement le siège »

**Message B — votre activité** :
« – Dans quelles communes travaillez-vous (3 à 6 principales, ou un rayon en km) ?
– Quand peut-on vous joindre (jours et heures) ?
– Les chantiers que vous voulez en priorité, et ceux que vous préférez éviter ? (ex. … adapté au métier) »

**Message C — votre différence** : « Qu'est-ce qui vous différencie des autres, en une ou deux phrases ? » Note mot pour mot. Puis applique la règle des preuves :
- **certification, label, garantie, assurance** (RGE, Qualibat, décennale…) : demande une preuve (photo de l'attestation, numéro, date). Sans preuve : note « non publié tant que pas de preuve » ;
- **nombre d'années, nombre de chantiers ou autre chiffre** : demande le chiffre exact s'il est approximatif (« une vingtaine » → « combien exactement ? ») et note « (dit par le gérant) ». Un chiffre exact donné par le gérant peut être publié ; une approximation, non.

## Étape 3 sur 3 — Pubs, site, fiche Google, chiffres (2 messages, environ 3 minutes)

**Message D — à choix** (même format « 1b 2a 3c 4a 5c ») :
« **1. Payez-vous de la publicité ?**
a. Oui, sur Google · b. Oui, ailleurs (Facebook…) · c. Les deux · d. Non
Si oui, combien par mois à peu près ? (écrivez le montant)

**2. Votre compte Google Ads, vous pouvez vous y connecter vous-même ?** (seulement si pubs Google)
a. Oui · b. Non, c'est une agence ou un prestataire qui gère · c. Je ne sais pas

**3. Avez-vous déjà un site internet ?**
a. Non · b. Oui, et je le modifie moi-même · c. Oui, un prestataire le modifie · d. Oui, mais je ne sais pas qui peut le modifier
Si oui, écrivez son adresse (et l'outil si vous le connaissez : WordPress, Wix…).

**4. Si vous avez un site : qui a acheté son adresse (le nom de domaine) ?**
a. Moi ou mon entreprise · b. Le prestataire · c. Je ne sais pas

**5. Avez-vous une fiche Google (celle qui apparaît sur Google Maps) ?**
a. Oui, et je peux la modifier · b. Oui, mais quelqu'un d'autre la gère · c. Non · d. Je ne sais pas »

- Question 1 = d : ignore la question 2.
- **Accès aux comptes pub (H2)** — question 2 = b ou c : note le blocage dans « 9. Accès et blocages » et prépare le message `modeles/messages/demande-acces-google-ads.md` (personnalisé, sans crochets) que le gérant enverra lui-même au prestataire. Ne l'envoie pas.
- Note `Suivi des demandes en place : non` sauf si le gérant dit spontanément savoir combien de demandes ses pubs lui apportent.
- **Site actuel** — question 3 : remplis « Adresse du site actuel » et « Qui peut modifier le site » (section 5). Question 3 = a : `Décision : pas de site actuel`, ignore la question 4. Sinon `Décision : garder` (règle « Site actuel du gérant » d'AGENTS.md : on ne remplace pas par défaut), sauf si le gérant a déjà dit vouloir un nouveau site (priorité, remarque « mon site est vieux ») : alors `remplacer`.
- **Nom de domaine (H3)** — question 4 = b ou c : note le blocage et prépare `modeles/messages/recuperer-nom-de-domaine.md`. Ce n'est urgent que si on remplace le site ; s'il le garde, note-le simplement.

**Message E — trois chiffres** : « À peu près : combien de demandes de devis recevez-vous par mois ? Sur 10 devis envoyés, combien sont signés ? Et combien rapporte un chantier signé, en moyenne ? » → noter « (estimation) ». Le montant moyen sert à juger tout de suite si le budget pub peut être rentable (ex. 150 € par mois pour des chantiers de 3 000 €).

Ne demande **pas** maintenant : le nombre d'avis et la note (relevés au premier bilan ou dans fiche-google), les réseaux sociaux (demandés à la création du site), les informations légales (section 8, demandées à la création du site).

## Fin du démarrage

1. Remplis « Ce que j'ai déjà essayé » (section 1) à partir des réponses de l'étape 3 (pubs, site, fiche Google), sans reposer de question.
2. Passe `Statut du profil` à `complet`, ou à `partiel` s'il reste des `inconnu` importants (accès aux comptes, nom de domaine) — dans ce cas liste-les dans « 9. Accès et blocages ». Mets la date. Les deux statuts terminent le démarrage : il ne sera pas relancé.
3. Affiche un **résumé lisible** (10 lignes maximum) et demande : « Est-ce juste ? Voulez-vous corriger quelque chose ? Et y a-t-il quelque chose qui vous inquiète ou vous a déçu jusqu'ici ? » Corrige jusqu'à validation ; note une éventuelle inquiétude dans « Inquiétudes / déceptions ».
4. Propose un **plan de 2 ou 3 étapes**, adapté aux réponses, et écris-le dans le profil (« Plan proposé »). Applique ces règles dans l'ordre :
   1. **Étape 1 = toujours le suivi** : s'il paie des pubs, `pubs-mise-en-place` complet (journal des devis + suivi Google Ads) ; sinon, seulement le journal des devis. Sans suivi, impossible de savoir ce qui rapporte.
   2. Étape 2 = la priorité n°1 (question 2 de l'étape 1) : a → analyse des pubs, b → annonces, fiche Google ou site selon ce qui manque, c → annonces et pages ciblées sur les chantiers prioritaires, d → fiche Google et référencement. « Site » veut dire : améliorer le site actuel si `Décision : garder` (seo-local, site-mise-a-jour), créer celui du kit s'il n'en a pas ou s'il a choisi de le remplacer.
   3. Étape 3 = le complément le plus utile (souvent la fiche Google et les avis, gratuits).
   4. Si la question 3 de l'étape 1 = « moins d'1 heure » : garde seulement les étapes 1 et 2, et préviens que le reste viendra plus tard.
   5. Si la question 6 de l'étape 1 = planning plein : formule l'objectif comme « mieux choisir ses chantiers » (annonces et pages ciblées sur les chantiers prioritaires) plutôt que « plus de demandes ».
5. Explique en 3 lignes comment utiliser le kit au quotidien : « Quand vous recevez une demande de devis, dites-le-moi. Quand vous finissez un chantier, envoyez-moi des photos. Une fois par mois, demandez le bilan. »
6. Ajoute la ligne de fin de session dans `entreprise/journal-actions.md`.

## Après le démarrage

Le menu est défini dans `AGENTS.md` ; c'est lui qui s'applique ensuite.



---

<!-- guide : fiche-google -->

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



---

<!-- guide : pubs-analyse -->

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



---

<!-- guide : pubs-annonces -->

---
name: pubs-annonces
description: Rédige ou réécrit des annonces Google Ads (annonces de recherche) à partir du profil et des réalisations, avec plusieurs variantes à tester. Utiliser quand le gérant dit « améliore mes annonces », « écris-moi une pub », « mes annonces sont nulles », « change le texte de ma pub », « je veux plus de demandes pour les rénovations de façade ».
---

# Annonces Google

## Limites en vigueur (vérifiées dans l'aide Google Ads « À propos des annonces responsives sur le Réseau de Recherche », novembre 2026)

- Titres : 3 minimum, **15 maximum**, **30 caractères** chacun (espaces compris).
- Descriptions : 2 minimum, **4 maximum**, **90 caractères** chacune.
- Chemins d'URL affichés : 2 champs de **15 caractères** chacun.
- Google mélange titres et descriptions automatiquement : chaque titre doit avoir du sens seul, dans n'importe quel ordre.

Si le gérant signale un message d'erreur de longueur, compte à nouveau et raccourcis.

## Sources autorisées

Uniquement : `entreprise/profil.md` (métiers, zone, chantiers prioritaires, ce qui différencie — sans les éléments marqués « non publié tant que pas de preuve »), `entreprise/realisations/*/fiche.md`, et ce que le gérant dit pendant la session.

Interdit sans preuve fournie : « n°1 », « meilleur », « garantie décennale », labels (RGE, Qualibat…), « devis en 24 h », « intervention rapide », prix, remises, « X ans d'expérience », « Y chantiers réalisés », avis / notes. Si le gérant veut l'un de ces éléments, demande la preuve ou le chiffre exact, note-le dans le profil, puis utilise-le.

Pas de fausse urgence (« offre limitée », « plus que 2 places »).

## Méthode

1. Demande quelle campagne / quel type de chantier est visé (proposer les chantiers prioritaires du profil). Si une annonce existe déjà, demande au gérant de copier-coller ses titres et descriptions actuels (ou une capture).
2. Rédige **15 titres** répartis ainsi : métier + commune principale (3–4), chantier précis (3–4), ce qui différencie selon le gérant (2–3), appel à l'action simple (2–3 : « Demandez votre devis », « Appelez-nous »), nom de l'entreprise (1).
3. Rédige **4 descriptions** : une centrée chantier, une centrée zone, une centrée façon de travailler (selon le gérant), une centrée prise de contact.
4. Propose 2 chemins d'URL (ex. `facade` / `le-mans`).
5. Écris l'annonce dans `entreprise/brouillons/annonce-AAAA-MM-JJ.txt`, une ligne par élément préfixée `T:` (titre), `D:` (description) ou `P:` (chemin), puis lance `python3 outils/verifier_annonce.py` sur ce fichier : il compte les caractères et signale tout dépassement. Corrige jusqu'à « OK ». Affiche ensuite le tout dans un tableau avec le nombre de caractères de chaque ligne.
6. Lance aussi `python3 outils/verifier_publication.py` sur ce fichier. Corrige si besoin.
7. Demande validation. Ensuite seulement, donne les étapes clic par clic pour coller les textes :
   « Campagnes » → « Annonces » → cliquer sur l'annonce existante → « Modifier » (ou « + » → « Annonce responsive sur le Réseau de Recherche ») → coller titre par titre → « Enregistrer ».
8. Conseille de **garder l'ancienne annonce active** à côté pendant un mois pour comparer (si elle existe), sauf si elle contient une promesse fausse.
9. Note dans `entreprise/journal-actions.md` : date, campagne, « nouvelle annonce publiée par le gérant » (seulement après qu'il a confirmé).

## Variantes pour tester

Si le gérant veut tester deux angles (ex. « rapidité de réponse » vs « soin du travail »), crée 2 annonces dans le même groupe, chacune avec un angle dominant. Au bilan suivant, compare le taux de clic et les demandes ; avec peu de volume, attendre 2 mois avant de conclure.



---

<!-- guide : pubs-mise-en-place -->

---
name: pubs-mise-en-place
description: Mise en place du suivi des demandes de devis (une seule fois) et tenue du journal des devis. Utiliser quand le gérant dit « je veux savoir ce que me rapportent mes pubs », « installer le suivi », « compter mes demandes », « j'ai reçu une demande de devis », « un client m'a appelé pour un devis », « note ce devis », « le devis de M. Martin est signé », « j'ai perdu le chantier de Mme Petit ».
---

# Suivi des demandes de devis

Deux parties :
- **A. Le journal des devis** (à faire tout de suite, et à chaque nouvelle demande). C'est la source de vérité.
- **B. Le suivi dans Google Ads** (une seule fois, si le gérant a des pubs Google).

Pourquoi les deux ? Google ne voit pas tout (appels directs, clients qui refusent les cookies, bouche-à-oreille). Le journal, lui, note ce que le client a répondu à « Comment nous avez-vous connu ? ». Les deux se complètent ; aucun n'est parfait. Dis-le simplement au gérant.

---

## A. Journal des devis

### Mettre en place (2 minutes)

1. Vérifie que `entreprise/journal-devis.csv` existe avec la ligne d'en-tête : `date,nom_client,source,type_chantier,commune,statut,montant_signe,notes`.
2. Donne au gérant la phrase à dire à chaque appel : « Pour info, comment nous avez-vous connu ? » — et explique : « Notez la réponse sur un papier ou dans vos notes de téléphone, puis dites-la-moi. »
3. Le formulaire du site (s'il est créé avec ce kit) pose déjà cette question.

### Ajouter une demande (« j'ai reçu une demande de devis »)

Pose au maximum ces 5 questions, regroupées si le gérant donne déjà les infos :

1. Nom du client (ou initiales si le gérant préfère).
2. Comment vous a-t-il connu ? Propose :
   1. Une annonce Google (lien « Annonce » / « Sponsorisé ») → `google-annonce`
   2. Google Maps / fiche Google → `google-maps`
   3. Google, sans précision → `google-recherche` (+ note « Google sans précision »)
   4. Votre site → `site`
   5. Facebook / Instagram → `facebook` / `instagram`
   6. ChatGPT ou un autre assistant IA → `assistant-ia`
   7. Bouche-à-oreille / recommandation → `bouche-a-oreille`
   8. Ancien client → `ancien-client`
   9. Panneau de chantier / véhicule → `panneau-chantier`
   10. Annuaire ou plateforme → `annuaire`
   11. Autre (préciser) → `autre`
   12. Je ne sais pas → `inconnu`
3. Type de chantier (en mots simples).
4. Commune du chantier.
5. Date de la demande (par défaut : aujourd'hui).

Statut = `en attente`. Ajoute la ligne, relis-la au gérant en une phrase, termine.

Astuce à donner une fois : « Les clients disent souvent "sur Google". Demandez-leur : "C'était une annonce marquée Sponsorisé, ou sur la carte ?" »

### Mettre à jour un devis (« signé », « perdu »)

Retrouve la ligne (par nom ; s'il y a plusieurs lignes possibles, demande laquelle). Mets `signé` + `montant_signe` (montant HT ou TTC : demande lequel une fois et note-le dans le profil pour toujours utiliser le même) ou `perdu` (+ raison dans `notes` si le gérant la donne).

Chaque mois, le bilan rappelle les devis encore « en attente » depuis plus de 30 jours.

---

## B. Suivi dans Google Ads (une seule fois, environ 30 minutes réparties en 2 sessions)

### Avant de commencer

- Lis la section « 4. Publicité » du profil. Si le gérant **ne peut pas se connecter lui-même** à Google Ads (hypothèse H2 fausse) : arrête la partie B. Prépare le message de `modeles/messages/demande-acces-google-ads.md`, complété avec les vraies infos (aucun crochet ne doit rester), lance `python3 outils/verifier_publication.py` sur le texte, puis donne-le au gérant pour qu'il l'envoie lui-même. Note le blocage dans le profil et le journal des actions.
- Rappel : tu ne demandes jamais ses identifiants. C'est lui qui clique.
- Les noms des menus Google Ads changent souvent. Les étapes ci-dessous sont un guide : si le gérant ne trouve pas, demande une capture d'écran et adapte.

### Ce qu'on va compter (3 « actions de conversion », c'est-à-dire 3 types de demandes comptées par Google)

| Ce qu'on compte | Nécessite |
|---|---|
| 1. Formulaire de devis envoyé depuis le site | Le site créé avec ce kit (ou un accès au site actuel) |
| 2. Clic sur le numéro de téléphone depuis le site (sur mobile) | Le site créé avec ce kit |
| 3. Appel depuis l'annonce (bouton « Appeler » dans la pub) | Un « composant Appel » sur les annonces + rapports d'appels activés |

Le n°3 utilise un « numéro de transfert Google » : Google affiche dans l'annonce un numéro à lui, qui renvoie vers le vrai numéro, pour compter les appels. **Vérifié en novembre 2026 : ce service est disponible en France** (page d'aide Google Ads « Numéro de transfert Google »). Si le gérant ne le voit pas dans son compte, repli : on compte seulement les clics sur le numéro depuis le site + la question « Comment nous avez-vous connu ? » du journal.

### Étapes pour le gérant (une par message, attendre « c'est fait »)

**Session 1 — créer les actions (sur ordinateur)**

Chemins vérifiés en novembre 2026 dans l'aide Google Ads en français (« Configurer le suivi des conversions sur un site Web », « Suivi des appels », « Composants Appel »).

1. Ouvrez ads.google.com et connectez-vous vous-même.
2. Dans le menu de gauche, cliquez sur « Objectifs » (icône de trophée), puis « Récapitulatif ».
3. Cliquez sur « + Créer une action de conversion ».
4. Si Google le propose, cliquez sur « Modifier les sources de données » à côté de « Conversions sur un site Web », tapez l'adresse de votre site et cliquez sur « Rechercher ».
5. Google propose des catégories : choisissez celle du formulaire de contact (par exemple « Envoi de formulaire pour prospects » ; sinon cliquez sur « Tout afficher »). Cliquez sur « + Créer une conversion » (pas « Accepter les suggestions »).
6. Source : « balise Google » → « Manuellement (avec du code) » → « OK ». Nom : `Formulaire devis`. Dans « Paramètres des conversions » : « Valeur » → aucune valeur ; « Nombre » → une seule conversion par clic. Cliquez sur « Enregistrer et continuer ».
7. Cliquez sur « Afficher l'extrait d'événement ». Vous voyez du code. **Copiez seulement** les deux informations qui ressemblent à `AW-123456789` (identifiant) et `AbC-D_efGhIjKlMnOp` (libellé, après la barre oblique dans `send_to`) et collez-les-moi. Ce ne sont pas des mots de passe : elles seront visibles dans le site. Puis « Accepter et terminer ».
8. Recommencez les étapes 3 à 7 pour une deuxième action, catégorie « Contact », nom `Clic téléphone site`. Collez-moi le nouveau libellé. (Si Google propose directement « Clics sur un numéro de téléphone sur votre site Web mobile », c'est équivalent : choisissez-le.)
9. Pour les appels depuis l'annonce : « + Créer une action de conversion » → type appels téléphoniques → « Appels à partir d'annonces ». Nom `Appel depuis annonce`. Durée minimale d'appel : proposez 60 secondes (le gérant peut choisir autre chose). « Enregistrer et continuer ».
10. Vérifiez que le suivi des appels est activé : icône « Administrateur » → « Paramètres du compte » → section « Suivi des appels » → activé.
11. Vérifiez que vos annonces ont un composant Appel : « Campagnes » → « Composants » → s'il n'y a pas de composant « Appel » avec votre numéro, cliquez sur le bouton « + » → « Appel », entrez le numéro du profil, activez le suivi des appels, enregistrez.

Ensuite, toi : écris l'identifiant et les deux libellés dans `entreprise/site-contenu.json` (bloc `suivi`), régénère le site (`python3 outils/generer_site.py`) et dis au gérant qu'il devra remettre le site en ligne (étapes du skill site-creation). Note tout dans le journal des actions.

**Si le site actuel n'est pas celui du kit** (section 5 du profil) : les conversions 1 et 2 ne peuvent être installées qu'en modifiant le site actuel. Ne le fais jamais toi-même dans un compte.
- Un prestataire modifie le site : prépare `modeles/messages/demande-installation-suivi-prestataire.md`, que le gérant envoie lui-même.
- Le gérant modifie lui-même son site : la plupart des outils (WordPress, Wix, Squarespace…) ont une façon officielle d'ajouter la balise Google ou une intégration Google Ads. Guide-le d'après l'aide officielle de **son** outil (cherche-la, ne l'invente pas) et demande une capture d'écran à chaque étape douteuse. Condition : un **bandeau cookies** qui bloque la balise tant que le visiteur n'a pas accepté (beaucoup d'outils en proposent un). S'il n'y en a pas ou si ça devient technique, passe par un prestataire ou propose le site du kit.
- Dans tous les cas, la conversion n°3 (appels depuis l'annonce) fonctionne sans toucher au site.

**Session 2 — vérifier que ça remonte (le lendemain, 10 minutes, test réel)**

1. Le gérant ouvre son site **sur son téléphone**, accepte les cookies, clique sur le numéro (il peut raccrocher aussitôt), puis envoie le formulaire avec « TEST — ne pas traiter » dans le message.
2. Sur ordinateur, il ouvre tagassistant.google.com, clique sur « Add domain », tape l'adresse de son site, « Connect ». Dans le nouvel onglet, il accepte les cookies, clique sur le bouton du formulaire de devis et l'envoie. Dans l'onglet Tag Assistant, il doit voir une balise « Google Ads » avec un événement « conversion ». Demande-lui une capture d'écran si doute.
3. 24 à 48 heures plus tard : dans « Objectifs » → « Récapitulatif », l'état de chaque action doit passer à « Enregistrement des conversions » ou « Active ». « Non validée » ou « Inactive » après 48 h : demande une capture et cherche la cause (balise absente, mauvais libellé, cookies refusés).
4. Les appels depuis l'annonce ne peuvent être testés que par un vrai client ; vérifie au bilan suivant qu'ils apparaissent dans la colonne « Conversions ».

Note le résultat de chaque test (OK / pas OK) dans `entreprise/journal-actions.md` et la section « 4. Publicité » du profil (`Suivi des demandes en place : oui depuis AAAA-MM-JJ`).

### Limites à expliquer au gérant (une fois, en mots simples)

- Les visiteurs qui refusent les cookies ne sont pas comptés par Google. C'est normal et légal.
- Un même client peut appeler et remplir le formulaire : Google compte 2, le journal compte 1. Le bilan se fonde d'abord sur le journal.
- Avec peu de demandes par mois, les chiffres bougent beaucoup d'un mois à l'autre.



---

<!-- guide : pubs-nouveau-canal -->

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



---

<!-- guide : seo-local -->

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



---

<!-- guide : site-creation -->

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



---

<!-- guide : site-mise-a-jour -->

---
name: site-mise-a-jour
description: Ajoute un chantier terminé au site (photos + texte), prépare les posts fiche Google et Facebook, et modifie les textes du site. Utiliser quand le gérant dit « j'ai fini un chantier », « voici des photos de mon dernier chantier », « ajoute ce chantier au site », « change mon numéro sur le site », « modifier mon site », « enlève cette photo ».
---

# Mise à jour du site

**Quel site ?** Lis la section 5 du profil (« Décision »). Si le gérant **garde son site actuel**, tout ce qui suit reste valable (photos, questions, texte, posts), mais au lieu de modifier `entreprise/site-contenu.json` et de régénérer :
1. Allège les photos (`python3 outils/reduire_photos.py`) et range-les dans `entreprise/realisations/<slug>/`.
2. Donne au gérant le texte final validé (titre, paragraphe, légendes des photos) et dis où le mettre (page « Réalisations » ou équivalent).
3. Il modifie lui-même : guide-le clic par clic d'après l'aide officielle de son outil (WordPress, Wix…), capture d'écran en cas de doute. Un prestataire modifie : prépare `modeles/messages/modifications-site-prestataire.md`. Règle « Site actuel du gérant » d'AGENTS.md.
4. Après la mise en ligne, ouvre la page publique (ou demande une capture) pour vérifier ; note dans le journal des actions.

## A. « J'ai fini un chantier » (10 minutes côté gérant)

1. **Photos** : demande 2 à 6 photos (avant / pendant / après si possible), prises en largeur, sans visage ni plaque d'immatriculation ni numéro de rue lisible. Le gérant les glisse dans la conversation ou dans `entreprise/realisations/`. S'il a des photos de clients reconnaissables ou de l'intérieur d'une maison, demande-lui s'il a l'accord du client.
2. **3 questions**, une à la fois :
   1. Quel type de travaux ? (ex. « ravalement de façade en enduit »)
   2. Dans quelle commune ?
   3. Qu'est-ce qui était difficile ou particulier sur ce chantier ?
   Facultatif, seulement s'il a le temps : mois de fin du chantier ; matériaux.
3. **Toi** :
   - Crée `entreprise/realisations/AAAA-MM-<type>-<commune>/` (minuscules, tirets, sans accents), déplace-y les photos renommées `01.jpg`, `02.jpg`… Lance ensuite `python3 outils/reduire_photos.py entreprise/realisations` : il réduit les photos de plus de 1 Mo à 1600 pixels (originaux gardés dans `originaux/`, qui n'est pas mis en ligne). S'il répond qu'aucun outil d'images n'est disponible, continue : le site reste publiable, juste plus lent sur mobile.
   - Écris `fiche.md` (modèle : `modeles/realisation-fiche.md`) avec les réponses **dans les mots du gérant**, et un texte de 80 à 200 mots pour le site. Pas de nom de client, pas de prix, pas de superlatif non fondé.
   - Rédige le texte alternatif de chaque photo (description factuelle).
   - Ajoute l'entrée dans `realisations` de `entreprise/site-contenu.json` (champs : `slug`, `titre`, `metier` (slug d'un métier existant), `commune`, `date` (AAAA-MM si connu), `texte`, `photos` [{`fichier`, `alt`}], `dossier`).
   - Lance `python3 outils/generer_site.py` et vérifie qu'il n'y a pas d'erreur.
4. **Prépare 2 posts** (après validation du texte de la réalisation) :
   - **Fiche Google** : 2 à 4 phrases + 1 photo + bouton vers la page de la réalisation (voir skill fiche-google, partie 3).
   - **Facebook** : 3 à 5 phrases, ton naturel, 1 à 4 photos (avant / après), commune, invitation à demander un devis avec le lien du site. 0 à 3 mots-dièse utiles au plus (#maçonnerie #<commune>).
   Passe les textes dans `outils/verifier_publication.py`. Montre-les, demande validation.
5. **Republication** : redonne les 3 étapes « Mettre à jour le site en ligne » du skill site-creation (glisser `entreprise/site` dans l'onglet « Deploys » de Netlify). Le gérant publie aussi les posts lui-même.
6. Propose, si le client était content : le message de demande d'avis (skill avis-clients).
7. Journal des actions : réalisation ajoutée + ce qui a été publié (après confirmation).

Si c'est la 3e réalisation et que le site n'était pas encore en ligne : dis-le, c'est le moment de la première mise en ligne.

## B. Modifier un texte ou une information

1. Demande ce qu'il faut changer, en une phrase.
2. Si c'est le **nom, l'adresse, le téléphone ou les horaires** : change-les aussi dans `entreprise/profil.md`, et rappelle de les changer **à l'identique** sur la fiche Google et Facebook (liste du skill visibilite-ia).
3. Modifie `entreprise/site-contenu.json`, régénère, montre la différence en mots simples (« Avant : … / Après : … »), demande validation, puis étapes de republication.
4. Retirer une photo ou une réalisation : supprime l'entrée dans le JSON (les fichiers photo peuvent rester dans le dossier du chantier), régénère.

Pour une demande de modification de mise en page plus large (couleurs, ordre des sections) : modifie `couleur` dans le JSON ; pour le reste, modifie les gabarits de `modeles/site/` avec prudence, régénère et vérifie l'affichage mobile.



---

<!-- guide : visibilite-ia -->

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
