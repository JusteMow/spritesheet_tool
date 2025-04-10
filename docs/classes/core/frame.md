# Frame

#class #core #frame #data

## Description
Structure de données représentant une image avec ses propriétés de traitement. Unité de base manipulée par le `FramelistManager`. Chaque frame encapsule une image PIL avec ses métadonnées (numéro, inclusion, offsets).

## Type
`INSTANCE`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `_image` | `PIL.Image.Image` | Image PIL en RGBA |
| `_frame_number` | `int` | Identifiant unique dans la liste |
| `_included` | `bool` | État d'inclusion pour l'export |
| `_offset_x` | `int` | Décalage horizontal individuel |
| `_offset_y` | `int` | Décalage vertical individuel |

## Méthodes

### Constructeur
#### `__init__(image: Image.Image, frame_number: int, included: bool = True, offset_x: int = 0, offset_y: int = 0) -> None`
Initialise une frame avec ses propriétés.
- **Args:**
  - `image`: L'image PIL
  - `frame_number`: Numéro de la frame
  - `included`: Si la frame est incluse dans l'export
  - `offset_x`: Décalage horizontal initial
  - `offset_y`: Décalage vertical initial
- **Usage:** Création d'une nouvelle frame par le `FramelistManager`

### Getters/Setters

- Edition/accès seulement via `FramelistManager`.

## Dépendances
- `PIL.Image` - Manipulation des images
- [States](/docs/classes/core/states.md) - Logging des modifications

## Pipelines Associés
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames
- [Import/Export Pipeline](/docs/pipelines/import_export.md) - Gestion des médias

## Points d'Attention
1. **Immutabilité Partielle**
   - `frame_number` non modifiable après création
   - Autres propriétés modifiables via setters

2. **Logging**
   - Chaque modification est loggée via `States`
   - Format : "Frame X property -> value"

3. **Image Management**
   - L'image est toujours un deep clone de l'original
   - Modifications via `FramelistManager` uniquement
   - Pas de traitement direct dans la classe

## Code Source
- [frame.py](/src/core/frame.py)

## Tags
#class #core #frame #data 