#!/usr/bin/env python3
"""Contrôle les longueurs d'une annonce Google (annonce responsive sur le Réseau de Recherche).

Fichier : une ligne par élément, préfixée « T: » (titre), « D: » (description) ou « P: » (chemin d'URL).
Limites (aide Google Ads, vérifiées en novembre 2026) : titres 30 caractères (3 à 15),
descriptions 90 caractères (2 à 4), chemins 15 caractères (2 maximum).

    python3 outils/verifier_annonce.py entreprise/brouillons/annonce.txt
"""
import sys
from pathlib import Path

LIMITES = {"T": (30, 3, 15, "Titre"), "D": (90, 2, 4, "Description"), "P": (15, 0, 2, "Chemin")}


def main(chemin):
    elements = {"T": [], "D": [], "P": []}
    for n, ligne in enumerate(Path(chemin).read_text(encoding="utf-8").splitlines(), 1):
        ligne = ligne.strip()
        if len(ligne) > 1 and ligne[0] in elements and ligne[1] == ":":
            elements[ligne[0]].append((n, ligne[2:].strip()))
    pb = []
    for cle, (maxi, mini, nb_max, nom) in LIMITES.items():
        liste = elements[cle]
        if not mini <= len(liste) <= nb_max:
            pb.append(f"{nom}s : {len(liste)} (attendu entre {mini} et {nb_max})")
        textes = [t for _, t in liste]
        for n, t in liste:
            etat = "OK" if len(t) <= maxi else f"TROP LONG (+{len(t) - maxi})"
            print(f"{nom:<11} {len(t):>3}/{maxi}  {etat:<16} {t}")
            if len(t) > maxi:
                pb.append(f"ligne {n} : {nom.lower()} de {len(t)} caractères (max {maxi})")
            if textes.count(t) > 1:
                pb.append(f"ligne {n} : {nom.lower()} en double")
    if pb:
        print("\nÀ CORRIGER :\n - " + "\n - ".join(dict.fromkeys(pb)))
        return 1
    print("\nOK : longueurs conformes.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
