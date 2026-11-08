#!/usr/bin/env python3
"""Refuse tout texte provisoire avant publication (site, annonces, posts, réponses aux avis, rapports).

Usage (par l'assistant) :
    python3 outils/verifier_publication.py <fichier ou dossier> [...]
    echo "texte" | python3 outils/verifier_publication.py -

Code de sortie 0 = rien à signaler, 1 = au moins un problème (listé).
Pour les fichiers HTML, seuls le texte visible et les attributs lus par les visiteurs
ou par Google (alt, title, content, placeholder, aria-label) sont contrôlés.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

MOTIFS = [
    (r"\[[^\]\n]{0,80}\](?!\()", "texte entre crochets"),
    (r"\{\{|\}\}", "accolades de gabarit"),
    (r"<\s*(?:ins[ée]rer|nom|ville|t[ée]l[ée]phone|prenom|prénom)[^>]*>", "balise à remplacer"),
    (r"\b[àa] (?:compl[ée]ter|remplir)\b", "« à compléter / à remplir »"),
    # « à définir », « à préciser »… seulement en fin de phrase ou entre parenthèses
    # (« Prix à définir. ») : « travaux à définir avec vous sur place » reste autorisé.
    (r"\b[àa] (?:d[ée]finir|pr[ée]ciser|confirmer|v[ée]rifier)\s*(?=$|[.;:!?,)\]»]|\n)", "« à définir / à préciser … »"),
    (r"\bnon renseign[ée]e?s?\b", "« non renseigné »"),
    (r"\blorem\b|\bipsum\b", "faux texte « lorem ipsum »"),
    (r"\bX{2,}\b|\bx{3,}\b|\b0{2} ?0{2} ?0{2} ?0{2} ?0{2}\b", "« XX / XXX » ou numéro factice"),
    (r"\?{2,}", "« ?? »"),
    (r"\b(?:TODO|TBD|TBC|FIXME)\b", "note interne (TODO…)"),
    (r"\bplaceholder\b", "« placeholder »"),
    (r"\bins[ée]rer ici\b|\b(?:votre|son|le|ton) (?:ville|nom|entreprise|num[ée]ro|texte|t[ée]l[ée]phone|adresse|lien|prix|m[ée]tier) ici\b", "« … ici »"),
    (r"\bexemple\.(?:fr|com)\b|@exemple\b|example\.(?:com|org)\b", "adresse d'exemple"),
]
_COMPILES = [(re.compile(m, re.IGNORECASE), lib) for m, lib in MOTIFS]


def motifs_interdits(texte):
    """Renvoie la liste des extraits problématiques trouvés dans un texte."""
    trouves = []
    for rx, lib in _COMPILES:
        for m in rx.finditer(texte or ""):
            trouves.append(f"{m.group(0)} ({lib})")
    return trouves


class _Visible(HTMLParser):
    ATTRS = {"alt", "title", "content", "placeholder", "aria-label", "data-confirmation", "data-erreur", "value"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.morceaux = []
        self._ignore = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._ignore += 1
        for k, v in attrs:
            if k in self.ATTRS and v:
                self.morceaux.append(v)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._ignore:
            self._ignore -= 1

    def handle_data(self, data):
        if not self._ignore:
            self.morceaux.append(data)


def texte_a_controler(chemin, contenu):
    if chemin.suffix.lower() in (".html", ".htm"):
        p = _Visible()
        p.feed(contenu)
        return "\n".join(p.morceaux)
    return contenu


def controler_fichier(chemin):
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return motifs_interdits(texte_a_controler(chemin, contenu))


def main(args):
    if not args:
        print(__doc__)
        return 1
    problemes = []
    for a in args:
        if a == "-":
            for m in motifs_interdits(sys.stdin.read()):
                problemes.append(("(texte)", m))
            continue
        p = Path(a)
        fichiers = [p] if p.is_file() else [f for f in p.rglob("*") if f.suffix.lower() in (".html", ".htm", ".txt", ".md", ".xml", ".json", ".csv")]
        for f in fichiers:
            for m in controler_fichier(f):
                problemes.append((str(f), m))
    if problemes:
        print("À CORRIGER avant toute publication :")
        for f, m in problemes:
            print(f" - {f} : {m}")
        return 1
    print("OK : aucun texte provisoire détecté.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
