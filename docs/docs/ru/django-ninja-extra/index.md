![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Документация Django Ninja Extra

**Django Ninja Extra** предоставляет **подход на основе классов** вместе с дополнительными возможностями, которые ускорят вашу разработку RESTful API с использованием [**Django Ninja**](https://django-ninja.cn).

**Ключевые особенности:**

Все возможности **Django-Ninja**:

- **Простота**: спроектирован быть лёгким в использовании и интуитивным.
- **Быстрое выполнение**: благодаря **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** и **<a href="/async-support/">async-поддержке</a>, он демонстрирует очень высокую производительность.**
- **Быстрое написание кода**: подсказки типов и автоматическая документация позволяют сосредоточиться на бизнес-логике.
- **Основан на стандартах**: построен на стандартах: **OpenAPI** (ранее Swagger) и **JSON Schema**.
- **Дружелюбен к Django**: (очевидно) хорошо интегрирован с ядром Django и ORM.

Плюс **Extra**:

- **Классовый подход (class-based)**: проектируйте свои API в виде классов.
- **Разрешения (permissions)**: легко защищайте доступ к эндпоинтам с помощью permissions и аутентификации, заданных на уровне маршрута или контроллера.
- **Внедрение зависимостей**: классы контроллеров поддерживают использование Python [**Injector** ](https://injector.readthedocs.io/en/latest/) или [**django_injector**](https://github.com/blubber/django_injector). Это позволяет внедрять сервисные зависимости API в классы APIController и использовать их там, где необходимо.

---

### Требования к версиям
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


Полную документацию можно найти по [этой ссылке](https://django-ninja.cn/django-ninja-extra/).

## Установка

```
pip install django-ninja-extra
```
После установки добавьте `ninja_extra` в ваш `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## Использование

В вашем Django-проекте создайте новый файл `api.py` рядом с `urls.py`:

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

Теперь перейдите в `urls.py` и добавьте следующее:

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### Интерактивная документация API

Теперь перейдите на <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Вы увидите автоматическую интерактивную документацию API (на движке <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

![Swagger UI](images/ui_swagger_preview_readme.gif)

## Туториалы
- [django-ninja - Using django-ninja-extra permissions, controllers and throttling!](https://www.youtube.com/watch?v=yQqig-c2dd4) - Узнайте, как использовать permissions, контроллеры и throttling в django-ninja-extra
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - Пример проекта, демонстрирующего использование django-ninja-extra с ninja schema и ninja-jwt

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
