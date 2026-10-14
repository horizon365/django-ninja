---
comments: true
---
# **Tutorial / Referenz**

Dieses Tutorial zeigt Ihnen, wie Sie **Django Ninja Extra** und die meisten seiner Funktionen verwenden.
Insbesondere setzt es voraus, dass Sie wissen, wie man **Django Ninja** verwendet


!!! info
    Ein großer Teil des Inhalts hier stammt aus Django-Ninja. Wenn Sie sich also zuerst mit dem Django-Ninja-Framework vertraut machen, wird vieles davon leicht verständlich sein.

## **Installation**

```
pip install django-ninja-extra
```

Nach der Installation fügen Sie `ninja_extra` zu `INSTALLED_APPS` hinzu

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Ein Django-Projekt erstellen**

(Wenn Sie bereits ein bestehendes Django-Projekt haben, springen Sie zum nächsten Schritt).

Starten Sie ein neues Django-Projekt (oder verwenden Sie ein bestehendes).

```
django-admin startproject myproject
```


## **Erster Schritt**

Erstellen wir ein Modul für unsere API. Erstellen Sie eine Datei **api.py** im selben Verzeichnis wie **urls.py**:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

Gehen Sie nun zu **urls.py** und fügen Sie Folgendes hinzu:


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **Operationsmethoden definieren**
Eine „Operation" kann eine der HTTP-„Methoden" sein:

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... und mehr.

Dies sind die Operationen, die Django-Ninja auf der API oder dem Django-Ninja-Router definiert.

Dieselben Operationen werden APIControllers über die Klasse `route` zur Verfügung gestellt.

Die Klasse `route` ist ein zusätzlicher Decorator, der Instanzmethoden eines APIController in Routenfunktionen oder Endpunkte umwandelt.

Andererseits ist `route` hier eine Kurzform der Klasse `ControllerRouter`, einer Adapterklasse, die einen APIController einfach an den Django-Ninja-Router anpasst. Sie bietet außerdem eine globale Steuerung über alle Routen, die in einer beliebigen APIController-Klasse definiert sind.

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
Um die Controller-Einrichtung abzuschließen, müssen Sie den APIController mit `ControllerRouter` dekorieren, bevor Sie ihn registrieren.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
