# Index des Pipelines

Ce document sert de sommaire pour tous les pipelines du projet. Chaque pipeline est décrit brièvement pour permettre à l'agent de comprendre rapidement sa pertinence dans le contexte d'une modification ou d'une implémentation.

## Pipelines Disponibles

### 1. Frame Edit (@docs/pipelines/frame_edit.md)
Pipeline concernant l'édition des frames individuelles ou groupées dans l'outil. Pertinent pour :
- Modifications sur une frame spécifique
- Gestion des outils d'édition
- Manipulation des calques
- Opérations de dessin et de modification

### 2. Events (@docs/pipelines/events.md)
Pipeline de gestion des événements dans l'application. À consulter pour :
- Gestion des inputs utilisateur
- Système de callbacks
- Propagation des événements
- Interactions UI

### 3. Playback (@docs/pipelines/playback.md)
Pipeline pour la lecture et prévisualisation des animations. Important pour :
- Contrôles de lecture
- Gestion de la timeline
- Preview des animations
- Contrôle de la vitesse de lecture

### 4. Grid Import Settings (@docs/pipelines/grid_import_settings.md)
Pipeline pour la configuration et l'import de grilles. Utile pour :
- Paramètres d'import de sprites
- Configuration de la grille
- Découpage automatique
- Préférences d'import

### 5. Import/Export (@docs/pipelines/import_export.md)
Pipeline général pour l'import et l'export de fichiers. Concerne :
- Import de sprites et d'images
- Export des animations
- Gestion des formats
- Sauvegarde et chargement des projets

## Utilisation
Chaque pipeline est référencé avec @ pour permettre à l'agent d'y accéder directement. Avant toute modification ou implémentation, consultez le pipeline approprié pour assurer la cohérence avec l'architecture existante. 