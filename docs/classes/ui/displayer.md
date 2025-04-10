# Displayer

#class #ui #display #view

## Description
Composant d'affichage responsable du rendu des frames à l'écran. Gère :
- Affichage des images avec zoom
- Pan (déplacement de la vue)
- Gestion du canvas et de ses dimensions
- Conversion et mise à l'échelle des images

## Type
`SINGLETON` `VIEW`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `zoom_factor` | `float` | Facteur de zoom actuel |
| `current_image` | `Optional[ImageTk.PhotoImage]` | Image actuellement affichée |
| `image_id` | `Optional[int]` | ID de l'image dans le canvas |
| `pan_start_x` | `int` | Position X de début de pan |
| `pan_start_y` | `int` | Position Y de début de pan |

## Méthodes

### Affichage
#### `show_frame(frame_number: int) -> None`
Affiche une frame spécifique.
- **Args:**
  - `frame_number`: Numéro de la frame à afficher
- **Actions:**
  - Vérifie la validité de la frame
  - Applique les offsets
  - Applique le zoom
  - Met à jour le canvas
- **Usage:** Affichage principal

### Gestion du Zoom
#### `set_zoom(factor: float) -> None`
Configure le facteur de zoom.
- **Args:**
  - `factor`: Nouveau facteur de zoom
- **Actions:**
  - Met à jour le zoom_factor
  - Réaffiche la frame courante
- **Usage:** Contrôle du zoom

### Gestion du Pan
#### `_setup_bindings() -> None`
Configure les événements souris.
- **Actions:**
  - Bind les événements de pan
  - Bind les événements de zoom
- **Usage:** Initialisation

#### `_on_framelist_updated() -> None`
Réagit aux changements de liste.
- **Actions:**
  - Met à jour l'affichage
- **Usage:** Event system

## Dépendances
- [FramelistManager](/docs/classes/core/framelist_manager.md) - Accès aux frames
- [EventManager](/docs/classes/core/event_manager.md) - Système d'événements
- [States](/docs/classes/core/states.md) - Configuration globale

## Pipelines Associés
- [Playback Pipeline](/docs/pipelines/playback.md) - Affichage des frames
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Prévisualisation des éditions

## Points d'Attention
1. **Performance d'Affichage**
   - Gestion efficace de la mémoire
   - Mise à l'échelle optimisée
   - Nettoyage des ressources

2. **Gestion des Erreurs**
   - Validation des frames
   - Protection contre les frames invalides
   - Gestion des erreurs de conversion

3. **Interface Utilisateur**
   - Réactivité du pan/zoom
   - Limites de zoom
   - Feedback visuel

## Code Source
- [displayer.py](/src/ui/displayer.py)

## Tags
#class #ui #display #view 