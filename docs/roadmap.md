🗺️ Feuille de Route SpriteTool

## Documentation (Prioritaire)

### Restructuration de la Documentation
- [x] Mise à jour de `architecture.md`
  - [x] Clarifier les règles fondamentales (Panels, States, Managers, Processors)
  - [x] Conserver uniquement le diagramme Mermaid des relations générales
  - [x] Ajouter des liens vers les pipelines et la documentation des classes

- [x] Création/Mise à jour des Pipelines
  - [x] `import_export.md` - Import/Export de médias
  - [x] `grid_import_settings.md` - Configuration de la grille d'import
  - [x] `frame_edit.md` - Gestion des offsets et édition des frames
  - [x] `playback.md` - Modes d'affichage et timing
  - [x] `events.md` - Flux des événements
  - [x] Ajouter des liens bidirectionnels entre pipelines et documentation des classes

- [x] Simplification de la Documentation des Classes
  - [x] Nettoyer les classes de leurs diagrammes
  - [x] Garder uniquement les descriptions techniques (variables, méthodes)
  - [x] Ajouter des liens vers les pipelines pertinents
  - [x] Standardiser le format de documentation des classes

### Validation
- [x] Vérifier que chaque pipeline est lié à sa documentation de classe
- [x] Tester tous les liens (code source et documentation)
- [x] Valider la cohérence avec les règles de `pipelines.mdc`
- [x] S'assurer que la documentation reflète l'état actuel du code

📋 Phase 1 : Fondations (MVP)


1.1 Structure de Base

- [x] Setup du projet Python
  [x] Configuration de l'environnement (requirements.txt)
  [x] Implémentation de States
  [x] Implémentation de EventManager (avec système pub/sub standard)
- [x] Classe Frame

1.2 Interface Minimale

- [x] MainWindow avec layout de base
  [x] MenuBar simple
  [x] Displayer basique (affichage uniquement)
  [x] Inspector (conteneur vide)
- [x] Thème de base (depuis themes.py)

1.3 Pipeline Import Simple

- [x] FramelistManager (structure de base)
  [x] ImageProcessor.split() basique
  [x] Import spritesheet simple
- [x] Test manuel du pipeline complet

📋 Phase 2 : Playback Core


2.1 Contrôles de Base

- [x] PlaybackPanel structure
  [x] Boutons previous/next
  [x] Slider basique
- [x] Checkbox "included"

2.2 Animation

- [x] Animator avec boucle simple
  [x] Play/Stop
  [x] Contrôle FPS
- [x] Gestion des événements pour éviter la récursivité

2.3 Intégration Events

- [x] Events FRAMELIST_PROP_UPDATED
  [x] Events FRAMELIST_LIST_UPDATED
- [x] Synchronisation UI/Data

📋 Phase 3 : Import/Export Complet


3.1 Import Avancé

- [x] Import dossier
  [x] Import vidéo (OpenCV)
  [x] Gestion des erreurs d'import
- [x] UI feedback

3.2 Export Base

- [x] Export spritesheet simple
  [x] Export frames individuelles
- [x] Export GIF basique

3.3 UI Import/Export

- [x] ImportExportPanel complet
  [x] Layout suggestions pour export
- [x] Prévisualisation export

📋 Phase 4 : Gestion des Frames

4.1 Frame Edit Base

- [x] FrameEditPanel structure
  [x] Liste des frames scrollable
  [x] Sélection multiple
- [x] Filtres (1 sur X, etc.)

4.2 Preview Controls

- [x] Mode "included only"
  [x] Navigation intelligente
- [x] Synchronisation slider/frames

4.3 Frame Management

- [x] Réorganisation frames
  [x] Suppression frames
- [x] Duplication frames

📋 Phase 5 : Système d'Offsets


5.1 Backend Offsets

- [x] OffsetManager complet
  [x] Calculs offsets (image/ligne/colonne)
- [x] Application des offsets sur images

5.2 UI Offsets

- [x] Interface d'édition des offsets
  [x] Prévisualisation en temps réel
- [x] Gestion des offsets groupés

5.3 Export avec Offsets

- [x] Export spritesheet avec offsets
  [x] Export GIF avec offsets
- [x] Export frames avec offsets

📋 Phase 6 : Polish et Optimisations

6.1 Performance

- [x] Optimisation mémoire images
  [x] Cache de prévisualisation

6.2 UX Improvements

- [x] Raccourcis clavier
  [ ] Drag & drop import
- [x] Améliorations UI critiques
  [x] Gestion des logs (debug/user)
  [x] Scrolling dans frame_edit_panel_row_cols_subpanel
  [ ] Correction des identifiants de Frame (démarrer à 1)
  [x] Centrage des images dans le displayer après split
  [x] Correction du zoom dans le displayer

6.3 Robustesse

- [x] Gestion des erreurs complète
- [x] Tests automatisés critiques

🎯 Points de Validation

- ✅ MVP : Import + Display + Playback simple
- ✅ Core : Tous imports/exports fonctionnels
- ✅ Features : Gestion frames complète
- ✅ Pro : Système d'offsets opérationnel
- [ ] Final : Application stable et optimisée

Cette feuille de route suit les pipelines définis tout en gardant une progression logique. Chaque phase construit sur la précédente et peut être testée indépendamment.
Voulez-vous que j'ajoute des détails sur certaines phases ou que je réorganise certaines priorités ? 