---
comments: true
---
# Versiebeheer

## Verschillende API versies

Met **Django Ninja** is het eenvoudig om meerdere API versies te draaien vanuit één Django project.
Het enige wat je hoeft te doen is twee of meer NinjaAPI instanties te maken met verschillende `version` argumenten:

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


Vervolgens in **urls.py**:

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


Nu kun je voor elke versie verschillende OpenAPI documentatiepagina's openen:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## Verschillende bedrijfslogica

Op dezelfde manier kun je verschillende API's definiëren voor verschillende componenten of domeinen:
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
    Als je verschillende **NinjaAPI** instanties gebruikt, moet je een andere `version` of een andere `urls_namespace` definiëren.

!!! success

    De How-to reeks is nu compleet!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
