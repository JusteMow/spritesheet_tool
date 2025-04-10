# FrameEditPanel

#class #ui #frame #edit #host

## Description
Panel hôte qui coordonne trois sous-panels spécialisés pour l'édition des frames :
- `FrameEditSelectionSubpanel` - Gestion de la sélection groupée des frames
- `FrameEditRowColsOffsetSubpanel` - Configuration des offsets de lignes/colonnes
- `FrameEditFramelistSubpanel` - Gestion individuelle des frames et leurs offsets

## Type
`SINGLETON` `HOST`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `selection_subpanel` | `FrameEditSelectionSubpanel` | Sous-panel de sélection groupée |
| `rowcols_offset_subpanel` | `FrameEditRowColsOffsetSubpanel` | Sous-panel d'offsets lignes/colonnes |
| `framelist_subpanel` | `FrameEditFramelistSubpanel` | Sous-panel de gestion des frames |

## Sous-Panels

### FrameEditSelectionSubpanel
Panel de sélection groupée.
- **Fonctionnalités:**
  - Sélection/désélection globale
  - Sélection 1 frame sur X
  - Inversion de la sélection
  - Reset des offsets
- **Usage:** Opérations groupées sur les frames

### FrameEditRowColsOffsetSubpanel
Panel d'offsets lignes/colonnes.
- **Fonctionnalités:**
  - Configuration des offsets de lignes
  - Configuration des offsets de colonnes
  - Prévisualisation en temps réel
- **Usage:** Ajustement des offsets par ligne/colonne

### FrameEditFramelistSubpanel
Panel de gestion individuelle.
- **Fonctionnalités:**
  - Liste scrollable des frames
  - Toggle d'inclusion par frame
  - Configuration des offsets par frame
  - Prévisualisation directe
- **Usage:** Édition frame par frame

## Méthodes

### Événements
#### `on_framelist_prop_updated() -> None`
Réagit aux changements de propriétés.
- **Actions:**
  - Met à jour les valeurs du `framelist_subpanel`
- **Usage:** Event system

#### `on_framelist_list_updated() -> None`
Réagit aux changements de liste.
- **Actions:**
  - Met à jour les sous-panels
- **Usage:** Event system

## Dépendances
- [FramelistManager](/docs/classes/core/framelist_manager.md) - Gestion des frames
- [EventManager](/docs/classes/core/event_manager.md) - Système d'événements
- [States](/docs/classes/core/states.md) - Configuration globale

## Pipelines Associés
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames
- [Events Pipeline](/docs/pipelines/events.md) - Système d'événements

## Points d'Attention
1. **Coordination des Sous-Panels**
   - Synchronisation des états
   - Propagation des événements
   - Cohérence des données

2. **Gestion des Événements**
   - Éviter les boucles de mise à jour
   - Ordre de propagation
   - Performance des mises à jour

3. **Interface Utilisateur**
   - Organisation logique des contrôles
   - Feedback visuel immédiat
   - Gestion du scroll et de l'espace

## Code Source
- [frame_edit_panel.py](/src/ui/panels/frame_edit_panel.py)

## Tags
#class #ui #frame #edit #host 