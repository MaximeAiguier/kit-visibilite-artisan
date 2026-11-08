# Modèle — demander au prestataire du site actuel d'installer le suivi Google Ads

> Usage : l'assistant remplace chaque {{…}} (identifiant et libellés copiés depuis Google Ads par le gérant),
> vérifie avec outils/verifier_publication.py ; le gérant envoie lui-même.

Objet : Installation du suivi des demandes sur {{ADRESSE_DU_SITE}}

Bonjour {{PRENOM_OU_NOM_DU_PRESTATAIRE}},

Je voudrais mesurer les demandes de devis venant de mes annonces Google. Pouvez-vous installer sur {{ADRESSE_DU_SITE}} :

1. la balise Google Ads {{IDENTIFIANT_AW}} sur toutes les pages, chargée uniquement après accord du visiteur dans le bandeau cookies, avec les signaux du mode Consentement v2 de Google ;
2. l'événement de conversion {{IDENTIFIANT_AW}}/{{LIBELLE_FORMULAIRE}} quand le formulaire de contact est envoyé avec succès ;
3. l'événement de conversion {{IDENTIFIANT_AW}}/{{LIBELLE_TELEPHONE}} au clic sur le numéro de téléphone ;
4. un champ obligatoire « Comment nous avez-vous connu ? » dans le formulaire de contact.

Pouvez-vous me dire quand c'est fait, pour que je teste ?

Merci,
{{PRENOM_DU_GERANT}} — {{NOM_COMMERCIAL}}
