from typing import Optional
from PIL import Image
from src.core.states import States

class Frame:
    """Représente une image avec ses propriétés."""
    
    def __init__(
        self,
        image: Image.Image,
        frame_number: int,
        included: bool = True,
        offset_x: int = 0,
        offset_y: int = 0
    ):
        """
        Initialise une frame.
        
        Args:
            image: L'image PIL
            frame_number: Numéro de la frame
            included: Si la frame est incluse dans l'export
            offset_x: Décalage horizontal
            offset_y: Décalage vertical
        """
        States.log_debug(f"Création de la frame {frame_number}")
        self._image = image
        self._frame_number = frame_number
        self._included = included
        self._offset_x = offset_x
        self._offset_y = offset_y
    
    @property
    def image(self) -> Image.Image:
        """L'image PIL."""
        return self._image
        
    @image.setter
    def image(self, value: Image.Image) -> None:
        """Modifie l'image."""
        States.log_debug(f"Frame {self._frame_number} image mise à jour")
        self._image = value
    
    @property
    def frame_number(self) -> int:
        """Numéro de la frame."""
        return self._frame_number
    
    @property
    def included(self) -> bool:
        """Si la frame est incluse dans l'export."""
        return self._included
    
    @included.setter
    def included(self, value: bool) -> None:
        """Modifie l'inclusion de la frame."""
        States.log_debug(f"Frame {self._frame_number} included -> {value}")
        self._included = value
    
    @property
    def offset_x(self) -> int:
        """Décalage horizontal."""
        return self._offset_x
    
    @offset_x.setter
    def offset_x(self, value: int) -> None:
        """Modifie le décalage horizontal."""
        States.log_debug(f"Frame {self._frame_number} offset_x -> {value}")
        self._offset_x = value
    
    @property
    def offset_y(self) -> int:
        """Décalage vertical."""
        return self._offset_y
    
    @offset_y.setter
    def offset_y(self, value: int) -> None:
        """Modifie le décalage vertical."""
        States.log_debug(f"Frame {self._frame_number} offset_y -> {value}")
        self._offset_y = value
    
    def get_image(self) -> Image.Image:
        """Retourne l'image. On peut éventuellement appliuquer des traitements."""
        return self._image
    
    def close(self) -> None:
        """Ferme l'image et libère la mémoire."""
        if self._image:
            self._image.close()
            self._image = None
    
    def __repr__(self) -> str:
        """Représentation textuelle de la frame."""
        return (
            f"Frame(number={self._frame_number}, "
            f"included={self._included}, "
            f"offset=({self._offset_x}, {self._offset_y}))"
        ) 