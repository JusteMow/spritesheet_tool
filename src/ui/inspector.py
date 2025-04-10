import tkinter as tk
from src.core.states import States
from src.utils.ui.scrollable_panel import ScrollablePanel

class Inspector(ScrollablePanel):
    """Conteneur latéral droit qui héberge des panneaux dynamiques."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'Inspector':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("Inspector n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise l'inspector."""
        if Inspector._instance is not None:
            raise Exception("Inspector est un singleton")
        Inspector._instance = self
        
        States.log("Initialisation de l'Inspector")
        
        # Initialise le ScrollablePanel avec une largeur fixe
        super().__init__(parent, style="Dark.TFrame")
        
        # Configure la frame principale
        self.configure(width=400)
        
        # Pack le panel
        self.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Force la largeur minimale après le pack
        self.pack_propagate(False)
        
        self.current_panel = None
    
    def load_panel(self, panel_type: str) -> None:
        """Charge dynamiquement un panel UI."""
        States.log(f"Chargement du panel {panel_type}")
        self.destroy_current_panel()
        
        if panel_type == "import_export":
            from .panels.import_export_panel import ImportExportPanel
            self.current_panel = ImportExportPanel(self.scrollable_frame)
        elif panel_type == "frame_edit":
            from .panels.frame_edit_panel import FrameEditPanel
            self.current_panel = FrameEditPanel(self.scrollable_frame)
    
    def destroy_current_panel(self) -> None:
        """Nettoie l'inspector avant de charger un nouveau panel."""
        if self.current_panel:
            States.log("Destruction du panel courant")
            self.current_panel.destroy()
            self.current_panel = None
    
    def destroy(self):
        """Détruit l'inspector."""
        States.log("Destruction de l'Inspector")
        if self.current_panel:
            self.current_panel.destroy()
        Inspector._instance = None
        super().destroy() 