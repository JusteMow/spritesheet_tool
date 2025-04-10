# FrameEditRowColsOffsetSubpanel

#class #ui #frame #offset #controller

## Description
Sous-panel spécialisé dans la gestion des offsets par lignes et colonnes. Fournit une interface pour :
- Configuration des offsets verticaux (Y) par ligne
- Configuration des offsets horizontaux (X) par colonne
- Prévisualisation en temps réel des modifications
- Interface scrollable pour gérer de nombreuses lignes/colonnes

## Type
`SINGLETON` `CONTROLLER`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `frame` | `ttk.Frame` | Frame principale du sous-panel |
| `canvas` | `tk.Canvas` | Canvas pour le scroll |
| `scrollbar` | `ttk.Scrollbar` | Barre de défilement verticale |
| `content_frame` | `ttk.Frame` | Frame de contenu scrollable |
| `row_entries` | `List[Tuple[tk.IntVar, ttk.Entry]]` | Liste des widgets pour les offsets de lignes |
| `col_entries` | `List[Tuple[tk.IntVar, ttk.Entry]]` | Liste des widgets pour les offsets de colonnes |

## Méthodes

### Gestion des Offsets
#### `_on_row_offset_change(row: int, var: tk.IntVar) -> None`
Gère la modification d'un offset de ligne.
- **Args:**
  - `row`: Index de la ligne modifiée
  - `var`: Variable contenant la nouvelle valeur
- **Actions:**
  - Valide et convertit l'entrée
  - Met à jour via `FramelistManager`
  - Retraite les images affectées
- **Usage:** Modification d'un offset de ligne

#### `_on_col_offset_change(col: int, var: tk.IntVar) -> None`
Gère la modification d'un offset de colonne.
- **Args:**
  - `col`: Index de la colonne modifiée
  - `var`: Variable contenant la nouvelle valeur
- **Actions:**
  - Valide et convertit l'entrée
  - Met à jour via `FramelistManager`
  - Retraite les images affectées
- **Usage:** Modification d'un offset de colonne

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
- [FramelistManager](/docs/classes/core/framelist_manager.md) - Gestion des frames et offsets
- [States](/docs/classes/core/states.md) - Configuration globale
- [EventManager](/docs/classes/core/event_manager.md) - Système d'événements

## Pipelines Associés
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames
- [Events Pipeline](/docs/pipelines/events.md) - Système d'événements

## Points d'Attention
1. **Validation des Entrées**
   - Conversion en entiers
   - Restauration en cas d'erreur
   - Protection contre les valeurs invalides

2. **Performance**
   - Retraitement efficace des images
   - Gestion optimisée du scroll
   - Mise à jour ciblée des frames

3. **Interface Utilisateur**
   - Organisation claire lignes/colonnes
   - Feedback visuel immédiat
   - Navigation fluide dans la liste

## Code Source
- [frame_edit_rowcols_offset_subpanel.py](/src/ui/panels/frame_edit_rowcols_offset_subpanel.py)

## Tags
#class #ui #frame #offset #controller 