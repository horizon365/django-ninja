---
comments: true
---
# **요청 본문**

요청 본문은 일반적으로 "생성" 및 "업데이트" 작업(POST, PUT, PATCH)에 사용됩니다.
예를 들어, POST나 PUT을 사용하여 리소스를 생성할 때 요청 본문에는 생성할 리소스의 표현(representation)이 담기게 됩니다.

**요청 본문**을 만들려면 **Django Ninja `Schema`** 또는 필요에 맞는 아무 Pydantic 스키마를 사용해야 합니다.

저는 [Ninja-Schema](https://pypi.org/project/ninja-schema/)를 추천합니다

## **데이터 모델 만들기**

그런 다음 `Schema`를 상속하는 클래스로 데이터 모델을 선언합니다.

모든 속성에는 표준 Python 타입을 사용합니다:

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

참고: 속성의 기본값으로 **`None`**을 사용하면 요청 본문에서 해당 속성은 선택 사항(optional)이 됩니다.
예를 들어, 위 모델은 다음과 같은 JSON "`object`"(또는 Python `dict`)를 선언합니다:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...`description`은 선택 사항(기본값이 `None`)이므로, 다음 JSON "`object`"도 유효합니다:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
