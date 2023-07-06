import os
import pyshortcuts
from cx_Freeze import setup, Executable
from pathlib import Path

repertoire = os.path.dirname(os.path.abspath(__file__))
repertoire = os.path.normpath(repertoire)

# Chemin vers le script Python
script = f"{repertoire}/code detecte/Détéctruite.py"


icon = f"{repertoire}/code detecte/image/truite.ico"

# Configuration de l'exécutable
exe = Executable(
    script=script,
    base="Win32GUI",
    icon=icon,
)

# Options de configuration supplémentaires
options = {
    "build_exe": {
        "packages": [],  # Liste des packages supplémentaires à inclure
        "excludes": [],  # Liste des modules à exclure
        "include_files": [],  # Liste des fichiers supplémentaires à inclure
        "build_exe": os.path.join(repertoire, "build") #crée le fichier executable dans le répertoir build
    }
}

# Création de l'installation
setup(
    name="Détéctruite",
    version="1.1",
    executables=[exe],
    options=options,
)

# Chemin vers le fichier exécutable généré
executable_path = os.path.join(f"{repertoire}/build/Détéctruite.exe")

# Chemin vers le bureau
desktop_path = Path.home() / "Desktop"

# Création du raccourci sur le bureau
pyshortcuts.make_shortcut(executable_path, name="Détéctruite", folder=str(desktop_path), icon=icon)
