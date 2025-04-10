import tkinter as tk
from tkinter import ttk
from src.core.states import States
from src.core.framelist_manager import FramelistManager
from src.utils.ui.scrollable_panel import ScrollablePanel

class FrameEditRowColsOffsetSubpanel(ScrollablePanel):
    """Sous-panel pour la gestion des offsets de lignes et colonnes."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'FrameEditRowColsOffsetSubpanel':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("FrameEditRowColsOffsetSubpanel n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise le sous-panel."""
        if FrameEditRowColsOffsetSubpanel._instance is not None:
            raise Exception("FrameEditRowColsOffsetSubpanel est un singleton")
        FrameEditRowColsOffsetSubpanel._instance = self
        
        States.log("Initialisation du FrameEditRowColsOffsetSubpanel")
        
        # Initialise le ScrollablePanel
        super().__init__(parent, height=200, style="Dark.TFrame")
        
        # Pack le panel
        self.pack(fill=tk.X, pady=5)
        
        # Listes pour stocker les widgets
        self.row_entries = []
        self.col_entries = []
        
        # Section des lignes
        rows_frame = ttk.Frame(self.scrollable_frame, style="Dark.TFrame")
        ttk.Label(rows_frame, text="Lignes (offset Y)", style="Bold.TLabel").pack(fill=tk.X, padx=5, pady=5)
        
        rows_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for row in range(States.import_rows_var):
            frame = ttk.Frame(rows_frame, style="Dark.TFrame")
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=f"Ligne {row}", style="Dark.TLabel").pack(side=tk.LEFT)
            
            var = tk.IntVar(value=States.rows_offsets[row] if row < len(States.rows_offsets) else 0)
            entry = ttk.Entry(frame, textvariable=var, width=5, style="Dark.TEntry", justify=tk.RIGHT)
            entry.pack(side=tk.RIGHT, padx=5)
            entry.bind("<Return>", lambda e, r=row, v=var: self._on_row_offset_change(r, v))
            entry.bind("<FocusOut>", lambda e, r=row, v=var: self._on_row_offset_change(r, v))
            
            self.row_entries.append((var, entry))
        
        # Section des colonnes
        cols_frame = ttk.Frame(self.scrollable_frame, style="Dark.TFrame")
        ttk.Label(cols_frame, text="Colonnes (offset X)", style="Bold.TLabel").pack(fill=tk.X, padx=5, pady=5)
        
        cols_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for col in range(States.import_columns_var):
            frame = ttk.Frame(cols_frame, style="Dark.TFrame")
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=f"Colonne {col}", style="Dark.TLabel").pack(side=tk.LEFT)
            
            var = tk.IntVar(value=States.cols_offsets[col] if col < len(States.cols_offsets) else 0)
            entry = ttk.Entry(frame, textvariable=var, width=5, style="Dark.TEntry", justify=tk.RIGHT)
            entry.pack(side=tk.RIGHT, padx=5)
            entry.bind("<Return>", lambda e, c=col, v=var: self._on_col_offset_change(c, v))
            entry.bind("<FocusOut>", lambda e, c=col, v=var: self._on_col_offset_change(c, v))
            
            self.col_entries.append((var, entry))
    
    def _on_row_offset_change(self, row: int, var: tk.IntVar):
        """Appelé quand un offset de ligne est modifié."""
        try:
            offset = int(var.get())
            States.log(f"Modification offset ligne {row} -> {offset}")
            FramelistManager.set_offset_row(row, offset)
        except ValueError:
            # Restaure l'ancienne valeur en cas d'erreur
            var.set(States.rows_offsets[row] if row < len(States.rows_offsets) else 0)
    
    def _on_col_offset_change(self, col: int, var: tk.IntVar):
        """Appelé quand un offset de colonne est modifié."""
        try:
            offset = int(var.get())
            States.log(f"Modification offset colonne {col} -> {offset}")
            FramelistManager.set_offset_column(col, offset)
        except ValueError:
            # Restaure l'ancienne valeur en cas d'erreur
            var.set(States.cols_offsets[col] if col < len(States.cols_offsets) else 0)
    
    def destroy(self):
        """Détruit le sous-panel."""
        States.log("Destruction du FrameEditRowColsOffsetSubpanel")
        FrameEditRowColsOffsetSubpanel._instance = None
        super().destroy() 