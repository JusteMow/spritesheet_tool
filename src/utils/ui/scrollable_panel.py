import tkinter as tk
from tkinter import ttk
from src.utils.ui.scroll_manager import ScrollManager
from src.ui.themes import Themes

class ScrollablePanel(ttk.Frame):
    """
    Panel de base avec fonctionnalité de scroll.
    Tout panel nécessitant du scroll doit hériter de cette classe.
    """
    def __init__(self, parent, height=None, width=None, style="Dark.TFrame"):
        super().__init__(parent, style=style)
        
        # Crée le canvas et la scrollbar
        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            bg=Themes.BACKGROUND
        )
        if height:
            self.canvas.configure(height=height)
        if width:
            self.canvas.configure(width=width)
            
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            style="Dark.Vertical.TScrollbar"
        )
        
        # Crée la frame qui contiendra le contenu scrollable
        self.scrollable_frame = ttk.Frame(self.canvas, style=style)
        
        # Configure le canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            tags="self.scrollable_frame"
        )
        
        # Configure la scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind les événements de configuration
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Pack les widgets
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Enregistre le panel auprès du ScrollManager
        self.scroll_manager = ScrollManager()
        self.scroll_manager.register_panel(self)
        
    def _on_frame_configure(self, event=None):
        """Met à jour la région de scroll quand la taille du contenu change."""
        # Met à jour la région de scroll pour inclure tout le contenu
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_canvas_configure(self, event):
        """Met à jour la taille de la frame interne quand le canvas est redimensionné."""
        # Ajuste la largeur de la frame au canvas
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )
        
    def needs_scroll(self) -> bool:
        """Vérifie si le scroll est nécessaire (contenu plus grand que la vue)."""
        return self.canvas.winfo_height() < self.canvas.bbox("all")[3]
        
    def apply_scroll(self, event):
        """Applique le scroll selon l'événement de la molette."""
        self.canvas.yview_scroll(int(-1 * (event.delta/120)), "units")
        
    def destroy(self):
        """Nettoie proprement le panel en le désenregistrant du ScrollManager."""
        self.scroll_manager.unregister_panel(self)
        super().destroy() 