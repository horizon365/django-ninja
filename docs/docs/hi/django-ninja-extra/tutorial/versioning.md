---
comments: true
---
# **Versioning**

## **विभिन्न API Version Numbers**

**Django Ninja Extra** का उपयोग करके, एक single Django project से कई API versions चलाना बहुत आसान है।

आपको बस अलग-अलग `version` parameters के साथ दो या अधिक NinjaAPI instances बनाने हैं:


**`api_v1.py`**:

```Python
from ninja_extra import NinjaExtraAPI, route, api_controller

@api_controller
class MyV1Controller:
    @route.get('/hello')
    def hello(self):
        return {'message': 'Hello from V1'}
    
    @route.get('/example')
    def example(self):
        return {'message': 'Hello from V1 Example'}

    
api = NinjaExtraAPI(version='1.0.0')
api.register_controllers(MyV1Controller)
```


api_**v2**.py:
आप अपने API controllers का पुनः उपयोग कर सकते हैं और specific routes में बदलाव कर सकते हैं।

```Python
from ninja_extra import NinjaExtraAPI, route, api_controller
from .api_v1 import MyV1Controller

@api_controller
class MyV2Controller(MyV1Controller):
    @route.get('/example')
    def example(self):
        return {'message': 'Hello from V2 Example'}

    
api = NinjaExtraAPI(version='2.0.0')
api.register_controllers(MyV2Controller)
```


फिर **urls.py** में:

```Python hl_lines="8 9"
...
from api_v1 import api as api_v1
from api_v2 import api as api_v2


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
]

```


अब आप प्रत्येक version के लिए अलग-अलग OpenAPI documentation pages access कर सकते हैं:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **विभिन्न Business Logic**

उसी तरह, आप विभिन्न components या domains के लिए अलग-अलग APIs define कर सकते हैं:

```Python
...


api = NinjaExtraAPI(auth=token_auth, urls_namespace='public_api')
...

api_private = NinjaExtraAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/', api.urls),
    path('internal-api/', api_private.urls),
]

```
!!! note
    यदि आप अलग-अलग **NinjaExtraAPI** instances का उपयोग करते हैं, तो आपको अलग-अलग `version`s या अलग-अलग `urls_namespace`s define करने की आवश्यकता है।
    यह **NinjaAPI** instances के लिए भी वैसा ही है।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
