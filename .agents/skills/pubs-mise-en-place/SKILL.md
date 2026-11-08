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
