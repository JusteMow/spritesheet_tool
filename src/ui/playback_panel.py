import tkinter as tk
from tkinter import ttk
from typing import Optional
from src.core.event_manager import EventManager
from src.core.framelist_manager import FramelistManager
from src.core.states import States

class PlaybackPanel:
    """Interface de navigation dans les frames."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'PlaybackPanel':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("PlaybackPanel n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise le panel."""
        if PlaybackPanel._instance is not None:
            raise Exception("PlaybackPanel est un singleton")
        PlaybackPanel._instance = self
        
        States.log_debug("Initialisation du PlaybackPanel")
        
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.frame_index = 0
        self.fps_var = tk.IntVar(value=10)
        self.current_frame = 0
        
        self._build_ui()
        self._setup_events()
    
    def _build_ui(self):
        """Construit l'interface utilisateur."""
        # Contrôles de lecture
        controls = ttk.Frame(self.frame, style="Dark.TFrame")
        controls.pack(pady=10)
        
        ttk.Button(controls, text="<", command=self.previous_frame, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Play", command=self.play_animation, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Stop", command=self.stop_animation, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text=">", command=self.next_frame, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        
        # FPS control
        ttk.Label(controls, text="FPS", style="Dark.TLabel").pack(side=tk.LEFT, padx=5)
        ttk.Entry(controls, textvariable=self.fps_var, width=5, style="Dark.TEntry").pack(side=tk.LEFT, padx=2)
        
        # Included checkbox
        self.included_var = tk.BooleanVar(value=True)
        ttk.Label(controls, text="Included", style="Dark.TLabel").pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(controls, variable=self.included_var, command=self.toggle_current_frame_included, style="Dark.TCheckbutton").pack(side=tk.LEFT, padx=2)
        
        # Show included only
        self.show_included_var = tk.BooleanVar(value=States.show_included_only)
        ttk.Label(controls, text="Show Included Only", style="Dark.TLabel").pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(controls, variable=self.show_included_var, command=self._on_show_included_changed, style="Dark.TCheckbutton").pack(side=tk.LEFT, padx=2)
        
        # Slider
        self.slider = ttk.Scale(self.frame, from_=0, to=0, orient=tk.HORIZONTAL, command=self.slider_update_by_user, style="Dark.Horizontal.TScale")
        self.slider.pack(fill=tk.X, padx=10)
        
        # Info label
        self.info_label = ttk.Label(self.frame, text="", style="Dark.TLabel")
        self.info_label.pack(pady=2)
    
    def _setup_events(self):
        """Configure les événements."""
        EventManager.subscribe(EventManager.FRAMELIST_PROP_UPDATED, self.on_framelist_prop_updated)
        EventManager.subscribe(EventManager.FRAMELIST_LIST_UPDATED, self.on_framelist_list_updated)
    
    def play_animation(self) -> None:
        """Lance l'animation."""
        States.log("Lecture démarrée")
        from .animator import Animator
        Animator.play()
    
    def stop_animation(self) -> None:
        """Arrête l'animation."""
        States.log("Lecture arrêtée")
        from .animator import Animator
        Animator.stop()
    
    def display_frame_manual(self, frame: int) -> None:
        """Affiche une frame manuellement (boutons)."""
        States.log_debug(f"Affichage manuel de la frame {frame}")
        self.stop_animation()
        self.slider_update_auto(frame)
        self.display_frame(frame)
    
    def display_frame(self, frame: int) -> None:
        """Affiche une frame (appelé par slider)."""
        from .displayer import Displayer
        framelist = FramelistManager.get_framelist()
        if not framelist or frame >= len(framelist):
            States.log_debug("Frame invalide")
            return
            
        # Vérifie si la frame est valide selon les filtres
        if States.show_included_only and not framelist[frame].included:
            States.log_debug("Frame non incluse, recherche de la prochaine frame incluse")
            # Cherche la prochaine frame incluse
            next_frame = self._get_next_included_frame(frame, 1)
            if next_frame == frame:  # Si pas de frame incluse trouvée
                States.log("Aucune frame incluse trouvée")
                return
            frame = next_frame
            
        self.frame_index = frame
        Displayer.get_instance().show_frame(frame)
        self.included_var.set(framelist[frame].included)
        self._update_info_label()
        States.log_debug(f"Frame {frame} affichée")
    
    def display_frame_animator(self, frame: int) -> None:
        """Affiche une frame (appelé par Animator)."""
        self.slider_update_auto(frame)
        self.display_frame(frame)
    
    def slider_update_by_user(self, value: str) -> None:
        """MAJ du slider par l'utilisateur."""
        try:
            frame = int(float(value))
            self.display_frame(frame)
        except ValueError:
            pass
    
    def slider_update_auto(self, frame: int) -> None:
        """MAJ du slider automatique."""
        self.slider.set(frame)
    
    def toggle_current_frame_included(self) -> None:
        """Change l'inclusion de la frame courante."""
        framelist = FramelistManager.get_framelist()
        if not framelist or self.frame_index >= len(framelist):
            return
            
        # Toggle l'état d'inclusion
        new_state = not framelist[self.frame_index].included
        FramelistManager.set_included(self.frame_index, new_state)
        self.included_var.set(new_state)
        States.log(f"Frame {self.frame_index + 1} {'incluse' if new_state else 'exclue'}")
    
    def _on_show_included_changed(self) -> None:
        """Appelé quand la checkbox Show Included Only change."""
        States.show_included_only = self.show_included_var.get()
        States.log(f"Affichage {'uniquement' if States.show_included_only else 'de toutes'} des frames incluses")
        self.on_framelist_list_updated()
    
    def _get_next_included_frame(self, current: int, direction: int) -> int:
        """
        Trouve la prochaine frame incluse dans la direction donnée.
        
        Args:
            current: Index actuel
            direction: 1 pour suivant, -1 pour précédent
        """
        framelist = FramelistManager.get_framelist()
        if not framelist:
            return 0
            
        total = len(framelist)
        next_index = current
        
        for _ in range(total):  # Évite la boucle infinie
            next_index = (next_index + direction) % total
            if not States.show_included_only or framelist[next_index].included:
                return next_index
        
        return current  # Si aucune frame incluse trouvée
    
    def previous_frame(self) -> None:
        """Frame précédente."""
        States.log("Frame précédente")
        new_index = self._get_next_included_frame(self.frame_index, -1)
        self.display_frame_manual(new_index)
    
    def next_frame(self) -> None:
        """Frame suivante."""
        States.log("Frame suivante")
        new_index = self._get_next_included_frame(self.frame_index, 1)
        self.display_frame_manual(new_index)
    
    def on_framelist_prop_updated(self) -> None:
        """Réaction au changement de propriété d'une frame."""
        self._update_info_label()
    
    def on_framelist_list_updated(self) -> None:
        """Réaction au changement de la liste de frames."""
        framelist = FramelistManager.get_framelist()
        if States.show_included_only:
            included_count = sum(1 for f in framelist if f.included)
            self.slider.configure(to=max(0, included_count - 1))
        else:
            self.slider.configure(to=max(0, len(framelist) - 1))
        self.frame_index = 0
        self.display_frame(0)
    
    def _update_info_label(self) -> None:
        """Met à jour le label d'information."""
        framelist = FramelistManager.get_framelist()
        if framelist:
            total = len(framelist)
            current = self.frame_index + 1
            included = sum(1 for f in framelist if f.included)
            self.info_label.config(text=f"Frame {current}/{total} (Included: {included})")
            
    def destroy(self):
        """Détruit le panel."""
        States.log_debug("Destruction du PlaybackPanel")
        EventManager.unsubscribe(EventManager.FRAMELIST_PROP_UPDATED, self.on_framelist_prop_updated)
        EventManager.unsubscribe(EventManager.FRAMELIST_LIST_UPDATED, self.on_framelist_list_updated)
        PlaybackPanel._instance = None
        self.frame.destroy()

    def toggle_play_stop(self) -> None:
        """Démarre ou arrête la lecture."""
        from .animator import Animator
        if Animator._is_playing:
            self.stop_animation()
        else:
            self.play_animation() 