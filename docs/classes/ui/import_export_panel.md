# ImportExportPanel

#class #ui #import #export #controller

## Description
Interface utilisateur pour l'import et l'export de médias. Gère :
- Import de spritesheet
- Import de dossier d'images
- Import de vidéo
- Export de spritesheet
- Export de frames individuelles
- Export de GIF
- Configuration de la grille d'import

## Type
`SINGLETON`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `import_rows_var` | `tk.IntVar` | Nombre de lignes pour l'import |
| `import_columns_var` | `tk.IntVar` | Nombre de colonnes pour l'import |
| `export_rows_var` | `tk.IntVar` | Nombre de lignes pour l'export |
| `export_columns_var` | `tk.IntVar` | Nombre de colonnes pour l'export |

## Méthodes

### Import
#### `import_spritesheet() -> None`
Import d'une spritesheet.
- **Actions:**
  - Sélection du fichier via dialogue
  - Stockage dans `States.loaded_media`
  - Découpage via `ImageProcessor.split()`
  - Création de la framelist
- **Usage:** Bouton Import Spritesheet

#### `import_folder() -> None`
Import d'un dossier d'images.
- **Actions:**
  - Sélection du dossier
  - Chargement des images PNG
  - Vérification des dimensions
  - Création de la framelist
- **Usage:** Bouton Import Folder

#### `import_video() -> None`
Import d'une vidéo.
- **Actions:**
  - Sélection du fichier
  - Import via `VideoProcessor`
  - Création de la framelist
- **Usage:** Bouton Import Video

### Export
#### `export_spritesheet() -> None`
Export en spritesheet.
- **Actions:**
  - Calcul des layouts possibles
  - Sélection du layout via dialogue
  - Création via `ImageProcessor`
  - Sauvegarde du fichier
- **Usage:** Bouton Export Spritesheet

#### `export_frames() -> None`
Export des frames individuelles.
- **Actions:**
  - Sélection du dossier
  - Configuration du préfixe
  - Export des frames incluses
- **Usage:** Bouton Export Frames

#### `export_gif() -> None`
Export en GIF animé.
- **Actions:**
  - Configuration de l'animation
  - Export via `ImageProcessor`
  - Sauvegarde du fichier
- **Usage:** Bouton Export GIF

### Configuration
#### `_on_rows_cols_changed() -> None`
Gestion du changement de grille.
- **Actions:**
  - Met à jour `States`
  - Redécoupe l'image si chargée
  - Recrée la framelist
- **Usage:** Modification des spinbox rows/cols

## Dépendances
- [ImageProcessor](/docs/classes/processor/image_processor.md) - Traitement des images
- [VideoProcessor](/docs/classes/processor/video_processor.md) - Import vidéo
- [FramelistManager](/docs/classes/core/framelist_manager.md) - Gestion des frames
- [States](/docs/classes/core/states.md) - Configuration globale

## Pipelines Associés
- [Import/Export Pipeline](/docs/pipelines/import_export.md) - Flux d'import/export
- [Grid Import Settings Pipeline](/docs/pipelines/grid_import_settings.md) - Configuration grille

## Points d'Attention
1. **Validation des Entrées**
   - Vérification des dimensions
   - Validation des formats de fichiers
   - Gestion des erreurs d'import/export

2. **Gestion de la Mémoire**
   - Deep copy des images
   - Nettoyage des ressources
   - Gestion des gros fichiers

3. **Configuration de la Grille**
   - Validation rows/cols > 0
   - Recalcul automatique
   - Préservation des proportions

## Code Source
- [import_export_panel.py](/src/ui/panels/import_export_panel.py)

## Tags
#class #ui #import #export #controller 