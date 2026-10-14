---
comments: true
---
# **Request Body**

Request body का उपयोग आमतौर पर "create" और "update" operations (POST, PUT, PATCH) के लिए किया जाता है।
उदाहरण के लिए, POST या PUT का उपयोग करके resource बनाते समय, request body में आमतौर पर बनाए जाने वाले resource का प्रतिनिधित्व होता है।

एक **request body** बनाने के लिए, आपको **Django Ninja `Schema`** या किसी भी Pydantic schema का उपयोग करने की आवश्यकता है जो आपकी आवश्यकताओं के अनुरूप हो।

मैं [Ninja-Schema](https://pypi.org/project/ninja-schema/) की अनुशंसा करता हूँ

## **अपना Data Model बनाना**

फिर आप अपने data model को एक class के रूप में घोषित करते हैं जो `Schema` से inherit करती है।

सभी attributes के लिए standard Python types का उपयोग करें:

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

ध्यान दें: यदि आप किसी attribute के डिफ़ॉल्ट मान के रूप में **`None`** का उपयोग करते हैं, तो वह request body में optional हो जाता है।
उदाहरण के लिए, ऊपर का model एक समान JSON "`object`" (या Python `dict`) घोषित करता है:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...क्योंकि `description` optional है (डिफ़ॉल्ट मान `None` है), यह JSON "`object`" भी valid होगा:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
