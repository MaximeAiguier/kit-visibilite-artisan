# Modèle — demander un avis à un vrai client

> Usage : l'assistant personnalise (prénom du client, travaux, commune, lien d'avis réel),
> vérifie avec outils/verifier_publication.py ; le gérant envoie lui-même. Jamais de contrepartie, jamais de note suggérée.

## SMS

Bonjour {{PRENOM_CLIENT}}, merci encore de nous avoir confié {{TRAVAUX}}. Si vous êtes satisfait, un petit avis sur Google nous aiderait beaucoup : {{LIEN_AVIS}} — {{PRENOM_DU_GERANT}}, {{NOM_COMMERCIAL}}

## E-mail

Objet : Merci pour votre confiance

Bonjour {{PRENOM_CLIENT}},

Merci encore de nous avoir confié {{TRAVAUX}} à {{COMMUNE}}.
Si vous êtes satisfait du travail, votre avis sur Google aiderait d'autres personnes à nous trouver. Cela prend une minute : {{LIEN_AVIS}}

Bonne journée,
{{PRENOM_DU_GERANT}}
{{NOM_COMMERCIAL}} — {{TELEPHONE}}
