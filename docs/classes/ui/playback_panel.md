# PlaybackPanel

#class #ui #playback #controller

## Description
Interface de navigation et de contrôle de lecture des frames. Composant central qui gère :
- Navigation manuelle (boutons précédent/suivant)
- Lecture automatique via `Animator`
- Contrôle du FPS
- Gestion de l'inclusion des frames
- Filtrage des frames (show included only)
- Affichage des informations de frame

## Type
`SINGLETON`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `frame_index` | `int` | Index de la frame actuelle |
| `fps_var` | `tk.IntVar` | Vitesse de lecture en FPS |
| `included_var` | `tk.BooleanVar` | État d'inclusion de la frame courante |
| `show_included_var` | `tk.BooleanVar` | Filtre d'affichage des frames incluses |

## Méthodes

### Navigation
#### `display_frame_manual(frame: int) -> None`
Navigation manuelle (boutons).
- **Args:**
  - `frame`: Index de la frame à afficher
- **Actions:**
  - Arrête l'animation en cours
  - Met à jour le slider
  - Affiche la frame
- **Usage:** Navigation utilisateur

#### `previous_frame() / next_frame() -> None`
Navigation séquentielle.
- **Actions:**
  - Calcule la frame suivante/précédente
  - Gère le mode "included only"
  - Appelle `display_frame_manual`
- **Usage:** Boutons de navigation

### Animation
#### `play_animation() -> None`
Lance la lecture automatique.
- **Actions:**
  - Démarre l'`Animator`
  - Utilise le FPS configuré
- **Usage:** Bouton Play

#### `stop_animation() -> None`
Arrête la lecture automatique.
- **Actions:**
  - Arrête l'`Animator`
- **Usage:** Bouton Stop

### Gestion des Frames
#### `toggle_current_frame_included() -> None`
Change l'inclusion de la frame courante.
- **Actions:**
  - Met à jour via `FramelistManager`
  - Déclenche `FRAMELIST_PROP_UPDATED`
- **Usage:** Checkbox Included

#### `_on_show_included_changed() -> None`
Change le mode de filtrage.
- **Actions:**
  - Met à jour `States.show_included_only`
  - Recharge la liste des frames
- **Usage:** Checkbox Show Included Only

### Événements
#### `on_framelist_prop_updated() -> None`
Réagit aux changements de propriétés.
- **Actions:**
  - Met à jour les informations affichées
- **Usage:** Event system

#### `on_framelist_list_updated() -> None`
Réagit aux changements de liste.
- **Actions:**
  - Reconfigure le slider
  - Réinitialise l'affichage
- **Usage:** Event system

## Dépendances
- [Animator](/docs/classes/ui/animator.md) - Gestion de l'animation
- [Displayer](/docs/classes/ui/displayer.md) - Affichage des frames
- [FramelistManager](/docs/classes/core/framelist_manager.md) - Accès aux frames
- [EventManager](/docs/classes/core/event_manager.md) - Système d'événements
- [States](/docs/classes/core/states.md) - Configuration globale

## Pipelines Associés
- [Playback Pipeline](/docs/pipelines/playback.md) - Navigation et animation
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Gestion des frames

## Points d'Attention
1. **Navigation Intelligente**
   - Gestion du mode "included only"
   - Calcul de la prochaine frame valide
   - Protection contre les listes vides

2. **Synchronisation UI**
   - Mise à jour du slider sans récursion
   - Affichage cohérent des informations
   - Gestion des événements

3. **Animation**
   - Séparation des modes manuel/automatique
   - Respect du FPS configuré
   - Arrêt propre de l'animation

## Code Source
- [playback_panel.py](/src/ui/playback_panel.py)

## Tags
#class #ui #playback #controller 