---
comments: true
---
# **请求体**

请求体通常用于 “创建” 和 “更新” 操作（POST、PUT、PATCH）。
例如，当使用 POST 或 PUT 创建资源时，请求主体通常包含要创建的资源的表示。

要创建一个 **request body**, 你需要使用 **Django Ninja `Schema`** 或任何适合你需求的 Pydantic 模式。

我推荐 [Ninja-Schema](https://pypi.org/project/ninja-schema/)

## **创建你的数据模型**

然后你将你的数据模型声明为一个继承自 `Schema` 的类。

对所有属性使用标准的 Python 类型：

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

注意: 如果你使用 **`None`** 作为一个属性的默认值，它在请求主体中将变为可选的。
例如，上面的这个模型声明了一个类似的 JSON "`对象`" (或 Python `字典`):

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...因为 `description` 是可选的 (默认值为 `None`), 所以这个 JSON "`对象`" 也将是有效的：

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```