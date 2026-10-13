![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Django Ninja Extra Documentation

**Django Ninja Extra** provides a **class-based** approach along with additional features that will accelerate your RESTful API development using [**Django Ninja**](https://django-ninja.cn).

**Key features:**

All **Django-Ninja** features:

- **Simple**: Designed to be easy to use and intuitive.
- **Fast execution**: Thanks to **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** and **<a href="/async-support/">async support</a>, it delivers very high performance.**
- **Fast coding**: Type hints and automatic documentation let you focus on business logic.
- **Standards-based**: Based on standards: **OpenAPI** (formerly Swagger) and **JSON Schema**.
- **Django friendly**: (Obviously) well integrated with Django core and ORM.

Plus **Extra**:

- **Class-based**: Design your APIs in a class-based manner.
- **Permissions**: Easily secure access endpoints via permissions and authentication defined at the route level or controller level.
- **Dependency injection**: Controller classes support using Python [**Injector** ](https://injector.readthedocs.io/en/latest/) or [**django_injector**](https://github.com/blubber/django_injector). This allows you to inject API dependency services into APIController classes and use them where needed.

---

### Version Requirements
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


For the full documentation, [visit this link](https://django-ninja.cn/django-ninja-extra/).

## Installation

```
pip install django-ninja-extra
```
After installation, add `ninja_extra` to your `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## Usage

In your Django project, create a new `api.py` file next to `urls.py`:

```Python
from ninja_extra import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()

# Function-based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}

# Class-based definition
@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/subtract',)
    def subtract(self, a: int, b: int):
        """Subtracts a from b"""
        return {"result": a - b}

    @http_get('/divide',)
    def divide(self, a: int, b: int):
        """Divides a by b"""
        return {"result": a / b}
    
    @http_get('/multiple',)
    def multiple(self, a: int, b: int):
        """Multiples a with b"""
        return {"result": a * b}
    
api.register_controllers(
    MathAPI
)
```

Now go to `urls.py` and add the following:

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### Interactive API documentation

Now go to <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

You will see the automatic interactive API documentation (powered by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

![Swagger UI](images/ui_swagger_preview_readme.gif)

## Tutorials
- [django-ninja - Using django-ninja-extra permissions, controllers and throttling!](https://www.youtube.com/watch?v=yQqig-c2dd4) - Learn how to use django-ninja-extra permissions, controllers and throttling
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - A sample project demonstrating how to use django-ninja-extra with ninja schema and ninja-jwt

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
