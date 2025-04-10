# OffsetProcessor

## Description
Processeur pur pour le calcul des offsets combinés. Fournit :
- Calcul des offsets finaux (frame + ligne + colonne)
- Identification des frames par position (ligne/colonne)
- Réinitialisation des offsets

## Type
`STATIC` `PROCESSOR`

## Méthodes

### Calcul d'Offsets
#### `get_frame_offset(frame_id: int) -> Tuple[int, int]`
Calcule l'offset final d'une frame.
- **Args:**
  - `frame_id`: Index de la frame
- **Returns:**
  - `(x, y)`: Offset combiné (frame + ligne + colonne)
- **Pure:** Utilise uniquement les données de States

#### `get_pictures_on_row(row: int) -> List[int]`
Identifie les frames sur une ligne.
- **Args:**
  - `row`: Index de la ligne
- **Returns:**
  - Liste des indices des frames sur cette ligne
- **Pure:** Calcul basé sur `import_columns_var`

#### `get_pictures_on_column(col: int) -> List[int]`
Identifie les frames sur une colonne.
- **Args:**
  - `col`: Index de la colonne
- **Returns:**
  - Liste des indices des frames sur cette colonne
- **Pure:** Calcul basé sur `import_rows_var`

### Gestion des Offsets
#### `reset() -> None`
Réinitialise tous les offsets.
- **Actions:**
  - Met à zéro les offsets lignes/colonnes dans States
- **Pure:** Modifie uniquement States

## Dépendances
- [States](/docs/classes/core/states.md) - Accès aux offsets et configuration

## Pipelines Associés
- [Frame Edit Pipeline](/docs/pipelines/frame_edit.md) - Édition des frames

## Points d'Attention

### 1. Pureté des Fonctions
- Pas de stockage interne
- Pas d'appels externes
- Uniquement des calculs purs

### 2. Performance
- Calculs optimisés
- Pas de recalculs inutiles
- Résultats immédiats

### 3. Précision
- Validation des indices
- Protection contre les débordements
- Cohérence des calculs

## Code Source
- [offset_processor.py](/src/core/offset_processor.py)

## Tags
#class #core #processor #offset #pure 