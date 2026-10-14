---
comments: true
---
# **Request Body**

Der Request Body wird typischerweise für "Create"- und "Update"-Operationen verwendet (POST, PUT, PATCH).
Wenn Sie beispielsweise mit POST oder PUT eine Ressource erstellen, enthält der Request Body normalerweise die Repräsentation der zu erstellenden Ressource.

Um einen **Request Body** zu erstellen, müssen Sie das **Django-Ninja-`Schema`** oder ein beliebiges Pydantic-Schema verwenden, das Ihren Anforderungen entspricht.

Ich empfehle [Ninja-Schema](https://pypi.org/project/ninja-schema/)

## **Ihr Datenmodell erstellen**

Dann deklarieren Sie Ihr Datenmodell als Klasse, die von `Schema` erbt.

Verwenden Sie für alle Attribute standardmäßige Python-Typen:

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

Hinweis: Wenn Sie **`None`** als Standardwert für ein Attribut verwenden, wird es im Request Body optional.
Das obige Modell deklariert beispielsweise ein ähnliches JSON-„`object`" (oder Python-`dict`):

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...da `description` optional ist (Standardwert ist `None`), ist auch dieses JSON-„`object`" gültig:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
