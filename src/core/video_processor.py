import cv2
from PIL import Image
import numpy as np
from typing import List, Optional

class VideoProcessor:
    """Processeur pour la conversion de vidéos en frames."""
    
    @staticmethod
    def extract_frames(video_path: str) -> Optional[List[Image.Image]]:
        """
        Extrait les frames d'une vidéo.
        
        Args:
            video_path: Chemin vers le fichier vidéo
            
        Returns:
            Optional[List[Image.Image]]: Liste des frames extraites ou None si erreur
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        frames = []
        success, frame = cap.read()
        while success:
            # Convertir BGR en RGB puis en PIL Image
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            frames.append(pil_image)  # Pas de .copy() ici, sera fait par le manager
            success, frame = cap.read()
        
        cap.release()
        return frames if frames else None
    
    @staticmethod
    def _cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
        """Convertit une image OpenCV en image PIL."""
        # Conversion BGR -> RGB
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image) 