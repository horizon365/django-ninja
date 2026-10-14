---
comments: true
---
# **Tutorial / Referentie**

Deze tutorial laat zien hoe je **Django Ninja Extra** en de meeste functies ervan gebruikt.
In het bijzonder gaat ervan uit dat je weet hoe je **Django Ninja** gebruikt


!!! info
    Veel van de inhoud hier is afgeleid van Django-Ninja. Dus als je je eerst vertrouwd maakt met het Django-Ninja-framework, zal veel hiervan logisch zijn.

## **Installatie**

```
pip install django-ninja-extra
```

Na installatie voeg je `ninja_extra` toe aan `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Een Django-project Maken**

(Als je al een bestaand Django-project hebt, ga dan naar de volgende stap).

Start een nieuw Django-project (of gebruik een bestaand).

```
django-admin startproject myproject
```


## **Eerste Stap**

Laten we een module maken voor onze API. Maak een bestand **api.py** aan op dezelfde maplocatie als **urls.py**:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

Ga nu naar **urls.py** en voeg het volgende toe:


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **Operatiemethoden Definiëren**
Een "operatie" kan een van de HTTP-"methoden" zijn:

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... en meer.

Dit zijn de operaties die Django-Ninja definieert op de API of de Django-Ninja router.

Dezelfde operaties worden via de klasse `route` beschikbaar gesteld aan APIControllers.

De klasse `route` is een extra decorator die instantiemethoden van APIController omzet in routefuncties of endpoints.

Aan de andere kant is `route` hier een afkorting voor de klasse `ControllerRouter`, een adapterklasse die APIController eenvoudigweg adapteert aan de Django-Ninja router. Deze biedt ook globale controle over alle routes die in een willekeurige APIController-klasse zijn gedefinieerd.

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
Om de controllerconfiguratie te voltooien, moet je de APIController decoreren met `ControllerRouter` voordat je deze registreert.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
