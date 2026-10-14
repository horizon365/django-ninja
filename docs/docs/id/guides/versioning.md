---
comments: true
---
# Versioning

## Berbagai versi API

Dengan **Django Ninja**, Anda dapat dengan mudah menjalankan beberapa versi API dari satu proyek Django.
Yang perlu Anda lakukan hanyalah membuat dua atau lebih instance NinjaAPI dengan argumen `version` yang berbeda:

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


Kemudian di **urls.py**:

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


Sekarang Anda dapat mengakses halaman dokumentasi OpenAPI yang berbeda untuk setiap versi:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## Logika bisnis yang berbeda

Dengan cara yang sama, Anda dapat mendefinisikan API yang berbeda untuk komponen atau domain yang berbeda:
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
    Jika Anda menggunakan beberapa instance **NinjaAPI** yang berbeda, Anda perlu mendefinisikan `version` yang berbeda atau `urls_namespace` yang berbeda.

!!! success

    Seri How-to telah selesai!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
