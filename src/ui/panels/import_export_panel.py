import tkinter as tk
from tkinter import ttk, filedialog
import os
from PIL import Image
from src.core.states import States
from src.core.image_processor import ImageProcessor
from src.core.video_processor import VideoProcessor
from src.core.framelist_manager import FramelistManager

class ImportExportPanel:
    """Interface pour l'import/export de médias."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'ImportExportPanel':
        """Retourne l'instance unique."""
        if cls._instance is None:
            raise Exception("ImportExportPanel n'est pas initialisé")
        return cls._instance
    
    def __init__(self, parent):
        """Initialise le panel."""
        if ImportExportPanel._instance is not None:
            raise Exception("ImportExportPanel est un singleton")
        ImportExportPanel._instance = self
        
        States.log("Initialisation de l'ImportExportPanel")
        
        self.frame = ttk.Frame(parent, style="Dark.TFrame")
        self.frame.pack(fill=tk.X, padx=10, pady=5)
        
        self._build_import_section()
        self._build_export_section()
    
    def _build_import_section(self):
        """Construit la section import."""
        # Titre
        ttk.Label(self.frame, text="Import Media", style="Dark.TLabel").pack(pady=(10, 2))
        
        # Import Spritesheet
        spritesheet_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        spritesheet_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(spritesheet_frame, text="Import Sprite Sheet", command=self.import_spritesheet, style="Dark.TButton").pack(fill=tk.X)
        
        # Rows/Columns
        rowcol_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        rowcol_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(rowcol_frame, text="Rows", style="Dark.TLabel").pack(side=tk.LEFT)
        self.import_rows_var = tk.IntVar(value=States.import_rows_var)
        self.import_rows_var.trace_add("write", self._on_rows_cols_changed)
        ttk.Entry(rowcol_frame, textvariable=self.import_rows_var, width=5, style="Dark.TEntry").pack(side=tk.LEFT, padx=2)
        
        ttk.Label(rowcol_frame, text="Columns", style="Dark.TLabel").pack(side=tk.LEFT)
        self.import_columns_var = tk.IntVar(value=States.import_columns_var)
        self.import_columns_var.trace_add("write", self._on_rows_cols_changed)
        ttk.Entry(rowcol_frame, textvariable=self.import_columns_var, width=5, style="Dark.TEntry").pack(side=tk.LEFT, padx=2)
        
        # Autres imports
        ttk.Button(self.frame, text="Import Folder", command=self.import_folder, style="Dark.TButton").pack(fill=tk.X, pady=2)
        ttk.Button(self.frame, text="Import Video", command=self.import_video, style="Dark.TButton").pack(fill=tk.X, pady=2)
    
    def _build_export_section(self):
        """Construit la section export."""
        # Titre
        ttk.Label(self.frame, text="Export Media", style="Dark.TLabel").pack(pady=(10, 2))
        
        # Export Spritesheet
        spritesheet_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        spritesheet_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(spritesheet_frame, text="Export Sprite Sheet", command=self.export_spritesheet, style="Dark.TButton").pack(fill=tk.X)
        
        # Autres exports
        ttk.Button(self.frame, text="Export Folder", command=self.export_frames, style="Dark.TButton").pack(fill=tk.X, pady=2)
        ttk.Button(self.frame, text="Export GIF", command=self.export_gif, style="Dark.TButton").pack(fill=tk.X, pady=2)
    
    def import_folder(self):
        """Importe un dossier d'images."""
        States.log("Import d'un dossier")
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
            
        # Nettoie l'état actuel
        FramelistManager.clear()
        
        # Liste les fichiers d'images
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        image_files = []
        for file in sorted(os.listdir(folder_path)):
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(folder_path, file))
        
        if not image_files:
            States.log("Aucune image trouvée dans le dossier")
            return
            
        States.log(f"{len(image_files)} images trouvées")
        
        # Charge les images
        frames = []
        for i, file_path in enumerate(image_files):
            try:
                image = Image.open(file_path)
                # Convertit en RGBA pour uniformiser le format
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                frames.append(image)
                States.log(f"Image chargée: {os.path.basename(file_path)}")
            except Exception as e:
                States.log(f"Erreur lors du chargement de {os.path.basename(file_path)}: {e}")
                continue
        
        if not frames:
            States.log("Aucune image n'a pu être chargée")
            return
            
        # Vérifie que toutes les images ont la même taille
        first_size = frames[0].size
        valid_frames = []
        for i, image in enumerate(frames):
            if image.size == first_size:
                valid_frames.append(image)
            else:
                States.log(f"Image {i} ignorée: taille différente ({image.size} vs {first_size})")
        
        if not valid_frames:
            States.log("Aucune image de taille compatible")
            return
            
        States.log(f"{len(valid_frames)} images valides")
        
        # Crée la framelist
        FramelistManager.set_split_images(valid_frames)
        FramelistManager.create_new_framelist()
    
    def import_spritesheet(self, file_path: str = None):
        """
        Importe une spritesheet.
        
        Args:
            file_path: Chemin optionnel du fichier à importer
        """
        States.log("Import d'une spritesheet")
        
        # Si pas de chemin fourni, ouvre le dialogue de sélection
        if not file_path:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
            )
        if file_path:
            # Nettoie l'état actuel
            FramelistManager.clear()
            
            # Charge l'image dans States
            from PIL import Image
            States.loaded_media = Image.open(file_path)
            States.import_rows_var = self.import_rows_var.get()
            States.import_columns_var = self.import_columns_var.get()
            
            # Découpe l'image en frames individuelles
            split_images = ImageProcessor.split()
            
            # Crée la nouvelle framelist avec les images découpées
            FramelistManager.set_split_images(split_images)
            
            # Crée la framelist
            FramelistManager.create_new_framelist()
    
    def import_video(self, video_path: str = None):
        """
        Importe une vidéo.
        
        Args:
            video_path: Chemin optionnel de la vidéo à importer
        """
        States.log("Import d'une vidéo")
        
        # Si pas de chemin fourni, ouvre le dialogue de sélection
        if not video_path:
            video_path = filedialog.askopenfilename(
                filetypes=[("Video files", "*.mp4;*.mov;*.avi")]
            )
        if not video_path:
            return
            
        # Nettoie l'état actuel
        FramelistManager.clear()
        
        # Extrait les frames
        frames = VideoProcessor.extract_frames(video_path)
        if not frames:
            States.log("Erreur lors de l'extraction des frames")
            return
            
        States.log(f"Création de {len(frames)} frames depuis la vidéo")
        
        # Crée la nouvelle framelist avec les frames extraites
        FramelistManager.set_split_images(frames)
        FramelistManager.create_new_framelist()
    
    def export_spritesheet(self):
        """Exporte en spritesheet."""
        States.log("Export en spritesheet")
        
        # Récupère les frames incluses
        framelist = FramelistManager._framelist
        included_frames = [frame.get_image() for frame in framelist if frame.included]
        
        if not included_frames:
            States.log("Aucune frame à exporter")
            return
            
        # Calcule les layouts possibles
        layouts = ImageProcessor.get_spritesheet_layouts(len(included_frames))
        if not layouts:
            States.log("Impossible de calculer un layout valide")
            return
            
        # Ouvre le dialogue de sélection du layout
        from .layout_suggestion_dialog import LayoutSuggestionDialog
        dialog = LayoutSuggestionDialog(self.frame, layouts)
        rows, cols = dialog.show()
        
        if not rows or not cols:  # L'utilisateur a annulé
            return
            
        # Crée la spritesheet
        spritesheet = ImageProcessor.create_spritesheet(included_frames, rows, cols)
        if not spritesheet:
            States.log("Erreur lors de la création de la spritesheet")
            return
            
        # Sauvegarde
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if file_path:
            spritesheet.save(file_path)
            States.log(f"Spritesheet exportée : {file_path}")
    
    def export_frames(self):
        """Exporte les frames individuellement."""
        States.log("Export des frames")
        
        # Récupère les frames incluses
        framelist = FramelistManager._framelist
        included_frames = [(i, frame) for i, frame in enumerate(framelist) if frame.included]
        
        if not included_frames:
            States.log("Aucune frame à exporter")
            return
            
        # Sélectionne le dossier de destination
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
            
        # Demande le préfixe du nom de fichier
        prefix_dialog = tk.Toplevel()
        prefix_dialog.title("Nom de base")
        prefix_dialog.transient(self.frame)
        prefix_dialog.grab_set()
        prefix_dialog.configure(bg='#2b2b2b')
        
        frame = ttk.Frame(prefix_dialog, style="Dark.TFrame")
        frame.pack(padx=10, pady=10)
        
        ttk.Label(frame, text="Préfixe pour les fichiers :", style="Dark.TLabel").pack(pady=(0, 5))
        prefix_var = tk.StringVar(value="frame")
        entry = ttk.Entry(frame, textvariable=prefix_var, style="Dark.TEntry")
        entry.pack(pady=5)
        
        def on_ok():
            prefix_dialog.quit()
            prefix_dialog.destroy()
            
        def on_cancel():
            prefix_var.set("")
            prefix_dialog.quit()
            prefix_dialog.destroy()
        
        btn_frame = ttk.Frame(frame, style="Dark.TFrame")
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(btn_frame, text="OK", command=on_ok, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Annuler", command=on_cancel, style="Dark.TButton").pack(side=tk.RIGHT, padx=5)
        
        # Centre la fenêtre
        prefix_dialog.update_idletasks()
        width = prefix_dialog.winfo_width()
        height = prefix_dialog.winfo_height()
        x = (prefix_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (prefix_dialog.winfo_screenheight() // 2) - (height // 2)
        prefix_dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        prefix_dialog.mainloop()
        base_name = prefix_var.get()
        
        if not base_name:  # L'utilisateur a annulé
            return
            
        # Sauvegarde chaque frame
        for i, frame in included_frames:
            filename = os.path.join(folder_path, f"{base_name}_{i:03d}.png")
            frame.get_image().save(filename)
            States.log(f"Frame exportée : {filename}")
            
        States.log(f"{len(included_frames)} frames exportées dans {folder_path}")
    
    def export_gif(self):
        """Exporte en GIF."""
        States.log("Export en GIF")
        
        # Récupère les frames incluses
        framelist = FramelistManager._framelist
        included_frames = [frame.get_image() for frame in framelist if frame.included]
        
        if not included_frames:
            States.log("Aucune frame à exporter")
            return
            
        # Crée le GIF
        gif = included_frames[0]  # Première frame comme base
        
        # Sauvegarde
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif")]
        )
        if file_path:
            gif.save(
                file_path,
                save_all=True,
                append_images=included_frames[1:],
                duration=int(1000 / 12),  # 12 FPS par défaut
                loop=0,  # 0 = boucle infinie
                disposal=2,  # Efface la frame précédente avant d'afficher la suivante
                transparency=0  # Index de la couleur transparente
            )
            States.log(f"GIF exporté : {file_path}")
    
    def show_layout_dialog(self):
        """Ouvre la boîte de dialogue de suggestion de layout."""
        States.log("Ouverture du dialogue de suggestion de layout")
        # TODO: Implémenter LayoutSuggestionDialog
        pass
    
    def destroy(self):
        """Détruit le panel."""
        States.log("Destruction de l'ImportExportPanel")
        ImportExportPanel._instance = None
        self.frame.destroy()

    def _on_rows_cols_changed(self, *args):
        """Appelé quand le nombre de lignes ou colonnes change."""
        try:
            rows = self.import_rows_var.get()
            cols = self.import_columns_var.get()
            if rows > 0 and cols > 0:
                States.log(f"Mise à jour grille {rows}x{cols}")
                States.import_rows_var = rows
                States.import_columns_var = cols
                if States.loaded_media:
                    # Nettoie l'état actuel
                    FramelistManager.clear()
                    
                    # Découpe l'image en frames individuelles
                    split_images = ImageProcessor.split()
                    
                    # Crée la nouvelle framelist avec les images découpées
                    FramelistManager.set_split_images(split_images)
                    FramelistManager.create_new_framelist()
        except tk.TclError:
            # Ignore les erreurs de conversion (quand le champ est vide)
            pass 