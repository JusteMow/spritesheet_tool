import os
import sys
from pathlib import Path

# Ajoute le dossier src au PYTHONPATH
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from src.ui.main_window import MainWindow
from src.core.states import States

def main() -> None:
    """Point d'entrée principal de l'application."""
    # Active le mode debug
    States.debug_mode = True
    
    # Lance l'application
    window = MainWindow()
    window.run()

if __name__ == "__main__":
    main() 