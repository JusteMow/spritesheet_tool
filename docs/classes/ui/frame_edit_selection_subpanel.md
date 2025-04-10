# FrameEditSelectionSubpanel

#class #ui #frame #selection #controller

## Description
Sous-panel spécialisé dans la gestion groupée des frames. Fournit une interface pour :
- Sélection/désélection globale des frames
- Sélection 1 frame sur X
- Inversion de la sélection
- Réinitialisation des offsets
- Gestion efficace des opérations en masse

## Type
`SINGLETON` `CONTROLLER`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `skip_var` | `tk.IntVar` | Intervalle pour la sélection 1 sur X |
| `frame` | `ttk.Frame` | Frame principale du sous-panel |

## Méthodes

### Sélection Globale
#### `select_all() -> None`
Sélectionne toutes les frames.
- **Actions:**
  - Parcourt toutes les frames
  - Met `included` à `True`
  - Déclenche `FRAMELIST_PROP_UPDATED`
- **Usage:** Bouton "Tout"

#### `select_none() -> None`
Désélectionne toutes les frames.
- **Actions:**
  - Parcourt toutes les frames
  - Met `included` à `False`
  - Déclenche `FRAMELIST_PROP_UPDATED`
- **Usage:** Bouton "Rien"

#### `select_invert() -> None`
Inverse l'état de sélection.
- **Actions:**
  - Parcourt toutes les frames
  - Inverse la valeur de `included`
  - Déclenche `FRAMELIST_PROP_UPDATED`
- **Usage:** Bouton "Inverser"

### Sélection Conditionnelle
#### `_select_every_x() -> None`
Sélectionne une frame sur X.
- **Args:**
  - Utilise `skip_var` pour l'intervalle
- **Actions:**
  - Sélectionne les frames aux indices multiples de X
  - Déclenche `FRAMELIST_PROP_UPDATED`
- **Usage:** Bouton "Sélectionner" avec intervalle

### Gestion des Offsets
#### `reset_offsets() -> None`
Réinitialise tous les offsets.
- **Actions:**
  - Réinitialise via `OffsetProcessor.reset()`
  - Met à zéro les offsets lignes/colonnes
- **Usage:** Bouton "Reset Offsets"

## Dépendances
- [FramelistManager](/docs/classes/core/framelist_manager.md) - Gestion des frames
- [OffsetProcessor](/docs/classes/core/offset_processor.md) - Gestion des offsets
- [States](/docs/classes/core/states.md) - Configuration globale

## Pipelines Associés
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames
- [Events Pipeline](/docs/pipelines/events.md) - Système d'événements

## Points d'Attention
1. **Performance**
   - Opérations en masse optimisées
   - Un seul événement par opération globale
   - Validation des entrées utilisateur

2. **Cohérence des Données**
   - Synchronisation avec `FramelistManager`
   - Validation de l'intervalle > 0
   - Protection contre les listes vides

3. **Interface Utilisateur**
   - Feedback visuel immédiat
   - Organisation logique des contrôles
   - Validation des entrées

## Code Source
- [frame_edit_selection_subpanel.py](/src/ui/panels/frame_edit_selection_subpanel.py)

## Tags
#class #ui #frame #selection #controller 