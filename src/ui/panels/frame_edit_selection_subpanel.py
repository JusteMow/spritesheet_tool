import tkinter as tk
from tkinter import ttk
from src.core.states import States
from src.core.offset_processor import OffsetProcessor
from src.core.framelist_manager import FramelistManager

class FrameEditSelectionSubpanel:
    """Sous-panel pour les commandes globales de sélection."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'FrameEditSelectionSubpanel':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("FrameEditSelectionSubpanel n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise le sous-panel."""
        if FrameEditSelectionSubpanel._instance is not None:
            raise Exception("FrameEditSelectionSubpanel est un singleton")
        FrameEditSelectionSubpanel._instance = self
        
        States.log("Initialisation du FrameEditSelectionSubpanel")
        
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill=tk.X, pady=5)
        
        self.skip_var = tk.IntVar(value=2)
        
        self._build_ui()
    
    def _build_ui(self):
        """Construit l'interface utilisateur."""
        # Titre
        ttk.Label(self.frame, text="Sélection", style="Dark.TLabel").pack(pady=(0, 5))
        
        # Boutons de sélection globale
        buttons_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Tout", command=self.select_all, style="Dark.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Rien", command=self.select_none, style="Dark.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Inverser", command=self.select_invert, style="Dark.TButton").pack(side=tk.LEFT, padx=2)
        
        # Sélection 1 sur X
        skip_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        skip_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(skip_frame, text="1 sur", style="Dark.TLabel").pack(side=tk.LEFT)
        ttk.Entry(skip_frame, textvariable=self.skip_var, width=5, style="Dark.TEntry").pack(side=tk.LEFT, padx=2)
        ttk.Button(skip_frame, text="Sélectionner", command=self._select_every_x, style="Dark.TButton").pack(side=tk.LEFT, padx=2)
        
        # Reset offsets
        ttk.Button(self.frame, text="Reset Offsets", command=self.reset_offsets, style="Dark.TButton").pack(fill=tk.X, pady=5)
    
    def select_all(self):
        """Sélectionne toutes les frames."""
        States.log("Sélection de toutes les frames")
        framelist = FramelistManager.get_framelist()
        for i in range(len(framelist)):
            FramelistManager.set_included(i, True)
    
    def select_none(self):
        """Désélectionne toutes les frames."""
        States.log("Désélection de toutes les frames")
        framelist = FramelistManager.get_framelist()
        for i in range(len(framelist)):
            FramelistManager.set_included(i, False)
    
    def select_invert(self):
        """Inverse la sélection."""
        States.log("Inversion de la sélection")
        framelist = FramelistManager.get_framelist()
        for i, frame in enumerate(framelist):
            FramelistManager.set_included(i, not frame.included)
    
    def _select_every_x(self):
        """Sélectionne une frame toutes les X frames."""
        States.log(f"Sélection 1 frame sur {self.skip_var.get()}")
        x = max(1, self.skip_var.get())
        framelist = FramelistManager.get_framelist()
        for i in range(len(framelist)):
            FramelistManager.set_included(i, i % x == 0)
    
    def reset_offsets(self): #TODO à finir d'implémenter 
        """Réinitialise tous les offsets."""
        States.log("Reset des offsets")
        OffsetProcessor.reset()
    
    def destroy(self):
        """Détruit le sous-panel."""
        States.log("Destruction du FrameEditSelectionSubpanel")
        FrameEditSelectionSubpanel._instance = None
        self.frame.destroy() 