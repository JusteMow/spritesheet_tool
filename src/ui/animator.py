import tkinter as tk
from typing import Optional
from src.core.framelist_manager import FramelistManager
from src.core.states import States

class Animator:
    """Gère la boucle de lecture animée."""
    
    # Variables de classe
    _is_playing = False
    _current_frame = 0
    _animation_id = None
    _fps = 10
    
    @staticmethod
    def play() -> None:
        """Démarre la boucle."""
        from .playback_panel import PlaybackPanel
        Animator.stop()
        Animator._is_playing = True
        Animator._fps = max(1, PlaybackPanel.get_instance().fps_var.get())
        States.log_debug(f"Animation démarrée à {Animator._fps} FPS")
        Animator.loop()
    
    @staticmethod
    def stop() -> None:
        """Stoppe la boucle."""
        Animator._is_playing = False
        if Animator._animation_id:
            tk._default_root.after_cancel(Animator._animation_id)
            Animator._animation_id = None
            States.log_debug("Animation arrêtée")
    
    @staticmethod
    def loop() -> None:
        """Appelle PlaybackPanel.display_frame_animator en boucle."""
        if not Animator._is_playing:
            return
        
        from .playback_panel import PlaybackPanel
        framelist = FramelistManager.get_framelist()
        
        if framelist:
            # Trouve la prochaine frame à afficher
            next_frame = Animator._current_frame
            found = False
            for _ in range(len(framelist)):
                next_frame = (next_frame + 1) % len(framelist)
                if not States.show_included_only or framelist[next_frame].included:
                    found = True
                    break
            
            if found:
                States.log_debug(f"Animation: affichage frame {next_frame}")
                Animator._current_frame = next_frame
                PlaybackPanel.get_instance().display_frame_animator(Animator._current_frame)
            else:
                States.log_debug("Animation: aucune frame incluse trouvée")
            
            # Programme la prochaine frame
            Animator._animation_id = tk._default_root.after(
                int(1000 / Animator._fps),
                Animator.loop
            ) 