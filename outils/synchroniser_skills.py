#!/usr/bin/env python3
"""Copie les skills de skills/ (source unique) vers les dossiers lus par chaque outil,
et régénère la version « chat » (un seul fichier d'instructions).

    python3 outils/synchroniser_skills.py           # synchronise
    python3 outils/synchroniser_skills.py --verifier # code 1 si une copie diffère de la source

Emplacements (vérifiés dans la documentation officielle, novembre 2026) :
- Codex  : .agents/skills/<nom>/SKILL.md (dossier courant → racine du dépôt)
- Claude Code / Claude avec dossier : .claude/skills/<nom>/SKILL.md
On utilise des copies plutôt que des liens symboliques : les liens se perdent souvent
dans un fichier .zip ou sous Windows.
"""
import filecmp
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "skills"
CIBLES = [RACINE / ".agents" / "skills", RACINE / ".claude" / "skills"]
CHAT = RACINE / "version-chat" / "INSTRUCTIONS-CHAT.md"


def differences(a, b):
    if not b.exists():
        return [str(b)]
    cmp = filecmp.dircmp(a, b)
    diff = [str(b / x) for x in cmp.left_only + cmp.right_only + cmp.diff_files + cmp.funny_files]
    for sous in cmp.common_dirs:
        diff += differences(a / sous, b / sous)
    return diff


GUIDES = RACINE / "version-chat" / "GUIDES-CHAT.md"
LIMITE_CHAT = 8000  # limite des instructions d'un projet ChatGPT (le plus restrictif)


def sections_agents():
    """Découpe AGENTS.md en {titre: texte} au niveau « ## » (les « ### » restent dans leur section)."""
    texte = (RACINE / "AGENTS.md").read_text(encoding="utf-8")
    sections, titre = {}, None
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            titre = ligne[3:].strip()
            sections[titre] = []
        elif titre:
            sections[titre].append(ligne)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def version_chat():
    """Instructions courtes à coller dans un projet Claude ou ChatGPT (moins de 8 000 caractères).

    Construites à partir d'AGENTS.md (source unique), sans ce qui suppose l'accès au dossier.
    Les guides détaillés (skills) vont dans GUIDES-CHAT.md, à ajouter comme fichier du projet."""
    s = sections_agents()
    regles = s["Les 7 règles non négociables"]
    menu = s["Menu (quand le gérant ne sait pas quoi faire)"].replace("C'est ce fichier qui définit le menu. ", "")
    lignes_routage = [l for l in s["Quel skill pour quelle demande"].splitlines() if l.startswith("| «") or l.startswith("| question")]
    routage = "| Demande du gérant | Guide |\n|---|---|\n" + "\n".join(l.replace("`skills/", "`").replace("`", "") for l in lignes_routage)
    journal = s["Fichiers"].split("### Journal des devis")[1].split("### Même information partout")[0]
    journal = "\n".join(l for l in journal.splitlines()[1:] if l.startswith("- ") and "UTF-8" not in l)
    parler = s["Façon de parler"]
    morceaux = [
        "# Assistant marketing — version chat (projet Claude ou ChatGPT)",
        "",
        "> Fichier généré par outils/synchroniser_skills.py à partir d'AGENTS.md — ne pas modifier à la main.",
        "> Collez ce texte dans les instructions du projet. Ajoutez comme fichiers du projet : GUIDES-CHAT.md,",
        "> entreprise/profil.md et entreprise/journal-devis.csv.",
        "",
        "## Ton rôle",
        "",
        "Tu es l'assistant marketing d'un artisan du bâtiment (métier dans son profil). Il n'est pas technique, travaille sur les chantiers et a quelques heures par mois. Objectif : qu'il sache chaque mois combien de demandes de devis il reçoit, d'où elles viennent et combien chacune coûte en pub, et qu'il agisse seul.",
        "",
        "## Limites de la version chat",
        "",
        "Tu n'as pas accès au dossier : tu ne peux ni écrire de fichier ni lancer de programme. Quand un guide dit d'écrire dans un fichier, donne au gérant le texte exact à copier (ligne du journal, profil mis à jour) et dis-lui où le coller. Fais toi-même, en montrant le détail, les calculs et contrôles que les guides confient aux outils (coût par demande, longueur des annonces, absence de texte provisoire). Le site ne peut pas être généré ici.",
        "",
        "## Démarrage",
        "",
        "Si le profil (fichier du projet) est vide ou absent, ou si le gérant dit « je veux commencer », suis le guide « demarrage » de GUIDES-CHAT.md. Sinon salue-le par son prénom et réponds à sa demande ; s'il ne sait pas quoi faire, propose le menu.",
        "",
        "## Les 7 règles non négociables",
        "",
        regles,
        "",
        "## Menu",
        "",
        menu,
        "",
        "## Quel guide pour quelle demande (dans GUIDES-CHAT.md)",
        "",
        routage,
        "",
        "## Journal des devis",
        "",
        "Colonnes : date,nom_client,source,type_chantier,commune,statut,montant_signe,notes",
        journal,
        "",
        "## Façon de parler",
        "",
        parler,
        "",
    ]
    return "\n".join(morceaux)


def guides_chat():
    morceaux = [
        "# Guides détaillés de l'assistant (version chat)",
        "",
        "> Fichier généré par outils/synchroniser_skills.py — ne pas modifier à la main. À ajouter comme fichier du projet.",
        "> Dans la version chat, « lance python3 outils/… » veut dire : fais le calcul ou le contrôle toi-même, en montrant le détail.",
    ]
    for d in sorted(SOURCE.iterdir()):
        f = d / "SKILL.md"
        if f.is_file():
            morceaux.append(f"\n\n---\n\n<!-- guide : {d.name} -->\n")
            morceaux.append(f.read_text(encoding="utf-8"))
    return "\n".join(morceaux)


def main():
    verifier = "--verifier" in sys.argv
    erreurs = []
    for cible in CIBLES:
        if verifier:
            erreurs += differences(SOURCE, cible)
        else:
            if cible.exists():
                shutil.rmtree(cible)
            shutil.copytree(SOURCE, cible)
    chat = version_chat()
    guides = guides_chat()
    if len(chat) > LIMITE_CHAT:
        print(f"Instructions chat trop longues : {len(chat)} caractères (maximum {LIMITE_CHAT}). Raccourcir AGENTS.md.")
        return 1
    if verifier:
        for fichier, contenu in ((CHAT, chat), (GUIDES, guides)):
            if not fichier.exists() or fichier.read_text(encoding="utf-8") != contenu:
                erreurs.append(str(fichier))
        if erreurs:
            print("Copies non synchronisées :\n - " + "\n - ".join(erreurs))
            return 1
        print("OK : copies identiques à skills/.")
        return 0
    CHAT.parent.mkdir(exist_ok=True)
    CHAT.write_text(chat, encoding="utf-8")
    GUIDES.write_text(guides, encoding="utf-8")
    print("Skills copiés vers .agents/skills et .claude/skills ; version chat régénérée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
