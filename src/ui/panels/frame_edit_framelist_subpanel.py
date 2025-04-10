import tkinter as tk
from tkinter import ttk
from src.core.framelist_manager import FramelistManager
from src.core.states import States
from src.utils.ui.scrollable_panel import ScrollablePanel

class FrameEditFramelistSubpanel(ScrollablePanel):
    """Sous-panel pour la liste scrollable des frames."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'FrameEditFramelistSubpanel':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("FrameEditFramelistSubpanel n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise le sous-panel."""
        if FrameEditFramelistSubpanel._instance is not None:
            raise Exception("FrameEditFramelistSubpanel est un singleton")
        FrameEditFramelistSubpanel._instance = self
        
        States.log("Initialisation du FrameEditFramelistSubpanel")
        
        # Initialise le ScrollablePanel
        super().__init__(parent, style="Dark.TFrame", height=600)
        
        # Pack le panel
        self.pack(fill=tk.X, pady=5)
        
        # Liste des lignes de frames
        self.frame_rows = []
        
        # Construit la liste
        self.rebuild_list()
    
    def rebuild_list(self):
        """Reconstruit la liste des frames."""
        States.log("Reconstruction de la liste des frames")
        
        # Nettoie les lignes existantes
        for row in self.frame_rows:
            row.destroy()
        self.frame_rows.clear()
        
        # En-tête avec statistiques
        framelist = FramelistManager.get_framelist()
        included_count = sum(1 for frame in framelist if frame.included)
        
        header_frame = ttk.Frame(self.scrollable_frame, style="Dark.TFrame")
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            header_frame,
            text=f"Frames ({included_count}/{len(framelist)} incluses)",
            style="Bold.TLabel"
        ).pack(side=tk.LEFT)
        
        # Crée une ligne par frame
        for i, frame in enumerate(framelist):
            row = FrameRow(self.scrollable_frame, i, frame)
            self.frame_rows.append(row)
    
    def update_values(self):
        """Met à jour les valeurs sans reconstruire la liste."""
        States.log("Mise à jour des valeurs de la liste des frames")
        framelist = FramelistManager.get_framelist()
        for row in self.frame_rows:
            if row.frame_number < len(framelist):
                frame = framelist[row.frame_number]
                row.update_values(frame)
    
    def destroy(self):
        """Détruit le sous-panel."""
        States.log("Destruction du FrameEditFramelistSubpanel")
        for row in self.frame_rows:
            row.destroy()
        FrameEditFramelistSubpanel._instance = None
        super().destroy()


class FrameRow:
    """Ligne représentant une frame dans la liste."""
    
    def __init__(self, parent, frame_number: int, frame):
        self.frame_number = frame_number
        
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Checkbox included
        self.included_var = tk.BooleanVar(value=frame.included)
        ttk.Checkbutton(
            self.frame,
            variable=self.included_var,
            command=self._on_included_change,
            style="Dark.TCheckbutton"
        ).pack(side=tk.LEFT)
        
        # Bouton frame
        ttk.Button(
            self.frame,
            text=f"Frame {frame_number + 1}",
            command=self._on_frame_click,
            style="Dark.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        # Offsets
        offset_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        offset_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(offset_frame, text="Offset", style="Dark.TLabel").pack(side=tk.LEFT)
        
        self.offset_x_var = tk.IntVar(value=frame.offset_x)
        offset_x_entry = ttk.Entry(
            offset_frame,
            textvariable=self.offset_x_var,
            width=5,
            style="Dark.TEntry"
        )
        offset_x_entry.pack(side=tk.LEFT, padx=2)
        offset_x_entry.bind("<Return>", self._on_offset_change)
        offset_x_entry.bind("<FocusOut>", self._on_offset_change)
        
        self.offset_y_var = tk.IntVar(value=frame.offset_y)
        offset_y_entry = ttk.Entry(
            offset_frame,
            textvariable=self.offset_y_var,
            width=5,
            style="Dark.TEntry"
        )
        offset_y_entry.pack(side=tk.LEFT, padx=2)
        offset_y_entry.bind("<Return>", self._on_offset_change)
        offset_y_entry.bind("<FocusOut>", self._on_offset_change)
    
    def _on_included_change(self):
        """Appelé quand la case included est cochée/décochée."""
        States.log(f"Modification de l'inclusion de la frame {self.frame_number}")
        FramelistManager.set_included(self.frame_number, self.included_var.get())
    
    def _on_frame_click(self):
        """Appelé quand on clique sur le bouton de la frame."""
        States.log(f"Clic sur la frame {self.frame_number}")
        from src.ui.playback_panel import PlaybackPanel
        PlaybackPanel.get_instance().display_frame_manual(self.frame_number)
    
    def _on_offset_change(self, event=None):
        """Appelé quand un offset est modifié."""
        States.log(f"Modification des offsets de la frame {self.frame_number}")
        try:
            offset_x = int(self.offset_x_var.get())
            offset_y = int(self.offset_y_var.get())
            
            # Met à jour les offsets via FramelistManager
            FramelistManager.set_offset_frame(self.frame_number, offset_x, offset_y)
        except ValueError:
            # Restaure les anciennes valeurs en cas d'erreur
            frame = FramelistManager.get_framelist()[self.frame_number]
            self.offset_x_var.set(frame.offset_x)
            self.offset_y_var.set(frame.offset_y)
    
    def update_values(self, frame):
        """Met à jour les valeurs depuis une frame."""
        self.included_var.set(frame.included)
        self.offset_x_var.set(frame.offset_x)
        self.offset_y_var.set(frame.offset_y)
    
    def destroy(self):
        """Détruit la ligne."""
        self.frame.destroy() 