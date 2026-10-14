---
comments: true
---
# **Versionering**

## **Verschillende API-versienummers**

Met **Django Ninja Extra** is het heel eenvoudig om meerdere API-versies vanuit één Django-project te draaien.

Het enige wat je hoeft te doen is twee of meer NinjaAPI-instanties aan te maken met verschillende `version`-parameters:


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
Je kunt je API-controllers hergebruiken en wijzigingen aanbrengen in specifieke routes.

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


Vervolgens in **urls.py**:

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


Nu kun je voor elke versie verschillende OpenAPI-documentatiepagina's openen:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **Verschillende Bedrijfslogica**

Op dezelfde manier kun je verschillende API's definiëren voor verschillende componenten of domeinen:

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
    Als je verschillende **NinjaExtraAPI**-instanties gebruikt, moet je verschillende `version`s of verschillende `urls_namespace`s definiëren.
    Dit geldt ook voor **NinjaAPI**-instanties.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
