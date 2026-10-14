---
comments: true
---
# **Request Body**

De request body wordt doorgaans gebruikt voor "create"- en "update"-operaties (POST, PUT, PATCH).
Bijvoorbeeld: wanneer je POST of PUT gebruikt om een resource aan te maken, bevat de request body meestal de representatie van de aan te maken resource.

Om een **request body** te maken, moet je de **Django Ninja `Schema`** gebruiken of een Pydantic-schema dat aan je behoeften voldoet.

Ik raad [Ninja-Schema](https://pypi.org/project/ninja-schema/) aan

## **Je Datamodel Maken**

Vervolgens declareer je je datamodel als een klasse die overerft van `Schema`.

Gebruik standaard Python-types voor alle attributen:

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

Let op: als je **`None`** gebruikt als standaardwaarde voor een attribuut, wordt het optioneel in de request body.
Het model hierboven declareert bijvoorbeeld een vergelijkbaar JSON "`object`" (of Python `dict`):

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...omdat `description` optioneel is (standaardwaarde is `None`), is dit JSON "`object`" ook geldig:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
