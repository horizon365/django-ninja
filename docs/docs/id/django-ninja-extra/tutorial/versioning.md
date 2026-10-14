---
comments: true
---
# **Versioning**

## **Nomor Versi API yang Berbeda**

Dengan menggunakan **Django Ninja Extra**, menjalankan beberapa versi API dari satu proyek Django menjadi sangat mudah.

Yang perlu Anda lakukan hanyalah membuat dua atau lebih instance NinjaAPI dengan parameter `version` yang berbeda:


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
Anda dapat menggunakan kembali controller API Anda dan melakukan perubahan pada route tertentu.

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


Kemudian di **urls.py**:

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


Sekarang Anda dapat mengakses halaman dokumentasi OpenAPI yang berbeda untuk setiap versi:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **Logika Bisnis yang Berbeda**

Dengan cara yang sama, Anda dapat mendefinisikan API yang berbeda untuk komponen atau domain yang berbeda:

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
    Jika Anda menggunakan instance **NinjaExtraAPI** yang berbeda, Anda perlu mendefinisikan `version` yang berbeda atau `urls_namespace` yang berbeda.
    Hal yang sama berlaku untuk instance **NinjaAPI**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
