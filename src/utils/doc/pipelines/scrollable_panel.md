# Pipeline ScrollablePanel

## Objectif
Définir la structure et l'implémentation d'un panneau scrollable réutilisable dans l'application.

## Structure
```
utils/
  ├── ui/
  │   ├── scrollable_panel.py       # Classe de base ScrollablePanel
  │   └── scroll_manager.py         # Gestionnaire global du scroll
  └── doc/
      └── pipelines/
          └── scrollable_panel.mdc  # Ce document
```

## Implémentation d'un panneau scrollable

1. Hériter de ScrollablePanel :
```python
class MonPanel(ScrollablePanel):
    def __init__(self, parent):
        super().__init__(parent)
```

2. Ajouter le contenu dans self.scrollable_frame :
```python
# Correct
button = ttk.Button(self.scrollable_frame, text="Mon Bouton")
# Incorrect
button = ttk.Button(self, text="Mon Bouton")  # Ne pas utiliser self directement
```

3. Gérer la destruction proprement :
```python
def destroy(self):
    # Le ScrollablePanel gère automatiquement la désinscription du ScrollManager
    super().destroy()
```

## Règles à suivre

1. Tout panneau nécessitant du scroll DOIT hériter de ScrollablePanel
2. Le contenu scrollable DOIT être ajouté à self.scrollable_frame
3. Les dimensions du panneau DOIVENT être gérées via pack() ou les paramètres de ScrollablePanel
4. La destruction DOIT être gérée proprement pour éviter les fuites mémoire

## Exemple d'utilisation

```python
class ExamplePanel(ScrollablePanel):
    def __init__(self, parent):
        super().__init__(parent, height=400)
        
        # Ajouter du contenu
        for i in range(20):
            ttk.Label(self.scrollable_frame, text=f"Item {i}").pack(pady=5)
            
    def destroy(self):
        super().destroy()
```

## Notes importantes

- Le ScrollManager est un singleton géré automatiquement
- Les événements de scroll sont gérés globalement
- La priorité de scroll est donnée au panneau le plus proche sous la souris
- Le scroll n'est activé que si le contenu dépasse la taille visible 