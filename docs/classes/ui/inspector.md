# Inspector

#class #ui #host #container

## Description
Conteneur latéral droit qui héberge dynamiquement les panneaux de configuration. Gère :
- Chargement dynamique des panels
- Nettoyage des panels précédents
- Gestion du scroll vertical
- Organisation de l'espace d'affichage

## Type
`SINGLETON` `HOST`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `current_panel` | `Optional[Panel]` | Panel actuellement affiché |
| `content_frame` | `ttk.Frame` | Frame de contenu scrollable |
| `canvas` | `tk.Canvas` | Canvas pour le scroll |
| `scrollbar` | `ttk.Scrollbar` | Barre de défilement verticale |

## Méthodes

### Gestion des Panels
#### `load_panel(panel_type: str) -> None`
Charge un nouveau panel.
- **Args:**
  - `panel_type`: Type de panel à charger ("import_export" ou "frame_edit")
- **Actions:**
  - Nettoie le panel actuel
  - Instancie le nouveau panel
  - Configure le scroll
- **Usage:** Changement de mode d'édition

#### `destroy_current_panel() -> None`
Nettoie le panel actuel.
- **Actions:**
  - Détruit le panel courant
  - Réinitialise les variables
- **Usage:** Nettoyage avant nouveau panel

### Gestion du Scroll
#### `_on_frame_configure() -> None`
Met à jour la zone scrollable.
- **Actions:**
  - Reconfigure la région du canvas
- **Usage:** Redimensionnement

#### `_on_canvas_configure() -> None`
Ajuste la largeur du contenu.
- **Actions:**
  - Ajuste la frame au canvas
- **Usage:** Redimensionnement

## Dépendances
- [ImportExportPanel](/docs/classes/ui/import_export_panel.md) - Panel d'import/export
- [FrameEditPanel](/docs/classes/ui/frame_edit_panel.md) - Panel d'édition
- [States](/docs/classes/core/states.md) - Logging

## Pipelines Associés
- [Import/Export Pipeline](/docs/pipelines/import_export.md) - Configuration import/export
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames

## Points d'Attention
1. **Gestion de la Mémoire**
   - Nettoyage complet des panels
   - Libération des ressources
   - Gestion des singletons

2. **Interface Utilisateur**
   - Scroll fluide
   - Adaptation à la taille
   - Organisation de l'espace

3. **Changement de Panels**
   - Transition propre
   - Sauvegarde des états
   - Cohérence des données

## Code Source
- [inspector.py](/src/ui/inspector.py)

## Tags
#class #ui #host #container 