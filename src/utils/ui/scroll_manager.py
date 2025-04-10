import tkinter as tk
from typing import Set, Any

class ScrollManager:
    """
    Gestionnaire singleton pour les événements de scroll.
    Gère la détection et la distribution des événements de scroll aux panels appropriés.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScrollManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialise les variables d'instance du singleton."""
        self.scrollable_panels: Set[Any] = set()  # Ensemble des panels scrollables enregistrés
        
    def register_panel(self, panel):
        """Enregistre un nouveau panel scrollable."""
        self.scrollable_panels.add(panel)
        if len(self.scrollable_panels) == 1:  # Premier panel enregistré
            self._bind_global_events(panel)
            
    def unregister_panel(self, panel):
        """Désenregistre un panel scrollable."""
        self.scrollable_panels.discard(panel)
        if not self.scrollable_panels:  # Plus aucun panel enregistré
            self._unbind_global_events(panel)
            
    def _bind_global_events(self, panel):
        """Bind les événements globaux de scroll sur un panel."""
        panel.bind_all("<MouseWheel>", self._on_mousewheel_global, add='+')
        
    def _unbind_global_events(self, panel):
        """Unbind les événements globaux de scroll d'un panel."""
        panel.unbind_all("<MouseWheel>")
        
    def _on_mousewheel_global(self, event):
        """
        Gère l'événement global de scroll.
        Trouve le panel scrollable le plus proche sous la souris et lui délègue le scroll.
        """
        # Trouve le widget sous la souris
        widget_under_mouse = event.widget.winfo_containing(event.x_root, event.y_root)
        if not widget_under_mouse:
            return
            
        # Remonte la hiérarchie pour trouver le ScrollablePanel le plus proche
        current_widget = widget_under_mouse
        while current_widget:
            # Vérifie si le widget est un panel scrollable enregistré
            if current_widget in self.scrollable_panels:
                panel = current_widget
                # Vérifie si le scroll est nécessaire (contenu plus grand que la vue)
                if panel.needs_scroll():
                    panel.apply_scroll(event)
                return
            current_widget = current_widget.master 