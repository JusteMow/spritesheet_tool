# Import/Export Pipelines

#pipeline #import #export

**Classes impliquées :**
- [ImportExportPanel](/docs/classes/ui/import_export_panel.md)
- [FramelistManager](/docs/classes/core/framelist_manager.md)
- [ImageProcessor](/docs/classes/core/image_processor.md)
- [States](/docs/classes/core/states.md)

## Import

### Import Spritesheet
**Déclencheur :** `ImportExportPanel > Bouton Import Spritesheet`

```pipeline
UI.import_spritesheet()
├─> file = filedialog.open()
├─> States.loaded_media = file
├─> ImageProcessor.split()
│   ├─> rows = States.import_rows_var
│   ├─> cols = States.import_columns_var
│   └─> return images[rows][cols]
└─> FramelistManager
    ├─> set_split_images(images)
    └─> create_new_framelist()
        └─> EventManager.FRAMELIST_LIST_UPDATED
```

**Voir aussi :**
- [Code source](/src/ui/panels/import_export_panel.py#L45-L60)
- [Création framelist](/src/core/framelist_manager.py#L120-L135)

### Import Folder
**Déclencheur :** `ImportExportPanel > Bouton Import Folder`

```pipeline
UI.import_folder()
├─> folder = filedialog.askdirectory()
├─> valid_frames = []
│   └─> pour chaque fichier:
│       ├─> si PNG/JPG et même taille
│       └─> valid_frames.append(image)
└─> FramelistManager
    ├─> set_split_images(valid_frames)
    └─> create_new_framelist()
```

**Voir aussi :**
- [Import Folder](/src/ui/panels/import_export_panel.py#L80-L100)
- [Validation](/src/core/framelist_manager.py#L150-L165)

## Export

### Export Spritesheet
**Déclencheur :** `ImportExportPanel > Bouton Export Spritesheet`

```pipeline
UI.export_spritesheet()
├─> frames = [f for f in FramelistManager._framelist if f.included]
├─> layouts = ImageProcessor.get_spritesheet_layouts(len(frames))
├─> layout = LayoutSuggestionDialog(layouts).show()
└─> si layout choisi:
    ├─> spritesheet = ImageProcessor.create_spritesheet(frames, *layout)
    └─> spritesheet.save(filedialog.asksaveasfile())
```

**Voir aussi :**
- [Export Spritesheet](/src/ui/panels/import_export_panel.py#L120-L140)
- [Layout Dialog](/src/ui/panels/layout_suggestion_dialog.py#L10-L50)

### Export GIF
**Déclencheur :** `ImportExportPanel > Bouton Export GIF`

```pipeline
UI.export_gif()
├─> frames = [f.get_processed_image() for f in FramelistManager._framelist if f.included]
├─> file = filedialog.asksaveasfile()
└─> save_gif(file, frames)
    ├─> duration = 1000/12  # 12 FPS
    ├─> disposal = 2        # Clear previous frame
    └─> transparency = 0    # Index transparent
```

**Voir aussi :**
- [Export GIF](/src/ui/panels/import_export_panel.py#L160-L180)

## Événements Communs

### Mise à jour Framelist
```pipeline
FramelistManager.create_new_framelist()
├─> _framelist.clear()
├─> pour chaque image dans _split_images:
│   └─> _framelist.append(new Frame(image))
└─> EventManager.FRAMELIST_LIST_UPDATED
    └─> UI.on_framelist_updated()
        ├─> PlaybackPanel.update()
        └─> FrameEditPanel.update()
```

**Voir aussi :**
- [Création Framelist](/src/core/framelist_manager.py#L200-L220)
- [Event Manager](/src/core/event_manager.py#L15-L30)

## Tags
#import #export #pipeline #framelist #gif #spritesheet 