# Installation du kit (pour la personne qui installe le kit chez l'artisan)

Durée : 20 à 30 minutes avec l'artisan, sur **son** ordinateur. Après cette séance, l'artisan est autonome : il n'y a pas d'accompagnement prévu.

## 1. Ce que l'artisan doit avoir

- Un ordinateur (Mac ou Windows) et une connexion internet.
- **Un** des deux outils, avec un abonnement qui l'inclut :
  - **Claude** : l'application de bureau Claude (mode Cowork, avec accès à un dossier) ou Claude Code ;
  - **Codex** (OpenAI) : l'application Codex ou Codex dans un éditeur de code.
- Ses propres accès : compte Google Ads (s'il fait de la pub), fiche Google, page Facebook. Le kit ne crée aucun compte à sa place.

## 2. Préparer le dossier à livrer

Partez du dossier `kit-visibilite-artisan` d'origine (jamais d'une copie déjà utilisée par un autre client), puis lancez (ou faites lancer par l'assistant) :

```
python3 outils/empaqueter.py
```

Le script crée `kit-visibilite-artisan-AAAA-MM-JJ.zip` à côté du dossier, **sans** `exemples/`, `tests/`, ni fichiers système (`.DS_Store`…), **avec** les dossiers cachés `.agents/` et `.claude/` (indispensables : ils contiennent les skills que les outils lisent). Il refuse de créer le zip si `entreprise/` n'est pas vide ou si une donnée d'un client traîne dans le kit. Le dossier d'origine n'est pas modifié.

## 3. Ouvrir le kit chez l'artisan

Décompressez le dossier dans un endroit simple (ex. `Documents/Assistant marketing`).

> **Ouvrez le dossier `kit-visibilite-artisan` lui-même** : celui où l'on voit directement `AGENTS.md`, `README.md`, `skills/`, `entreprise/`. Pas le dossier qui le contient. Ouvert un niveau trop haut, l'assistant ne trouve ni ses instructions ni ses skills, et rien ne le signale à l'artisan (constaté en test avec Codex, novembre 2026). Vérification : à « je veux commencer », il doit se présenter et poser une question **à choix multiples** sur le métier. S'il répond autre chose, le dossier ouvert n'est pas le bon.

**Avec Claude (application de bureau, mode Cowork)**
1. Ouvrez l'application Claude → onglet Cowork → choisissez le dossier du kit comme dossier de travail.
2. Écrivez « je veux commencer ». Si l'assistant ne lance pas le questionnaire, écrivez « Lis le fichier AGENTS.md puis je veux commencer » (certaines versions de l'application ne lisent pas automatiquement `CLAUDE.md`).

**Avec Claude Code**
1. Ouvrez le dossier du kit comme projet (application de bureau, onglet Code, ou extension d'éditeur).
2. Au premier lancement, Claude Code peut demander d'**autoriser l'import** de `AGENTS.md` depuis `CLAUDE.md` : acceptez.
3. Écrivez « je veux commencer ».

**Avec Codex**
1. Ouvrez le dossier du kit comme projet dans l'application Codex (ou l'éditeur).
2. Écrivez « je veux commencer ».

Dans tous les cas, autorisez l'assistant à **lire et écrire dans ce dossier** et à **lancer des programmes Python** dans ce dossier (les outils du kit). Ne lui donnez aucun autre accès.

## 4. Vérifications avant de partir (5 minutes)

- [ ] « je veux commencer » lance bien le questionnaire à choix multiples.
- [ ] L'assistant arrive à lancer `outils/verifier_publication.py`. Sur un Mac neuf, Python n'est pas installé : au premier lancement, le système propose d'installer les « outils de ligne de commande » (environ 10 minutes de téléchargement) — faites-le **pendant la séance d'installation**, pas chez l'artisan seul. Sur Windows, installez Python depuis le Microsoft Store. L'artisan n'a rien à taper. Sans Python, le kit fonctionne en mode dégradé (l'assistant fait les calculs lui-même, sans les contrôles automatiques).
- [ ] L'artisan sait où sont `entreprise/` et `rapports/`.
- [ ] L'artisan a compris les deux habitudes : demander « Comment nous avez-vous connu ? » à chaque client, et faire le bilan en début de mois.
- [ ] Un rappel mensuel est créé dans l'agenda de son téléphone (« Bilan marketing »).

## 5. Comment le kit est construit (pour maintenance)

| Élément | Rôle |
|---|---|
| `AGENTS.md` | **Seule** source des instructions. Lu par Codex. |
| `CLAUDE.md` | Une ligne : `@AGENTS.md` (import officiel de Claude Code). Aucune règle dupliquée. |
| `skills/<nom>/SKILL.md` | **Source** des 12 skills (format standard : dossier + `SKILL.md` avec `name` et `description`). |
| `.agents/skills/` | Copie lue par Codex (emplacement officiel : `.agents/skills` du dossier courant jusqu'à la racine). |
| `.claude/skills/` | Copie lue par Claude Code (emplacement officiel : `.claude/skills`). |
| `version-chat/` | Version dégradée, sans accès au dossier : `INSTRUCTIONS-CHAT.md` (moins de 8 000 caractères) à coller dans les instructions d'un projet Claude ou ChatGPT, et `GUIDES-CHAT.md` à ajouter comme fichier du projet. Générés depuis `AGENTS.md` et `skills/`. |
| `outils/` | Programmes Python 3 sans dépendance : génération du site, contrôle des textes, calcul du bilan, réduction des photos, synchronisation des skills, vérification et empaquetage du kit. |
| `modeles/` | Gabarits du site, messages, rapports, idées par métier. |

Après **toute** modification d'un skill dans `skills/`, faites lancer par l'assistant (ou lancez) :

```
python3 outils/synchroniser_skills.py
python3 outils/verifier_kit.py
```

`verifier_kit.py` contrôle : présence des fichiers obligatoires, en-têtes des skills, copies identiques à la source, `CLAUDE.md` sans duplication, dossier `entreprise/` vide, absence de données d'un client dans le kit générique, README d'une page, absence de texte provisoire dans les modèles publiables.

## 6. Adapter le kit à un autre métier

Rien à changer : le métier est demandé au démarrage et l'assistant s'appuie sur `modeles/metiers.md`. Pour un métier fréquent dans votre clientèle, ajoutez-y une ligne (exemples de chantiers, type de données structurées, catégorie Google probable).

## 7. Limites connues

- Les menus de Google Ads, de la fiche Google, de Netlify et de Formspree changent régulièrement : l'assistant demande une capture d'écran quand l'artisan ne trouve pas un bouton.
- Formspree gratuit : 50 demandes par mois via le formulaire.
- Exports Google Ads : le calcul du bilan a été testé sur des exports reconstitués (format connu, en français et en anglais, .csv, .xlsx), pas encore sur les exports réels d'un artisan. Au premier bilan, l'assistant vérifie à la main 2 ou 3 valeurs.
- Netlify Drop : le site doit être « réclamé » (compte gratuit créé par l'artisan) pour rester en ligne.
- L'origine des demandes est déclarative : les chiffres sont des ordres de grandeur, pas une comptabilité.
