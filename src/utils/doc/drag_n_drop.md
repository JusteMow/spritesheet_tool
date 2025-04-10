# Drag and Drop

## Principe d'implémentation

Le drag and drop est géré de manière centralisée par le `DragNDropManager`. Ce manager :
- Est initialisé au démarrage de l'application par la `MainWindow`
- Utilise la bibliothèque `tkinterdnd2` pour gérer les événements de drag and drop
- Redirige les fichiers déposés vers les fonctions d'import appropriées
- Ne contient pas de logique métier, uniquement du routage d'événements
- Fonctionne sur toute la surface de l'application

## Types de Fichiers Supportés

### Images
| Extension | Action | Description |
|-----------|--------|-------------|
| `.png` | `ImportExportPanel.import_spritesheet()` | Import comme spritesheet |
| `.jpg/.jpeg` | `ImportExportPanel.import_spritesheet()` | Import comme spritesheet |
| `.gif/.bmp` | `ImportExportPanel.import_spritesheet()` | Import comme spritesheet |

### Vidéos
| Extension | Action | Description |
|-----------|--------|-------------|
| `.mp4` | `ImportExportPanel.import_video()` | Import comme séquence de frames |
| `.mov` | `ImportExportPanel.import_video()` | Import comme séquence de frames |
| `.avi` | `ImportExportPanel.import_video()` | Import comme séquence de frames |

## Implémentation

```python
# Exemple de structure dans DragNDropManager
class DragNDropManager:
    def __init__(self, root: tkinterdnd2.TkinterDnD.Tk):
        self.root = root
        self._setup_drag_n_drop()
    
    def _setup_drag_n_drop(self):
        # Configure le drag and drop sur la fenêtre principale
        self.root.drop_target_register(tkinterdnd2.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self._on_drop)
    
    def _on_drop(self, event):
        # Récupère le chemin du fichier
        file_path = event.data
        
        # Vérifie l'extension
        _, ext = os.path.splitext(file_path.lower())
        
        # Redirige vers la fonction appropriée
        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            ImportExportPanel.get_instance().import_spritesheet(file_path)
        elif ext in ['.mp4', '.mov', '.avi']:
            ImportExportPanel.get_instance().import_video(file_path)
```

## Notes
- Le drag and drop est actif sur toute la surface de l'application
- Les fichiers non supportés sont ignorés avec un message de log
- Les fonctions d'import sont appelées via le singleton `ImportExportPanel`
- Les logs de debug tracent tous les événements de drag and drop
- L'import se fait avec les paramètres de grille actuels pour les spritesheets 