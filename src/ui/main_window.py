import tkinter as tk
from tkinter import ttk
import tkinterdnd2
from src.ui.themes import Themes
from src.ui.menu_bar import MenuBar
from src.ui.displayer import Displayer
from src.ui.playback_panel import PlaybackPanel
from src.ui.inspector import Inspector
from src.ui.panels.import_export_panel import ImportExportPanel
from src.ui.keybinding_manager import KeybindingManager
from src.utils.ui.drag_n_drop_manager import DragNDropManager
from src.core.states import States

class MainWindow:
    """Fenêtre principale de l'application."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'MainWindow':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("MainWindow n'est pas initialisée")
        return cls._instance
    
    def __init__(self):
        """Initialise la fenêtre principale."""
        if MainWindow._instance is not None:
            raise Exception("MainWindow est un singleton")
        MainWindow._instance = self
        
        # Active le mode debug
        States.debug_mode = True
        States.log("Initialisation de la MainWindow")
        
        # Crée la fenêtre avec support du drag and drop
        self.root = tkinterdnd2.TkinterDnD.Tk()
        self.root.title("Sprite Tool")
        self.root.geometry("1280x1024")
        self.root.configure(bg=Themes.BACKGROUND)
        
        # Setup theme
        Themes.setup()
        
        # Main layout
        self.main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column
        self.left_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Menu bar
        self.menu_bar = MenuBar(self.root)
        
        # Displayer
        self.displayer = Displayer(self.left_frame)
        
        # Playback panel
        self.playback_panel = PlaybackPanel(self.left_frame)
        
        # Inspector (right column)
        self.inspector = Inspector(self.main_frame)
        
        # Import/Export panel (dans l'inspector)
        self.inspector.load_panel("import_export")
        
        # Initialise le manager de raccourcis
        self.keybinding_manager = KeybindingManager(self.root)
        
        # Initialise le manager de drag and drop
        self.drag_n_drop_manager = DragNDropManager(self.root)
        
        # Bind window close
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
    
    def run(self):
        """Lance l'application."""
        States.log("Démarrage de l'application")
        self.root.mainloop()
        
    def destroy(self):
        """Détruit la fenêtre principale."""
        States.log("Fermeture de l'application")
        self.inspector.destroy()
        self.playback_panel.destroy()
        self.displayer.destroy()
        self.menu_bar.destroy()
        if self.keybinding_manager:
            self.keybinding_manager.destroy()
        if self.drag_n_drop_manager:
            self.drag_n_drop_manager.destroy()
        MainWindow._instance = None
        self.root.destroy() 