#!/usr/bin/env python3
"""Calcule les chiffres du mois à partir des exports Google Ads et du journal des devis.

Usage (par l'assistant) :
    python3 outils/bilan.py --mois 2026-10
    python3 outils/bilan.py --mois 2026-10 --rapport --avis-nombre 23 --avis-note 4.8 \
        --test-ia "oui,non,non" --realisations 2

Options utiles :
    --entreprise DOSSIER   (défaut : entreprise/)
    --rapports DOSSIER     (défaut : rapports/)
    --depense 198.40       dépense pub déclarée si aucun export Google Ads
    --aujourdhui AAAA-MM-JJ (tests)

Exports attendus dans <entreprise>/exports/ : AAAA-MM-campagnes.csv (obligatoire pour la dépense),
AAAA-MM-termes.csv, AAAA-MM-lieux.csv, AAAA-MM-horaires.csv (facultatifs). Formats acceptés : .csv
(UTF-8 ou « Excel » UTF-16 à tabulations), .tsv, .xlsx. Le type de rapport est pris dans le nom du
fichier, sinon reconnu d'après les colonnes ; le séparateur, l'encodage et la virgule décimale sont
détectés. La période écrite en tête de l'export est contrôlée : un export qui ne couvre pas
exactement le mois demandé est écarté, avec un message.
"""
import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path
from string import Template

RACINE = Path(__file__).resolve().parent.parent
SOURCES_PUB = {"google-annonce"}
LIB_SOURCES = {
    "google-annonce": "Annonce Google", "google-maps": "Google Maps / fiche", "google-recherche": "Google (sans précision)",
    "site": "Site", "facebook": "Facebook", "instagram": "Instagram", "assistant-ia": "Assistant IA",
    "bouche-a-oreille": "Bouche-à-oreille", "ancien-client": "Ancien client", "panneau-chantier": "Panneau / véhicule",
    "annuaire": "Annuaire / plateforme", "autre": "Autre", "inconnu": "Inconnu",
}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
COLS = {
    "cout": ["coût", "cout", "cost"],
    "conversions": ["conversions", "conv."],
    "clics": ["clics", "clicks"],
    "impressions": ["impr.", "impressions"],
    "campagne": ["campagne", "campaign"],
    "terme": ["terme de recherche", "search term"],
    "lieu": ["lieu correspondant", "lieu de l'utilisateur", "ville", "city", "matched location", "user location", "emplacement", "location"],
    "jour": ["jour de la semaine", "day of week", "day of the week"],
    "heure": ["heure de la journée", "heure", "hour of day", "hour"],
}


def norm(t):
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t).strip()


def nombre(v):
    s = str(v or "").strip().replace(" ", "").replace(" ", "").replace(" ", "")
    s = re.sub(r"[€%$]|EUR", "", s)
    if s in ("", "--", "-", "—"):
        return 0.0
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def lire_xlsx(chemin):
    """Première feuille d'un .xlsx, rendue en texte à tabulations.

    Lecture par expressions régulières (pas de module XML : certains Python n'ont pas « expat »)."""
    from html import unescape

    def textes(bloc):
        return "".join(unescape(x) for x in re.findall(r"<(?:\w+:)?t(?:\s[^>]*)?>(.*?)</(?:\w+:)?t>", bloc, re.S))

    with zipfile.ZipFile(chemin) as z:
        noms = z.namelist()
        partages = []
        if "xl/sharedStrings.xml" in noms:
            xml = z.read("xl/sharedStrings.xml").decode("utf-8")
            partages = [textes(si) for si in re.findall(r"<(?:\w+:)?si>(.*?)</(?:\w+:)?si>", xml, re.S)]
        feuilles = sorted((n for n in noms if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)),
                          key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[1]).group(1)))
        if not feuilles:
            raise ValueError(f"{chemin} : aucune feuille trouvée dans le fichier Excel.")
        xml = z.read(feuilles[0]).decode("utf-8")
    lignes = []
    for row in re.findall(r"<(?:\w+:)?row\b[^>]*>(.*?)</(?:\w+:)?row>", xml, re.S):
        cellules = {}
        for attrs, corps in re.findall(r"<(?:\w+:)?c\b([^>]*?)(?:/>|>(.*?)</(?:\w+:)?c>)", row, re.S):
            ref = re.search(r'\br="([A-Z]+)\d+"', attrs)
            col = 0
            for lettre in (ref.group(1) if ref else "A"):
                col = col * 26 + ord(lettre) - 64
            typ = re.search(r'\bt="(\w+)"', attrs)
            typ = typ.group(1) if typ else ""
            v = re.search(r"<(?:\w+:)?v>(.*?)</(?:\w+:)?v>", corps or "", re.S)
            if typ == "s" and v:
                val = partages[int(v.group(1))]
            elif typ == "inlineStr":
                val = textes(corps)
            else:
                val = unescape(v.group(1)) if v else ""
            cellules[col] = val.replace("\t", " ").replace("\n", " ")
        if cellules:
            lignes.append("\t".join(cellules.get(i, "") for i in range(1, max(cellules) + 1)))
    return "\n".join(lignes)


def lire_texte(chemin):
    if Path(chemin).suffix.lower() == ".xlsx":
        return lire_xlsx(chemin)
    brut = Path(chemin).read_bytes()
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            t = brut.decode(enc)
            if "\x00" not in t:
                return t
        except UnicodeDecodeError:
            continue
    return brut.decode("utf-8", "replace")


MOIS_NOMS = {
    "jan": 1, "janv": 1, "janvier": 1, "january": 1, "fev": 2, "fevr": 2, "fevrier": 2, "feb": 2, "february": 2,
    "mars": 3, "mar": 3, "march": 3, "avr": 4, "avril": 4, "apr": 4, "april": 4, "mai": 5, "may": 5,
    "juin": 6, "jun": 6, "june": 6, "juil": 7, "juillet": 7, "jul": 7, "july": 7, "aout": 8, "aug": 8, "august": 8,
    "sept": 9, "sep": 9, "septembre": 9, "september": 9, "oct": 10, "octobre": 10, "october": 10,
    "nov": 11, "novembre": 11, "november": 11, "dec": 12, "decembre": 12, "december": 12,
}
TYPES_FICHIER = {"campagnes": "campagnes", "termes": "termes", "lieux": "lieux", "horaires": "horaires"}
RX_TOTAL = re.compile(r"^total(?:\s*[:\-–]|$)")
TERMES_MASQUES = ("autres termes de recherche", "other search terms", "autres termes")


def dates_dans(texte):
    """Dates écrites dans l'en-tête d'un export (français, anglais, ISO, JJ/MM/AAAA)."""
    n = norm(texte)
    trouvees = []
    for a, m, j in re.findall(r"(\d{4})-(\d{1,2})-(\d{1,2})", n):
        trouvees.append((int(a), int(m), int(j)))
    for j, m, a in re.findall(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", n):
        trouvees.append((int(a), int(m), int(j)))
    for j, nom, a in re.findall(r"\b(\d{1,2})(?:er)? ([a-z]+)\.? (\d{4})\b", n):
        if nom in MOIS_NOMS:
            trouvees.append((int(a), MOIS_NOMS[nom], int(j)))
    for nom, j, a in re.findall(r"\b([a-z]+)\.? (\d{1,2}),? (\d{4})\b", n):
        if nom in MOIS_NOMS:
            trouvees.append((int(a), MOIS_NOMS[nom], int(j)))
    dates = []
    for a, m, j in trouvees:
        try:
            dates.append(dt.date(a, m, j))
        except ValueError:
            pass
    return dates


def periode_export(chemin):
    """(début, fin) lus dans les lignes au-dessus des colonnes, ou None."""
    lignes = lire_texte(chemin).splitlines()[:15]
    avant = []
    for l in lignes:
        if any(a in norm(l) for a in COLS["cout"]) and ("," in l or "\t" in l or ";" in l):
            break
        avant.append(l)
    dates = dates_dans("\n".join(avant))
    return (min(dates), max(dates)) if dates else None


def bornes_mois(mois):
    a, m = map(int, mois.split("-"))
    debut = dt.date(a, m, 1)
    fin = (dt.date(a + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1))
    return debut, fin


def lire_export(chemin):
    """Renvoie (type, lignes) où lignes = liste de dicts avec clés normalisées."""
    texte = lire_texte(chemin)
    lignes_brutes = texte.splitlines()
    idx_entete, sep = None, ","
    for i, l in enumerate(lignes_brutes[:15]):
        n = norm(l)
        if any(a in n for a in COLS["cout"]) and ("," in l or "\t" in l or ";" in l):
            idx_entete = i
            sep = max([",", "\t", ";"], key=l.count)
            break
    if idx_entete is None:
        raise ValueError(f"{chemin} : colonne « Coût » introuvable.")
    lecteur = csv.reader(io.StringIO("\n".join(lignes_brutes[idx_entete:])), delimiter=sep)
    entete = [norm(c) for c in next(lecteur)]

    def colonne(cle):
        for alias in COLS[cle]:
            for j, c in enumerate(entete):
                if c == norm(alias):
                    return j
        for alias in COLS[cle]:
            for j, c in enumerate(entete):
                if c.startswith(norm(alias)) and "/" not in c and "taux" not in c and "cout/" not in c:
                    return j
        return None

    idx = {k: colonne(k) for k in COLS}
    indice = next((v for k, v in TYPES_FICHIER.items() if Path(chemin).stem.endswith("-" + k)), None)
    if indice:
        type_ = indice
    elif idx["terme"] is not None:
        type_ = "termes"
    elif idx["jour"] is not None or (idx["heure"] is not None and idx["campagne"] is None):
        type_ = "horaires"
    elif idx["lieu"] is not None:
        type_ = "lieux"
    else:
        type_ = "campagnes"
    lignes = []
    for row in lecteur:
        if not row or not any(c.strip() for c in row):
            continue
        if any(RX_TOTAL.match(norm(c)) for c in row[:3] if c):
            continue
        d = {}
        for k, j in idx.items():
            if j is not None and j < len(row):
                d[k] = row[j]
        for k in ("cout", "conversions", "clics", "impressions"):
            d[k] = nombre(d.get(k))
        lignes.append(d)
    return type_, lignes


def lire_journal(chemin):
    if not Path(chemin).exists():
        return []
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.DictReader(f))
    for l in lignes:
        l["statut"] = norm(l.get("statut", "")).replace("signe", "signé")
        l["source"] = (l.get("source") or "inconnu").strip() or "inconnu"
        l["montant"] = nombre(l.get("montant_signe"))
    return lignes


def mois_precedent(m):
    a, mo = map(int, m.split("-"))
    return f"{a - 1}-12" if mo == 1 else f"{a}-{mo - 1:02d}"


def mois_lettres(m):
    a, mo = map(int, m.split("-"))
    return f"{MOIS[mo - 1]} {a}"


def euros(v, dec=True):
    if v is None:
        return "—"
    s = f"{v:,.2f}" if dec else f"{v:,.0f}"
    return s.replace(",", " ").replace(".", ",") + " €"


def zone_communes(ent_dir):
    f = Path(ent_dir) / "site-contenu.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))["entreprise"]["zone"]["communes"]
        except (KeyError, json.JSONDecodeError):
            pass
    p = Path(ent_dir) / "profil.md"
    if p.exists():
        m = re.search(r"Zone d'intervention[^:]*:\s*(.+)", p.read_text(encoding="utf-8"))
        if m and "non renseign" not in m.group(1):
            return [c.strip() for c in re.split(r"[,;]", re.sub(r"\(.*?\)", "", m.group(1))) if c.strip()]
    return []


def calculer(mois, ent_dir, journal, depense_declaree=None, aujourdhui=None):
    exports = {}
    avertissements = []
    debut, fin = bornes_mois(mois)
    fichiers = sorted(f for f in (Path(ent_dir) / "exports").glob(f"{mois}-*")
                      if f.suffix.lower() in (".csv", ".tsv", ".xlsx", ".txt"))
    for f in fichiers:
        try:
            periode = periode_export(f)
            if periode and periode != (debut, fin):
                avertissements.append(
                    f"{f.name} couvre du {periode[0].strftime('%d/%m/%Y')} au {periode[1].strftime('%d/%m/%Y')}, "
                    f"pas le mois entier : fichier écarté. Refaire l'export avec la période « Le mois dernier ».")
                continue
            if not periode:
                avertissements.append(f"{f.name} : période non indiquée dans le fichier, vérifiez qu'il couvre bien {mois_lettres(mois)}.")
            t, lignes = lire_export(f)
            exports.setdefault(t, []).extend(lignes)
        except (ValueError, zipfile.BadZipFile, IndexError, UnicodeDecodeError) as err:
            avertissements.append(f"{f.name} illisible : {err}")
    for a in avertissements:
        print("Attention :", a, file=sys.stderr)
    r = {"mois": mois, "exports": sorted(exports), "avertissements": avertissements}
    if "campagnes" in exports:
        r["depense"] = round(sum(l["cout"] for l in exports["campagnes"]), 2)
        r["conversions_google"] = round(sum(l["conversions"] for l in exports["campagnes"]), 2)
        r["clics"] = int(sum(l["clics"] for l in exports["campagnes"]))
        r["source_depense"] = "export Google Ads"
    elif depense_declaree is not None:
        r["depense"], r["conversions_google"], r["clics"] = depense_declaree, None, None
        r["source_depense"] = "déclarée par le gérant"
    else:
        r["depense"] = r["conversions_google"] = r["clics"] = None
        r["source_depense"] = "inconnue"

    du_mois = [l for l in journal if (l.get("date") or "").startswith(mois)]
    pubs = [l for l in du_mois if l["source"] in SOURCES_PUB]
    signes = [l for l in du_mois if l["statut"] == "signé"]
    signes_pubs = [l for l in pubs if l["statut"] == "signé"]
    par_source = {}
    for l in du_mois:
        par_source[l["source"]] = par_source.get(l["source"], 0) + 1
    r.update({
        "demandes": len(du_mois),
        "demandes_pubs": len(pubs),
        "par_source": dict(sorted(par_source.items(), key=lambda kv: (-kv[1], kv[0]))),
        "signes": len(signes),
        "signes_pubs": len(signes_pubs),
        "ca_signe": round(sum(l["montant"] for l in signes), 2),
        "ca_signe_pubs": round(sum(l["montant"] for l in signes_pubs), 2),
        "en_attente": sum(1 for l in du_mois if l["statut"] == "en attente"),
        "perdus": sum(1 for l in du_mois if l["statut"] == "perdu"),
    })
    r["cout_par_demande_pubs"] = round(r["depense"] / len(pubs), 2) if r["depense"] is not None and pubs else None
    r["cout_par_conversion_google"] = (
        round(r["depense"] / r["conversions_google"], 2) if r.get("conversions_google") else None)
    r["cout_par_devis_signe_pubs"] = round(r["depense"] / len(signes_pubs), 2) if r["depense"] is not None and signes_pubs else None

    # Analyses
    if "termes" in exports:
        masques = [l for l in exports["termes"] if norm(l.get("terme", "")) in TERMES_MASQUES]
        r["depense_termes_masques"] = round(sum(l["cout"] for l in masques), 2)
        sans = [l for l in exports["termes"] if l["cout"] > 0 and l["conversions"] == 0 and l not in masques]
        r["termes_sans_demande"] = [{"terme": l.get("terme", ""), "cout": round(l["cout"], 2), "clics": int(l["clics"])}
                                    for l in sorted(sans, key=lambda x: -x["cout"])[:10]]
        r["depense_termes_sans_demande"] = round(sum(l["cout"] for l in sans), 2)
    if "lieux" in exports:
        zone = [norm(c) for c in zone_communes(ent_dir)]
        hors = [l for l in exports["lieux"] if l["cout"] > 0 and zone and not any(z in norm(l.get("lieu", "")) for z in zone)]
        r["lieux_hors_zone"] = [{"lieu": l.get("lieu", ""), "cout": round(l["cout"], 2), "conversions": l["conversions"]}
                                for l in sorted(hors, key=lambda x: -x["cout"])[:10]]
        r["zone_utilisee"] = zone_communes(ent_dir)
    if "horaires" in exports:
        cles = [k for k in ("jour", "heure") if any(k in l for l in exports["horaires"])]
        agg = {}
        for l in exports["horaires"]:
            k = " ".join(str(l.get(c, "")) for c in cles)
            a = agg.setdefault(k, {"cout": 0.0, "conversions": 0.0})
            a["cout"] += l["cout"]
            a["conversions"] += l["conversions"]
        r["creneaux_sans_demande"] = [{"creneau": k, "cout": round(v["cout"], 2)}
                                      for k, v in sorted(agg.items(), key=lambda kv: -kv[1]["cout"]) if v["cout"] > 0 and v["conversions"] == 0][:5]

    ref = aujourdhui or dt.date.today()
    attente = []
    for l in journal:
        try:
            d = dt.date.fromisoformat(l["date"])
        except (ValueError, KeyError):
            continue
        if l["statut"] == "en attente" and (ref - d).days > 30:
            attente.append({"date": l["date"], "client": l.get("nom_client", ""), "type": l.get("type_chantier", "")})
    r["en_attente_plus_30j"] = attente
    return r


def texte_resume(r):
    o = [f"=== {mois_lettres(r['mois'])} ==="]
    o.append(f"Dépense pub : {euros(r['depense'])} ({r['source_depense']})")
    o.append(f"Demandes de devis (journal) : {r['demandes']} dont {r['demandes_pubs']} venant des annonces Google")
    conv = "—" if r["conversions_google"] is None else f"{r['conversions_google']:g}".replace(".", ",")
    o.append(f"Demandes comptées par Google Ads : {conv}")
    o.append(f"Coût par demande (annonces, d'après le journal) : {euros(r['cout_par_demande_pubs'])}")
    o.append(f"Coût par demande comptée par Google : {euros(r['cout_par_conversion_google'])}")
    o.append(f"Devis signés : {r['signes']} ({euros(r['ca_signe'], False)}) dont annonces : {r['signes_pubs']} ({euros(r['ca_signe_pubs'], False)})")
    o.append("Par source : " + (", ".join(f"{LIB_SOURCES.get(k, k)} {v}" for k, v in r["par_source"].items()) or "aucune demande"))
    if r.get("termes_sans_demande"):
        o.append(f"Recherches payées sans demande : {euros(r['depense_termes_sans_demande'])} au total. Principales :")
        o += [f"  - « {t['terme']} » : {euros(t['cout'])} ({t['clics']} clics)" for t in r["termes_sans_demande"][:5]]
    if r.get("lieux_hors_zone"):
        o.append("Lieux absents de votre liste de communes qui ont coûté (certains peuvent être dans votre rayon) :")
        o += [f"  - {l['lieu']} : {euros(l['cout'])}" for l in r["lieux_hors_zone"][:5]]
    if r.get("creneaux_sans_demande"):
        o.append("Créneaux qui ont coûté sans demande : " + ", ".join(f"{c['creneau']} ({euros(c['cout'])})" for c in r["creneaux_sans_demande"]))
    if r.get("depense_termes_masques"):
        o.append(f"Recherches non détaillées par Google (« autres termes ») : {euros(r['depense_termes_masques'])}, impossibles à exclure une par une.")
    if r["en_attente_plus_30j"]:
        o.append(f"Devis en attente depuis plus de 30 jours : {len(r['en_attente_plus_30j'])}")
    for a in r.get("avertissements", []):
        o.append("ATTENTION : " + a)
    return "\n".join(o)


def releves_manuels(r, args):
    """Ajoute au résultat les relevés faits par le gérant (avis, test IA, réalisations)."""
    if args.avis_nombre is None:
        r["avis_texte"] = "non relevé"
    else:
        note = f", note {str(args.avis_note).replace('.', ',')}/5" if args.avis_note is not None else ""
        r["avis_texte"] = f"{args.avis_nombre} avis{note}"
    if args.test_ia:
        rep = [norm(x) for x in args.test_ia.split(",")]
        r["test_ia_texte"] = f"{sum(1 for x in rep if x == 'oui')} sur {len(rep)}"
    else:
        r["test_ia_texte"] = "non fait"
    r["realisations_texte"] = str(args.realisations) if args.realisations is not None else "non compté"


def ecrire_rapport(r, p, args, ent_dir, rapports_dir):
    nom = ""
    profil = Path(ent_dir) / "profil.md"
    if profil.exists():
        m = re.search(r"Nom commercial\s*:\s*(.+)", profil.read_text(encoding="utf-8"))
        if m and "non renseign" not in m.group(1):
            nom = " — " + re.sub(r"\s*\(.*?\)\s*$", "", m.group(1)).strip()
    prec_donnees = Path(rapports_dir) / f"donnees-{p['mois']}.json"
    avis_prec = test_prec = real_prec = "—"
    if prec_donnees.exists():
        d = json.loads(prec_donnees.read_text(encoding="utf-8"))
        avis_prec = d.get("avis_texte", "—")
        test_prec = d.get("test_ia_texte", "—")
        real_prec = d.get("realisations_texte", "—")


    def ligne(lib, a, b):
        return f"| {lib} | {a} | {b} |"

    def n(v):
        return "—" if v is None else (f"{v:g}".replace(".", ",") if isinstance(v, float) else str(v))

    lignes = [
        ligne("Demandes de devis (toutes origines)", r["demandes"], p["demandes"]),
        ligne("… dont venant des annonces Google (selon le client)", r["demandes_pubs"], p["demandes_pubs"]),
        ligne("Dépense Google Ads", euros(r["depense"]), euros(p["depense"])),
        ligne("**Coût par demande venant des annonces**", f"**{euros(r['cout_par_demande_pubs'])}**", euros(p["cout_par_demande_pubs"])),
        ligne("Demandes comptées par Google Ads", n(r["conversions_google"]), n(p["conversions_google"])),
        ligne("Devis signés (demandes du mois)", r["signes"], p["signes"]),
        ligne("… dont venant des annonces", r["signes_pubs"], p["signes_pubs"]),
        ligne("Chiffre d'affaires signé (demandes du mois)", euros(r["ca_signe"], False), euros(p["ca_signe"], False)),
        ligne("… dont venant des annonces", euros(r["ca_signe_pubs"], False), euros(p["ca_signe_pubs"], False)),
        ligne("Avis Google (fin de mois)", r["avis_texte"], avis_prec),
        ligne("Réalisations ajoutées", r["realisations_texte"], real_prec),
        ligne("Questions où un assistant IA cite l'entreprise", r["test_ia_texte"], test_prec),
    ]
    sources = ", ".join(f"{LIB_SOURCES.get(k, k)} : {v}" for k, v in r["par_source"].items()) or "aucune demande notée"
    alertes = []
    if r.get("termes_sans_demande"):
        top = ", ".join(f"« {t['terme']} » ({euros(t['cout'])})" for t in r["termes_sans_demande"][:3])
        alertes.append(f"- Recherches payées sans aucune demande : {euros(r['depense_termes_sans_demande'])} ce mois-ci, surtout {top}.")
    if r.get("lieux_hors_zone"):
        alertes.append("- Annonces payées dans des communes absentes de votre liste (certaines peuvent être dans votre rayon) : " + ", ".join(f"{l['lieu'].split(',')[0]} ({euros(l['cout'])})" for l in r["lieux_hors_zone"][:3]) + ".")
    if r["en_attente_plus_30j"]:
        alertes.append(f"- {len(r['en_attente_plus_30j'])} devis toujours « en attente » depuis plus de 30 jours : à relancer ou à classer.")
    limites = [
        "- L'origine des demandes est celle que les clients déclarent : elle peut être imprécise.",
        "- Les montants signés concernent les demandes reçues ce mois-ci ; un devis signé plus tard sera ajouté au prochain bilan.",
        "- Google ne compte pas les visiteurs qui refusent les cookies ni les appels passés directement.",
    ]
    if r["demandes"] < 10:
        limites.insert(0, f"- Petit volume ({r['demandes']} demandes) : une demande de plus ou de moins change beaucoup les résultats. Regardez la tendance sur 3 mois.")
    for a in r.get("avertissements", []):
        if "écarté" in a or "illisible" in a:
            limites.append("- Export écarté : " + a)
    if r["source_depense"] != "export Google Ads":
        limites.append(f"- Dépense {r['source_depense']}, sans export Google Ads.")
    modele = Template((RACINE / "modeles/rapports/bilan-mensuel.md").read_text(encoding="utf-8"))
    contenu = modele.substitute(
        titre=("Bilan d'" if mois_lettres(r["mois"])[0] in "aeiouéû" else "Bilan de ") + mois_lettres(r["mois"]) + nom,
        mois=mois_lettres(r["mois"]).capitalize(),
        mois_prec=mois_lettres(p["mois"]).capitalize(),
        tableau="\n".join(lignes),
        sources=sources,
        alertes="\n".join(alertes) if alertes else "- Rien d'anormal repéré dans les exports.",
        limites="\n".join(limites),
        date=dt.date.today().isoformat(),
    )
    Path(rapports_dir).mkdir(parents=True, exist_ok=True)
    sortie = Path(rapports_dir) / f"{r['mois']}.md"
    sortie.write_text(contenu, encoding="utf-8")
    return sortie


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mois", required=True, help="AAAA-MM")
    ap.add_argument("--entreprise", default=str(RACINE / "entreprise"))
    ap.add_argument("--rapports", default=str(RACINE / "rapports"))
    ap.add_argument("--depense", type=float)
    ap.add_argument("--rapport", action="store_true", help="écrit rapports/AAAA-MM.md")
    ap.add_argument("--avis-nombre", type=int)
    ap.add_argument("--avis-note", type=float)
    ap.add_argument("--test-ia", help='ex. "oui,non,non"')
    ap.add_argument("--realisations", type=int)
    ap.add_argument("--aujourdhui")
    args = ap.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}", args.mois):
        print("Format du mois attendu : AAAA-MM")
        return 1
    auj = dt.date.fromisoformat(args.aujourdhui) if args.aujourdhui else None
    journal = lire_journal(Path(args.entreprise) / "journal-devis.csv")
    r = calculer(args.mois, args.entreprise, journal, args.depense, auj)
    releves_manuels(r, args)
    p = calculer(mois_precedent(args.mois), args.entreprise, journal, None, auj)
    print(texte_resume(r))
    print()
    print(texte_resume(p))
    if args.rapport:
        sortie = ecrire_rapport(r, p, args, args.entreprise, args.rapports)
        print(f"\nRapport écrit : {sortie} — compléter les deux parties marquées « À COMPLÉTER PAR L'ASSISTANT ».")
    Path(args.rapports).mkdir(parents=True, exist_ok=True)
    (Path(args.rapports) / f"donnees-{args.mois}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
