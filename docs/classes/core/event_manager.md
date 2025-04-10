# EventManager

#class #core #events

## Description
Gestionnaire d'événements de l'application. Implémente un système de publication/abonnement pour synchroniser les mises à jour UI et éviter la récursivité.

## Type
`STATIC`

## Variables
| Nom | Type | Description |
|-----|------|-------------|
| `_subscribers` | `Dict[str, Set[Callable]]` | Dictionnaire des callbacks par type d'événement |

## Constantes
| Nom | Type | Description |
|-----|------|-------------|
| `FRAMELIST_PROP_UPDATED` | `str` | Événement de modification de propriété sans changement du nombre d'images |
| `FRAMELIST_LIST_UPDATED` | `str` | Événement de modification des images ou de leur quantité |

## Méthodes

### `subscribe(event_type: str, callback: Callable) -> None`
Abonne une fonction à un type d'événement.
- **Args:**
  - `event_type`: Type d'événement à écouter
  - `callback`: Fonction à appeler lors de l'événement
- **Voir:** [Events Pipeline - Setup](/docs/pipelines/events.md#setup-des-events)

### `unsubscribe(event_type: str, callback: Callable) -> None`
Désabonne une fonction d'un type d'événement.
- **Args:**
  - `event_type`: Type d'événement
  - `callback`: Fonction à désabonner
- **Voir:** [Events Pipeline - Cleanup](/docs/pipelines/events.md#cleanup-des-events)

### `publish(event_type: str, *args, **kwargs) -> None`
Publie un événement à tous les abonnés.
- **Args:**
  - `event_type`: Type d'événement à publier
  - `*args, **kwargs`: Arguments passés aux callbacks
- **Voir:** [Events Pipeline - Publication](/docs/pipelines/events.md#publication-devents)

### `clear_all() -> None`
Supprime tous les abonnements.
- **Usage:** Nettoyage lors de la réinitialisation de l'application

## Dépendances
- [States](/docs/classes/core/states.md) - Pour le logging

## Pipelines Associés
- [Events Pipeline](/docs/pipelines/events.md) - Flux complet des événements

## Code Source
- [event_manager.py](/src/core/event_manager.py)

## Tags
#class #core #events #static 