---
comments: true
---
# **Request Body**

The request body is typically used for "create" and "update" operations (POST, PUT, PATCH).
For example, when using POST or PUT to create a resource, the request body usually contains the representation of the resource to be created.

To create a **request body**, you need to use the **Django Ninja `Schema`** or any Pydantic schema that suits your needs.

I recommend [Ninja-Schema](https://pypi.org/project/ninja-schema/)

## **Creating Your Data Model**

Then you declare your data model as a class that inherits from `Schema`.

Use standard Python types for all attributes:

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

Note: If you use **`None`** as the default value for an attribute, it becomes optional in the request body.
For example, the model above declares a similar JSON "`object`" (or Python `dict`):

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...because `description` is optional (default value is `None`), this JSON "`object`" will also be valid:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
