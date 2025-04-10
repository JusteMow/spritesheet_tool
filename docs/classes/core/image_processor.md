# ImageProcessor

#class #core #processor #image

## Description
Processeur principal pour la manipulation des images. Fournit des fonctions pures pour le traitement des images, sans état interne.

## Type
`STATIC`

## Méthodes

### Découpage
#### `split() -> List[Image.Image]`
Découpe une spritesheet en frames individuelles.
- **Entrées:**
  - `States.loaded_media` - Image source
  - `States.import_rows_var` - Nombre de lignes
  - `States.import_columns_var` - Nombre de colonnes
- **Sortie:** Liste des images découpées
- **Usage:** Découpage initial d'une spritesheet

### Traitement des Offsets
#### `process_offset(image: Image.Image, offset_x: int, offset_y: int) -> Image.Image`
Applique des offsets à une image.
- **Args:**
  - `image` - Image source
  - `offset_x` - Décalage horizontal
  - `offset_y` - Décalage vertical
- **Retour:** Nouvelle image avec offsets appliqués
- **Usage:** Application des offsets individuels aux frames

### Export
#### `create_spritesheet(frames: List[Image.Image], rows: int, cols: int) -> Optional[Image.Image]`
Crée une spritesheet à partir d'une liste de frames.
- **Args:**
  - `frames` - Liste des images à assembler
  - `rows` - Nombre de lignes
  - `cols` - Nombre de colonnes
- **Retour:** Image assemblée ou None si erreur
- **Usage:** Export final en spritesheet

#### `export_gif() -> Optional[Image.Image]`
Exporte les frames en GIF animé.
- **Entrées:**
  - Frames incluses depuis `FramelistManager`
- **Retour:** GIF animé ou None si erreur
- **Usage:** Export en format GIF animé

### Calcul de Layout
#### `get_spritesheet_layouts(num_frames: int) -> List[Tuple[int, int]]`
Calcule les dispositions possibles pour une spritesheet.
- **Args:**
  - `num_frames` - Nombre de frames à disposer
- **Retour:** Liste de tuples (rows, cols) triée par ratio optimal
- **Usage:** Suggestion de layouts pour l'export

## Dépendances
- `PIL.Image` - Manipulation d'images
- `States` - Configuration et logging
- `Frame` - Structure de données des frames
- `FramelistManager` - Accès aux frames

## Pipelines Associés
- [Import Pipeline](/docs/pipelines/import_export.md#import) - Découpage initial
- [Export Pipeline](/docs/pipelines/import_export.md#export) - Création des fichiers finaux
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Application des offsets

## Points d'Attention

1. **Pureté des Fonctions**
   - Ne modifie jamais les images d'entrée
   - Crée toujours de nouvelles images
   - Pas d'état interne

2. **Performance**
   - Gestion de la mémoire avec `copy()`
   - Protection contre les images invalides
   - Validation des dimensions

3. **Formats**
   - Standardisation en RGBA
   - Gestion de la transparence
   - Compatibilité des dimensions

## Code Source
- [image_processor.py](/src/core/image_processor.py)

## Tags
#class #core #processor #image #static 