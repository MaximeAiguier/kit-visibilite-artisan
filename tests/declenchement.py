#!/usr/bin/env python3
"""Teste le déclenchement RÉEL des skills dans Claude Code ou Codex (sections A et A2 de tests/scenarios.md).

    python3 tests/declenchement.py claude [--modele sonnet] [--paralleles 6]
    python3 tests/declenchement.py codex

Différence avec l'ancien declenchement.sh : on n'interroge pas le modèle (« quel skill utiliserais-tu ? »),
on lui envoie la phrase du gérant telle quelle et on regarde quel skill il CHARGE vraiment
(outil Skill de Claude Code, ou lecture d'un fichier skills/<nom>/SKILL.md).

Chaque phrase est jouée dans une copie temporaire du kit, en lecture seule (aucune écriture, aucun Bash) :
- profil vide pour les phrases qui doivent lancer le démarrage ;
- profil fictif « complet » (plombier fictif, aucune donnée réelle) pour les autres.
Claude Code est lancé sans les réglages ni les serveurs MCP de l'utilisateur, comme chez un artisan.

Le mode codex utilise `codex exec --json --sandbox read-only` (testé avec codex-cli 0.167.0, novembre 2026) :
le skill chargé est repéré dans les commandes lancées par Codex (lecture de skills/<nom>/SKILL.md).
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
RX = [re.compile(r'"skill"\s*:\s*"(?:[\w-]+:)?([a-z-]+)"'), re.compile(r"skills/([a-z-]+)/SKILL\.md")]

PROFIL_COMPLET = {
    "Statut du profil : vide": "Statut du profil : complet",
    "Nom commercial : (non renseigné)": "Nom commercial : Plomberie Test (entreprise fictive)",
    "Prénom du gérant : (non renseigné)": "Prénom du gérant : Paul",
    "Métier(s) : (non renseigné)": "Métier(s) : plombier",
    "Zone d'intervention (communes / rayon) : (non renseigné)": "Zone d'intervention (communes / rayon) : Bourg-Test, Ville-Test",
    "Plateformes utilisées : (non renseigné)": "Plateformes utilisées : Google Ads (150 € par mois)",
    "Suivi des demandes en place : (non renseigné)": "Suivi des demandes en place : non",
}


def cas():
    t = (RACINE / "tests/scenarios.md").read_text(encoding="utf-8")
    sections = {"A": t.split("## A.")[1].split("## A2")[0], "A2": t.split("## A2.")[1].split("## B.")[0]}
    for sec, bloc in sections.items():
        for ligne in bloc.splitlines():
            if not ligne.startswith("| ") or "Phrase du gérant" in ligne:
                continue
            _, phrase, attendu, _ = ligne.split("|")
            vide = "profil vide" in phrase or "demarrage" in attendu
            phrase = re.sub(r"\s*\(profil vide\)", "", phrase.strip())
            question = "question" in attendu
            direct = bool(re.search(r"(^|/)\s*aucun", attendu))
            noms = [a.strip() for a in re.sub(r"\(.*?\)", "", attendu).split("/") if a.strip() and a.strip() != "aucun"]
            yield {"section": sec, "phrase": phrase, "attendu": noms, "vide": vide, "question": question, "direct": direct}


def preparer(dossier, vide):
    kit = Path(dossier) / "kit"
    shutil.copytree(RACINE, kit, ignore=shutil.ignore_patterns("exemples", "tests", "__pycache__", ".DS_Store"))
    if not vide:
        p = kit / "entreprise/profil.md"
        t = p.read_text(encoding="utf-8")
        for a, b in PROFIL_COMPLET.items():
            t = t.replace(a, b)
        p.write_text(t, encoding="utf-8")
    return kit


def jouer(outil, modele, c):
    with tempfile.TemporaryDirectory() as d:
        kit = preparer(d, c["vide"])
        if outil == "claude":
            cmd = ["claude", "-p", c["phrase"], "--strict-mcp-config", "--setting-sources", "project,local",
                   "--disallowedTools", "Write", "Edit", "Bash", "NotebookEdit", "WebFetch", "WebSearch",
                   "--max-turns", "5", "--no-session-persistence", "--output-format", "stream-json", "--verbose"]
            if modele:
                cmd[3:3] = ["--model", modele]
        else:
            cmd = ["codex", "exec", "--json", "--sandbox", "read-only", "--skip-git-repo-check", c["phrase"]]
        r = subprocess.run(cmd, cwd=kit, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
    charges, texte = [], ""
    for ligne in r.stdout.splitlines():
        if '"type":"system"' in ligne.replace(" ", ""):
            continue  # liste des skills disponibles annoncée au démarrage : pas un chargement
        try:
            x = json.loads(ligne)
        except ValueError:
            continue
        # Codex : seules les commandes lancées comptent (pas le texte qu'elles affichent)
        source = x.get("item", {}).get("command", "") if outil == "codex" else ligne
        for rx in RX:
            charges += rx.findall(source or "")
        try:
            if x.get("type") == "result":
                texte = x.get("result", "")
            elif x.get("type") == "item.completed" and x.get("item", {}).get("type") == "agent_message":
                texte = x["item"].get("text", "")
        except (ValueError, AttributeError):
            pass
    charges = list(dict.fromkeys(charges))
    ok = bool(charges) and charges[0] in c["attendu"]
    if not charges and c["question"]:
        ok = "?" in texte
    if not charges and c["direct"]:
        ok = bool(texte)  # réponse directe admise (aucun skill attendu)
    return dict(c, charges=charges, ok=ok, texte=texte[:300])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outil", choices=["claude", "codex"])
    ap.add_argument("--modele", default=None, help="ex. sonnet (Claude Code)")
    ap.add_argument("--paralleles", type=int, default=6)
    ap.add_argument("--limite", type=int, help="ne jouer que les N premières phrases (essai rapide)")
    args = ap.parse_args()
    if not shutil.which(args.outil):
        print(f"{args.outil} n'est pas installé sur cette machine : test impossible (ne pas simuler).")
        return 2
    liste = list(cas())[: args.limite]
    with ThreadPoolExecutor(args.paralleles) as ex:
        resultats = list(ex.map(lambda c: jouer(args.outil, args.modele, c), liste))
    bons = 0
    for r in resultats:
        bons += r["ok"]
        print(("OK    " if r["ok"] else "ÉCHEC "), r["section"], "|", r["phrase"], "| attendu", "/".join(r["attendu"]) or "question",
              "| chargé", ", ".join(r["charges"]) or "aucun")
        if not r["ok"]:
            print("        réponse :", r["texte"].replace("\n", " ")[:200])
    print(f"{bons} / {len(resultats)}")
    return 0 if bons == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
