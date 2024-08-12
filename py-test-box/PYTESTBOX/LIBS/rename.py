from os import walk
from os.path import dirname
import os


for dossier, sous_dossiers, fichiers in os.walk(dirname(__file__)):
    for fichier in fichiers:
        full_path = os.path.join(dossier, fichier)
        if os.path.basename(dossier)=="test":
            if fichier.endswith("test.py"):
                if not fichier.endswith("_test.py"):
                    new_full_path = os.path.join(dossier, fichier[:-7] + "_test.py")
                    print("rename " + full_path + " as " + new_full_path)
                    #os.rename(full_path, new_full_path)

            elif fichier != "__init__.py":
                print("!!!forget " + full_path)
#check __init__ exists everywhere
