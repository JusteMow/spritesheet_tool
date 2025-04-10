from src.core.states import States
from typing import Callable, Dict, List, Set

class EventManager:
    """Gestionnaire d'événements de l'application."""
    
    # Types d'événements
    FRAMELIST_PROP_UPDATED = "FRAMELIST_PROP_UPDATED"  # Modification d'une propriété sans changer le nombre d'images
    FRAMELIST_LIST_UPDATED = "FRAMELIST_LIST_UPDATED"  # Modification des images ou de leur quantité
    
    # Dictionnaire des abonnements {event_type: set(callbacks)}
    _subscribers: Dict[str, Set[Callable]] = {}
    
    @classmethod
    def subscribe(cls, event_type: str, callback: Callable) -> None:
        """Abonne une fonction à un type d'événement."""
        States.log(f"Abonnement à l'événement {event_type}")
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = set()
        cls._subscribers[event_type].add(callback)
    
    @classmethod
    def unsubscribe(cls, event_type: str, callback: Callable) -> None:
        """Désabonne une fonction d'un type d'événement."""
        States.log(f"Désabonnement de l'événement {event_type}")
        if event_type in cls._subscribers and callback in cls._subscribers[event_type]:
            cls._subscribers[event_type].remove(callback)
    
    @classmethod
    def publish(cls, event_type: str, *args, **kwargs) -> None:
        """Publie un événement à tous les abonnés."""
        States.log(f"Publication de l'événement {event_type}")
        if event_type in cls._subscribers:
            # Copie du set pour éviter les problèmes si un callback modifie les abonnements
            subscribers = cls._subscribers[event_type].copy()
            for callback in subscribers:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    States.log(f"Erreur lors de l'exécution du callback {callback.__name__}: {str(e)}")
    
    @classmethod
    def clear_all(cls) -> None:
        """Supprime tous les abonnements."""
        States.log("Suppression de tous les abonnements")
        cls._subscribers.clear() 