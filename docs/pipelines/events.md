# Events Pipelines

#pipeline #events #synchronisation

**Classes impliquées :**
- [EventManager](/docs/classes/core/event_manager.md)
- [FramelistManager](/docs/classes/core/framelist_manager.md)
- [PlaybackPanel](/docs/classes/ui/playback_panel.md)
- [FrameEditPanel](/docs/classes/ui/frame_edit_panel.md)
- [Displayer](/docs/classes/ui/displayer.md)

## Types d'Événements

### FRAMELIST_PROP_UPDATED
**Déclencheur :** Modification d'une propriété sans changer le nombre d'images

```pipeline
FramelistManager.set_included/set_offset_frame/set_offset_row/set_offset_column
└─> EventManager.publish(FRAMELIST_PROP_UPDATED)
    ├─> PlaybackPanel.on_framelist_prop_updated()
    │   └─> _update_info_label()
    ├─> FrameEditPanel.on_framelist_prop_updated()
    │   └─> framelist_subpanel.update_values()
```

**Exemples de déclenchement :**
- Modification de l'inclusion d'une frame
- Changement d'offset d'une frame
- Changement d'offset ligne/colonne

### FRAMELIST_LIST_UPDATED
**Déclencheur :** Modification des images ou de leur quantité

```pipeline
FramelistManager.create_new_framelist/clear
└─> EventManager.publish(FRAMELIST_LIST_UPDATED)
    ├─> PlaybackPanel.on_framelist_list_updated()
    │   ├─> si States.show_included_only:
    │   │   └─> slider.configure(to=included_count - 1)
    │   ├─> sinon:
    │   │   └─> slider.configure(to=total_count - 1)
    │   ├─> frame_index = 0
    │   └─> display_frame(0)
    ├─> FrameEditPanel.on_framelist_list_updated()
    │   └─> framelist_subpanel.rebuild_list()
    └─> Displayer._on_framelist_updated()
        ├─> reset_zoom()
        ├─> show_frame(0)
        └─> center_image()
```

**Exemples de déclenchement :**
- Import d'une nouvelle image/vidéo
- Modification de la grille de découpage
- Nettoyage de la liste des frames

## Gestion des Abonnements

### Setup des Events
**Déclencheur :** Initialisation des panels

```pipeline
Panel.__init__()
└─> _setup_events()
    ├─> EventManager.subscribe(FRAMELIST_PROP_UPDATED, on_framelist_prop_updated)
    └─> EventManager.subscribe(FRAMELIST_LIST_UPDATED, on_framelist_list_updated)
```

### Cleanup des Events
**Déclencheur :** Destruction des panels

```pipeline
Panel.destroy()
├─> EventManager.unsubscribe(FRAMELIST_PROP_UPDATED, on_framelist_prop_updated)
└─> EventManager.unsubscribe(FRAMELIST_LIST_UPDATED, on_framelist_list_updated)
```

## Protection contre la Récursivité

### Publication d'Events
```pipeline
EventManager.publish(event_type)
├─> States.log(f"Publication de l'événement {event_type}")
├─> subscribers = _subscribers[event_type].copy()
└─> pour chaque callback dans subscribers:
    └─> try:
        └─> callback(*args, **kwargs)
```

**Remarques :**
- Les subscribers sont copiés avant itération pour éviter les problèmes de modification pendant l'itération
- Chaque callback est exécuté dans un try/except pour éviter la propagation d'erreurs
- Les événements sont utilisés uniquement pour éviter la récursivité dans les mises à jour UI
- Les modifications de données sont toujours faites via FramelistManager

**Voir aussi :**
- [Event Manager](/src/core/event_manager.py#L1-L46)
- [Event Setup](/src/ui/playback_panel.py#L69-L93)
- [Event Handling](/src/ui/panels/frame_edit_panel.py#L30-L50)

## Tags
#events #synchronisation #pipeline 