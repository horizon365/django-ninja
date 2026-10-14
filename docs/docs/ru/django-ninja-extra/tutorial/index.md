---
comments: true
---
# **Руководство / Справочник**

Это руководство показывает, как использовать **Django Ninja Extra** и большинство его возможностей.
В частности, предполагается, что вы знаете, как пользоваться **Django Ninja**


!!! info
    Значительная часть содержимого здесь взята из Django-Ninja. Поэтому, если вы сначала изучите фреймворк Django-Ninja, многое из этого станет понятно.

## **Установка**

```
pip install django-ninja-extra
```

После установки добавьте `ninja_extra` в `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Создание Django-проекта**

(Если у вас уже есть существующий Django-проект, переходите к следующему шагу).

Начните новый Django-проект (или используйте существующий).

```
django-admin startproject myproject
```


## **Первый шаг**

Давайте создадим модуль для нашего API. Создайте файл **api.py** в том же каталоге, где находится **urls.py**:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

Теперь откройте **urls.py** и добавьте следующее:


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **Определение методов операций**
«Операция» может быть одним из HTTP-«методов»:

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... и другими.

Это операции, определённые Django-Ninja на API или маршрутизаторе Django-Ninja.

Те же операции доступны в APIControllers через класс `route`.

Класс `route` — это дополнительный декоратор, который преобразует методы экземпляров APIController в функции маршрутов или эндпоинты.

С другой стороны, `route` здесь — это сокращение от класса `ControllerRouter`, класса-адаптера, который просто адаптирует APIController к маршрутизатору Django-Ninja. Он также предоставляет глобальное управление всеми маршрутами, определёнными в любом классе APIController.

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
Чтобы завершить настройку контроллера, вы должны декорировать APIController с помощью `ControllerRouter` перед его регистрацией.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
