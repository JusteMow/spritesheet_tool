# Playback Pipelines

#pipeline #playback #display #animation

**Classes impliquées :**
- [PlaybackPanel](/docs/classes/ui/playback_panel.md)
- [Animator](/docs/classes/ui/animator.md)
- [Displayer](/docs/classes/ui/displayer.md)
- [FramelistManager](/docs/classes/core/framelist_manager.md)
- [States](/docs/classes/core/states.md)

## Navigation Manuelle

### Navigation Boutons
**Déclencheur :** `PlaybackPanel > Boutons < / >`

```pipeline
PlaybackPanel.previous_frame() / next_frame()
├─> new_index = _get_next_included_frame(frame_index, -1/+1)
└─> display_frame_manual(new_index)
    ├─> stop_animation()
    ├─> slider_update_auto(new_index)
    └─> display_frame(new_index)
        ├─> frame = FramelistManager.get_framelist()[new_index]
        ├─> Displayer.show_frame(new_index)
        ├─> included_var.set(frame.included)
        └─> _update_info_label()
```

### Navigation Slider
**Déclencheur :** `PlaybackPanel > Slider (user drag)`

```pipeline
PlaybackPanel.slider_update_by_user(value)
└─> display_frame(int(value))
    ├─> si States.show_included_only et non frame.included:
    │   └─> next_frame = _get_next_included_frame(frame, 1)
    ├─> frame = FramelistManager.get_framelist()[frame]
    ├─> Displayer.show_frame(frame)
    ├─> included_var.set(frame.included)
    └─> _update_info_label()
```

**Remarques :**
- La navigation manuelle arrête toujours l'animation en cours
- Le slider est mis à jour automatiquement pour refléter la frame actuelle
- En mode "Show Included Only", on saute automatiquement à la prochaine frame incluse

## Animation Automatique

### Démarrage Animation
**Déclencheur :** `PlaybackPanel > Bouton Play`

```pipeline
PlaybackPanel.play_animation()
└─> Animator.play()
    ├─> _is_playing = True
    ├─> _fps = PlaybackPanel.fps_var.get()
    └─> loop()
        ├─> next_frame = _get_next_included_frame(_current_frame, 1)
        ├─> PlaybackPanel.display_frame_animator(next_frame)
        │   ├─> slider_update_auto(next_frame)
        │   └─> display_frame(next_frame)
        └─> schedule next loop (1000/_fps ms)
```

### Arrêt Animation
**Déclencheur :** `PlaybackPanel > Bouton Stop`

```pipeline
PlaybackPanel.stop_animation()
└─> Animator.stop()
    ├─> _is_playing = False
    └─> cancel _animation_id
```

## Filtrage des Frames

### Toggle Show Included Only
**Déclencheur :** `PlaybackPanel > Checkbox Show Included Only`

```pipeline
PlaybackPanel._on_show_included_changed()
├─> States.show_included_only = show_included_var.get()
└─> on_framelist_list_updated()
    ├─> si States.show_included_only:
    │   └─> slider.configure(to=included_count - 1)
    ├─> sinon:
    │   └─> slider.configure(to=total_count - 1)
    ├─> frame_index = 0
    └─> display_frame(0)
```

### Toggle Frame Inclusion
**Déclencheur :** `PlaybackPanel > Checkbox Included`

```pipeline
PlaybackPanel.toggle_current_frame_included()
└─> FramelistManager.set_included(frame_index, included_var.get())
    ├─> frame.included = value
    └─> EventManager.FRAMELIST_PROP_UPDATED
        ├─> PlaybackPanel.on_framelist_prop_updated()
        │   └─> _update_info_label()
        └─> FrameEditPanel.on_framelist_prop_updated()
            └─> framelist_subpanel.update_values()
```

**Voir aussi :**
- [Playback Controls](/src/ui/playback_panel.py#L30-L50)
- [Animation Loop](/src/ui/animator.py#L30-L60)
- [Frame Display](/src/ui/displayer.py#L50-L70)

## Tags
#playback #animation #display #pipeline 