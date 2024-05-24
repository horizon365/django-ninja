# 教程 - 第一步

本教程向您展示如何使用 **Django Ninja** 的大部分功能.

本教程假定您至少了解 <a href="https://www.djangoproject.com/" target="_blank">Django 框架</a>的一些基础知识，例如如何创建项目并运行它。

## 安装

```console
pip install django-ninja
```

!!! 注意

    这不是必需的，但您也可以将 `ninja` 添加到 `INSTALLED_APPS`。
    在这种情况下，OpenAPI/Swagger UI（或 Redoc）将从自带的 JavaScript 捆绑包中加载（更快）（否则 JavaScript 捆绑包来自内容分发网络）

## 创建 Django 项目

启动一个新的 Django 项目（或者如果您已经有一个现有的 Django 项目，请跳到下一步）。

```
django-admin startproject myproject
```

## 创建 API

让我们为我们的 API 创建一个模块。在与您的 Django 项目的根 `urls.py` 相同的目录位置创建一个 `api.py` 文件：

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

现在转到 `urls.py` 并添加以下内容:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## 我们的第一个操作

**Django Ninja** 为每个 HTTP 方法 (`GET`, `POST`,
`PUT`, 等) 配备了一个装饰器。在我们的 `api.py` 文件中，让我们添加一个简单的 "hello world" 操作。

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

现在去浏览器打开 <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> 将返回一个简单的 JSON 响应:
```json
"Hello world"
```

!!! 大功告成

    继续下一章节 **[解析传入参数](step2.md)**.