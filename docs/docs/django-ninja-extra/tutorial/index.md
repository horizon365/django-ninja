---
comments: true
---
# **教程 / 参考**

本教程向您展示如何使用 **Django Ninja Extra** 及其大部分功能。
特别是假设您知道如何使用 **Django Ninja**


!!! info
    这里的很多内容都来自 Django-Ninja。因此，如果您首先了解 Django-Ninja 框架，很多内容都会有意义。

## **安装**

```
pip install django-ninja-extra
```

安装后，将 `ninja_extra` 添加到 `INSTALLED_APPS` 中

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **创建 Django 项目**

（如果您已经有一个现有的 Django 项目，请跳到下一步）。

启动一个新的 Django 项目（或使用现有的项目）。

```
django-admin startproject myproject
```


## **第一步**

让我们为我们的 API 创建一个模块。 在与 **urls.py** 相同的目录位置创建一个 **api.py** 文件:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

现在转到 **urls.py** 并添加以下内容:


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
“操作” 可以是 HTTP “方法”之一：

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... and more.

这些是 Django-Ninja 在 API 或 Django-Ninja 路由器上定义的操作。

相同的操作通过 `route` 类暴露给 APIControllers。

`route` 类是一个额外的装饰器，它将 APIController 实例方法转换为路由函数或端点。

另一方面，这里的 `route` 是 `ControllerRouter` 类的缩写，是一个适配器类，它仅将 APIController 适配到 Django-Ninja 路由器。它还提供对在任何 APIController 类中定义的所有路由的全局控制。

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
要完成控制器设置，必须在注册之前使用 `ControllerRouter` 装饰 APIController。


<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
