#!/usr/bin/env python3
"""Prépare le zip à livrer à un artisan (pour la personne qui installe le kit, ou lancé par l'assistant à sa demande).

    python3 outils/empaqueter.py [--sortie DOSSIER]

- Copie le kit dans un dossier temporaire SANS : exemples/, tests/, __pycache__/, .DS_Store,
  entreprise/site/, entreprise/site-apercu/, les fichiers d'un client (refusés par verifier_kit).
- Lance `outils/verifier_kit.py --livraison` sur la copie : si un contrôle échoue, aucun zip n'est créé.
- Crée kit-visibilite-artisan-AAAA-MM-JJ.zip en GARDANT les dossiers cachés .agents/ et .claude/
  (indispensables : c'est là que Codex et Claude Code lisent les skills), puis vérifie le zip.

Le kit d'origine n'est jamais modifié.
"""
import argparse
import datetime as dt
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
NOM = "kit-visibilite-artisan"
EXCLUS_RACINE = {"exemples", "tests", ".git", ".github", ".gitignore", ".clients-reels.txt"}
EXCLUS_PARTOUT = {"__pycache__", ".DS_Store", "Thumbs.db", "desktop.ini"}
EXCLUS_ENTREPRISE = {"site", "site-apercu"}
OBLIGATOIRES_ZIP = [".agents/skills/demarrage/SKILL.md", ".claude/skills/demarrage/SKILL.md", "AGENTS.md", "CLAUDE.md",
                    "README.md", "entreprise/profil.md", "entreprise/journal-devis.csv"]


def ignorer(dossier, noms):
    rel = Path(dossier).resolve().relative_to(RACINE)
    exclus = set(EXCLUS_PARTOUT)
    if rel == Path("."):
        exclus |= EXCLUS_RACINE
    if rel == Path("entreprise"):
        exclus |= EXCLUS_ENTREPRISE
    return [n for n in noms if n in exclus]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sortie", default=str(RACINE.parent), help="dossier où écrire le zip (défaut : à côté du kit)")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        copie = Path(tmp) / NOM
        shutil.copytree(RACINE, copie, ignore=ignorer)
        r = subprocess.run([sys.executable, str(copie / "outils" / "verifier_kit.py"), "--livraison"],
                           capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode != 0:
            print("Zip NON créé : corrigez d'abord ce qui est signalé ci-dessus.")
            return 1
        for p in copie.rglob("__pycache__"):  # créés par la vérification elle-même
            shutil.rmtree(p, ignore_errors=True)
        zip_chemin = Path(args.sortie) / f"{NOM}-{dt.date.today().isoformat()}.zip"
        with zipfile.ZipFile(zip_chemin, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(copie.rglob("*")):
                arc = Path(NOM) / f.relative_to(copie)
                z.write(f, arc.as_posix())
    with zipfile.ZipFile(zip_chemin) as z:
        noms = set(z.namelist())
    manquants = [m for m in OBLIGATOIRES_ZIP if f"{NOM}/{m}" not in noms]
    interdits = [n for n in noms if any(f"/{x}/" in n or n.endswith("/" + x) for x in EXCLUS_RACINE | EXCLUS_PARTOUT)]
    if manquants or interdits:
        print("Zip incorrect :", "manquants " + ", ".join(manquants) if manquants else "", "en trop " + ", ".join(interdits[:5]) if interdits else "")
        zip_chemin.unlink()
        return 1
    print(f"Zip prêt ({len(noms)} fichiers, dossiers cachés .agents/ et .claude/ inclus) : {zip_chemin}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
