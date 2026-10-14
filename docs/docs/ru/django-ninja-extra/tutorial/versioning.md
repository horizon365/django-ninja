---
comments: true
---
# **Версионирование**

## **Разные номера версий API**

С использованием **Django Ninja Extra** очень легко запускать несколько версий API из одного Django-проекта.

Всё, что вам нужно сделать, — это создать два или более экземпляра NinjaAPI с разными параметрами `version`:


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
Вы можете повторно использовать свои контроллеры API и вносить изменения в конкретные маршруты.

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


Затем в **urls.py**:

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


Теперь вы можете обращаться к разным страницам документации OpenAPI для каждой версии:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **Разная бизнес-логика**

Аналогичным образом вы можете определить разные API для разных компонентов или доменов:

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
    Если вы используете разные экземпляры **NinjaExtraAPI**, вам нужно определить разные `version` или разные `urls_namespace`.
    То же самое справедливо для экземпляров **NinjaAPI**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
