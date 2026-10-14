---
comments: true
---
# **Gestion des versions (Versioning)**

## **Différents numéros de version d'API**

Avec **Django Ninja Extra**, il est très facile de faire fonctionner plusieurs versions d'API à partir d'un même projet Django.

Tout ce que vous avez à faire est de créer deux instances NinjaAPI ou plus avec des paramètres `version` différents :


**`api_v1.py`** :

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


api_**v2**.py :
Vous pouvez réutiliser vos contrôleurs d'API et apporter des modifications à des routes spécifiques.

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


Puis dans **urls.py** :

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


Vous pouvez désormais accéder aux différentes pages de documentation OpenAPI pour chaque version :

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **Différentes logiques métier**

De la même manière, vous pouvez définir différentes API pour différents composants ou domaines :

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
    Si vous utilisez différentes instances **NinjaExtraAPI**, vous devez définir des `version`s différentes ou des `urls_namespace`s différents.
    Il en va de même pour les instances **NinjaAPI**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
