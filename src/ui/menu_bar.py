import tkinter as tk
from src.core.states import States

class MenuBar:
    """Barre de menu horizontale."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'MenuBar':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("MenuBar n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise la barre de menu."""
        if MenuBar._instance is not None:
            raise Exception("MenuBar est un singleton")
        MenuBar._instance = self
        
        States.log("Initialisation du MenuBar")
        
        self.menu_bar = tk.Menu(parent)
        parent.config(menu=self.menu_bar)
        
        # Menu File
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Menu Edit
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        self._setup_menus()
    
    def _setup_menus(self):
        """Configure les menus."""
        # File menu
        self.file_menu.add_command(label="Import/Export", command=self.on_click_import_export)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self._quit)
        
        # Edit menu
        self.edit_menu.add_command(label="Frame Edit", command=self.on_click_frame_edit)
    
    def on_click_import_export(self):
        """Charge ImportExportPanel dans Inspector."""
        States.log("Chargement du panel Import/Export")
        from .inspector import Inspector
        Inspector.get_instance().load_panel("import_export")
    
    def on_click_frame_edit(self):
        """Charge FrameEditPanel dans Inspector."""
        States.log("Chargement du panel Frame Edit")
        from .inspector import Inspector
        Inspector.get_instance().load_panel("frame_edit")
    
    def _quit(self):
        """Quitte l'application."""
        States.log("Demande de fermeture de l'application")
        from .main_window import MainWindow
        MainWindow.get_instance().destroy()
        
    def destroy(self):
        """Détruit la barre de menu."""
        States.log("Destruction du MenuBar")
        MenuBar._instance = None
        self.menu_bar.destroy() 