# States

#class #core #config #logging

## Description
Conteneur statique des variables globales et système de logging centralisé. Point central de configuration et de traçabilité de l'application.

## Type
`STATIC`

## Variables

### Configuration Média
| Nom | Type | Description |
|-----|------|-------------|
| `loaded_media` | `Optional[Image.Image]` | Image source chargée (spritesheet) |
| `show_included_only` | `bool` | Filtre d'affichage des frames |

### Configuration Import
| Nom | Type | Description |
|-----|------|-------------|
| `import_rows_var` | `int` | Nombre de lignes pour le découpage |
| `import_columns_var` | `int` | Nombre de colonnes pour le découpage |

### Gestion des Offsets
| Nom | Type | Description |
|-----|------|-------------|
| `rows_offsets` | `List[int]` | Liste des offsets verticaux par ligne |
| `cols_offsets` | `List[int]` | Liste des offsets horizontaux par colonne |

### Debug
| Nom | Type | Description |
|-----|------|-------------|
| `debug_mode` | `bool` | Active/désactive le logging détaillé |

## Méthodes

### Logging
#### `log(message: str) -> None`
Affiche un message de log standard.
- **Args:**
  - `message`: Message à logger
- **Usage:** Logging général d'actions

#### `log_debug(message: str) -> None`
Affiche un message de debug si le mode debug est activé.
- **Args:**
  - `message`: Message de debug à logger
- **Usage:** Logging détaillé pour le développement

## Dépendances
- `PIL.Image` - Type pour l'image source

## Pipelines Associés
- [Import/Export Pipeline](/docs/pipelines/import_export.md) - Configuration du découpage
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Gestion des offsets
- [Events Pipeline](/docs/pipelines/events.md) - Logging des événements

## Points d'Attention
1. **Variables Globales**
   - Accessibles depuis toute l'application
   - Pas de protection contre les modifications
   - Responsabilité du code appelant

2. **Logging**
   - Centralisation des logs
   - Traçabilité des actions
   - Mode debug pour diagnostic

3. **Configuration**
   - Point unique de configuration
   - Impact sur toute l'application
   - Cohérence à maintenir

## Code Source
- [states.py](/src/core/states.py)

## Tags
#class #core #config #logging #static 