from typing import List
from PIL import Image
from src.core.frame import Frame
from src.core.event_manager import EventManager
from src.core.states import States

class FramelistManager:
    """Gère les listes de frames avant et après traitement."""
    
    # Variables de classe
    _split_images: List[Image.Image] = []  # Images brutes issues du découpage
    _framelist: List[Frame] = []  # Liste des frames avec leurs propriétés
    
    @classmethod
    def get_split_images(cls) -> List[Image.Image]:
        """Retourne une copie profonde des images brutes."""
        States.log_debug("Copie des images brutes demandée")
        return [img.copy() for img in cls._split_images]
    
    @classmethod
    def set_split_images(cls, images: List[Image.Image]) -> None:
        """Définit la liste des images brutes."""
        States.log("Images chargées")
        States.log_debug(f"Mise à jour des images brutes - {len(images)} images")
        cls._split_images = images
    
    @classmethod
    def get_framelist(cls) -> List[Frame]:
        """Liste des frames avec offsets."""
        States.log_debug("Accès à la framelist")
        return cls._framelist
    
    @classmethod
    def set_frame_image(cls, frame_number: int, image: Image.Image) -> None:
        """Met à jour l'image d'une frame."""
        States.log_debug(f"Mise à jour de l'image de la frame {frame_number}")
        if 0 <= frame_number < len(cls._framelist):
            cls._framelist[frame_number].image = image
            EventManager.publish(EventManager.FRAMELIST_PROP_UPDATED)
    
    @classmethod
    def create_new_framelist(cls) -> None:
        """
        Crée une nouvelle liste de frames à partir des images découpées.
        Initialise les offsets et traite les images.
        """
        States.log("Grille mise à jour")
        States.log_debug("Création d'une nouvelle framelist")
        
        # Ferme les images de l'ancienne framelist
        States.log_debug("Nettoyage de l'ancienne framelist")
        for frame in cls._framelist:
            frame.close()
        cls._framelist.clear()
        
        # Récupère les copies des images sources
        split_images = cls.get_split_images()
        States.log_debug(f"Création de {len(split_images)} frames")
        
        # Crée la liste des frames avec leurs propriétés
        cls._framelist = [
            Frame(
                image=img,
                frame_number=i,
                included=True,
                offset_x=0,
                offset_y=0
            )
            for i, img in enumerate(split_images)
        ]
        
        # Initialise les offsets dans States
        States.rows_offsets = [0] * States.import_rows_var
        States.cols_offsets = [0] * States.import_columns_var
        States.log_debug("Offsets initialisés")
        
        # Traite les images avec les offsets initiaux
        States.log_debug("Application des offsets initiaux")
        for i in range(len(cls._framelist)):
            # Calcule l'offset final
            from src.core.offset_processor import OffsetProcessor
            processed_x, processed_y = OffsetProcessor.get_frame_offset(i)
            
            # Applique l'offset à une copie de l'image source
            from src.core.image_processor import ImageProcessor
            image_clone = split_images[i]
            processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
            
            # Met à jour l'image dans la frame
            cls.set_frame_image(i, processed_image)
        
        # Notifie du changement
        EventManager.publish(EventManager.FRAMELIST_LIST_UPDATED)
    
    @classmethod
    def set_included(cls, frame_number: int, value: bool) -> None:
        """
        Modifie l'inclusion d'une frame.
        
        Args:
            frame_number: Numéro de la frame à modifier
            value: Nouvelle valeur d'inclusion
        """
        States.log(f"Frame {frame_number + 1} {'incluse' if value else 'exclue'}")
        
        if 0 <= frame_number < len(cls._framelist):
            cls._framelist[frame_number].included = value
            EventManager.publish(EventManager.FRAMELIST_PROP_UPDATED)
            
    @classmethod
    def set_offset_frame(cls, frame_index: int, offset_x: int, offset_y: int) -> None:
        """
        Met à jour les offsets d'une frame et retraite son image.
        
        Args:
            frame_index: Index de la frame à modifier
            offset_x: Nouvel offset horizontal
            offset_y: Nouvel offset vertical
        """
        States.log(f"Modification des offsets de la frame {frame_index}: ({offset_x}, {offset_y})")
        
        # Met à jour les offsets dans la frame
        frame = cls._framelist[frame_index]
        frame.offset_x = offset_x
        frame.offset_y = offset_y
        
        # Calcule l'offset final
        from src.core.offset_processor import OffsetProcessor
        processed_x, processed_y = OffsetProcessor.get_frame_offset(frame_index)
        States.log_debug(f"Offsets finaux calculés: ({processed_x}, {processed_y})")
        
        # Récupère une copie de l'image source
        split_images = cls.get_split_images()
        image_clone = split_images[frame_index]
        
        # Applique l'offset
        from src.core.image_processor import ImageProcessor
        processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
        
        # Met à jour l'image dans la frame
        cls.set_frame_image(frame_index, processed_image)
        
    @classmethod
    def set_offset_row(cls, row_index: int, offset: int) -> None:
        """
        Met à jour l'offset d'une ligne et retraite les images concernées.
        
        Args:
            row_index: Index de la ligne à modifier
            offset: Nouvel offset vertical
        """
        States.log(f"Modification de l'offset de la ligne {row_index}: {offset}")
        
        # Met à jour l'offset dans States
        States.rows_offsets[row_index] = offset
        
        # Récupère les frames de la ligne
        from src.core.offset_processor import OffsetProcessor
        frames = OffsetProcessor.get_pictures_on_row(row_index)
        States.log_debug(f"Frames à mettre à jour: {frames}")
        
        # Récupère les copies des images sources
        split_images = cls.get_split_images()
        
        # Retraite chaque frame
        for frame_index in frames:
            # Calcule l'offset final
            processed_x, processed_y = OffsetProcessor.get_frame_offset(frame_index)
            
            # Applique l'offset à l'image (déjà une copie)
            from src.core.image_processor import ImageProcessor
            image_clone = split_images[frame_index]  # Déjà une copie depuis get_split_images()
            processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
            
            # Met à jour l'image dans la frame
            cls.set_frame_image(frame_index, processed_image)
            
    @classmethod
    def set_offset_column(cls, col_index: int, offset: int) -> None:
        """
        Met à jour l'offset d'une colonne et retraite les images concernées.
        
        Args:
            col_index: Index de la colonne à modifier
            offset: Nouvel offset horizontal
        """
        States.log(f"Modification de l'offset de la colonne {col_index}: {offset}")
        
        # Met à jour l'offset dans States
        States.cols_offsets[col_index] = offset
        
        # Récupère les frames de la colonne
        from src.core.offset_processor import OffsetProcessor
        frames = OffsetProcessor.get_pictures_on_column(col_index)
        
        # Récupère les copies des images sources
        split_images = cls.get_split_images()
        
        # Retraite chaque frame
        for frame_index in frames:
            # Calcule l'offset final
            processed_x, processed_y = OffsetProcessor.get_frame_offset(frame_index)
            
            # Applique l'offset à l'image
            from src.core.image_processor import ImageProcessor
            image_clone = split_images[frame_index]  # Déjà une copie depuis get_split_images()
            processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
            
            # Met à jour l'image dans la frame
            cls.set_frame_image(frame_index, processed_image)
    
    @classmethod
    def clear(cls) -> None:
        """Vide les listes de frames et libère la mémoire des images."""
        States.log_debug("Nettoyage des listes de frames")
        
        # Ferme les images sources
        for img in cls._split_images:
            img.close()
        cls._split_images.clear()
        
        # Ferme les frames
        for frame in cls._framelist:
            frame.close()
        cls._framelist.clear()
        
        EventManager.publish(EventManager.FRAMELIST_LIST_UPDATED) 