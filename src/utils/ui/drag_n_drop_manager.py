import tkinter as tk
import tkinterdnd2
from typing import Any
import os
from src.core.states import States
from src.ui.panels.import_export_panel import ImportExportPanel

class DragNDropManager:
    """Gestionnaire de drag and drop pour l'application."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'DragNDropManager':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("DragNDropManager n'est pas initialisé")
        return cls._instance
    
    def __init__(self, root: tkinterdnd2.TkinterDnD.Tk):
        """
        Initialise le gestionnaire.
        
        Args:
            root: La fenêtre principale de l'application
        """
        if DragNDropManager._instance is not None:
            raise Exception("DragNDropManager est un singleton")
        DragNDropManager._instance = self
        
        States.log("Initialisation du DragNDropManager")
        
        self.root = root
        self._setup_drag_n_drop()
    
    def _setup_drag_n_drop(self):
        """Configure le drag and drop sur la fenêtre principale."""
        self.root.drop_target_register(tkinterdnd2.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self._on_drop)
    
    def _on_drop(self, event: Any):
        """
        Gère le drop d'un fichier.
        
        Args:
            event: L'événement de drop contenant le chemin du fichier
        """
        # Nettoie le chemin du fichier (peut contenir des accolades sur certaines plateformes)
        file_path = event.data.strip('{}')
        States.log(f"Fichier déposé (nettoyé) : {file_path}")
        
        # Vérifie l'extension du fichier
        _, ext = os.path.splitext(file_path.lower())
        
        # Images
        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            States.log("Import d'une spritesheet par drag and drop")
            ImportExportPanel.get_instance().import_spritesheet(file_path)
            
        # Vidéos
        elif ext in ['.mp4', '.mov', '.avi']:
            States.log("Import d'une vidéo par drag and drop")
            ImportExportPanel.get_instance().import_video(file_path)
            
        else:
            States.log(f"Extension non supportée : {ext}")
    
    def destroy(self):
        """Détruit le gestionnaire."""
        States.log("Destruction du DragNDropManager")
        DragNDropManager._instance = None 