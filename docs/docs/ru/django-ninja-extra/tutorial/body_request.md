---
comments: true
---
# **Тело запроса**

Тело запроса обычно используется для операций «создание» и «обновление» (POST, PUT, PATCH).
Например, при использовании POST или PUT для создания ресурса тело запроса обычно содержит представление создаваемого ресурса.

Чтобы создать **тело запроса**, вам нужно использовать **`Schema` из Django Ninja** или любую Pydantic-схему, соответствующую вашим потребностям.

Я рекомендую [Ninja-Schema](https://pypi.org/project/ninja-schema/)

## **Создание вашей модели данных**

Затем вы объявляете свою модель данных в виде класса, наследующегося от `Schema`.

Используйте стандартные типы Python для всех атрибутов:

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

Примечание: если вы используете **`None`** в качестве значения по умолчанию для атрибута, он становится необязательным в теле запроса.
Например, модель выше описывает похожий JSON-«`object`» (или Python `dict`):

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...поскольку `description` является необязательным (значение по умолчанию — `None`), этот JSON-«`object`» также будет валидным:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
