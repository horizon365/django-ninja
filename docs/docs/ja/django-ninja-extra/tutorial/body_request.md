---
comments: true
---
# **リクエストボディ**

リクエストボディは通常、「作成」や「更新」の操作（POST、PUT、PATCH）で使われます。
たとえば、POST や PUT でリソースを作成する場合、リクエストボディには通常、作成しようとしているリソースの表現が含まれます。

**リクエストボディ** を作成するには、**Django Ninja の `Schema`** か、ニーズに合った任意の Pydantic スキーマを使用する必要があります。

[Ninja-Schema](https://pypi.org/project/ninja-schema/) をおすすめします。

## **データモデルの作成**

次に、データモデルを `Schema` を継承したクラスとして宣言します。

すべての属性には標準的な Python の型を使用します：

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

注意： 属性のデフォルト値として **`None`** を使うと、リクエストボディにおいてその属性は任意（オプショナル）になります。
たとえば、上記のモデルは次のような JSON の "`object`"（Python では `dict`）を宣言していることに相当します：

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

`description` は任意（デフォルト値が `None`）なので、次のような JSON "`object`" も有効です：

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
