---
comments: true
---
# Tutorial - First steps

This tutorial shows you how to use most of the features of **Django Ninja**.

This tutorial assumes that you know at least the basics of the <a href="https://www.djangoproject.com/" target="_blank">Django framework</a>, such as how to create a project and run it.

## Installation

```console
pip install django-ninja
```

!!! note

    This is not required, but you can also add `ninja` to `INSTALLED_APPS`.
    In that case, the OpenAPI/Swagger UI (or Redoc) will be loaded from the bundled JavaScript package (which is faster) (otherwise the JavaScript bundle comes from a CDN)

## Create a Django project

Start a new Django project (or, if you already have an existing Django project, skip to the next step).

```
django-admin startproject myproject
```

## Create an API

Let's create a module for our API. Create an `api.py` file in the same location as your Django project's root `urls.py`:

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

Now go to `urls.py` and add the following:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## Our first operation

**Django Ninja** ships with a decorator for each HTTP method (`GET`, `POST`,
`PUT`, etc.). In our `api.py` file, let's add a simple "hello world" operation.

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

Now go to the browser and open <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> which will return a simple JSON response:
```json
"Hello world"
```

!!! success

    Continue to the next chapter **[Handling input parameters](step2.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
