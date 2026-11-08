#!/usr/bin/env python3
"""Génère le site statique de l'entreprise à partir de entreprise/site-contenu.json.

Usage (lancé par l'assistant, jamais par le gérant) :
    python3 outils/generer_site.py [--entreprise DOSSIER] [--sortie DOSSIER]

- Si tout est publiable : écrit <entreprise>/site/ (et supprime site-apercu/).
- Sinon : écrit <entreprise>/site-apercu/ avec un bandeau « APERÇU », liste les blocages,
  et supprime un éventuel <entreprise>/site/ périmé. Code de sortie 2.
- Erreur de contenu (texte provisoire, JSON invalide…) : code de sortie 1, rien n'est écrit.

Python 3.8+ ; bibliothèque standard uniquement.
"""
import argparse
import html
import json
import re
import shutil
import struct
import sys
import unicodedata
from pathlib import Path
from string import Template

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verifier_publication import motifs_interdits  # noqa: E402

FORMES_AVEC_CAPITAL = {"sarl", "eurl", "sas", "sasu", "sa", "snc", "sarl unipersonnelle", "scop"}
# Entrepreneur individuel (y compris micro-entrepreneur) : la mention « EI » doit suivre le nom (loi du 14/02/2022)
FORMES_EI = {"ei", "entrepreneur individuel", "entreprise individuelle", "micro-entreprise", "micro-entrepreneur",
             "auto-entrepreneur", "micro entreprise", "micro entrepreneur", "auto entrepreneur"}
SOURCES_FORMULAIRE = [
    ("google-annonce", "Annonce Google (lien « Sponsorisé »)"),
    ("google-maps", "Google Maps / fiche Google"),
    ("google-recherche", "Recherche Google"),
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("assistant-ia", "ChatGPT ou un autre assistant IA"),
    ("bouche-a-oreille", "Recommandation / bouche-à-oreille"),
    ("ancien-client", "Je suis déjà client"),
    ("panneau-chantier", "Panneau de chantier ou véhicule"),
    ("annuaire", "Annuaire ou plateforme"),
    ("autre", "Autre"),
]


class ErreurContenu(Exception):
    pass


def e(t):
    return html.escape(str(t), quote=True)


def slugifier(t):
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def paragraphes(texte):
    blocs = [b.strip() for b in re.split(r"\n\s*\n", str(texte or "")) if b.strip()]
    return "\n".join(f"<p>{e(b)}</p>" for b in blocs)


def tel_href(numero):
    chiffres = re.sub(r"[^\d+]", "", numero)
    if chiffres.startswith("+"):
        return "tel:" + chiffres
    if chiffres.startswith("00"):
        return "tel:+" + chiffres[2:]
    if chiffres.startswith("0") and len(chiffres) == 10:
        return "tel:+33" + chiffres[1:]
    return "tel:" + chiffres


def dimensions_image(chemin):
    """Largeur/hauteur pour JPEG ou PNG, sans dépendance. None si inconnu."""
    try:
        with open(chemin, "rb") as f:
            debut = f.read(26)
            if debut[:8] == b"\x89PNG\r\n\x1a\n":
                return struct.unpack(">II", debut[16:24])
            if debut[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    octet = f.read(1)
                    while octet and octet != b"\xff":
                        octet = f.read(1)
                    while octet == b"\xff":
                        octet = f.read(1)
                    if not octet:
                        return None
                    marqueur = octet[0]
                    if marqueur in (0xD8, 0x01) or 0xD0 <= marqueur <= 0xD7:
                        continue
                    longueur = struct.unpack(">H", f.read(2))[0]
                    if marqueur in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        f.read(1)
                        h, w = struct.unpack(">HH", f.read(4))
                        return (w, h)
                    f.seek(longueur - 2, 1)
    except (OSError, struct.error):
        return None
    return None


def textes(obj, chemin="contenu"):
    """Parcourt toutes les chaînes du contenu (pour le contrôle des textes provisoires)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("_"):
                continue
            yield from textes(v, f"{chemin}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from textes(v, f"{chemin}[{i}]")
    elif isinstance(obj, str):
        yield chemin, obj


class Generateur:
    def __init__(self, dossier_entreprise, sortie=None):
        self.ent_dir = Path(dossier_entreprise).resolve()
        fichier = self.ent_dir / "site-contenu.json"
        if not fichier.exists():
            raise ErreurContenu(f"Fichier introuvable : {fichier}. Rédigez-le d'abord (modèle : modeles/site/site-contenu.exemple.json).")
        try:
            self.c = json.loads(fichier.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            raise ErreurContenu(f"site-contenu.json n'est pas un JSON valide : {err}")
        self.sortie_forcee = Path(sortie).resolve() if sortie else None
        self.blocages = []
        self.avertissements = []
        self.pages = {}  # nom de fichier -> html
        self.titres = {}

    # ---------- Contrôles ----------
    def controler(self):
        if self.c.get("_modele"):
            raise ErreurContenu("Ce fichier est le modèle (_modele: true), pas les données de l'entreprise. Copiez-le et remplacez toutes les valeurs par les vraies réponses du gérant.")
        erreurs = []
        for chemin, valeur in textes(self.c):
            for motif in motifs_interdits(valeur):
                erreurs.append(f"{chemin} contient un texte provisoire ou interdit : « {motif} »")
        if erreurs:
            raise ErreurContenu("\n".join(erreurs))

        ent = self.c.get("entreprise", {})
        adr = ent.get("adresse", {})
        leg = self.c.get("legal", {})
        heb = leg.get("hebergeur", {})
        obligatoires = {
            "Nom commercial": ent.get("nom"),
            "Téléphone": ent.get("telephone"),
            "E-mail": ent.get("email"),
            "Adresse (rue)": adr.get("rue"),
            "Code postal": adr.get("code_postal"),
            "Ville": adr.get("ville"),
            "Titre de la page d'accueil": self.c.get("accueil", {}).get("titre"),
            "Texte d'introduction de l'accueil": self.c.get("accueil", {}).get("intro"),
        }
        for nom, val in obligatoires.items():
            if not val:
                raise ErreurContenu(f"Information indispensable manquante : {nom}.")
        if not ent.get("zone", {}).get("communes"):
            raise ErreurContenu("Zone d'intervention manquante (entreprise.zone.communes).")
        if not self.c.get("metiers"):
            raise ErreurContenu("Aucun métier décrit (metiers).")
        slugs_metiers = {m.get("slug") for m in self.c["metiers"]}
        for m in self.c["metiers"]:
            if not m.get("slug") or not m.get("nom") or not m.get("intro"):
                raise ErreurContenu(f"Métier incomplet (slug, nom et intro obligatoires) : {m}")

        # Mentions légales
        legal_requis = {
            "forme juridique": leg.get("forme_juridique"),
            "raison sociale ou nom de l'entrepreneur": leg.get("raison_sociale"),
            "SIRET": leg.get("siret"),
            "immatriculation (RNE, ou RCS pour une société)": leg.get("immatriculation"),
            "directeur de la publication": leg.get("directeur_publication"),
            "nom de l'hébergeur": heb.get("nom"),
            "adresse de l'hébergeur": heb.get("adresse"),
            # médiateur de la consommation : affichage obligatoire sur le site (Code de la consommation, R616-1)
            "médiateur de la consommation (nom)": (leg.get("mediateur") or {}).get("nom"),
            "médiateur de la consommation (site internet)": (leg.get("mediateur") or {}).get("site"),
        }
        manquants = [k for k, v in legal_requis.items() if not v]
        if not heb.get("telephone") and not heb.get("contact"):
            manquants.append("téléphone de l'hébergeur (ou, s'il n'en publie pas, l'adresse de sa page de contact : hebergeur.contact)")
        elif not heb.get("telephone"):
            self.avertissements.append("L'hébergeur ne publie pas de téléphone : sa page de contact est affichée à la place. "
                                       "La loi (LCEN, art. 1-1) demande un téléphone : ajoutez-le dès qu'il est connu.")
        if re.match(r"\s*RM\b", leg.get("immatriculation") or "", re.I):
            manquants.append("immatriculation à jour (le Répertoire des métiers n'existe plus depuis 2023 : indiquer « RNE » + SIREN)")
        if (leg.get("forme_juridique") or "").strip().lower() in FORMES_AVEC_CAPITAL and not leg.get("capital"):
            manquants.append("capital social")
        if not leg.get("tva_intracom") and not leg.get("tva_non_applicable"):
            manquants.append("numéro de TVA intracommunautaire (ou indiquer tva_non_applicable: true)")
        siret = re.sub(r"\s", "", leg.get("siret") or "")
        if siret and not re.fullmatch(r"\d{14}", siret):
            manquants.append("SIRET valide (14 chiffres)")
        self.legal_complet = not manquants
        if manquants:
            self.blocages.append("Mentions légales incomplètes, page non générée : " + ", ".join(manquants) + ".")

        # Redirections depuis l'ancien site (remplacement d'un site existant, même nom de domaine)
        for r in self.c.get("redirections", []) or []:
            de, vers = (r.get("de") or "").strip(), (r.get("vers") or "").strip()
            if not de.startswith("/") or de == "/" or " " in de or not vers.startswith("/") or " " in vers:
                raise ErreurContenu(f"Redirection invalide (« de » et « vers » commencent par /, sans espace, « de » différent de /) : {r}")

        # Formulaire
        endpoint = self.c.get("formulaire", {}).get("endpoint", "")
        if not re.match(r"^https://formspree\.io/f/[A-Za-z0-9_-]+$", endpoint or ""):
            self.blocages.append("Adresse du formulaire Formspree manquante ou invalide (formulaire.endpoint).")

        # Réalisations
        valides = 0
        for r in self.c.get("realisations", []):
            if r.get("metier") not in slugs_metiers:
                raise ErreurContenu(f"Réalisation « {r.get('titre')} » : métier inconnu « {r.get('metier')} ».")
            photos_ok = [p for p in r.get("photos", []) if (self.ent_dir / "realisations" / r.get("dossier", "") / p.get("fichier", "")).is_file()]
            manquantes = [p.get("fichier") for p in r.get("photos", []) if p not in photos_ok]
            if manquantes:
                raise ErreurContenu(f"Réalisation « {r.get('titre')} » : photo(s) introuvable(s) {manquantes} dans realisations/{r.get('dossier')}/.")
            for p in photos_ok:
                if not p.get("alt"):
                    raise ErreurContenu(f"Réalisation « {r.get('titre')} » : description (alt) manquante pour {p.get('fichier')}.")
            for p in photos_ok:
                taille = (self.ent_dir / "realisations" / r.get("dossier", "") / p["fichier"]).stat().st_size
                if taille > 1_000_000:
                    self.avertissements.append(
                        f"Photo lourde ({taille / 1e6:.1f} Mo) : realisations/{r.get('dossier')}/{p['fichier']}. "
                        "Lancer « python3 outils/reduire_photos.py entreprise/realisations » pour un site rapide sur mobile.")
            if photos_ok and r.get("texte") and r.get("commune"):
                valides += 1
        if valides < 3:
            self.blocages.append(f"{valides} réalisation(s) avec photos sur 3 minimum : ajoutez des chantiers avant la mise en ligne.")

        if self.c.get("_simulation"):
            self.blocages.append("Données simulées (_simulation: true) : ce site sert uniquement de test.")

        if not ent.get("site_url"):
            self.avertissements.append("Adresse définitive du site inconnue (entreprise.site_url) : plan du site (sitemap) et liens absolus non générés. À ajouter après la première mise en ligne.")
        for z in self.c.get("pages_zones", []):
            if z.get("commune") not in ent["zone"]["communes"]:
                raise ErreurContenu(f"Page de zone « {z.get('commune')} » hors de la zone d'intervention déclarée.")
            if z.get("metier") not in slugs_metiers:
                raise ErreurContenu(f"Page de zone « {z.get('commune')} » : métier inconnu.")
        if len(self.c.get("pages_zones", [])) > 6:
            raise ErreurContenu("Plus de 6 pages de zone : risque de pages quasi identiques (voir skill seo-local).")

    # ---------- Éléments communs ----------
    @property
    def apercu(self):
        return bool(self.blocages)

    def url_abs(self, fichier):
        base = (self.c["entreprise"].get("site_url") or "").rstrip("/")
        return f"{base}/{fichier}" if base else None

    def jsonld_entreprise(self):
        ent = self.c["entreprise"]
        adr = ent["adresse"]
        d = {
            "@context": "https://schema.org",
            "@type": ent.get("type_schema") or "HomeAndConstructionBusiness",
            "name": ent["nom"],
            "telephone": ent["telephone"],
            "email": ent["email"],
            "address": {"@type": "PostalAddress", "postalCode": adr["code_postal"], "addressLocality": adr["ville"], "addressCountry": adr.get("pays", "FR")},
            "areaServed": [{"@type": "City", "name": c} for c in ent["zone"]["communes"]],
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Prestations",
                "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": m["nom"]}} for m in self.c["metiers"]],
            },
        }
        if ent.get("afficher_adresse", True):
            d["address"]["streetAddress"] = adr["rue"]
        if adr.get("region"):
            d["address"]["addressRegion"] = adr["region"]
        if ent.get("site_url"):
            d["url"] = ent["site_url"].rstrip("/") + "/"
            d["@id"] = d["url"] + "#entreprise"
            photo = self.premiere_photo()
            if photo:
                d["image"] = self.url_abs(photo)
        reseaux = [u for u in (ent.get("reseaux") or {}).values() if u]
        if reseaux:
            d["sameAs"] = reseaux
        if ent.get("horaires_schema"):
            d["openingHoursSpecification"] = [
                {"@type": "OpeningHoursSpecification", "dayOfWeek": h["jours"], "opens": h["ouverture"], "closes": h["fermeture"]}
                for h in ent["horaires_schema"]
            ]
        return d

    def premiere_photo(self):
        for r in self.c.get("realisations", []):
            for p in r.get("photos", []):
                return f"photos/{r['slug']}/{p['fichier']}"
        return None

    def image_partage(self, fichier):
        """Photo montrée quand on partage la page : celle de la réalisation, sinon la première."""
        for r in self.c.get("realisations", []):
            if fichier == f'realisation-{r["slug"]}.html' and r.get("photos"):
                return f'photos/{r["slug"]}/{r["photos"][0]["fichier"]}'
        return self.premiere_photo()

    def favicon(self):
        """Icône d'onglet : initiale du nom sur la couleur du site (fichier SVG, sans dépendance)."""
        ent = self.c["entreprise"]
        initiale = next((ch for ch in ent["nom"] if ch.isalnum()), "?").upper()
        couleur = ent.get("couleur") or "#1f4e79"
        if not re.fullmatch(r"#[0-9a-fA-F]{3,8}", couleur):
            couleur = "#1f4e79"
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
                f'<rect width="64" height="64" rx="12" fill="{couleur}"/>'
                '<text x="32" y="44" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" '
                f'text-anchor="middle" fill="#ffffff">{html.escape(initiale)}</text></svg>\n')

    def bloc_nap(self):
        ent = self.c["entreprise"]
        adr = ent["adresse"]
        lignes = [f'<p class="pied-titre">{e(ent["nom"])}</p>']
        if ent.get("afficher_adresse", True):
            lignes.append(f'<p>{e(adr["rue"])}</p>')
        lignes.append(f'<p>{e(adr["code_postal"])} {e(adr["ville"])}</p>')
        lignes.append(f'<p><a href="{tel_href(ent["telephone"])}" data-suivi="telephone">{e(ent["telephone"])}</a></p>')
        lignes.append(f'<p><a href="mailto:{e(ent["email"])}">{e(ent["email"])}</a></p>')
        if ent.get("horaires"):
            lignes.append(f'<p>{e(ent["horaires"])}</p>')
        return "\n      ".join(lignes)

    def navigation(self, courant):
        liens = [("index.html", "Accueil")]
        liens += [(f'{m["slug"]}.html', m["nom"]) for m in self.c["metiers"]]
        if self.c.get("realisations"):
            liens.append(("realisations.html", "Réalisations"))
        liens += [("a-propos.html", "À propos"), ("contact.html", "Devis")]
        actuel = ' aria-current="page"'
        return "\n      ".join(
            f'<a href="{h}"{actuel if h == courant else ""}>{e(t)}</a>' for h, t in liens
        )

    def zone_texte(self):
        z = self.c["entreprise"]["zone"]
        if z.get("texte"):
            return e(z["texte"])
        txt = ", ".join(z["communes"])
        if z.get("rayon_km"):
            txt += f" et environ {int(z['rayon_km'])} km autour"
        return e(txt)

    def page(self, fichier, titre, description, contenu, jsonld_extra=None):
        ent = self.c["entreprise"]
        if titre in self.titres.values():
            raise ErreurContenu(f"Titre de page en double : « {titre} ». Chaque page doit avoir un titre unique.")
        self.titres[fichier] = titre
        graphe = [self.jsonld_entreprise()] + (jsonld_extra or [])
        jsonld = json.dumps(graphe if len(graphe) > 1 else graphe[0], ensure_ascii=False, indent=1).replace("</", "<\\/")
        suivi = self.c.get("suivi", {}) or {}
        balises = []
        canon = self.url_abs("" if fichier == "index.html" else fichier)
        if canon:
            balises.append(f'<link rel="canonical" href="{e(canon)}">')
        if suivi.get("google_site_verification") and fichier == "index.html":
            balises.append(f'<meta name="google-site-verification" content="{e(suivi["google_site_verification"])}">')
        if self.apercu or fichier == "404.html":
            balises.append('<meta name="robots" content="noindex">')
        if fichier == "404.html":
            # servie par l'hébergeur à n'importe quelle adresse : liens relatifs à la racine du site
            balises.insert(0, '<base href="/">')
        balises.append('<link rel="icon" href="favicon.svg" type="image/svg+xml">')
        # Aperçu lors d'un partage (Facebook, WhatsApp…) : balises Open Graph
        balises += [
            '<meta property="og:type" content="website">',
            '<meta property="og:locale" content="fr_FR">',
            f'<meta property="og:site_name" content="{e(ent["nom"])}">',
            f'<meta property="og:title" content="{e(titre)}">',
            f'<meta property="og:description" content="{e(description)}">',
        ]
        if canon:
            balises.append(f'<meta property="og:url" content="{e(canon)}">')
        image = self.image_partage(fichier)
        if image and self.url_abs(image):
            balises.append(f'<meta property="og:image" content="{e(self.url_abs(image))}">')
        marque = e(ent["nom"])
        if ent.get("logo") and (self.ent_dir / ent["logo"]).is_file():
            marque = f'<img src="{e(Path(ent["logo"]).name)}" alt="{e(ent["nom"])}">'
        cookies = ""
        if suivi.get("google_ads_id"):
            cookies = (
                '<div id="cookies" class="cookies" role="dialog" aria-label="Cookies" hidden>\n'
                "  <p>Avec votre accord, nous utilisons un cookie Google Ads pour savoir si nos annonces vous ont amené ici. Aucun autre usage. "
                '<a href="confidentialite.html">En savoir plus</a></p>\n'
                '  <div class="actions"><button class="bouton" type="button" data-consentement="oui">Accepter</button>'
                '<button class="bouton bouton-secondaire" type="button" data-consentement="non">Refuser</button></div>\n</div>'
            )
        liens_pied = []
        if self.legal_complet:
            liens_pied.append('<li><a href="mentions-legales.html">Mentions légales</a></li>')
        liens_pied.append('<li><a href="confidentialite.html">Confidentialité</a></li>')
        if suivi.get("google_ads_id"):
            liens_pied.append('<li><button class="lien-bouton" type="button" data-consentement="choisir">Gérer les cookies</button></li>')
        reseaux = ent.get("reseaux") or {}
        for nom, url in reseaux.items():
            if url:
                liens_pied.append(f'<li><a href="{e(url)}" rel="noopener">{e(nom.capitalize())}</a></li>')
        suivi_js = json.dumps({
            "id": suivi.get("google_ads_id") or "",
            "labelForm": suivi.get("label_formulaire") or "",
            "labelTel": suivi.get("label_clic_telephone") or "",
        })
        gabarit = Template((RACINE / "modeles/site/gabarit.html").read_text(encoding="utf-8"))
        self.pages[fichier] = gabarit.substitute(
            titre_page=e(titre),
            description_page=e(description),
            balises_supplementaires="\n".join(balises),
            couleur=e(ent.get("couleur") or "#1f4e79"),
            jsonld=jsonld,
            id_page=e(fichier[:-5]),
            bandeau_apercu='<div class="apercu">APERÇU — ce site n\'est pas encore prêt à être mis en ligne</div>' if self.apercu else "",
            marque=marque,
            navigation=self.navigation(fichier),
            tel_href=tel_href(ent["telephone"]),
            telephone=e(ent["telephone"]),
            contenu=contenu,
            bloc_nap=self.bloc_nap(),
            zone_texte=self.zone_texte(),
            liens_pied="\n        ".join(liens_pied),
            bandeau_cookies=cookies,
            suivi_js=suivi_js,
        )

    def cartes_realisations(self, realisations):
        cartes = []
        for r in realisations:
            img = ""
            if r.get("photos"):
                p = r["photos"][0]
                img = self.balise_img(r, p, paresseux=True)
            cartes.append(
                f'<article class="carte"><a href="realisation-{e(r["slug"])}.html">{img}'
                f'<div class="carte-corps"><h3>{e(r["titre"])}</h3>'
                f'<p class="etiquette">{e(r["commune"])}{(" · " + e(r["date"])) if r.get("date") else ""}</p></div></a></article>'
            )
        return '<div class="grille">' + "".join(cartes) + "</div>"

    def balise_img(self, r, p, paresseux=True):
        src = f'photos/{r["slug"]}/{p["fichier"]}'
        dims = dimensions_image(self.ent_dir / "realisations" / r.get("dossier", "") / p["fichier"])
        taille = f' width="{dims[0]}" height="{dims[1]}"' if dims else ""
        lazy = ' loading="lazy"' if paresseux else ""
        return f'<img src="{e(src)}" alt="{e(p["alt"])}"{taille}{lazy} decoding="async">'

    def appel_action(self):
        ent = self.c["entreprise"]
        return (
            '<section class="section section-grise"><div class="conteneur">'
            "<h2>Un projet ? Parlons-en</h2>"
            "<p>Appelez-nous ou décrivez votre projet en quelques lignes.</p>"
            f'<div class="actions"><a class="bouton bouton-tel" href="{tel_href(ent["telephone"])}" data-suivi="telephone">{e(ent["telephone"])}</a>'
            '<a class="bouton bouton-secondaire" href="contact.html">Demander un devis</a></div>'
            "</div></section>"
        )

    # ---------- Pages ----------
    def construire(self):
        ent = self.c["entreprise"]
        acc = self.c["accueil"]
        ville = ent["adresse"]["ville"]
        reals = self.c.get("realisations", [])

        # Accueil
        points = "".join(f"<li>{e(p)}</li>" for p in acc.get("points_forts", []))
        cartes_metiers = "".join(
            f'<article class="carte"><a href="{e(m["slug"])}.html"><div class="carte-corps"><h3>{e(m["nom"])}</h3><p>{e(m["intro"])}</p></div></a></article>'
            for m in self.c["metiers"]
        )
        contenu = (
            f'<section class="heros"><div class="conteneur"><h1>{e(acc["titre"])}</h1>'
            f'<p class="intro">{e(acc["intro"])}</p>'
            f'<div class="actions"><a class="bouton bouton-tel" href="{tel_href(ent["telephone"])}" data-suivi="telephone">{e(ent["telephone"])}</a>'
            '<a class="bouton bouton-secondaire" href="contact.html">Demander un devis</a></div>'
            + (f'<ul class="points">{points}</ul>' if points else "")
            + "</div></section>"
            f'<section class="section"><div class="conteneur"><h2>Nos métiers</h2><div class="grille">{cartes_metiers}</div></div></section>'
        )
        if reals:
            contenu += (
                '<section class="section section-grise"><div class="conteneur"><h2>Nos derniers chantiers</h2>'
                + self.cartes_realisations(reals[:3])
                + '<p style="margin-top:16px"><a href="realisations.html">Voir toutes les réalisations</a></p></div></section>'
            )
        contenu += f'<section class="section"><div class="conteneur"><h2>Où intervenons-nous ?</h2><p>{self.zone_texte()}</p></div></section>'
        contenu += self.appel_action()
        self.page("index.html", acc.get("titre_seo") or f'{ent["nom"]} – {", ".join(m["nom"] for m in self.c["metiers"])} à {ville}',
                  acc.get("description_seo") or acc["intro"][:155], contenu)

        # Métiers
        for m in self.c["metiers"]:
            reals_m = [r for r in reals if r["metier"] == m["slug"]]
            zones_m = [z for z in self.c.get("pages_zones", []) if z["metier"] == m["slug"]]
            prest = "".join(f"<li>{e(p)}</li>" for p in m.get("prestations", []))
            contenu = (
                f'<section class="heros"><div class="conteneur"><p class="fil"><a href="index.html">Accueil</a> › {e(m["nom"])}</p>'
                f'<h1>{e(m.get("titre") or m["nom"] + " à " + ville + " et alentours")}</h1><p class="intro">{e(m["intro"])}</p></div></section>'
                '<section class="section"><div class="conteneur">'
                + paragraphes(m.get("texte"))
                + (f'<h2>Prestations</h2><ul class="prestations">{prest}</ul>' if prest else "")
                + "</div></section>"
            )
            if reals_m:
                contenu += f'<section class="section section-grise"><div class="conteneur"><h2>Chantiers de {e(m["nom"].lower())}</h2>{self.cartes_realisations(reals_m[:6])}</div></section>'
            if zones_m:
                contenu += '<section class="section"><div class="conteneur"><h2>Par commune</h2><ul>' + "".join(
                    f'<li><a href="zone-{e(z["slug"])}.html">{e(m["nom"])} à {e(z["commune"])}</a></li>' for z in zones_m) + "</ul></div></section>"
            contenu += self.appel_action()
            self.page(f'{m["slug"]}.html', m.get("titre_seo") or f'{m["nom"]} à {ville} | {ent["nom"]}',
                      m.get("description_seo") or m["intro"][:155], contenu)

        # Réalisations
        if reals:
            contenu = (
                '<section class="heros"><div class="conteneur"><h1>Nos réalisations</h1>'
                "<p class=\"intro\">Quelques chantiers récents, photographiés par nos soins.</p></div></section>"
                f'<section class="section"><div class="conteneur">{self.cartes_realisations(reals)}</div></section>'
                + self.appel_action()
            )
            self.page("realisations.html", f'Réalisations – {ent["nom"]}', f'Chantiers réalisés par {ent["nom"]} : photos et descriptions.', contenu)
            metiers = {m["slug"]: m for m in self.c["metiers"]}
            zones = {(z["metier"], z["commune"]): z for z in self.c.get("pages_zones", [])}
            for r in reals:
                m = metiers[r["metier"]]
                galerie = "".join(self.balise_img(r, p, paresseux=i > 0) for i, p in enumerate(r.get("photos", [])))
                z = zones.get((r["metier"], r["commune"]))
                liens = f'<a href="{e(m["slug"])}.html">{e(m["nom"])}</a>'
                if z:
                    liens += f' · <a href="zone-{e(z["slug"])}.html">{e(m["nom"])} à {e(z["commune"])}</a>'
                contenu = (
                    f'<section class="section"><div class="conteneur"><p class="fil"><a href="index.html">Accueil</a> › <a href="realisations.html">Réalisations</a> › {e(r["titre"])}</p>'
                    f'<h1>{e(r["titre"])}</h1><p class="etiquette">{e(r["commune"])}{(" · " + e(r["date"])) if r.get("date") else ""}</p>'
                    f'<div class="galerie">{galerie}</div>{paragraphes(r["texte"])}<p>Voir aussi : {liens}</p></div></section>'
                    + self.appel_action()
                )
                self.page(f'realisation-{r["slug"]}.html', r.get("titre_seo") or f'{r["titre"]} | {ent["nom"]}',
                          r.get("description_seo") or re.sub(r"\s+", " ", r["texte"])[:155], contenu)

        # Pages de zone
        for z in self.c.get("pages_zones", []):
            m = next(mm for mm in self.c["metiers"] if mm["slug"] == z["metier"])
            reals_z = [r for r in reals if r["commune"] == z["commune"] and r["metier"] == z["metier"]]
            contenu = (
                f'<section class="heros"><div class="conteneur"><p class="fil"><a href="index.html">Accueil</a> › <a href="{e(m["slug"])}.html">{e(m["nom"])}</a> › {e(z["commune"])}</p>'
                f'<h1>{e(z.get("titre") or m["nom"] + " à " + z["commune"])}</h1></div></section>'
                f'<section class="section"><div class="conteneur">{paragraphes(z["texte"])}</div></section>'
            )
            if reals_z:
                contenu += f'<section class="section section-grise"><div class="conteneur"><h2>Chantiers à {e(z["commune"])}</h2>{self.cartes_realisations(reals_z)}</div></section>'
            contenu += self.appel_action()
            self.page(f'zone-{z["slug"]}.html', z.get("titre_seo") or f'{m["nom"]} à {z["commune"]} | {ent["nom"]}',
                      z.get("description_seo") or re.sub(r"\s+", " ", z["texte"])[:155], contenu)

        # À propos + FAQ
        ap = self.c.get("a_propos", {}) or {}
        faq = self.c.get("faq", [])
        contenu = '<section class="heros"><div class="conteneur"><h1>À propos</h1></div></section><section class="section"><div class="conteneur">'
        contenu += paragraphes(ap.get("texte")) if ap.get("texte") else ""
        extra = []
        if faq:
            contenu += '<h2 id="faq">Questions fréquentes</h2>' + "".join(
                f'<details><summary>{e(q["question"])}</summary>{paragraphes(q["reponse"])}</details>' for q in faq)
            extra.append({
                "@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q["question"], "acceptedAnswer": {"@type": "Answer", "text": q["reponse"]}} for q in faq],
            })
        contenu += "</div></section>" + self.appel_action()
        self.page("a-propos.html", ap.get("titre_seo") or f'À propos de {ent["nom"]}',
                  ap.get("description_seo") or f'Qui sommes-nous ? {ent["nom"]}, {", ".join(m["nom"] for m in self.c["metiers"]).lower()} à {ville}.', contenu, extra)

        # Contact / devis
        form = self.c.get("formulaire", {})
        delai = form.get("delai_rappel")
        confirmation = "Merci, nous avons bien reçu votre demande. " + (f"Nous vous rappelons {delai}." if delai else "Nous vous recontactons.")
        erreur = f'L\'envoi n\'a pas fonctionné. Appelez-nous au {ent["telephone"]} ou réessayez dans quelques minutes.'
        options_metiers = "".join(f'<option>{e(m["nom"])}</option>' for m in self.c["metiers"]) + "<option>Autre</option>"
        options_sources = '<option value="">Choisissez une réponse</option>' + "".join(f'<option value="{v}">{e(t)}</option>' for v, t in SOURCES_FORMULAIRE)
        action = form.get("endpoint") or "#"
        contenu = (
            '<section class="section"><div class="conteneur"><h1>Demander un devis</h1>'
            f'<p>Décrivez votre projet en quelques lignes, ou appelez-nous au <a href="{tel_href(ent["telephone"])}" data-suivi="telephone">{e(ent["telephone"])}</a>.</p>'
            f'<form id="form-devis" class="formulaire" action="{e(action)}" method="POST" data-confirmation="{e(confirmation)}" data-erreur="{e(erreur)}">'
            '<input type="hidden" name="_subject" value="Nouvelle demande de devis (site)">'
            '<div class="cache" aria-hidden="true"><label>Ne pas remplir <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>'
            '<div><label for="nom">Nom <span class="obligatoire">*</span></label><input id="nom" name="nom" required autocomplete="name"></div>'
            '<div><label for="telephone">Téléphone <span class="obligatoire">*</span></label><input id="telephone" name="telephone" type="tel" required autocomplete="tel"></div>'
            '<div><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email"></div>'
            '<div><label for="commune">Commune du chantier <span class="obligatoire">*</span></label><input id="commune" name="commune" required></div>'
            f'<div><label for="travaux">Type de travaux</label><select id="travaux" name="type_travaux">{options_metiers}</select></div>'
            '<div><label for="message">Votre projet en quelques mots</label><textarea id="message" name="message" rows="4"></textarea></div>'
            f'<div><label for="source">Comment nous avez-vous connu ? <span class="obligatoire">*</span></label><select id="source" name="source" required>{options_sources}</select></div>'
            '<div><label class="case"><input type="checkbox" name="accord" value="oui" required> '
            '<span>J\'accepte que ces informations soient utilisées uniquement pour me recontacter au sujet de ma demande. '
            '<a href="confidentialite.html">Confidentialité</a></span></label></div>'
            '<div><button class="bouton" type="submit">Envoyer ma demande</button></div>'
            "</form>"
            '<div id="form-message" class="message-form" tabindex="-1" role="status" hidden></div>'
            "</div></section>"
        )
        self.page("contact.html", f'Demande de devis – {ent["nom"]}', f'Demandez un devis à {ent["nom"]} : formulaire rapide ou téléphone.', contenu)

        # Mentions légales (seulement si complètes)
        if self.legal_complet:
            leg = self.c["legal"]
            heb = leg["hebergeur"]
            forme = leg["forme_juridique"].strip()
            nom_legal = leg["raison_sociale"].strip()
            if forme.lower() in FORMES_EI:
                forme = "entrepreneur individuel"
                if not re.search(r"\bEI\b|entrepreneur individuel", nom_legal, re.I):
                    nom_legal += " EI"
            adr_legale = leg.get("adresse_domiciliation") or (
                f'{ent["adresse"]["rue"]}, {ent["adresse"]["code_postal"]} {ent["adresse"]["ville"]}')
            med = leg["mediateur"]
            lignes = [
                f'<p><strong>{e(nom_legal)}</strong> — {e(forme)}'
                + (f', au capital de {e(leg["capital"])}' if leg.get("capital") else "") + "</p>",
                f'<p>Adresse : {e(adr_legale)}</p>',
                f'<p>SIRET : {e(leg["siret"])} — {e(leg["immatriculation"])}</p>',
                f'<p>TVA intracommunautaire : {e(leg["tva_intracom"])}</p>' if leg.get("tva_intracom") else "<p>TVA non applicable, article 293 B du Code général des impôts.</p>",
                f'<p>Téléphone : {e(ent["telephone"])} — E-mail : {e(ent["email"])}</p>',
                f'<p>Directeur de la publication : {e(leg["directeur_publication"])}</p>',
            ]
            ass = leg.get("assurance") or {}
            if ass.get("assureur"):
                lignes.append(f'<p>Assurance professionnelle : {e(ass["assureur"])}' + (f' ({e(ass["coordonnees"])})' if ass.get("coordonnees") else "")
                              + (f', contrat n° {e(ass["contrat"])}' if ass.get("contrat") else "")
                              + (f', couverture géographique : {e(ass["zone_couverte"])}' if ass.get("zone_couverte") else "") + "</p>")
            contact_heb = e(heb["telephone"]) if heb.get("telephone") else f'contact : <a href="{e(heb["contact"])}" rel="noopener">{e(heb["contact"])}</a>'
            site_med = med["site"] if med["site"].startswith("http") else "https://" + med["site"]
            contenu = (
                '<section class="section"><div class="conteneur"><h1>Mentions légales</h1><h2>Éditeur du site</h2>' + "".join(lignes)
                + f'<h2>Hébergement</h2><p>{e(heb["nom"])} — {e(heb["adresse"])} — {contact_heb}</p>'
                + "<h2>Médiation de la consommation</h2><p>En cas de litige non résolu avec nous, vous pouvez recourir gratuitement au médiateur de la consommation : "
                + f'{e(med["nom"])}' + (f', {e(med["adresse"])}' if med.get("adresse") else "")
                + f' — <a href="{e(site_med)}" rel="noopener">{e(med["site"])}</a>.</p>'
                + "<h2>Photos et textes</h2><p>Les photos et textes de ce site appartiennent à l'entreprise. Toute reproduction nécessite son accord.</p>"
                + "</div></section>"
            )
            self.page("mentions-legales.html", f'Mentions légales – {ent["nom"]}', f'Mentions légales du site de {ent["nom"]}.', contenu)

        # Confidentialité
        suivi = self.c.get("suivi", {}) or {}
        contenu = (
            '<section class="section"><div class="conteneur"><h1>Confidentialité</h1>'
            f'<p>Responsable du traitement : {e(ent["nom"])}, {e(ent["adresse"]["code_postal"])} {e(ent["adresse"]["ville"])}, {e(ent["email"])}.</p>'
            "<h2>Formulaire de devis</h2>"
            "<p><strong>Pourquoi :</strong> les informations envoyées (nom, téléphone, e-mail, commune, projet, façon dont vous nous avez connus) servent uniquement "
            "à vous recontacter et à établir un devis, à votre demande (mesures précontractuelles, article 6.1.b du RGPD). "
            "La question « Comment nous avez-vous connu ? » nous sert à savoir quelle publicité fonctionne.</p>"
            "<p><strong>Champs obligatoires :</strong> ceux marqués d'une étoile. Sans eux, nous ne pouvons pas traiter votre demande ; vous pouvez aussi nous appeler.</p>"
            "<p><strong>Qui les reçoit :</strong> uniquement notre entreprise. Le formulaire est transmis par le service Formspree (Formspree, Inc., États-Unis), "
            "qui agit pour notre compte et nous les envoie par e-mail. Vos données sont donc transférées aux États-Unis, avec les garanties prévues par Formspree "
            "(voir sa politique de confidentialité sur formspree.io). Elles ne sont ni vendues ni utilisées pour de la publicité.</p>"
            "<p><strong>Combien de temps :</strong> 3 ans après notre dernier échange si vous ne devenez pas client ; si vous devenez client, le temps nécessaire "
            "au chantier et aux obligations légales (factures, garanties).</p>"
            "<h2>Vos droits</h2><p>Vous pouvez demander à consulter, corriger, supprimer vos informations, limiter leur utilisation, vous y opposer ou les récupérer, "
            "en écrivant à l'adresse e-mail ci-dessus. Si vous estimez que vos droits ne sont pas respectés, vous pouvez adresser une réclamation à la CNIL "
            '(<a href="https://www.cnil.fr" rel="noopener">cnil.fr</a>).</p>'
        )
        if suivi.get("google_ads_id"):
            contenu += (
                "<h2>Cookies</h2><p>Seulement si vous cliquez sur « Accepter », un cookie de Google Ads (Google Ireland Ltd / Google LLC) est déposé pour savoir si votre visite vient "
                "d'une de nos annonces et si vous nous avez contactés (mesure de l'efficacité de nos publicités). "
                "Sans votre accord, aucun cookie de mesure n'est déposé. Votre choix (accord ou refus) est conservé 6 mois, puis la question vous est reposée. "
                "Vous pouvez changer d'avis à tout moment avec le lien « Gérer les cookies » en bas de page.</p>"
            )
        else:
            contenu += "<h2>Cookies</h2><p>Ce site ne dépose aucun cookie de mesure ou de publicité.</p>"
        contenu += "</div></section>"
        self.page("confidentialite.html", f'Confidentialité – {ent["nom"]}', f'Utilisation des données personnelles sur le site de {ent["nom"]}.', contenu)

        # Page introuvable (servie automatiquement par Netlify et la plupart des hébergeurs)
        contenu = (
            '<section class="section"><div class="conteneur"><h1>Page introuvable</h1>'
            "<p>Cette page n'existe pas ou a été déplacée.</p>"
            '<div class="actions"><a class="bouton" href="index.html">Retour à l\'accueil</a>'
            '<a class="bouton bouton-secondaire" href="contact.html">Demander un devis</a></div>'
            "</div></section>"
        )
        self.page("404.html", f'Page introuvable – {ent["nom"]}', f'Page introuvable sur le site de {ent["nom"]}.', contenu)

    def fichiers_annexes(self):
        ent = self.c["entreprise"]
        fichiers = {}
        base = (ent.get("site_url") or "").rstrip("/")
        # llms.txt
        lignes = [f'# {ent["nom"]}', "", f'> {self.c["accueil"]["intro"]}', ""]
        lignes.append(f'- Métiers : {", ".join(m["nom"] for m in self.c["metiers"])}')
        lignes.append(f'- Zone d\'intervention : {html.unescape(self.zone_texte())}')
        adr = ent["adresse"]
        if ent.get("afficher_adresse", True):
            lignes.append(f'- Adresse : {adr["rue"]}, {adr["code_postal"]} {adr["ville"]}')
        else:
            lignes.append(f'- Basée à : {adr["code_postal"]} {adr["ville"]}')
        lignes.append(f'- Téléphone : {ent["telephone"]}')
        lignes.append(f'- E-mail : {ent["email"]}')
        if ent.get("horaires"):
            lignes.append(f'- Horaires : {ent["horaires"]}')
        lignes += ["", "## Pages principales", ""]
        lien = (lambda f: f"{base}/{f}") if base else (lambda f: f)
        for m in self.c["metiers"]:
            lignes.append(f'- [{m["nom"]}]({lien(m["slug"] + ".html")}) : {m["intro"]}')
        if self.c.get("realisations"):
            lignes.append(f'- [Réalisations]({lien("realisations.html")}) : chantiers récents avec photos')
        lignes.append(f'- [À propos et questions fréquentes]({lien("a-propos.html")})')
        lignes.append(f'- [Demande de devis]({lien("contact.html")})')
        if self.c.get("faq"):
            lignes += ["", "## Questions fréquentes", ""]
            for q in self.c["faq"]:
                lignes.append(f'- {q["question"]} {q["reponse"]}')
        fichiers["llms.txt"] = "\n".join(lignes) + "\n"
        # robots / sitemap
        robots = "User-agent: *\n" + ("Disallow: /\n" if self.apercu else "Allow: /\n")
        if base and not self.apercu:
            robots += f"Sitemap: {base}/sitemap.xml\n"
            urls = "".join(f"  <url><loc>{e(base + '/' + ('' if f == 'index.html' else f))}</loc></url>\n" for f in self.pages if f not in ("confidentialite.html", "404.html"))
            fichiers["sitemap.xml"] = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
        fichiers["robots.txt"] = robots
        # _redirects (lu par Netlify et Cloudflare Pages) : anciennes adresses → nouvelles pages, redirection permanente
        lignes_redir = []
        for r in self.c.get("redirections", []) or []:
            de, vers = r["de"].strip(), r["vers"].strip()
            cible = vers.lstrip("/").split("#")[0] or "index.html"
            if cible not in self.pages:
                self.avertissements.append(f"Redirection ignorée : la page « {vers} » n'existe pas dans le nouveau site (ancienne adresse {de}).")
                continue
            lignes_redir.append(f"{de} {vers} 301")
        if lignes_redir:
            fichiers["_redirects"] = "\n".join(lignes_redir) + "\n"
        return fichiers

    # ---------- Vérifications de sortie ----------
    def verifier_sortie(self):
        nap = None
        tel = tel_href(self.c["entreprise"]["telephone"])
        for f, h in self.pages.items():
            if re.search(r"\$[a-z_]+", re.sub(r"<script[\s\S]*?</script>", "", h)):
                raise ErreurContenu(f"{f} : variable de gabarit non remplacée.")
            bloc = re.search(r"<div class=\"nap\" data-nap>([\s\S]*?)</div>", h)
            if not bloc:
                raise ErreurContenu(f"{f} : bloc nom/adresse/téléphone absent.")
            if nap is None:
                nap = bloc.group(1)
            elif bloc.group(1) != nap:
                raise ErreurContenu(f"{f} : nom/adresse/téléphone différents des autres pages.")
            if f'href="{tel}"' not in h:
                raise ErreurContenu(f"{f} : numéro cliquable absent.")
            for bloc_json in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', h):
                json.loads(bloc_json.replace("<\\/", "</"))
            for motif in motifs_interdits(re.sub(r"<(script|style)[\s\S]*?</\1>", "", h)):
                raise ErreurContenu(f"{f} : texte interdit dans la page générée : « {motif} »")

    def ecrire(self):
        dest_final = self.ent_dir / "site"
        dest_apercu = self.ent_dir / "site-apercu"
        dest = self.sortie_forcee or (dest_apercu if self.apercu else dest_final)
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        for f, h in self.pages.items():
            (dest / f).write_text(h, encoding="utf-8")
        for f, t in self.fichiers_annexes().items():
            (dest / f).write_text(t, encoding="utf-8")
        (dest / "favicon.svg").write_text(self.favicon(), encoding="utf-8")
        shutil.copy(RACINE / "modeles/site/style.css", dest / "style.css")
        shutil.copy(RACINE / "modeles/site/site.js", dest / "site.js")
        for r in self.c.get("realisations", []):
            for p in r.get("photos", []):
                src = self.ent_dir / "realisations" / r.get("dossier", "") / p["fichier"]
                (dest / "photos" / r["slug"]).mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dest / "photos" / r["slug"] / p["fichier"])
        logo = self.c["entreprise"].get("logo")
        if logo and (self.ent_dir / logo).is_file():
            shutil.copy(self.ent_dir / logo, dest / Path(logo).name)
        if not self.sortie_forcee:
            perime = dest_final if self.apercu else dest_apercu
            if perime.exists():
                shutil.rmtree(perime)
        return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entreprise", default=str(RACINE / "entreprise"))
    ap.add_argument("--sortie", help="dossier de sortie forcé (tests)")
    args = ap.parse_args()
    try:
        g = Generateur(args.entreprise, args.sortie)
        g.controler()
        g.construire()
        g.verifier_sortie()
        dest = g.ecrire()
    except ErreurContenu as err:
        print("ERREUR — rien n'a été écrit :\n" + str(err))
        return 1
    print(f"{len(g.pages)} pages générées dans : {dest}")
    for a in g.avertissements:
        print("Avertissement : " + a)
    if g.blocages:
        print("\nAPERÇU SEULEMENT — mise en ligne bloquée :")
        for b in g.blocages:
            print(" - " + b)
        return 2
    print("\nSite publiable : le dossier à glisser sur l'hébergeur est « entreprise/site ».")
    return 0


if __name__ == "__main__":
    sys.exit(main())
