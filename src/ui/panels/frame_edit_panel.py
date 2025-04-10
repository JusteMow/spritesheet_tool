import tkinter as tk
from tkinter import ttk
from src.core.event_manager import EventManager
from src.core.states import States
from src.ui.panels.frame_edit_selection_subpanel import FrameEditSelectionSubpanel
from src.ui.panels.frame_edit_framelist_subpanel import FrameEditFramelistSubpanel
from src.ui.panels.frame_edit_rowcols_offset_subpanel import FrameEditRowColsOffsetSubpanel

class FrameEditPanel:
    """Interface pour modifier les frames."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'FrameEditPanel':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("FrameEditPanel n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise le panel."""
        if FrameEditPanel._instance is not None:
            raise Exception("FrameEditPanel est un singleton")
        FrameEditPanel._instance = self
        
        States.log("Initialisation du FrameEditPanel")
        
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sous-panels dans l'ordre d'affichage
        self.selection_subpanel = FrameEditSelectionSubpanel(self.frame)
        self.rowcols_offset_subpanel = FrameEditRowColsOffsetSubpanel(self.frame)
        self.framelist_subpanel = FrameEditFramelistSubpanel(self.frame)
        
        self._setup_events()
    
    def _setup_events(self):
        """Configure les événements."""
        EventManager.subscribe(EventManager.FRAMELIST_PROP_UPDATED, self.on_framelist_prop_updated)
        EventManager.subscribe(EventManager.FRAMELIST_LIST_UPDATED, self.on_framelist_list_updated)
    
    def on_framelist_prop_updated(self):
        """Réaction au changement de propriété d'une frame."""
        self.framelist_subpanel.update_values()
    
    def on_framelist_list_updated(self):
        """Réaction au changement de la liste de frames."""
        self.framelist_subpanel.rebuild_list()
    
    def destroy(self):
        """Détruit le panel et ses sous-panels."""
        States.log("Destruction du FrameEditPanel")
        EventManager.unsubscribe(EventManager.FRAMELIST_PROP_UPDATED, self.on_framelist_prop_updated)
        EventManager.unsubscribe(EventManager.FRAMELIST_LIST_UPDATED, self.on_framelist_list_updated)
        self.selection_subpanel.destroy()
        self.framelist_subpanel.destroy()
        self.rowcols_offset_subpanel.destroy()
        FrameEditPanel._instance = None
        self.frame.destroy() 