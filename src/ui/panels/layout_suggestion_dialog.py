import tkinter as tk
from tkinter import ttk
from src.core.states import States

class LayoutSuggestionDialog:
    """Dialogue de suggestion de layout pour l'export de spritesheet."""
    
    def __init__(self, parent, layouts):
        """
        Initialise le dialogue.
        
        Args:
            parent: Widget parent
            layouts: Liste de tuples (rows, cols) possibles
        """
        self.parent = parent
        self.layouts = layouts
        self.result = None
        
        # Crée la fenêtre
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Suggestion de Layout")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Applique le thème sombre
        self.dialog.configure(bg='#2b2b2b')  # Même couleur que Dark.TFrame
        
        # Construit l'UI
        self._build_ui()
        
        # Force la mise à jour pour obtenir les dimensions réelles
        self.dialog.update_idletasks()
        
        # Calcule la taille minimale nécessaire
        min_width = max(
            self.layout_frame.winfo_reqwidth(),  # Largeur des boutons
            250  # Largeur minimale
        ) + 40  # Padding horizontal total
        
        min_height = (
            self.layout_frame.winfo_reqheight() +  # Hauteur des boutons de layout
            60 +  # Hauteur du titre + padding
            40 +  # Hauteur du bouton annuler + padding
            20    # Padding vertical total
        )
        
        # Limite la hauteur maximale
        window_height = min(min_height, 600)
        window_width = min_width
        
        # Centre la fenêtre
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Applique la géométrie
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _build_ui(self):
        """Construit l'interface utilisateur."""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, style="Dark.TFrame")
        main_frame.pack(padx=10, pady=10)
        
        # Label explicatif
        ttk.Label(main_frame, text="Choisissez un layout pour la spritesheet :", style="Dark.TLabel").pack(pady=(0, 10))
        
        # Liste des layouts
        self.layout_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        self.layout_frame.pack(fill=tk.BOTH, expand=True)
        
        # Trie les layouts par nombre de lignes croissant
        sorted_layouts = sorted(self.layouts, key=lambda x: x[0])
        
        for rows, cols in sorted_layouts:
            layout_btn = ttk.Button(
                self.layout_frame,
                text=f"{rows}×{cols}",
                command=lambda r=rows, c=cols: self._on_layout_selected(r, c),
                style="Dark.TButton"
            )
            layout_btn.pack(fill=tk.X, pady=2)
        
        # Boutons
        btn_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            btn_frame,
            text="Annuler",
            command=self._on_cancel,
            style="Dark.TButton"
        ).pack(side=tk.RIGHT, padx=5)
    
    def _on_layout_selected(self, rows, cols):
        """
        Appelé quand un layout est sélectionné.
        
        Args:
            rows: Nombre de lignes
            cols: Nombre de colonnes
        """
        States.log(f"Layout sélectionné : {rows}x{cols}")
        self.result = (rows, cols)
        self.dialog.destroy()
    
    def _on_cancel(self):
        self.dialog.destroy()
    
    def show(self) -> tuple[int, int]:
        """
        Affiche le dialogue et attend la sélection.
        
        Returns:
            Tuple (rows, cols) ou (None, None) si annulé
        """
        self.dialog.wait_window()
        return self.result if self.result else (None, None) 