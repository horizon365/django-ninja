---
comments: true
---
# **Tutorial / Reference**

This tutorial shows you how to use **Django Ninja Extra** and most of its features.
In particular, it assumes you know how to use **Django Ninja**


!!! info
    Much of the content here is derived from Django-Ninja. So if you learn about the Django-Ninja framework first, much of this will make sense.

## **Installation**

```
pip install django-ninja-extra
```

After installation, add `ninja_extra` to `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Creating a Django Project**

(If you already have an existing Django project, skip to the next step).

Start a new Django project (or use an existing one).

```
django-admin startproject myproject
```


## **First Step**

Let's create a module for our API. Create an **api.py** file in the same directory location as **urls.py**:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

Now go to **urls.py** and add the following:


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **Defining operation methods**
An "operation" can be one of the HTTP "methods":

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... and more.

These are the operations defined by Django-Ninja on the API or Django-Ninja router.

The same operations are exposed to APIControllers via the `route` class.

The `route` class is an additional decorator that transforms APIController instance methods into route functions or endpoints.

On the other hand, `route` here is shorthand for the `ControllerRouter` class, an adapter class that simply adapts APIController to the Django-Ninja router. It also provides global control over all routes defined in any APIController class.

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
To complete the controller setup, you must decorate the APIController with `ControllerRouter` before registering it.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
