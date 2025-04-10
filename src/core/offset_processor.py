from typing import Tuple, List
from src.core.states import States
from src.core.framelist_manager import FramelistManager

class OffsetProcessor:
    """Calcule les offsets finaux à appliquer (image + ligne + colonne)."""
    
    @staticmethod
    def get_frame_offset(frame_number: int) -> Tuple[int, int]:
        """
        Calcule l'offset final pour une frame.
        Combine les offsets individuels avec les offsets de ligne/colonne.
        
        Args:
            frame_number: Numéro de la frame
        
        Returns:
            Tuple[int, int]: Offset final (x, y)
        """
        # Récupère la ligne et colonne de la frame
        row = frame_number // States.import_columns_var
        col = frame_number % States.import_columns_var
        
        States.log(f"Calcul offset frame {frame_number} (ligne {row}, colonne {col})")
        
        # Offset de ligne/colonne
        row_offset_y = States.rows_offsets[row] if row < len(States.rows_offsets) else 0
        col_offset_x = States.cols_offsets[col] if col < len(States.cols_offsets) else 0
        
        States.log(f"Offset ligne {row}: {row_offset_y}")
        States.log(f"Offset colonne {col}: {col_offset_x}")
        
        # Récupère l'offset de la frame depuis framelist
        frame = FramelistManager.get_framelist()[frame_number]
        frame_offset_x = frame.offset_x
        frame_offset_y = frame.offset_y
        
        States.log(f"Offset frame: ({frame_offset_x}, {frame_offset_y})")
        
        # Combine les offsets
        final_offset_x = col_offset_x + frame_offset_x
        final_offset_y = row_offset_y + frame_offset_y
        
        States.log(f"Offset final: ({final_offset_x}, {final_offset_y})")
        return final_offset_x, final_offset_y
    
    @staticmethod
    def get_pictures_on_row(row: int) -> List[int]:
        """
        Retourne la liste des indices des frames sur une ligne.
        
        Args:
            row: Numéro de la ligne
            
        Returns:
            List[int]: Liste des indices des frames
        """
        frames = []
        start = row * States.import_columns_var
        end = start + States.import_columns_var
        
        for i in range(start, end):
            if i < len(FramelistManager.get_framelist()):
                frames.append(i)
                
        return frames
    
    @staticmethod
    def get_pictures_on_column(col: int) -> List[int]:
        """
        Retourne la liste des indices des frames sur une colonne.
        
        Args:
            col: Numéro de la colonne
            
        Returns:
            List[int]: Liste des indices des frames
        """
        frames = []
        for row in range(States.import_rows_var):
            frame_index = row * States.import_columns_var + col
            if frame_index < len(FramelistManager.get_framelist()):
                frames.append(frame_index)
                
        return frames
    
    @staticmethod
    def reset() -> None:
        """Réinitialise tous les offsets."""
        States.log("Reset des offsets")
        States.rows_offsets = [0] * States.import_rows_var
        States.cols_offsets = [0] * States.import_columns_var 