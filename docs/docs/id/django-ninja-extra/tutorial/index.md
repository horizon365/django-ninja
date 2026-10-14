---
comments: true
---
# **Tutorial / Referensi**

Tutorial ini menunjukkan kepada Anda cara menggunakan **Django Ninja Extra** dan sebagian besar fiturnya.
Secara khusus, tutorial ini mengasumsikan Anda sudah tahu cara menggunakan **Django Ninja**


!!! info
    Sebagian besar konten di sini diambil dari Django-Ninja. Jadi jika Anda mempelajari framework Django-Ninja terlebih dahulu, sebagian besar materi ini akan lebih mudah dipahami.

## **Instalasi**

```
pip install django-ninja-extra
```

Setelah instalasi, tambahkan `ninja_extra` ke `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Membuat Proyek Django**

(Jika Anda sudah memiliki proyek Django yang ada, lanjutkan ke langkah berikutnya).

Mulai proyek Django baru (atau gunakan proyek yang sudah ada).

```
django-admin startproject myproject
```


## **Langkah Pertama**

Mari kita buat module untuk API kita. Buat file **api.py** di lokasi direktori yang sama dengan **urls.py**:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

Sekarang buka **urls.py** dan tambahkan kode berikut:


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **Mendefinisikan method operasi**
Sebuah "operasi" dapat berupa salah satu dari HTTP "methods":

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... dan lainnya.

Ini adalah operasi-operasi yang didefinisikan oleh Django-Ninja pada API atau router Django-Ninja.

Operasi yang sama diekspos ke APIController melalui kelas `route`.

Kelas `route` adalah dekorator tambahan yang mengubah method instance APIController menjadi fungsi route atau endpoint.

Di sisi lain, `route` di sini adalah singkatan dari kelas `ControllerRouter`, yaitu kelas adaptor yang mengadaptasikan APIController ke router Django-Ninja. Kelas ini juga menyediakan kontrol global atas semua route yang didefinisikan di kelas APIController mana pun.

```Python
from ninja_extra import (
    api_controller, 
    http_get, http_post, http_put, http_delete, http_patch, http_generic
)
from ninja.constants import NOT_SET

@api_controller('', tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyAPIController:
    @http_get("/path")
    def get_operation(self):
        ...
    
    @http_post("/path")
    def post_operation(self):
        ...
    
    @http_put("/path")
    def put_operation(self):
        ...
    
    @http_delete("/path")
    def delete_operation(self):
        ...
    
    @http_patch("/path")
    def patch_operation(self):
        ...
    
    # If you need to handle multiple methods with a single function, you can use the `generic` method as shown above
    @http_generic(["POST", "PATCH"]) 
    def mixed(request):
        ...

api.register_controllers(MyAPIController)
```
Untuk melengkapi setup controller, Anda harus mendekorasi APIController dengan `ControllerRouter` sebelum mendaftarkannya.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
