# MenuBar

#class #ui #menu #controller

## Description
Barre de menu horizontale qui fournit l'accès aux fonctionnalités principales. Gère :
- Menu File (Import/Export)
- Menu Edit (Frame Edit)
- Navigation entre les panels
- Actions globales de l'application

## Type
`SINGLETON` `CONTROLLER`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `menu_bar` | `tk.Menu` | Menu principal |
| `file_menu` | `tk.Menu` | Sous-menu File |
| `edit_menu` | `tk.Menu` | Sous-menu Edit |

## Méthodes

### Configuration
#### `_setup_menus() -> None`
Configure les menus et sous-menus.
- **Actions:**
  - Configure le menu File
  - Configure le menu Edit
  - Ajoute les commandes
- **Usage:** Initialisation

### Navigation
#### `on_click_import_export() -> None`
Charge le panel Import/Export.
- **Actions:**
  - Charge via `Inspector`
  - Log via `States`
- **Usage:** Menu File > Import/Export

#### `on_click_frame_edit() -> None`
Charge le panel Frame Edit.
- **Actions:**
  - Charge via `Inspector`
  - Log via `States`
- **Usage:** Menu Edit > Frame Edit

### Système
#### `_quit() -> None`
Quitte l'application.
- **Actions:**
  - Ferme proprement
- **Usage:** Menu File > Quit

## Dépendances
- [Inspector](/docs/classes/ui/inspector.md) - Chargement des panels
- [States](/docs/classes/core/states.md) - Logging

## Pipelines Associés
- [Import/Export Pipeline](/docs/pipelines/import_export.md) - Via menu File
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Via menu Edit

## Points d'Attention
1. **Navigation**
   - Transition fluide entre panels
   - État cohérent de l'interface
   - Feedback utilisateur

2. **Interface Utilisateur**
   - Menus organisés logiquement
   - Raccourcis clavier (à venir)
   - Cohérence visuelle

3. **Extensibilité**
   - Structure modulaire
   - Facilité d'ajout de menus
   - Gestion des commandes

## Code Source
- [menu_bar.py](/src/ui/menu_bar.py)

## Tags
#class #ui #menu #controller 