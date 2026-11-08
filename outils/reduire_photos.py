#!/usr/bin/env python3
"""Réduit les photos trop lourdes pour le site (photos de téléphone de 4 à 8 Mo).

Usage (par l'assistant, jamais par le gérant) :
    python3 outils/reduire_photos.py entreprise/realisations [--largeur 1600] [--essai]

- Ne touche qu'aux JPEG/PNG de plus de 1 Mo.
- L'original est gardé dans un sous-dossier « originaux/ » du chantier (rien n'est perdu).
- Sans dépendance : utilise l'outil d'images livré avec le système
  (« sips » sur Mac, PowerShell sur Windows, « magick »/« convert » s'il existe ailleurs).
  Si aucun n'est disponible, liste les photos à réduire et sort avec le code 2 :
  le site reste publiable, simplement plus lent sur mobile.
"""
import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generer_site import dimensions_image  # noqa: E402

SEUIL = 1_000_000
EXTENSIONS = {".jpg", ".jpeg", ".png"}

POWERSHELL = r"""
param([string]$Source, [string]$Dest, [int]$Largeur)
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile($Source)
try {
  if ($img.PropertyIdList -contains 0x0112) {
    $o = $img.GetPropertyItem(0x0112).Value[0]
    switch ($o) { 3 {$img.RotateFlip('Rotate180FlipNone')} 6 {$img.RotateFlip('Rotate90FlipNone')} 8 {$img.RotateFlip('Rotate270FlipNone')} }
  }
  $ratio = [Math]::Min(1.0, $Largeur / [Math]::Max($img.Width, $img.Height))
  $w = [int]($img.Width * $ratio); $h = [int]($img.Height * $ratio)
  $bmp = New-Object System.Drawing.Bitmap $w, $h
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = 'HighQualityBicubic'
  $g.DrawImage($img, 0, 0, $w, $h)
  $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
  $p = New-Object System.Drawing.Imaging.EncoderParameters 1
  $p.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), 82L
  if ($Dest.ToLower().EndsWith('.png')) { $bmp.Save($Dest, [System.Drawing.Imaging.ImageFormat]::Png) } else { $bmp.Save($Dest, $codec, $p) }
  $g.Dispose(); $bmp.Dispose()
} finally { $img.Dispose() }
"""


def outil_disponible():
    if platform.system() == "Darwin" and shutil.which("sips"):
        return "sips"
    if platform.system() == "Windows" and (shutil.which("powershell") or shutil.which("pwsh")):
        return "powershell"
    for nom in ("magick", "convert"):
        if shutil.which(nom):
            return nom
    return None


def reduire(outil, source, dest, largeur):
    if outil == "sips":
        cmd = ["sips", "-Z", str(largeur), "-s", "formatOptions", "82", str(source), "--out", str(dest)]
    elif outil == "powershell":
        script = dest.parent / "_reduire.ps1"
        script.write_text(POWERSHELL, encoding="utf-8")
        exe = shutil.which("powershell") or shutil.which("pwsh")
        cmd = [exe, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
               "-Source", str(source), "-Dest", str(dest), "-Largeur", str(largeur)]
    else:
        cmd = [outil, str(source), "-auto-orient", "-resize", f"{largeur}x{largeur}>", "-quality", "82", str(dest)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        if outil == "powershell":
            (dest.parent / "_reduire.ps1").unlink(missing_ok=True)
    return r.returncode == 0 and dest.is_file() and dest.stat().st_size > 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier", help="ex. entreprise/realisations")
    ap.add_argument("--largeur", type=int, default=1600, help="plus grand côté, en pixels (défaut 1600)")
    ap.add_argument("--essai", action="store_true", help="liste seulement, ne modifie rien")
    args = ap.parse_args()

    lourdes = [f for f in sorted(Path(args.dossier).rglob("*"))
               if f.suffix.lower() in EXTENSIONS and f.is_file() and "originaux" not in f.parts
               and f.stat().st_size > SEUIL
               and max(dimensions_image(f) or (args.largeur + 1, 0)) > args.largeur]
    if not lourdes:
        print("OK : aucune photo à réduire (toutes font moins de 1 Mo ou sont déjà à la bonne taille).")
        return 0
    outil = outil_disponible()
    if args.essai or not outil:
        for f in lourdes:
            print(f" - {f} : {f.stat().st_size / 1e6:.1f} Mo")
        if not outil:
            print("Aucun outil d'images disponible sur cet ordinateur : photos laissées telles quelles "
                  "(site publiable, mais plus lent sur mobile).")
            return 2
        return 0
    erreurs = 0
    for f in lourdes:
        sauvegarde = f.parent / "originaux" / f.name
        sauvegarde.parent.mkdir(exist_ok=True)
        if not sauvegarde.exists():
            shutil.copy2(f, sauvegarde)
        avant = f.stat().st_size
        tmp = f.with_name(f.stem + ".reduite" + f.suffix)
        if reduire(outil, sauvegarde, tmp, args.largeur) and tmp.stat().st_size < avant:
            tmp.replace(f)
            print(f" - {f} : {avant / 1e6:.1f} Mo -> {f.stat().st_size / 1e6:.2f} Mo")
        else:
            tmp.unlink(missing_ok=True)
            erreurs += 1
            print(f" - {f} : non réduite (original conservé)")
    print(f"Photos réduites avec « {outil} ». Originaux gardés dans les dossiers « originaux/ ».")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
