---
comments: true
---
# **Versionierung**

## **Unterschiedliche API-Versionsnummern**

Mit **Django Ninja Extra** ist es sehr einfach, mehrere API-Versionen aus einem einzigen Django-Projekt zu betreiben.

Alles, was Sie tun müssen, ist zwei oder mehr NinjaAPI-Instanzen mit unterschiedlichen `version`-Parametern zu erstellen:


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
Sie können Ihre API-Controller wiederverwenden und Änderungen an bestimmten Routen vornehmen.

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


Dann in **urls.py**:

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


Jetzt können Sie für jede Version unterschiedliche OpenAPI-Dokumentationsseiten aufrufen:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **Unterschiedliche Geschäftslogik**

Auf dieselbe Weise können Sie unterschiedliche APIs für verschiedene Komponenten oder Domänen definieren:

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
    Wenn Sie verschiedene **NinjaExtraAPI**-Instanzen verwenden, müssen Sie unterschiedliche `version`s oder unterschiedliche `urls_namespace`s definieren.
    Dies gilt gleichermaßen für **NinjaAPI**-Instanzen.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
