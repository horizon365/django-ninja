---
comments: true
---
# Versioning

## अलग-अलग API versions

**Django Ninja** के साथ, एक single Django project से कई API versions चलाना आसान है।
आपको बस अलग-अलग `version` arguments के साथ दो या अधिक NinjaAPI instances बनाने हैं:

**api_v1.py**:

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='1.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V1'}

```


api_**v2**.py:

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='2.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V2'}
```


फिर **urls.py** में:

```python hl_lines="8 9"
...
from api_v1 import api as api_v1
from api_v2 import api as api_v2


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
]

```


अब आप प्रत्येक version के लिए अलग-अलग OpenAPI दस्तावेज़ीकरण pages तक पहुँच सकते हैं:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## अलग-अलग business logic

उसी तरह, आप अलग-अलग components या domains के लिए अलग-अलग APIs परिभाषित कर सकते हैं:
```python hl_lines="4 7"
...


api = NinjaAPI(auth=token_auth, urls_namespace='public_api')
...

api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/', api.urls),
    path('internal-api/', api_private.urls),
]

```
!!! note
    यदि आप अलग-अलग **NinjaAPI** instances का उपयोग करते हैं, तो आपको एक अलग `version` या एक अलग `urls_namespace` परिभाषित करने की आवश्यकता है।

!!! success

    How-to श्रृंखला अब पूरी हो गई है!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
