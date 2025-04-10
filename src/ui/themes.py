import tkinter as tk
from tkinter import ttk

class Themes:
    """Gestion des thèmes et styles de l'interface."""
    
    # Couleurs
    BACKGROUND = "#2b2b2b"
    FOREGROUND = "#ffffff"
    BUTTON_BG = "#333333"
    BUTTON_ACTIVE_BG = "#8B0000"
    ENTRY_BG = "#333333"
    SCROLLBAR_BG = "#333333"
    SCROLLBAR_TROUGH = "#1e1e1e"
    
    @classmethod
    def setup(cls):
        """Configure les styles ttk."""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frame sombre
        style.configure(
            "Dark.TFrame",
            background=cls.BACKGROUND
        )
        
        # Label sombre
        style.configure(
            "Dark.TLabel",
            background=cls.BACKGROUND,
            foreground=cls.FOREGROUND
        )
        
        # Bouton sombre
        style.configure(
            "Dark.TButton",
            background=cls.BUTTON_BG,
            foreground=cls.FOREGROUND,
            padding=5
        )
        style.map(
            "Dark.TButton",
            background=[("active", cls.BUTTON_ACTIVE_BG)],
            foreground=[("active", cls.FOREGROUND)]
        )
        
        # Entry sombre
        style.configure(
            "Dark.TEntry",
            fieldbackground=cls.ENTRY_BG,
            foreground=cls.FOREGROUND,
            padding=5
        )
        
        # Checkbutton sombre
        style.configure(
            "Dark.TCheckbutton",
            background=cls.BACKGROUND,
            foreground=cls.FOREGROUND
        )
        
        # Scrollbar sombre
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=cls.SCROLLBAR_BG,
            troughcolor=cls.SCROLLBAR_TROUGH,
            bordercolor=cls.SCROLLBAR_TROUGH,
            arrowcolor=cls.FOREGROUND
        )
        style.map(
            "Dark.Vertical.TScrollbar",
            background=[
                ("pressed", "#444444"),
                ("active", "#3c3c3c")
            ],
            arrowcolor=[
                ("pressed", "#888888"),
                ("active", "#777777")
            ]
        )
        
        # Scale
        style.configure("Dark.Horizontal.TScale", 
                       background=cls.BACKGROUND)
        
        # Scrollbar
        style.configure("Dark.TScrollbar", 
                       background=cls.BUTTON_BG,
                       troughcolor=cls.BACKGROUND) 