---
comments: true
---
# **Corps de la requête**

Le corps de la requête est généralement utilisé pour les opérations de « création » et de « mise à jour » (POST, PUT, PATCH).
Par exemple, lors de l'utilisation de POST ou PUT pour créer une ressource, le corps de la requête contient généralement la représentation de la ressource à créer.

Pour créer un **corps de requête**, vous devez utiliser le **`Schema` de Django Ninja** ou tout schéma Pydantic qui correspond à vos besoins.

Je recommande [Ninja-Schema](https://pypi.org/project/ninja-schema/)

## **Créer votre modèle de données**

Ensuite, vous déclarez votre modèle de données sous forme de classe qui hérite de `Schema`.

Utilisez les types Python standard pour tous les attributs :

```Python
from ninja import Schema, constants
from ninja_extra import api_controller, route


class Item(Schema):
    name: str
    description: str = None
    price: float
    quantity: int

    
@api_controller(tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.post("/items")
    def create(self, item: Item):
        return item

```

Remarque : si vous utilisez **`None`** comme valeur par défaut pour un attribut, celui-ci devient optionnel dans le corps de la requête.
Par exemple, le modèle ci-dessus déclare un « `object` » JSON similaire (ou un `dict` Python) :

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...parce que `description` est optionnel (la valeur par défaut est `None`), ce « `object` » JSON sera également valide :

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
