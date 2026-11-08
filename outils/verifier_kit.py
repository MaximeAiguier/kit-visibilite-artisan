#!/usr/bin/env python3
"""Vérifie que le kit générique est prêt à livrer. Code 0 = OK, 1 = problème(s).

    python3 outils/verifier_kit.py [--livraison]

--livraison : exige en plus l'absence des dossiers exemples/ et tests/.
"""
import py_compile
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import synchroniser_skills  # noqa: E402

SKILLS = ["demarrage", "pubs-mise-en-place", "pubs-analyse", "pubs-annonces", "pubs-nouveau-canal", "fiche-google",
          "avis-clients", "seo-local", "visibilite-ia", "site-creation", "site-mise-a-jour", "bilan-mensuel"]
OBLIGATOIRES = ["README.md", "INSTALLATION.md", "AGENTS.md", "CLAUDE.md", "entreprise/profil.md", "entreprise/journal-devis.csv",
                "entreprise/journal-actions.md", "entreprise/realisations", "entreprise/exports", "modeles", "rapports", "outils"]
# Données propres à un client : ne doivent apparaître que dans exemples/ ou tests/
# Liste des clients réels : fichier local .clients-reels.txt (un motif par ligne), jamais publié ni livré.
_LOCAL = Path(__file__).resolve().parent.parent / ".clients-reels.txt"
DONNEES_CLIENT = [l.strip() for l in (_LOCAL.read_text(encoding="utf-8").splitlines() if _LOCAL.is_file() else [])
                  if l.strip() and not l.startswith("#")]
# + le cas d'exemple fictif, qui ne doit pas déborder dans le kit générique
DONNEES_CLIENT += [r"Val Rénovation", r"Valbourg", r"val-renovation"]
JARGON_README = [r"\bCSV\b", r"\bJSON\b", r"\bHTML\b", r"\bCPC\b", r"\bSEO\b", r"\bGEO\b", r"\bAPI\b", r"\bconversions?\b",
                 r"\bschema\b", r"\bterminal\b", r"\bcommande\b", r"\bskill", r"\bmarkdown\b", r"\bprompt\b"]
EN_TETE = "date,nom_client,source,type_chantier,commune,statut,montant_signe,notes"


def frontmatter(texte):
    m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    if not m:
        return None
    champs = {}
    for ligne in m.group(1).splitlines():
        if ":" in ligne:
            k, v = ligne.split(":", 1)
            champs[k.strip()] = v.strip()
    return champs


def main():
    livraison = "--livraison" in sys.argv
    pb = []
    ok = []

    for f in OBLIGATOIRES:
        if not (RACINE / f).exists():
            pb.append(f"Fichier ou dossier manquant : {f}")
    ok.append("fichiers obligatoires")

    claude = (RACINE / "CLAUDE.md").read_text(encoding="utf-8").strip()
    if claude != "@AGENTS.md":
        pb.append("CLAUDE.md doit contenir uniquement la ligne « @AGENTS.md » (pas de règles dupliquées).")
    agents = (RACINE / "AGENTS.md").read_text(encoding="utf-8")
    for attendu in ["entreprise/profil.md", "demarrage", "journal-actions.md", "Faire mon bilan du mois", "J'ai fini un chantier",
                    "J'ai reçu une demande de devis", "Répondre à un avis", "Améliorer mes pubs", "Modifier mon site"]:
        if attendu not in agents:
            pb.append(f"AGENTS.md : élément attendu absent : {attendu}")
    if len(re.findall(r"^\d\. \*\*", agents, re.M)) < 7:
        pb.append("AGENTS.md : les 7 règles non négociables ne sont pas toutes présentes.")
    if len(agents.encode()) > 32 * 1024:
        pb.append("AGENTS.md dépasse 32 Kio (limite par défaut de Codex).")
    ok.append("instructions racine")

    presents = sorted(d.name for d in (RACINE / "skills").iterdir() if d.is_dir())
    if presents != sorted(SKILLS):
        pb.append(f"Skills attendus {sorted(SKILLS)}, trouvés {presents}")
    for s in presents:
        f = RACINE / "skills" / s / "SKILL.md"
        if not f.exists():
            pb.append(f"{s} : SKILL.md manquant")
            continue
        fm = frontmatter(f.read_text(encoding="utf-8"))
        if not fm:
            pb.append(f"{s} : en-tête --- name/description absent")
            continue
        if fm.get("name") != s:
            pb.append(f"{s} : name « {fm.get('name')} » différent du nom du dossier")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s) or len(s) > 64:
            pb.append(f"{s} : nom de dossier non conforme (minuscules, chiffres, tirets, 64 max)")
        d = fm.get("description", "")
        if not d or len(d) > 1024:
            pb.append(f"{s} : description absente ou > 1024 caractères ({len(d)})")
        if len(re.findall(r"«[^»]+»", d)) < 3:
            pb.append(f"{s} : moins de 3 formulations d'artisan entre « » dans la description")
    ok.append("12 skills et leurs en-têtes")

    diff = synchroniser_skills.differences(RACINE / "skills", RACINE / ".agents" / "skills") + \
        synchroniser_skills.differences(RACINE / "skills", RACINE / ".claude" / "skills")
    if diff:
        pb.append("Copies des skills non synchronisées (lancer outils/synchroniser_skills.py) : " + ", ".join(diff[:5]))
    chat = RACINE / "version-chat" / "INSTRUCTIONS-CHAT.md"
    if not chat.exists() or chat.read_text(encoding="utf-8") != synchroniser_skills.version_chat():
        pb.append("version-chat/INSTRUCTIONS-CHAT.md périmé (lancer outils/synchroniser_skills.py)")
    guides = RACINE / "version-chat" / "GUIDES-CHAT.md"
    if not guides.exists() or guides.read_text(encoding="utf-8") != synchroniser_skills.guides_chat():
        pb.append("version-chat/GUIDES-CHAT.md périmé (lancer outils/synchroniser_skills.py)")
    if len(synchroniser_skills.version_chat()) > synchroniser_skills.LIMITE_CHAT:
        pb.append("version-chat/INSTRUCTIONS-CHAT.md dépasse 8 000 caractères (limite des projets ChatGPT)")
    ok.append("copies .agents/ .claude/ et version chat")

    ent = RACINE / "entreprise"
    profil = (ent / "profil.md").read_text(encoding="utf-8")
    if "Statut du profil : vide" not in profil or re.search(r":\s*(?!\(non renseigné\)|vide)[^\n(]*\w", "\n".join(
            l for l in profil.splitlines() if l.startswith("- ") and "aucun pour l'instant" not in l)):
        pb.append("entreprise/profil.md n'est pas le gabarit vide")
    if (ent / "journal-devis.csv").read_text(encoding="utf-8").strip() != EN_TETE:
        pb.append("entreprise/journal-devis.csv doit contenir seulement l'en-tête")
    if re.search(r"^- \d{4}-\d{2}-\d{2}", (ent / "journal-actions.md").read_text(encoding="utf-8"), re.M):
        pb.append("entreprise/journal-actions.md contient des entrées")
    for sous in ("realisations", "exports"):
        restants = [p.name for p in (ent / sous).iterdir() if p.name != "LISEZ-MOI.md"]
        if restants:
            pb.append(f"entreprise/{sous} n'est pas vide : {restants}")
    for interdit in ("site", "site-apercu", "site-contenu.json", "controle-coherence.md"):
        if (ent / interdit).exists():
            pb.append(f"entreprise/{interdit} ne doit pas exister dans le kit livré")
    rapports = [p.name for p in (RACINE / "rapports").iterdir() if p.name != "LISEZ-MOI.md"]
    if rapports:
        pb.append(f"rapports/ n'est pas vide : {rapports}")
    ok.append("dossier entreprise/ vide")

    for f in RACINE.rglob("*"):
        rel = f.relative_to(RACINE)
        if not f.is_file() or rel.parts[0] in ("exemples", "tests", ".git") or f.suffix in (".pyc",) or rel.as_posix() in ("outils/verifier_kit.py", ".clients-reels.txt"):
            continue
        try:
            t = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for motif in DONNEES_CLIENT:
            if re.search(motif, t):
                pb.append(f"Donnée d'un client dans le kit générique : {rel} ({motif})")
    ok.append("aucune donnée client hors exemples/")

    readme = (RACINE / "README.md").read_text(encoding="utf-8")
    mots = len(re.findall(r"\w+", readme))
    if mots > 650:
        pb.append(f"README.md trop long pour une page ({mots} mots, 650 max)")
    for j in JARGON_README:
        if re.search(j, readme, re.I):
            pb.append(f"README.md contient un terme technique : {j}")
    ok.append(f"README d'une page ({mots} mots), sans jargon")

    for f in (RACINE / "outils").glob("*.py"):
        try:
            py_compile.compile(str(f), doraise=True)
        except py_compile.PyCompileError as err:
            pb.append(f"Erreur de syntaxe : {f.name} : {err}")
    ok.append("outils Python compilables")

    if livraison:
        for d in ("exemples", "tests"):
            if (RACINE / d).exists():
                pb.append(f"Livraison : supprimer le dossier {d}/")
        attendus = {"AGENTS.md", "CLAUDE.md", "README.md", "INSTALLATION.md", ".agents", ".claude", "entreprise",
                    "modeles", "outils", "rapports", "skills", "version-chat", ".DS_Store", "Thumbs.db", "desktop.ini",
                    ".git", ".gitignore", ".github", ".clients-reels.txt", "LICENSE"}
        for f in sorted(RACINE.iterdir()):
            if f.name not in attendus:
                pb.append(f"Livraison : fichier inattendu à la racine du kit (rapport de test ?) : {f.name}")

    if pb:
        print("PROBLÈMES :")
        for p in pb:
            print(" - " + p)
        return 1
    print("OK : " + " ; ".join(ok))
    return 0


if __name__ == "__main__":
    sys.exit(main())
