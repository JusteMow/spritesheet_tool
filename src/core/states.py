from typing import Optional
from PIL import Image

class States:
    """Variables globales temporaires."""
    
    # Media chargé
    _loaded_media = None  # Variable privée
    
    # Paramètres d'import
    import_rows_var = 1
    import_columns_var = 1
    
    # Offsets de lignes et colonnes
    rows_offsets: list[int] = []
    cols_offsets: list[int] = []
    
    # Affichage
    show_included_only = False
    
    # Debug mode
    debug_mode = False
    
    @classmethod
    def get_loaded_media(cls) -> Optional[Image.Image]:
        """Retourne une copie profonde de l'image chargée."""
        return cls._loaded_media.copy() if cls._loaded_media is not None else None
    
    @classmethod
    def set_loaded_media(cls, value: Optional[Image.Image]) -> None:
        """Définit l'image chargée."""
        cls._loaded_media = value  # L'ancienne image sera collectée par le GC
    
    @staticmethod
    def log(message: str) -> None:
        """Affiche un message de log."""
        print(f"[SpriteTool] {message}")

    @staticmethod
    def log_debug(message: str) -> None:
        """Affiche un message de debug si le mode debug est activé."""
        if States.debug_mode:
            print(f"[DEBUG] {message}") 