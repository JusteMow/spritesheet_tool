# FrameEditFramelistSubpanel

#class #ui #frame #list #controller

## Description
Sous-panel spécialisé dans la gestion individuelle des frames. Fournit une interface scrollable pour :
- Visualisation et édition de chaque frame individuellement
- Gestion de l'inclusion/exclusion par frame
- Configuration des offsets individuels (X/Y)
- Prévisualisation directe des frames
- Statistiques sur les frames incluses

## Type
`SINGLETON` `CONTROLLER`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `frame` | `ttk.Frame` | Frame principale du sous-panel |
| `canvas` | `tk.Canvas` | Canvas pour le scroll |
| `scrollbar` | `ttk.Scrollbar` | Barre de défilement verticale |
| `content_frame` | `ttk.Frame` | Frame de contenu scrollable |
| `frame_rows` | `List[FrameRow]` | Liste des lignes de frames |

## Classes Internes

### FrameRow
Représente une ligne dans la liste des frames.
- **Variables:**
  - `frame_number` : Index de la frame
  - `included_var` : État d'inclusion (BooleanVar)
  - `offset_x_var` : Offset horizontal (IntVar)
  - `offset_y_var` : Offset vertical (IntVar)
- **Méthodes:**
  - `_on_included_change()` : Gère le toggle d'inclusion
  - `_on_frame_click()` : Affiche la frame dans le Displayer
  - `_on_offset_change()` : Met à jour les offsets
  - `update_values()` : Synchronise avec FramelistManager

## Méthodes

### Gestion de la Liste
#### `rebuild_list() -> None`
Reconstruit entièrement la liste des frames.
- **Actions:**
  - Nettoie les lignes existantes
  - Crée l'en-tête avec les statistiques
  - Crée une ligne par frame
  - Met à jour la zone scrollable
- **Usage:** Changement de la liste des frames

#### `update_values() -> None`
Met à jour les valeurs sans reconstruire.
- **Actions:**
  - Synchronise chaque ligne avec FramelistManager
- **Usage:** Changement de propriétés des frames

### Gestion du Scroll
#### `_on_frame_configure(event=None) -> None`
Met à jour la zone scrollable.
- **Actions:**
  - Reconfigure la région du canvas
- **Usage:** Redimensionnement du contenu

#### `_on_canvas_configure(event) -> None`
Ajuste la largeur du contenu.
- **Actions:**
  - Adapte la frame au canvas
- **Usage:** Redimensionnement de la fenêtre

#### `_on_mousewheel(event) -> None`
Gère le scroll avec la molette.
- **Actions:**
  - Défile le contenu verticalement
- **Usage:** Navigation utilisateur

## Dépendances
- [FramelistManager](/docs/classes/core/framelist_manager.md) - Gestion des frames
- [PlaybackPanel](/docs/classes/ui/playback_panel.md) - Prévisualisation des frames
- [States](/docs/classes/core/states.md) - Configuration globale
- [EventManager](/docs/classes/core/event_manager.md) - Système d'événements

## Pipelines Associés
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames
- [Events Pipeline](/docs/pipelines/events.md) - Système d'événements

## Points d'Attention
1. **Performance**
   - Gestion efficace des mises à jour
   - Reconstruction minimale de la liste
   - Optimisation du scroll

2. **Validation des Entrées**
   - Conversion des offsets en entiers
   - Restauration en cas d'erreur
   - Protection contre les valeurs invalides

3. **Interface Utilisateur**
   - Organisation claire des informations
   - Feedback visuel immédiat
   - Navigation fluide dans la liste

## Code Source
- [frame_edit_framelist_subpanel.py](/src/ui/panels/frame_edit_framelist_subpanel.py)

## Tags
#class #ui #frame #list #controller 