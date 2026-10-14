---
comments: true
---
# Versionnage

## Différentes versions d'API

Avec **Django Ninja**, il est facile de faire tourner plusieurs versions d'API à partir d'un seul projet Django.
Tout ce que vous avez à faire est de créer deux instances NinjaAPI ou plus avec des arguments `version` différents :

**api_v1.py** :

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='1.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V1'}

```


api_**v2**.py :

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='2.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V2'}
```


Puis dans **urls.py** :

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


Vous pouvez maintenant accéder à différentes pages de documentation OpenAPI pour chaque version :

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## Différentes logiques métier

De la même manière, vous pouvez définir différentes API pour différents composants ou domaines :
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
    Si vous utilisez différentes instances **NinjaAPI**, vous devez définir une `version` différente ou un `urls_namespace` différent.

!!! success

    La série How-to est désormais terminée !

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
