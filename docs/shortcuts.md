# Raccourcis Clavier

## Principe d'implémentation

Les raccourcis clavier sont gérés de manière centralisée par le `KeybindingManager`. Ce manager :
- Écoute les événements clavier au niveau de l'application
- Associe directement les touches à des fonctions spécifiques des panels
- Ne contient pas de logique métier, uniquement du routage d'événements
- Est initialisé au démarrage de l'application

## Liste des Raccourcis

### Navigation
| Touche | Fonction | Description |
|--------|----------|-------------|
| `←` | `PlaybackPanel.previous_frame()` | Frame précédente |
| `→` | `PlaybackPanel.next_frame()` | Frame suivante |

### Contrôles de lecture
| Touche | Fonction | Description |
|--------|----------|-------------|
| `P` | `PlaybackPanel.toggle_play_stop()` | Démarre/Arrête la lecture |
| `I` | `PlaybackPanel.toggle_current_frame_included()` | Inclut/Exclut la frame courante |

### Application
| Touche | Fonction | Description |
|--------|----------|-------------|
| `R` | `States.restart_app()` | Recharge l'application |

## Implémentation

```python
# Exemple de structure dans KeybindingManager
class KeybindingManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_bindings()
    
    def _setup_bindings(self):
        # Navigation
        self.root.bind('<Left>', lambda e: PlaybackPanel.get_instance().previous_frame())
        self.root.bind('<Right>', lambda e: PlaybackPanel.get_instance().next_frame())
        
        # Contrôles
        self.root.bind('p', lambda e: PlaybackPanel.get_instance().toggle_play_stop())
        self.root.bind('i', lambda e: PlaybackPanel.get_instance().toggle_current_frame_included())
        
        # Application
        self.root.bind('r', lambda e: States.restart_app())
```

## Notes
- Les raccourcis sont actifs globalement dans l'application
- Les fonctions appelées doivent être accessibles via des singletons
- Les raccourcis ne doivent pas interférer avec les champs de saisie
- Les logs de debug doivent tracer l'utilisation des raccourcis 