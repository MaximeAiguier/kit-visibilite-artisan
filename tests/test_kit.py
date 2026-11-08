#!/usr/bin/env python3
"""Tests automatiques du kit (bibliothèque standard uniquement).

    python3 tests/test_kit.py           # tests Python
    python3 tests/test_kit.py --navigateur  # + tests navigateur (nécessite Node + Playwright)
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
OUTILS = RACINE / "outils"
EXEMPLE = RACINE / "exemples" / "val-renovation"
FICTIVE = RACINE / "tests" / "fixtures" / "entreprise-fictive"
sys.path.insert(0, str(OUTILS))

import bilan  # noqa: E402
import verifier_publication as vp  # noqa: E402


def lancer(*args):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, cwd=RACINE)
    return r.returncode, r.stdout + r.stderr


class Kit(unittest.TestCase):
    def test_verifier_kit(self):
        code, sortie = lancer(OUTILS / "verifier_kit.py")
        self.assertEqual(code, 0, sortie)

    def test_empaquetage(self):
        import zipfile
        with tempfile.TemporaryDirectory() as d:
            code, sortie = lancer(OUTILS / "empaqueter.py", "--sortie", d)
            self.assertEqual(code, 0, sortie)
            noms = zipfile.ZipFile(next(Path(d).glob("*.zip"))).namelist()
            self.assertIn("kit-visibilite-artisan/.claude/skills/demarrage/SKILL.md", noms)
            self.assertIn("kit-visibilite-artisan/.agents/skills/demarrage/SKILL.md", noms)
            self.assertFalse([n for n in noms if "/exemples/" in n or "/tests/" in n or ".DS_Store" in n or "__pycache__" in n])

    def test_livraison_refuse_fichier_parasite(self):
        with tempfile.TemporaryDirectory() as d:
            copie = Path(d) / "kit"
            shutil.copytree(RACINE, copie, ignore=shutil.ignore_patterns("exemples", "tests", "__pycache__"))
            code, sortie = lancer(copie / "outils" / "verifier_kit.py", "--livraison")
            self.assertEqual(code, 0, sortie)
            (copie / "rapport-test-codex.md").write_text("test", encoding="utf-8")
            code, sortie = lancer(copie / "outils" / "verifier_kit.py", "--livraison")
            self.assertEqual(code, 1, sortie)
            self.assertIn("rapport-test-codex.md", sortie)

    def test_synchro_skills(self):
        code, sortie = lancer(OUTILS / "synchroniser_skills.py", "--verifier")
        self.assertEqual(code, 0, sortie)


class TextesProvisoires(unittest.TestCase):
    def test_detecte(self):
        for t in ["Appelez le [TÉLÉPHONE]", "Texte à compléter", "Lorem ipsum", "Tel : XXX", "{{NOM}}", "TODO relire",
                  "Zone : (non renseigné)", "contact@exemple.fr", "Votre ville ici", "Prix à définir",
                  # faux négatifs corrigés en novembre 2026
                  "Prix : XX €", "Appelez le 06 XX XX XX XX", "Votre texte ici", "?? €", "TBC", "Délai : à préciser."]:
            self.assertTrue(vp.motifs_interdits(t), t)

    def test_laisse_passer(self):
        for t in ["Ravalement de façade à Arnage, par exemple sur une maison des années 70.",
                  "Voir [la page devis](contact.html).", "Nous vous rappelons sous 48 heures ouvrées.",
                  # faux positifs corrigés en novembre 2026
                  "Les finitions sont à définir avec vous sur place.", "Un projet ? Appelez-nous.", "Taille XXL", "Grandval (99)"]:
            self.assertFalse(vp.motifs_interdits(t), t)

    def test_html_ignore_scripts(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.html"
            f.write_text('<p>Bonjour</p><script>var a=[1,2];</script><img alt="photo [à compléter]">', encoding="utf-8")
            pb = vp.controler_fichier(f)
            self.assertEqual(len(pb), 2)  # le alt fautif (crochets + « à compléter »), pas le script


class Site(unittest.TestCase):
    def generer(self, dossier, sortie):
        return lancer(OUTILS / "generer_site.py", "--entreprise", dossier, "--sortie", sortie)

    def copie_fictive(self, d, modif):
        cible = Path(d) / "ent"
        shutil.copytree(FICTIVE, cible)
        c = json.loads((cible / "site-contenu.json").read_text(encoding="utf-8"))
        modif(c)
        (cible / "site-contenu.json").write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")
        return cible

    def test_mentions_legales_ei_mediateur_hebergeur(self):
        def ei(c):
            L = c["legal"]
            L.update(forme_juridique="micro-entrepreneur", raison_sociale="Camille Test", capital="",
                     immatriculation="RNE – SIREN 123 456 789", tva_intracom="", tva_non_applicable=True,
                     adresse_domiciliation="5 rue du Bureau, 99000 Ville-Test")
            L["hebergeur"] = {"nom": "Netlify, Inc.", "adresse": "101 2nd Street, San Francisco, CA 94105", "contact": "https://www.netlify.com/support/"}
        with tempfile.TemporaryDirectory() as d:
            s = Path(d) / "s"
            code, sortie = self.generer(self.copie_fictive(d, ei), s)
            self.assertEqual(code, 0, sortie)
            self.assertIn("ne publie pas de téléphone", sortie)
            h = (s / "mentions-legales.html").read_text(encoding="utf-8")
            for attendu in ["Camille Test EI", "entrepreneur individuel", "5 rue du Bureau", "RNE", "Médiation de la consommation",
                            "https://mediateur-test.example", "https://www.netlify.com/support/", "293 B"]:
                self.assertIn(attendu, h)
            c = (s / "confidentialite.html").read_text(encoding="utf-8")
            for attendu in ["6.1.b", "États-Unis", "3 ans", "CNIL", "obligatoires"]:
                self.assertIn(attendu, c)
        # sans médiateur, ou avec l'ancien « RM », ou sans téléphone ni contact d'hébergeur : page bloquée
        for modif, motif in [(lambda c: c["legal"].pop("mediateur"), "médiateur"),
                             (lambda c: c["legal"].update(immatriculation="RM 72"), "Répertoire des métiers"),
                             (lambda c: c["legal"]["hebergeur"].pop("telephone"), "téléphone de l'hébergeur")]:
            with tempfile.TemporaryDirectory() as d:
                code, sortie = self.generer(self.copie_fictive(d, modif), Path(d) / "s")
                self.assertEqual(code, 2, sortie)
                self.assertIn(motif, sortie)
                self.assertFalse((Path(d) / "s" / "mentions-legales.html").exists())

    def test_redirections_ancien_site(self):
        def redir(c):
            c["redirections"] = [{"de": "/nos-services/plomberie/", "vers": "/plomberie.html"},
                                 {"de": "/contactez-nous", "vers": "/contact.html"},
                                 {"de": "/page-disparue", "vers": "/inexistante.html"}]
        with tempfile.TemporaryDirectory() as d:
            s = Path(d) / "s"
            code, sortie = self.generer(self.copie_fictive(d, redir), s)
            self.assertEqual(code, 0, sortie)
            r = (s / "_redirects").read_text(encoding="utf-8")
            self.assertEqual(r, "/nos-services/plomberie/ /plomberie.html 301\n/contactez-nous /contact.html 301\n")
            self.assertIn("Redirection ignorée", sortie)
        with tempfile.TemporaryDirectory() as d:
            code, sortie = self.generer(self.copie_fictive(d, lambda c: c.update(redirections=[{"de": "ancienne", "vers": "/"}])), Path(d) / "s")
            self.assertNotEqual(code, 0)
            self.assertIn("Redirection invalide", sortie)
        with tempfile.TemporaryDirectory() as d:
            s = Path(d) / "s"
            code, sortie = self.generer(FICTIVE, s)
            self.assertFalse((s / "_redirects").exists())

    def test_exemple_apercu_bloque(self):
        with tempfile.TemporaryDirectory() as d:
            code, sortie = self.generer(EXEMPLE / "entreprise", Path(d) / "s")
            self.assertEqual(code, 2, sortie)
            for attendu in ["SIRET", "0 réalisation", "Données simulées"]:
                self.assertIn(attendu, sortie)
            self.assertFalse((Path(d) / "s" / "mentions-legales.html").exists())
            html = (Path(d) / "s" / "index.html").read_text(encoding="utf-8")
            self.assertIn("APERÇU", html)
            self.assertIn('content="noindex"', html)
            self.assertIn("Disallow: /", (Path(d) / "s" / "robots.txt").read_text())

    def test_fictive_publiable(self):
        with tempfile.TemporaryDirectory() as d:
            s = Path(d) / "s"
            code, sortie = self.generer(FICTIVE, s)
            self.assertEqual(code, 0, sortie)
            for f in ["index.html", "contact.html", "mentions-legales.html", "confidentialite.html", "a-propos.html",
                      "realisations.html", "plomberie.html", "electricite.html", "zone-plombier-bourg-test.html",
                      "llms.txt", "sitemap.xml", "robots.txt"]:
                self.assertTrue((s / f).exists(), f)
            code, sortie = lancer(OUTILS / "verifier_publication.py", s)
            self.assertEqual(code, 0, sortie)
            naps = set()
            for p in s.glob("*.html"):
                h = p.read_text(encoding="utf-8")
                self.assertIn('href="tel:+33199001234"', h, p.name)
                self.assertIn('name="source"' if p.name == "contact.html" else "", h)
                bloc = h.split('<div class="nap" data-nap>')[1].split("</div>")[0]
                naps.add(bloc)
                ld = json.loads(h.split('<script type="application/ld+json">')[1].split("</script>")[0].replace("<\\/", "</"))
                ld = ld[0] if isinstance(ld, list) else ld
                self.assertEqual(ld["@type"], "Plumber")
                for champ in ["name", "telephone", "address", "areaServed", "url"]:
                    self.assertIn(champ, ld)
            self.assertEqual(len(naps), 1, "nom/adresse/téléphone différents selon les pages")

    def test_404_icone_et_apercu_partage(self):
        with tempfile.TemporaryDirectory() as d:
            s = Path(d) / "s"
            code, sortie = self.generer(FICTIVE, s)
            self.assertEqual(code, 0, sortie)
            page404 = (s / "404.html").read_text(encoding="utf-8")
            self.assertIn('<base href="/">', page404)
            self.assertIn('content="noindex"', page404)
            self.assertNotIn("404.html", (s / "sitemap.xml").read_text(encoding="utf-8"))
            self.assertTrue((s / "favicon.svg").read_text(encoding="utf-8").startswith("<svg"))
            accueil = (s / "index.html").read_text(encoding="utf-8")
            self.assertIn('rel="icon" href="favicon.svg"', accueil)
            for prop in ("og:title", "og:description", "og:url", "og:image", "og:locale"):
                self.assertIn(f'property="{prop}"', accueil)
            self.assertIn('content="https://', accueil.split('property="og:image"')[1][:40])
            self.assertIn("01 99 00 12 34", (s / "llms.txt").read_text(encoding="utf-8"))

    def test_refus_modele(self):
        with tempfile.TemporaryDirectory() as d:
            ent = Path(d) / "ent"
            ent.mkdir()
            shutil.copy(RACINE / "modeles/site/site-contenu.exemple.json", ent / "site-contenu.json")
            code, sortie = self.generer(ent, Path(d) / "s")
            self.assertEqual(code, 1, sortie)
            self.assertIn("modèle", sortie)

    def test_refus_placeholder(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.copie_fictive(d, lambda c: c["accueil"].__setitem__("intro", "Plombier à [VILLE]"))
            code, sortie = self.generer(ent, Path(d) / "s")
            self.assertEqual(code, 1, sortie)
            self.assertFalse((Path(d) / "s").exists())

    def test_refus_zone_hors_zone(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.copie_fictive(d, lambda c: c["pages_zones"][0].__setitem__("commune", "Paris"))
            code, sortie = self.generer(ent, Path(d) / "s")
            self.assertEqual(code, 1, sortie)

    def test_refus_trop_de_pages_zones(self):
        def modif(c):
            c["entreprise"]["zone"]["communes"] = [f"Commune{i}" for i in range(8)]
            c["pages_zones"] = [{"slug": f"z{i}", "commune": f"Commune{i}", "metier": "plomberie", "texte": f"Texte {i}"} for i in range(7)]
        with tempfile.TemporaryDirectory() as d:
            code, sortie = self.generer(self.copie_fictive(d, modif), Path(d) / "s")
            self.assertEqual(code, 1, sortie)

    def test_titre_en_double(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.copie_fictive(d, lambda c: [m.__setitem__("titre_seo", "Même titre") for m in c["metiers"]])
            code, sortie = self.generer(ent, Path(d) / "s")
            self.assertEqual(code, 1, sortie)

    def test_moins_de_3_realisations(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.copie_fictive(d, lambda c: c.__setitem__("realisations", c["realisations"][:2]))
            code, sortie = self.generer(ent, Path(d) / "s")
            self.assertEqual(code, 2, sortie)
            self.assertIn("2 réalisation", sortie)

    def test_mentions_incompletes(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.copie_fictive(d, lambda c: c["legal"].pop("siret"))
            code, sortie = self.generer(ent, Path(d) / "s")
            self.assertEqual(code, 2, sortie)
            self.assertFalse((Path(d) / "s" / "mentions-legales.html").exists())

    def test_sans_suivi_pas_de_bandeau(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.copie_fictive(d, lambda c: c.__setitem__("suivi", {}))
            self.generer(ent, Path(d) / "s")
            h = (Path(d) / "s" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn('id="cookies"', h)
            self.assertIn("aucun cookie", (Path(d) / "s" / "confidentialite.html").read_text(encoding="utf-8"))


class Bilan(unittest.TestCase):
    def setUp(self):
        self.journal = bilan.lire_journal(EXEMPLE / "entreprise" / "journal-devis.csv")
        import datetime
        self.auj = datetime.date(2026, 11, 8)

    def test_nombres_francais(self):
        self.assertEqual(bilan.nombre("1 234,56"), 1234.56)
        self.assertEqual(bilan.nombre("4,07 %"), 4.07)
        self.assertEqual(bilan.nombre("1,234.56"), 1234.56)
        self.assertEqual(bilan.nombre("--"), 0.0)

    def test_export_utf16_tabulations(self):
        t, lignes = bilan.lire_export(EXEMPLE / "entreprise/exports/2026-10-campagnes.csv")
        self.assertEqual(t, "campagnes")
        self.assertEqual(len(lignes), 2)  # lignes « Total » ignorées
        self.assertAlmostEqual(sum(l["cout"] for l in lignes), 198.40)

    def test_octobre(self):
        r = bilan.calculer("2026-10", EXEMPLE / "entreprise", self.journal, aujourdhui=self.auj)
        self.assertEqual(r["depense"], 198.40)
        self.assertEqual(r["conversions_google"], 6)
        self.assertEqual(r["demandes"], 9)
        self.assertEqual(r["demandes_pubs"], 4)
        self.assertEqual(r["cout_par_demande_pubs"], 49.60)
        self.assertEqual(r["cout_par_conversion_google"], 33.07)
        self.assertEqual((r["signes"], r["ca_signe"]), (2, 12400))
        self.assertEqual((r["signes_pubs"], r["ca_signe_pubs"]), (1, 4200))
        self.assertEqual(r["depense_termes_sans_demande"], 56.80)
        self.assertEqual([l["lieu"].split(",")[0] for l in r["lieux_hors_zone"]], ["La Flèche", "Angers", "Tours"])
        self.assertEqual(len(r["en_attente_plus_30j"]), 2)

    def test_septembre(self):
        r = bilan.calculer("2026-09", EXEMPLE / "entreprise", self.journal, aujourdhui=self.auj)
        self.assertEqual(r["depense"], 205.10)
        self.assertEqual(r["cout_par_demande_pubs"], 68.37)
        self.assertEqual((r["signes"], r["ca_signe"]), (3, 11000))

    def test_sans_export_depense_declaree(self):
        r = bilan.calculer("2026-08", EXEMPLE / "entreprise", self.journal, depense_declaree=200.0, aujourdhui=self.auj)
        self.assertEqual(r["source_depense"], "déclarée par le gérant")
        self.assertIsNone(r["cout_par_demande_pubs"])  # aucune demande en août

    def test_rapport_genere_puis_bloque_tant_que_non_complete(self):
        with tempfile.TemporaryDirectory() as d:
            code, sortie = lancer(OUTILS / "bilan.py", "--mois", "2026-10", "--entreprise", EXEMPLE / "entreprise", "--rapports", d,
                                  "--aujourdhui", "2026-11-08", "--rapport", "--avis-nombre", "12", "--avis-note", "4.7")
            self.assertEqual(code, 0, sortie)
            rapport = Path(d) / "2026-10.md"
            texte = rapport.read_text(encoding="utf-8")
            self.assertIn("**49,60 €**", texte)
            self.assertIn("déclarent", texte)  # limites d'attribution
            self.assertLessEqual(len(texte.splitlines()), 50)  # une page
            code, _ = lancer(OUTILS / "verifier_publication.py", rapport)
            self.assertEqual(code, 1)  # sections « À COMPLÉTER » non remplies

    def test_rapport_exemple_complete(self):
        code, sortie = lancer(OUTILS / "verifier_publication.py", EXEMPLE / "rapports" / "2026-10.md")
        self.assertEqual(code, 0, sortie)


def ecrire_xlsx(chemin, lignes):
    """Petit .xlsx (chaînes en ligne) pour les tests, sans dépendance."""
    import zipfile
    from xml.sax.saxutils import escape
    lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rows = []
    for i, l in enumerate(lignes, 1):
        cells = []
        for j, v in enumerate(l):
            ref = f"{lettres[j]}{i}"
            if isinstance(v, (int, float)):
                cells.append(f'<c r="{ref}"><v>{v}</v></c>')
            else:
                cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(v)}</t></is></c>')
        rows.append(f'<row r="{i}">{"".join(cells)}</row>')
    feuille = ('<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
               f'<sheetData>{"".join(rows)}</sheetData></worksheet>')
    with zipfile.ZipFile(chemin, "w") as z:
        z.writestr("xl/worksheets/sheet1.xml", feuille)


class BilanExportsReels(unittest.TestCase):
    """Cas rencontrés sur des exports au format Google Ads (bugs corrigés en novembre 2026)."""

    def preparer(self, d, fichiers):
        ent = Path(d)
        (ent / "exports").mkdir()
        (ent / "journal-devis.csv").write_text(
            "date,nom_client,source,type_chantier,commune,statut,montant_signe,notes\n"
            "2026-10-03,A,google-annonce,façade,Bourg,en attente,,\n", encoding="utf-8")
        for nom, contenu in fichiers.items():
            (ent / "exports" / nom).write_text(contenu, encoding="utf-8")
        return ent

    def test_periode_differente_ecartee(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.preparer(d, {"2026-10-campagnes.csv":
                "Rapport sur les campagnes\n9 octobre 2026 - 7 novembre 2026\nCampagne,Clics,Coût,Conversions\nFaçade,5,\"10,30\",\"1,00\"\n"})
            r = bilan.calculer("2026-10", ent, bilan.lire_journal(ent / "journal-devis.csv"))
            self.assertIsNone(r["depense"])
            self.assertTrue(any("pas le mois entier" in a for a in r["avertissements"]))

    def test_periode_anglaise_acceptee(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.preparer(d, {"2026-10-campagnes.csv":
                "Campaign report\n\"October 1, 2026 - October 31, 2026\"\nCampaign,Clicks,Cost,Conversions\nFacade,5,\"1,010.30\",1.00\nTotal: Account,5,\"1,010.30\",1.00\n"})
            r = bilan.calculer("2026-10", ent, bilan.lire_journal(ent / "journal-devis.csv"))
            self.assertEqual(r["depense"], 1010.30)
            self.assertEqual(r["avertissements"], [])

    def test_terme_commencant_par_total_garde_et_termes_masques(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.preparer(d, {"2026-10-termes.csv":
                "Rapport sur les termes de recherche\n1 octobre 2026 - 31 octobre 2026\n"
                "Terme de recherche,Campagne,Clics,Coût,Conversions\n"
                "total renovation facade,Façade,4,\"12,00\",\"0,00\"\n"
                "Autres termes de recherche,Façade,9,\"30,00\",\"0,00\"\n"
                "Total : termes de recherche,,13,\"42,00\",\"0,00\"\n"})
            r = bilan.calculer("2026-10", ent, bilan.lire_journal(ent / "journal-devis.csv"))
            self.assertEqual([t["terme"] for t in r["termes_sans_demande"]], ["total renovation facade"])
            self.assertEqual(r["depense_termes_sans_demande"], 12.0)
            self.assertEqual(r["depense_termes_masques"], 30.0)

    def test_export_excel_xlsx(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.preparer(d, {})
            ecrire_xlsx(ent / "exports" / "2026-10-campagnes.xlsx", [
                ["Rapport sur les campagnes"], ["1 octobre 2026 - 31 octobre 2026"],
                ["Campagne", "Clics", "Coût", "Conversions"], ["Façade", 52, 198.4, 4], ["Total : compte", 52, 198.4, 4]])
            r = bilan.calculer("2026-10", ent, bilan.lire_journal(ent / "journal-devis.csv"))
            self.assertEqual(r["depense"], 198.40)
            self.assertEqual(r["cout_par_demande_pubs"], 198.40)

    def test_type_pris_dans_le_nom_du_fichier(self):
        with tempfile.TemporaryDirectory() as d:
            ent = self.preparer(d, {"2026-10-campagnes.csv":
                "Rapport\n1 octobre 2026 - 31 octobre 2026\nJour de la semaine,Campagne,Coût,Conversions\nLundi,Façade,\"20,00\",\"0,00\"\n"})
            r = bilan.calculer("2026-10", ent, bilan.lire_journal(ent / "journal-devis.csv"))
            self.assertEqual(r["depense"], 20.0)


class Photos(unittest.TestCase):
    def grosse_photo(self, dossier):
        import os
        import struct
        w, h = 2400, 1600
        ligne = w * 3
        donnees = b"".join(os.urandom(ligne) for _ in range(h))
        bmp = Path(dossier) / "x.bmp"
        bmp.write_bytes(b"BM" + struct.pack("<IHHI", 54 + len(donnees), 0, 0, 54)
                        + struct.pack("<IiiHHIIiiII", 40, w, h, 1, 24, 0, len(donnees), 2835, 2835, 0, 0) + donnees)
        return bmp

    @unittest.skipUnless(shutil.which("sips"), "outil sips (Mac) absent")
    def test_reduction_avec_original_garde(self):
        with tempfile.TemporaryDirectory() as d:
            chantier = Path(d) / "2026-10-test"
            chantier.mkdir()
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "95", str(self.grosse_photo(d)),
                            "--out", str(chantier / "01.jpg")], capture_output=True)
            avant = (chantier / "01.jpg").stat().st_size
            self.assertGreater(avant, 1_000_000)
            code, sortie = lancer(OUTILS / "reduire_photos.py", d)
            self.assertEqual(code, 0, sortie)
            import generer_site
            self.assertEqual(max(generer_site.dimensions_image(chantier / "01.jpg")), 1600)
            self.assertEqual((chantier / "originaux" / "01.jpg").stat().st_size, avant)
            code, sortie = lancer(OUTILS / "reduire_photos.py", d)  # deuxième passage : rien à faire
            self.assertEqual(code, 0, sortie)
            self.assertIn("aucune photo à réduire", sortie)

    def test_generateur_signale_photo_lourde(self):
        with tempfile.TemporaryDirectory() as d:
            ent = Path(d) / "e"
            shutil.copytree(FICTIVE, ent)
            premiere = next((ent / "realisations").rglob("01.jpg"))
            premiere.write_bytes(premiere.read_bytes() + b"\0" * 1_100_000)
            code, sortie = lancer(OUTILS / "generer_site.py", "--entreprise", ent, "--sortie", Path(d) / "s")
            self.assertIn("Photo lourde", sortie)
            self.assertIn("reduire_photos.py", sortie)


class Annonce(unittest.TestCase):
    def test_exemple_conforme(self):
        code, sortie = lancer(OUTILS / "verifier_annonce.py", EXEMPLE / "entreprise/brouillons/annonce-2026-10-22.txt")
        self.assertEqual(code, 0, sortie)

    def test_trop_long(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "a.txt"
            f.write_text("T: Un titre beaucoup trop long pour Google Ads\nT: B\nT: C\nD: Desc 1\nD: Desc 2\n", encoding="utf-8")
            code, sortie = lancer(OUTILS / "verifier_annonce.py", f)
            self.assertEqual(code, 1)
            self.assertIn("TROP LONG", sortie)


if __name__ == "__main__":
    navigateur = "--navigateur" in sys.argv
    if navigateur:
        sys.argv.remove("--navigateur")
    prog = unittest.main(exit=False, verbosity=1)
    ok = prog.result.wasSuccessful()
    if navigateur and ok:
        import http.server
        import threading
        import functools
        for dossier, opts in ((FICTIVE, ["--complet"]), (EXEMPLE / "entreprise", [])):
            with tempfile.TemporaryDirectory() as d:
                lancer(OUTILS / "generer_site.py", "--entreprise", dossier, "--sortie", Path(d) / "s")
                h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(Path(d) / "s"))
                srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
                threading.Thread(target=srv.serve_forever, daemon=True).start()
                r = subprocess.run(["node", str(RACINE / "tests/test_navigateur.js"), f"http://127.0.0.1:{srv.server_port}", *opts])
                srv.shutdown()
                ok = ok and r.returncode == 0
    sys.exit(0 if ok else 1)
