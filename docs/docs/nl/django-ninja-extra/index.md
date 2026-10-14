![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Django Ninja Extra-documentatie

**Django Ninja Extra** biedt een **class-based** aanpak samen met extra functies die je RESTful API-ontwikkeling met [**Django Ninja**](https://django-ninja.cn) versnellen.

**Belangrijkste functies:**

Alle **Django-Ninja**-functies:

- **Eenvoudig**: ontworpen om gemakkelijk en intuïtief te gebruiken.
- **Snelle uitvoering**: dankzij **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** en **<a href="/async-support/">async-ondersteuning</a> levert het zeer hoge prestaties.**
- **Snel coderen**: type hints en automatische documentatie laten je je richten op de bedrijfslogica.
- **Gebaseerd op standaarden**: gebaseerd op standaarden: **OpenAPI** (voorheen Swagger) en **JSON Schema**.
- **Django-vriendelijk**: (uiteraard) goed geïntegreerd met de Django-kern en de ORM.

Plus **Extra**:

- **Class-based**: ontwerp je API's op een class-based manier.
- **Machtigingen**: beveilig toegangsendpoints eenvoudig via machtigingen en authenticatie, gedefinieerd op route- of controllerniveau.
- **Dependency injection**: controllerklassen ondersteunen het gebruik van Python [**Injector** ](https://injector.readthedocs.io/en/latest/) of [**django_injector**](https://github.com/blubber/django_injector). Zo kun je API-afhankelijkheidsdiensten injecteren in APIController-klassen en ze waar nodig gebruiken.

---

### Versievereisten
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


Voor de volledige documentatie, [bezoek deze link](https://django-ninja.cn/django-ninja-extra/).

## Installatie

```
pip install django-ninja-extra
```
Voeg na installatie `ninja_extra` toe aan je `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## Gebruik

Maak in je Django-project een nieuw bestand `api.py` aan naast `urls.py`:

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

Ga nu naar `urls.py` en voeg het volgende toe:

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### Interactieve API-documentatie

Ga nu naar <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Je ziet de automatische interactieve API-documentatie (aangedreven door <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

![Swagger UI](images/ui_swagger_preview_readme.gif)

## Tutorials
- [django-ninja - django-ninja-extra machtigingen, controllers en throttling gebruiken!](https://www.youtube.com/watch?v=yQqig-c2dd4) - Leer hoe je django-ninja-extra-machtigingen, controllers en throttling gebruikt
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - Een voorbeeldproject dat laat zien hoe je django-ninja-extra gebruikt met ninja schema en ninja-jwt

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
