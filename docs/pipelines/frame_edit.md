# Frame Edit Pipelines

#pipeline #frame #offset #edit

**Classes impliquées :**
- [FrameEditPanel](/docs/classes/ui/frame_edit_panel.md) (host)
- [FrameEditFramelistSubpanel](/docs/classes/ui/frame_edit_framelist_subpanel.md)
- [FrameEditRowColsOffsetSubpanel](/docs/classes/ui/frame_edit_rowcols_offset_subpanel.md)
- [FrameEditSelectionSubpanel](/docs/classes/ui/frame_edit_selection_subpanel.md)
- [FramelistManager](/docs/classes/core/framelist_manager.md)
- [OffsetProcessor](/docs/classes/core/offset_processor.md)
- [States](/docs/classes/core/states.md)

## Gestion des Offsets

### Offset de Frame
**Déclencheur :** `FrameEditFramelistSubpanel > Entry Frame Offset (Return/FocusOut)`

```pipeline
FrameRow._on_offset_change()
├─> offset_x = int(offset_x_var.get())
├─> offset_y = int(offset_y_var.get())
└─> FramelistManager.set_offset_frame(frame_number, offset_x, offset_y)
    ├─> frame = _framelist[frame_number]
    ├─> frame.offset_x = offset_x
    ├─> frame.offset_y = offset_y
    ├─> processed_x, processed_y = OffsetProcessor.get_frame_offset(frame_id)
    ├─> processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
    ├─> set_frame_image(frame_index, processed_image)
    └─> EventManager.FRAMELIST_PROP_UPDATED
        ├─> PlaybackPanel.on_framelist_prop_updated()
        │   └─> _update_info_label()
        └─> FrameEditPanel.on_framelist_prop_updated()
            └─> framelist_subpanel.update_values()
```

- le rôle de l'offset processor est de calculer l'offset en fonction d'une image cumulant offset de frame et de rows/cols

**Voir aussi :**
- [Code source](/src/ui/panels/frame_edit_framelist_subpanel.py#L150-L170)
- [Frame Offset](/src/core/frame.py#L50-L65)

### Offset de Ligne/Colonne
**Déclencheur :** `FrameEditRowColsOffsetSubpanel > Entry Row/Col Offset (Return/FocusOut)`

```pipeline
FrameEditRowColsOffsetSubpanel._on_row_offset_change(row, var)
└─> FramelistManager.set_offset_row(row, offset)
    ├─> States.rows_offsets[row] = offset
    ├─> frames = OffsetProcessor.get_pictures_on_row(row)
    └─> pour chaque frame_index dans frames:
        ├─> processed_x, processed_y = OffsetProcessor.get_frame_offset(frame_index)
        ├─> processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
        └─> set_frame_image(frame_index, processed_image)
        └─> EventManager.FRAMELIST_PROP_UPDATED
        ...
        

FrameEditRowColsOffsetSubpanel._on_col_offset_change(col, var)
└─> FramelistManager.set_offset_column(col, offset)
    ├─> States.cols_offsets[col] = offset
    ├─> frames = OffsetProcessor.get_pictures_on_column(col)
    └─> pour chaque frame_index dans frames:
        ├─> processed_x, processed_y = OffsetProcessor.get_frame_offset(frame_index)
        ├─> processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
        └─> set_frame_image(frame_index, processed_image)
        └─> EventManager.FRAMELIST_PROP_UPDATED
        ...
```

**Voir aussi :**
- [Row/Col Offset](/src/ui/panels/frame_edit_rowcols_offset_subpanel.py#L90-L110)
- [Offset Manager](/src/core/offset_manager.py#L30-L45)

### Reset des Offsets
**Déclencheur :** `FrameEditSelectionSubpanel > Bouton Reset Offsets`

```pipeline
FrameEditSelectionSubpanel.reset_offsets()
└─> OffsetProcessor.reset()
    ├─> States.rows_offsets = [0] * States.import_rows_var
    └─> States.cols_offsets = [0] * States.import_columns_var
```

## Sélection Multiple

### Sélection Globale
**Déclencheur :** `FrameEditSelectionSubpanel > Boutons Tout/Rien/Inverser`

```pipeline
FrameEditSelectionSubpanel.select_all()
└─> pour chaque frame dans FramelistManager.get_framelist():
    └─> FramelistManager.set_included(i, True)
        ├─> _framelist[i].included = True
        └─> EventManager.FRAMELIST_PROP_UPDATED
            ├─> PlaybackPanel.on_framelist_prop_updated()
            │   └─> _update_info_label()
            └─> FrameEditPanel.on_framelist_prop_updated()
                └─> framelist_subpanel.update_values()

FrameEditSelectionSubpanel.select_none()
└─> pour chaque frame dans FramelistManager.get_framelist():
    └─> FramelistManager.set_included(i, False)

FrameEditSelectionSubpanel.select_invert()
└─> pour chaque frame dans FramelistManager.get_framelist():
    └─> FramelistManager.set_included(i, not frame.included)
```

### Sélection 1 sur X
**Déclencheur :** `FrameEditSelectionSubpanel > Bouton Sélectionner 1/X`

```pipeline
FrameEditSelectionSubpanel._select_every_x()
├─> x = max(1, skip_var.get())
└─> pour chaque frame dans FramelistManager.get_framelist():
    └─> FramelistManager.set_included(i, i % x == 0)
```

## Gestion des Frames

### Toggle Frame Inclusion
**Déclencheur :** `FrameEditFramelistSubpanel > Checkbox Frame Included`

```pipeline
FrameRow._on_included_change()
└─> FramelistManager.set_included(frame_number, included_var.get())
    ├─> _framelist[frame_number].included = value
    └─> EventManager.FRAMELIST_PROP_UPDATED
        ├─> PlaybackPanel.on_framelist_prop_updated()
        │   └─> _update_info_label()
        └─> FrameEditPanel.on_framelist_prop_updated()
            └─> framelist_subpanel.update_values()
```

### Navigation vers Frame
**Déclencheur :** `FrameEditFramelistSubpanel > Bouton Frame`

```pipeline
FrameRow._on_frame_click()
└─> PlaybackPanel.display_frame_manual(frame_number)
    ├─> stop_animation()
    ├─> slider_update_auto(frame_number)
    └─> display_frame(frame_number)
```

**Remarques :**
- Les offsets sont cumulatifs : offset de frame + offset de ligne/colonne
- Le reset des offsets ne retraite pas automatiquement les images
- La sélection multiple déclenche un événement par frame modifiée
- Les changements d'offsets déclenchent un retraitement immédiat des images

**Voir aussi :**
- [Frame Offsets](/src/core/frame.py#L50-L65)
- [Offset Processing](/src/core/offset_processor.py#L30-L45)
- [Frame Selection](/src/ui/panels/frame_edit_selection_subpanel.py#L50-L70)

## Tags
#frame #offset #edit #selection #pipeline 