---
comments: true
---
# **Tutoriel / Référence**

Ce tutoriel vous montre comment utiliser **Django Ninja Extra** et la plupart de ses fonctionnalités.
En particulier, il suppose que vous savez utiliser **Django Ninja**


!!! info
    Une grande partie du contenu présenté ici est tiré de Django-Ninja. Ainsi, si vous apprenez d'abord le framework Django-Ninja, la plupart de ces éléments vous sembleront naturels.

## **Installation**

```
pip install django-ninja-extra
```

Après l'installation, ajoutez `ninja_extra` à `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Création d'un projet Django**

(Si vous disposez déjà d'un projet Django existant, passez à l'étape suivante).

Démarrez un nouveau projet Django (ou utilisez-en un existant).

```
django-admin startproject myproject
```


## **Première étape**

Créons un module pour notre API. Créez un fichier **api.py** dans le même répertoire que **urls.py** :


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

Allez maintenant dans **urls.py** et ajoutez ce qui suit :


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **Définition des méthodes d'opération**
Une « opération » peut être l'une des « méthodes » HTTP :

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... et plus encore.

Ce sont les opérations définies par Django-Ninja sur l'API ou le routeur Django-Ninja.

Les mêmes opérations sont exposées aux APIControllers via la classe `route`.

La classe `route` est un décorateur supplémentaire qui transforme les méthodes d'instance d'un APIController en fonctions de route ou en endpoints.

D'autre part, `route` ici est un raccourci pour la classe `ControllerRouter`, une classe adaptateur qui adapte simplement l'APIController au routeur Django-Ninja. Elle fournit également un contrôle global sur toutes les routes définies dans n'importe quelle classe APIController.

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
Pour finaliser la configuration du contrôleur, vous devez décorer l'APIController avec `ControllerRouter` avant de l'enregistrer.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
