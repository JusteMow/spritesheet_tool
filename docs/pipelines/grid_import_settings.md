# Grid Import Settings Pipelines

#pipeline #import #grid #settings

**Classes impliquées :**
- [ImportExportPanel](/docs/classes/ui/import_export_panel.md)
- [ImageProcessor](/docs/classes/core/image_processor.md)
- [FramelistManager](/docs/classes/core/framelist_manager.md)
- [States](/docs/classes/core/states.md)

## Configuration de la Grille

### Modification Rows/Columns
**Déclencheur :** `ImportExportPanel > Entry Rows/Cols (write)`

```pipeline
ImportExportPanel._on_rows_cols_changed()
├─> rows = import_rows_var.get()
├─> cols = import_columns_var.get()
└─> si rows > 0 et cols > 0:
    ├─> States.import_rows_var = rows
    ├─> States.import_columns_var = cols
    └─> si States.loaded_media:
        ├─> split_images = ImageProcessor.split()
        ├─> FramelistManager.set_split_images(split_images)
        └─> FramelistManager.create_new_framelist()
            ├─> _framelist.clear()
            ├─> _framelist = [Frame(img.copy(), i) for i, img in enumerate(_split_images)]
            ├─> States.rows_offsets = [0] * States.import_rows_var
            ├─> States.cols_offsets = [0] * States.import_columns_var
            ├─> pour chaque frame:
            │   ├─> processed_x, processed_y = OffsetProcessor.get_frame_offset(i)
            │   ├─> processed_image = ImageProcessor.process_offset(image_clone, processed_x, processed_y)
            │   └─> set_frame_image(i, processed_image)
            └─> EventManager.FRAMELIST_LIST_UPDATED
                ├─> PlaybackPanel.on_framelist_list_updated()
                │   ├─> configure slider
                │   └─> display_frame(0)
                └─> FrameEditPanel.on_framelist_list_updated()
                    └─> framelist_subpanel.rebuild_list()
```

**Remarques :**
- La modification de la grille déclenche un retraitement complet des images
- Les offsets sont réinitialisés à chaque changement de grille
- Le changement est ignoré si les valeurs ne sont pas valides (conversion, champs vides)

**Voir aussi :**
- [Grid Change](/src/ui/panels/import_export_panel.py#L310-L340)
- [Framelist Creation](/src/core/framelist_manager.py#L50-L90)

## Impact sur les Offsets

### Réinitialisation des Offsets
**Déclencheur :** `FramelistManager.create_new_framelist()`

```pipeline
FramelistManager.create_new_framelist()
├─> States.rows_offsets = [0] * States.import_rows_var
└─> States.cols_offsets = [0] * States.import_columns_var
```

**Voir aussi :**
- [Offset Reset](/src/core/offset_processor.py#L80-L95)

## Tags
#grid #import #settings #offset #pipeline 