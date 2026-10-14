---
comments: true
---
# Versionierung

## Unterschiedliche API-Versionen

Mit **Django Ninja** ist es einfach, mehrere API-Versionen aus einem einzigen Django-Projekt zu betreiben.
Alles, was Sie tun müssen, ist zwei oder mehr NinjaAPI-Instanzen mit unterschiedlichen `version`-Argumenten zu erstellen:

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


Dann in **urls.py**:

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


Nun können Sie für jede Version unterschiedliche OpenAPI-Dokumentationsseiten aufrufen:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## Unterschiedliche Geschäftslogik

Auf dieselbe Weise können Sie unterschiedliche APIs für verschiedene Komponenten oder Domänen definieren:
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
    Wenn Sie verschiedene **NinjaAPI**-Instanzen verwenden, müssen Sie eine unterschiedliche `version` oder einen unterschiedlichen `urls_namespace` definieren.

!!! success

    Die How-to-Reihe ist damit abgeschlossen!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
