import sys
import os
from src.core.states import States

def restart_app() -> None:
    """
    Redémarre l'application en exécutant un nouveau processus
    et en terminant le processus actuel.
    """
    States.log("Redémarrage de l'application")
    python = sys.executable
    os.execl(python, python, *sys.argv) 