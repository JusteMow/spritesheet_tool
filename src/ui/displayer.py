import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import Optional
from src.core.framelist_manager import FramelistManager
from src.core.event_manager import EventManager
from src.core.states import States

class Displayer:
    """Affiche une image avec gestion du zoom et du pan."""
    
    _instance = None
    MIN_ZOOM = 0.1
    MAX_ZOOM = 10.0
    
    @classmethod
    def get_instance(cls) -> 'Displayer':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("Displayer n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise le displayer."""
        if Displayer._instance is not None:
            raise Exception("Displayer est un singleton")
        Displayer._instance = self
        
        States.log_debug("Initialisation du Displayer")
        
        # Frame principale
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas pour l'affichage
        self.canvas = tk.Canvas(
            self.frame,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Variables d'état
        self.zoom_factor = 1.0
        self.current_image: Optional[ImageTk.PhotoImage] = None
        self.original_image: Optional[Image.Image] = None  # Garde l'image originale pour le zoom
        self.image_id: Optional[int] = None
        self.pan_start_x = 0
        self.pan_start_y = 0
        
        # Bindings
        self._setup_bindings()
        
        # Abonnement aux événements
        EventManager.subscribe(EventManager.FRAMELIST_LIST_UPDATED, self._on_framelist_updated)
    
    def _on_framelist_updated(self, *args, **kwargs) -> None:
        """Appelé quand la liste des frames change."""
        States.log_debug("Mise à jour du Displayer suite à un changement dans la framelist")
        framelist = FramelistManager.get_framelist()
        if framelist:
            self.reset_zoom()
            self.show_frame(0)
            self.center_image()
    
    def _setup_bindings(self) -> None:
        """Configure les événements souris."""
        # Zoom avec la molette
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)  # Windows
        self.canvas.bind("<Button-4>", self._on_mousewheel)    # Linux up
        self.canvas.bind("<Button-5>", self._on_mousewheel)    # Linux down
        
        # Pan avec le clic gauche
        self.canvas.bind("<ButtonPress-1>", self.pan_start)
        self.canvas.bind("<B1-Motion>", self.pan_move)
    
    def center_image(self) -> None:
        """Centre l'image dans le canvas."""
        if not self.image_id or not self.current_image:
            return
            
        States.log_debug("Centrage de l'image")
        
        # Obtient les dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width = self.current_image.width()
        image_height = self.current_image.height()
        
        # Calcule la position centrée
        x = (canvas_width - image_width) // 2
        y = (canvas_height - image_height) // 2
        
        # Déplace l'image
        self.canvas.coords(self.image_id, x, y)
        States.log_debug(f"Image centrée à ({x}, {y})")
    
    def show_frame(self, frame_number: int) -> None:
        """
        Affiche une frame spécifique.
        
        Args:
            frame_number: Numéro de la frame à afficher
        """
        States.log_debug(f"Affichage de la frame {frame_number}")
        
        framelist = FramelistManager.get_framelist()
        if not framelist or frame_number >= len(framelist):
            States.log_debug("Pas de frame à afficher")
            return
        
        # Récupère l'image
        frame = framelist[frame_number]
        if not frame or not frame.image:
            States.log_debug("Frame invalide")
            return
            
        # Vérifie si la frame doit être affichée
        if States.show_included_only and not frame.included:
            States.log_debug("Frame non incluse, ignorée")
            return
        
        # Récupère l'image avec les offsets
        try:
            self.original_image = frame.get_image()
            if not self.original_image:
                States.log_debug("Image invalide")
                return
                
            # Clone l'image pour le zoom
            pil_image = self.original_image.copy()
            
            # Applique le zoom
            if self.zoom_factor != 1.0:
                try:
                    new_size = tuple(int(dim * self.zoom_factor) for dim in pil_image.size)
                    States.log_debug(f"Application du zoom {self.zoom_factor} -> {new_size}")
                    pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
                except Exception as e:
                    States.log(f"Erreur de zoom: {e}")
                    return
            
            # Convertit en PhotoImage
            self.current_image = ImageTk.PhotoImage(pil_image)
            
            # Affiche ou met à jour l'image
            if self.image_id is None:
                self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
                self.center_image()
            else:
                # Garde la position actuelle
                x, y = self.canvas.coords(self.image_id)
                self.canvas.itemconfig(self.image_id, image=self.current_image)
                
            States.log_debug("Image affichée avec succès")
            
        except Exception as e:
            States.log(f"Erreur d'affichage: {e}")
            return
    
    def set_zoom(self, factor: float) -> None:
        """
        Définit le facteur de zoom, centré sur le milieu du displayer.
        
        Args:
            factor: Nouveau facteur de zoom
        """
        if not self.image_id or not self.current_image:
            return
            
        old_factor = self.zoom_factor
        self.zoom_factor = max(self.MIN_ZOOM, min(self.MAX_ZOOM, factor))
        
        if self.zoom_factor != old_factor:
            States.log_debug(f"Zoom modifié : {old_factor} -> {self.zoom_factor}")
            
            # Récupère les dimensions du canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Récupère la position actuelle de l'image
            old_x, old_y = self.canvas.coords(self.image_id)
            
            # Calcule le point central du canvas
            center_x = canvas_width / 2
            center_y = canvas_height / 2
            
            # Calcule la distance entre le point central et le coin de l'image
            dx = center_x - old_x
            dy = center_y - old_y
            
            # Ajuste la position en fonction du changement de zoom
            zoom_ratio = self.zoom_factor / old_factor
            new_x = center_x - (dx * zoom_ratio)
            new_y = center_y - (dy * zoom_ratio)
            
            States.log_debug(f"Nouvelle position après zoom : ({new_x:.1f}, {new_y:.1f})")
            
            # Réaffiche la frame courante avec le nouveau zoom et la nouvelle position
            from .playback_panel import PlaybackPanel
            current_frame = PlaybackPanel.get_instance().frame_index
            self.show_frame(current_frame)
            
            # Applique la nouvelle position
            self.canvas.coords(self.image_id, new_x, new_y)
            States.log(f"Zoom appliqué : {self.zoom_factor:.1f}x")
    
    def zoom_in(self) -> None:
        """Augmente le zoom."""
        self.set_zoom(self.zoom_factor * 1.2)
    
    def zoom_out(self) -> None:
        """Diminue le zoom."""
        self.set_zoom(self.zoom_factor / 1.2)
    
    def reset_zoom(self) -> None:
        """Réinitialise le zoom."""
        States.log_debug("Reset du zoom")
        old_factor = self.zoom_factor
        self.zoom_factor = 1.0
        if old_factor != 1.0:
            from .playback_panel import PlaybackPanel
            current_frame = PlaybackPanel.get_instance().frame_index
            self.show_frame(current_frame)
    
    def _on_mousewheel(self, event) -> None:
        """Gère le zoom avec la molette."""
        # Détermine la direction
        if event.num == 5 or event.delta < 0:
            States.log("Zoom out via molette")
            self.zoom_out()
        else:
            States.log("Zoom in via molette")
            self.zoom_in()
    
    def pan_start(self, event) -> None:
        """Démarre le pan."""
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.canvas.config(cursor="fleur")
    
    def pan_move(self, event) -> None:
        """Déplace l'image pendant le pan."""
        if self.image_id is not None:
            # Calcule le déplacement
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y
            
            # Déplace l'image
            self.canvas.move(self.image_id, dx, dy)
            
            # Met à jour le point de départ
            self.pan_start_x = event.x
            self.pan_start_y = event.y
    
    def destroy(self) -> None:
        """Détruit le displayer."""
        States.log_debug("Destruction du Displayer")
        EventManager.unsubscribe(EventManager.FRAMELIST_LIST_UPDATED, self._on_framelist_updated)
        EventManager.unsubscribe(EventManager.FRAMELIST_PROP_UPDATED, self._on_framelist_updated)
        Displayer._instance = None
        self.frame.destroy() 