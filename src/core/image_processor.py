from typing import List, Tuple, Optional
from PIL import Image
from src.core.states import States
from src.core.frame import Frame


class ImageProcessor:
    """Gestion du traitement des images."""
    
    @staticmethod
    def split() -> List[Image.Image]:
        """
        Découpe une spritesheet en frames individuelles.
        
        Returns:
            List[Image.Image]: Liste des images découpées
        """
        States.log_debug("[ImageProcessor.split] Début du découpage")
        States.log("Découpage de la spritesheet en frames individuelles")
        if not States.loaded_media:
            States.log("Pas d'image chargée")
            States.log_debug("[ImageProcessor.split] Sortie anticipée - pas d'image chargée")
            return []
            
        img_width, img_height = States.loaded_media.size
        frame_width = img_width // States.import_columns_var
        frame_height = img_height // States.import_rows_var
        
        States.log(f"Dimensions des frames: {frame_width}x{frame_height}")
        States.log_debug(f"[ImageProcessor.split] Dimensions image: {img_width}x{img_height}, grille: {States.import_columns_var}x{States.import_rows_var}")
        
        # Découpe les images
        split_images = []
        for row in range(States.import_rows_var):
            for col in range(States.import_columns_var):
                box = (
                    col * frame_width,
                    row * frame_height,
                    (col + 1) * frame_width,
                    (row + 1) * frame_height
                )
                States.log_debug(f"[ImageProcessor.split] Découpe frame [{row},{col}] à la position {box}")
                # Crée une copie de l'image découpée
                image = States.loaded_media.crop(box).copy()
                split_images.append(image)
        
        States.log(f"{len(split_images)} images découpées")
        States.log_debug("[ImageProcessor.split] Fin du découpage")
        return split_images
    
    @staticmethod
    def process_offset(image: Image.Image, offset_x: int, offset_y: int) -> Image.Image:
        """
        Applique des offsets à une image.
        Fonction pure qui ne modifie pas l'image d'entrée.
        
        Args:
            image: Image source à traiter
            offset_x: Décalage horizontal
            offset_y: Décalage vertical
            
        Returns:
            Image.Image: Nouvelle image avec les offsets appliqués
        """
        States.log_debug(f"[ImageProcessor.process_offset] Début du traitement - image {image.size}, offsets ({offset_x}, {offset_y})")
        States.log(f"Application des offsets ({offset_x}, {offset_y}) à une image")
        
        # Crée une nouvelle image avec les mêmes dimensions
        width, height = image.size
        processed = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        States.log_debug(f"[ImageProcessor.process_offset] Image vide créée: {width}x{height}")
        
        # Colle l'image avec les offsets
        processed.paste(
            image,
            (offset_x, offset_y),
            image if image.mode == 'RGBA' else None
        )
        States.log_debug("[ImageProcessor.process_offset] Image collée avec offsets")
        
        return processed
    
    @staticmethod
    def export_spritesheet(frames: List[Frame], path: str, layout: Tuple[int, int]) -> None:
        """
        Exporte les frames dans une spritesheet.
        
        Args:
            frames: Liste des frames à exporter
            path: Chemin du fichier de sortie
            layout: Tuple (colonnes, lignes) définissant la disposition
        """
        States.log_debug(f"[ImageProcessor.export_spritesheet] Début export vers {path} avec layout {layout}")
        if not frames:
            States.log("Pas de frames à exporter")
            States.log_debug("[ImageProcessor.export_spritesheet] Sortie anticipée - pas de frames")
            return
            
        cols, rows = layout
        States.log(f"Export en spritesheet {cols}x{rows}")
        
        # Calcule les dimensions maximales des frames
        max_width = max(frame.image.size[0] for frame in frames)
        max_height = max(frame.image.size[1] for frame in frames)
        States.log_debug(f"[ImageProcessor.export_spritesheet] Dimensions max des frames: {max_width}x{max_height}")
        
        # Crée la spritesheet vide
        sheet_width = cols * max_width
        sheet_height = rows * max_height
        sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        States.log_debug(f"[ImageProcessor.export_spritesheet] Spritesheet créée: {sheet_width}x{sheet_height}")
        
        # Place les frames
        for i, frame in enumerate(frames):
            if i >= cols * rows:
                States.log_debug(f"[ImageProcessor.export_spritesheet] Limite de frames atteinte à {i}")
                break
                
            row = i // cols
            col = i % cols
            x = col * max_width
            y = row * max_height
            
            States.log_debug(f"[ImageProcessor.export_spritesheet] Placement frame {i} à ({x}, {y})")
            sheet.paste(
                frame.image,
                (x, y),
                frame.image if frame.image.mode == 'RGBA' else None
            )
            
        # Sauvegarde
        sheet.save(path)
        States.log(f"Spritesheet exportée vers {path}")
        States.log_debug("[ImageProcessor.export_spritesheet] Export terminé")
    
    @staticmethod
    def export_gif(frames: List[Frame], path: str) -> None:
        """
        Exporte les frames en GIF animé.
        
        Args:
            frames: Liste des frames à exporter
            path: Chemin du fichier de sortie
        """
        States.log_debug(f"[ImageProcessor.export_gif] Début export vers {path}")
        if not frames:
            States.log("Pas de frames à exporter")
            States.log_debug("[ImageProcessor.export_gif] Sortie anticipée - pas de frames")
            return
            
        States.log(f"Export en GIF de {len(frames)} frames")
        
        # Prépare les images pour le GIF
        images = []
        for i, frame in enumerate(frames):
            States.log_debug(f"[ImageProcessor.export_gif] Préparation frame {i}")
            # Convertit en RGB pour éviter les problèmes de transparence
            rgb_image = Image.new('RGB', frame.image.size, (255, 255, 255))
            rgb_image.paste(frame.image, mask=frame.image.split()[3] if frame.image.mode == 'RGBA' else None)
            images.append(rgb_image)
            
        # Sauvegarde
        duration = 1000 // States.fps_var  # Durée en ms
        States.log_debug(f"[ImageProcessor.export_gif] Sauvegarde avec durée {duration}ms par frame")
        images[0].save(
            path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0
        )
        States.log(f"GIF exporté vers {path}")
        States.log_debug("[ImageProcessor.export_gif] Export terminé")
    
    @staticmethod
    def get_spritesheet_layouts(num_frames: int) -> List[Tuple[int, int]]:
        """
        Calcule les dispositions possibles pour une spritesheet.
        
        Args:
            num_frames: Nombre de frames à disposer
            
        Returns:
            Liste de tuples (rows, cols) triée par ratio largeur/hauteur
        """
        States.log(f"Calcul des dispositions pour {num_frames} frames")
        layouts = []
        
        # Calcule toutes les paires possibles
        for rows in range(1, num_frames + 1):
            if num_frames % rows == 0:
                cols = num_frames // rows
                # Calcule le ratio largeur/hauteur
                ratio = abs(cols / rows - 1.6)  # 1.6 est proche du ratio d'or
                layouts.append((rows, cols, ratio))
        
        # Trie par ratio et retire le ratio du résultat
        layouts.sort(key=lambda x: x[2])
        return [(r, c) for r, c, _ in layouts]
    
    @staticmethod
    def create_spritesheet(frames: List[Image.Image], rows: int, cols: int) -> Optional[Image.Image]:
        """
        Crée une spritesheet à partir d'une liste de frames.
        Fonction pure qui ne modifie pas les images d'entrée.
        
        Args:
            frames: Liste des images à assembler
            rows: Nombre de lignes
            cols: Nombre de colonnes
            
        Returns:
            Image assemblée ou None si erreur
        """
        if not frames:
            States.log("Aucune frame à assembler")
            return None
            
        # Calcule les dimensions
        frame_width, frame_height = frames[0].size
        sheet_width = frame_width * cols
        sheet_height = frame_height * rows
        
        # Crée la spritesheet
        spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        
        # Colle les frames
        for i, frame in enumerate(frames):
            if i >= rows * cols:  # Protection contre les dépassements
                break
            x = (i % cols) * frame_width
            y = (i // cols) * frame_height
            spritesheet.paste(frame, (x, y))
        
        return spritesheet
    
