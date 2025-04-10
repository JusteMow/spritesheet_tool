import tkinter as tk
from typing import Optional
from src.core.states import States
from src.core.app_utils import restart_app
from src.ui.playback_panel import PlaybackPanel

class KeybindingManager:
    """Gère les raccourcis clavier de l'application."""
    
    _instance: Optional['KeybindingManager'] = None
    
    @classmethod
    def get_instance(cls) -> 'KeybindingManager':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("KeybindingManager n'est pas initialisé")
        return cls._instance
    
    def __init__(self, root: tk.Tk):
        """
        Initialise le manager de raccourcis.
        
        Args:
            root: Fenêtre principale de l'application
        """
        if KeybindingManager._instance is not None:
            raise Exception("KeybindingManager est un singleton")
        KeybindingManager._instance = self
        
        States.log("Initialisation du KeybindingManager")
        self.root = root
        self._setup_bindings()
    
    def _setup_bindings(self) -> None:
        """Configure les raccourcis clavier."""
        States.log("Configuration des raccourcis clavier")
        
        # Navigation - bind_all pour capture globale
        self.root.bind_all('<Left>', self._on_previous_frame)
        self.root.bind_all('<Right>', self._on_next_frame)
        
        # Contrôles de lecture - bind_all pour capture globale
        self.root.bind_all('p', self._on_toggle_play)
        self.root.bind_all('i', self._on_toggle_included)
        
        # Application - bind_all pour capture globale
        self.root.bind_all('r', self._on_reload_app)
        
        States.log("Raccourcis clavier configurés globalement")
    
    def _on_previous_frame(self, event) -> None:
        """Passe à la frame précédente."""
        States.log("Raccourci: Frame précédente")
        PlaybackPanel.get_instance().previous_frame()
    
    def _on_next_frame(self, event) -> None:
        """Passe à la frame suivante."""
        States.log("Raccourci: Frame suivante")
        PlaybackPanel.get_instance().next_frame()
    
    def _on_toggle_play(self, event) -> None:
        """Démarre/Arrête la lecture."""
        States.log("Raccourci: Toggle lecture")
        PlaybackPanel.get_instance().toggle_play_stop()
    
    def _on_toggle_included(self, event) -> None:
        """Inclut/Exclut la frame courante."""
        States.log("Raccourci: Toggle inclusion frame")
        PlaybackPanel.get_instance().toggle_current_frame_included()
    
    def _on_reload_app(self, event) -> None:
        """Recharge l'application."""
        States.log("Raccourci: Reload application")
        restart_app()
    
    def destroy(self) -> None:
        """Détruit le manager."""
        States.log("Destruction du KeybindingManager")
        KeybindingManager._instance = None 