# Kit visibilité artisan

Un **assistant marketing autonome pour les artisans du bâtiment**, qui fonctionne dans **Claude** (Claude Code, Cowork) ou **Codex**. Il n'y a ni serveur ni abonnement technique : c'est un dossier de fichiers que l'artisan ouvre dans son assistant IA.

L'assistant aide l'artisan à :
- **savoir ce que lui rapportent ses pubs Google** : il tient un journal des devis, installe le suivi des conversions et fait un bilan mensuel à partir des exports Google Ads ;
- **être mieux trouvé** : fiche Google, avis clients, référencement local, visibilité dans ChatGPT et les autres assistants ;
- **avoir un site simple et rapide**, généré en HTML statique et mis en ligne gratuitement par glisser-déposer, ou **améliorer le site qu'il a déjà** ;
- **tester d'autres canaux** (Facebook, Instagram) de façon encadrée.

L'artisan ne tape aucune commande et ne donne jamais ses mots de passe. Rien n'est publié, envoyé ni dépensé sans son accord explicite. L'assistant n'invente rien : pas de faux avis, pas de chiffre sans source.

## Télécharger

Prenez le zip de la dernière version dans l'onglet **Releases** du dépôt (colonne de droite). Il contient le kit prêt à livrer, sans les exemples ni les tests.

> Le bouton « Code → Download ZIP » donne le dépôt complet, avec les exemples et les tests. Il convient pour contribuer, pas pour livrer à un artisan.

Installation chez l'artisan (20 à 30 minutes) : voir [INSTALLATION.md](../INSTALLATION.md). Le point clé : ouvrir **le dossier du kit lui-même** dans l'assistant, puis écrire « je veux commencer ».

## Comment ça marche

| Élément | Rôle |
|---|---|
| [`AGENTS.md`](../AGENTS.md) | Instructions de l'assistant (rôle, règles, routage vers les skills). Lu par Codex ; `CLAUDE.md` l'importe pour Claude. |
| [`skills/`](../skills) | 12 skills (démarrage, suivi des devis, analyse des pubs, annonces, fiche Google, avis, SEO local, visibilité IA, création et mise à jour du site, bilan mensuel, nouveau canal). Copiés dans `.claude/skills/` et `.agents/skills/` par `outils/synchroniser_skills.py`. |
| [`outils/`](../outils) | Scripts Python, bibliothèque standard uniquement (Python 3.9 ou plus) : générateur de site, bilan mensuel, contrôle des textes avant publication, contrôle des annonces, réduction des photos, empaquetage. C'est l'assistant qui les lance. |
| [`modeles/`](../modeles) | Gabarits du site, messages types (prestataire, agence, demande d'avis), fiches métiers. |
| `entreprise/`, `rapports/` | Données de l'artisan : vides dans le dépôt. |
| [`version-chat/`](../version-chat) | Version dégradée pour un projet ChatGPT ou Claude sans accès aux fichiers. |
| [`exemples/`](../exemples), [`tests/`](../tests) | Cas d'exemple et tests, absents du zip livré. |

Services utilisés, tous côté artisan avec ses propres comptes : Google Ads, Google Business Profile, Search Console, Formspree (formulaire), Netlify ou Cloudflare Pages (hébergement). Aucun serveur MCP et aucune clé d'API.

## Développer

Modifiez seulement `skills/` (jamais `.claude/skills/` ni `.agents/skills/`) et `AGENTS.md`, puis :

```bash
python3 outils/synchroniser_skills.py
python3 outils/verifier_kit.py
python3 tests/test_kit.py
```

- `python3 tests/test_kit.py --navigateur` lance en plus les contrôles navigateur (il faut Node et Playwright).
- `python3 tests/declenchement.py claude` (ou `codex`) vérifie, dans l'outil réel, quel skill chaque phrase d'artisan déclenche.
- `python3 outils/empaqueter.py` fabrique le zip de livraison (contrôles compris).

Contraintes du projet : Python en bibliothèque standard uniquement ; aucune donnée d'un client réel hors `exemples/` ; textes destinés à l'artisan en français simple ; `README.md` (celui de l'artisan) tenu sur une page.

## Limites

- Les chemins de clic (Google Ads, fiche Google, Netlify, Formspree) suivent l'aide officielle de novembre 2026. Les interfaces changent : l'assistant demande une capture d'écran en cas de doute.
- Les mentions légales générées suivent les textes français (LCEN, Code de la consommation, RGPD) en novembre 2026. Ce n'est pas un conseil juridique : une relecture par un professionnel est recommandée.

## Licence

[CC BY-NC-SA 4.0](../LICENSE) : utilisation, copie et modification libres en citant l'auteur, **sans usage commercial** sans son accord écrit (revente du kit, ou kit facturé dans une prestation), et partage des versions modifiées sous la même licence. **Un artisan peut l'utiliser librement pour sa propre entreprise.** Pour revendre le kit ou l'inclure dans une prestation payante, contactez l'auteur.
