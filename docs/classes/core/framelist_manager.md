# FramelistManager

#class #core #frames #manager

## Description
Gestionnaire central des frames et de leurs modifications. Point névralgique de l'application qui maintient l'intégrité des images sources, gère les modifications des frames et orchestre les mises à jour UI.

## Type
`STATIC`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `_split_images` | `List[Image.Image]` | Images brutes issues du découpage, servant de source pour toutes les opérations |
| `_framelist` | `List[Frame]` | Liste des frames avec leurs propriétés (image, inclusion, offsets) |

## Méthodes

### Gestion des Images Sources
#### `set_split_images(images: List[Image.Image]) -> None`
Stocke les images brutes issues du découpage.
- **Args:**
  - `images` - Liste des images PIL à stocker
- **Note:** Effectue une copie profonde de chaque image
- **Usage:** Stockage initial après découpage

#### `get_split_images_deep_clones() -> List[Image.Image]`
Retourne des copies profondes des images sources.
- **Returns:** Liste des copies des images sources
- **Usage:** Utilisé pour les opérations de traitement d'image

### Gestion des Frames
#### `create_new_framelist() -> None`
Crée une nouvelle liste de frames à partir des images découpées.
- **Actions:**
  - Initialise les frames avec leurs propriétés
  - Initialise les offsets dans States
  - Traite les images avec les offsets initiaux
- **Events:** `FRAMELIST_LIST_UPDATED`

#### `set_included(frame_number: int, value: bool) -> None`
Modifie l'inclusion d'une frame.
- **Args:**
  - `frame_number`: Numéro de la frame à modifier
  - `value`: Nouvelle valeur d'inclusion
- **Events:** `FRAMELIST_PROP_UPDATED`

### Gestion des Offsets
#### `set_offset_frame(frame_index: int, offset_x: int, offset_y: int) -> None`
Met à jour les offsets d'une frame et retraite son image.
- **Args:**
  - `frame_index`: Index de la frame à modifier
  - `offset_x`: Nouvel offset horizontal
  - `offset_y`: Nouvel offset vertical
- **Events:** `FRAMELIST_PROP_UPDATED`
- **Voir:** [Frame Edit Pipeline](/docs/pipelines/frame_edit.md#offset-de-frame)

#### `set_offset_row(row_index: int, offset: int) -> None`
Met à jour l'offset d'une ligne et retraite les images concernées.
- **Args:**
  - `row_index`: Index de la ligne à modifier
  - `offset`: Nouvel offset vertical
- **Events:** `FRAMELIST_PROP_UPDATED`
- **Voir:** [Frame Edit Pipeline](/docs/pipelines/frame_edit.md#offset-de-lignecolonne)

#### `set_offset_column(col_index: int, offset: int) -> None`
Met à jour l'offset d'une colonne et retraite les images concernées.
- **Args:**
  - `col_index`: Index de la colonne à modifier
  - `offset`: Nouvel offset horizontal
- **Events:** `FRAMELIST_PROP_UPDATED`
- **Voir:** [Frame Edit Pipeline](/docs/pipelines/frame_edit.md#offset-de-lignecolonne)

### Autres Méthodes
#### `clear() -> None`
Vide les listes de frames.
- **Events:** `FRAMELIST_LIST_UPDATED`
- **Usage:** Nettoyage lors du changement de média

## Dépendances
- [Frame](/docs/classes/core/frame.md) - Structure de données pour les frames
- [EventManager](/docs/classes/core/event_manager.md) - Publication des événements
- [States](/docs/classes/core/states.md) - Configuration et logging
- [ImageProcessor](/docs/classes/processor/image_processor.md) - Traitement des images
- [OffsetProcessor](/docs/classes/processor/offset_processor.md) - Calcul des offsets

## Pipelines Associés
- [Import/Export Pipeline](/docs/pipelines/import_export.md) - Gestion des médias
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames
- [Events Pipeline](/docs/pipelines/events.md) - Système d'événements

## Points d'Attention
- Toujours utiliser des copies profondes des images sources
- Les modifications de frames déclenchent des événements UI
- Les offsets sont cumulatifs (frame + ligne + colonne)

## Code Source
- [framelist_manager.py](/src/core/framelist_manager.py)

## Tags
#class #core #frames #manager #static 