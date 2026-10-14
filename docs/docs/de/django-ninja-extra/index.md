![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Django Ninja Extra Dokumentation

**Django Ninja Extra** bietet einen **klassenbasierten** Ansatz sowie zusätzliche Funktionen, die Ihre RESTful-API-Entwicklung mit [**Django Ninja**](https://django-ninja.cn) beschleunigen.

**Hauptmerkmale:**

Alle **Django-Ninja**-Funktionen:

- **Einfach**: Gestaltet, um leicht zu bedienen und intuitiv zu sein.
- **Schnelle Ausführung**: Dank **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** und **<a href="/async-support/">async-Unterstützung</a> liefert sie eine sehr hohe Performance.**
- **Schnelles Programmieren**: Type-Hints und automatische Dokumentation lassen Sie sich auf die Geschäftslogik konzentrieren.
- **Standardsbasiert**: Basiert auf Standards: **OpenAPI** (ehemals Swagger) und **JSON Schema**.
- **Django-freundlich**: (Natürlich) gut in Django Core und ORM integriert.

Zusätzlich **Extra**:

- **Klassenbasiert**: Entwerfen Sie Ihre APIs auf klassenbasierte Weise.
- **Berechtigungen**: Sichern Sie Endpunkte leicht über Berechtigungen und Authentifizierung ab, definiert auf Routen- oder Controller-Ebene.
- **Dependency Injection**: Controller-Klassen unterstützen die Verwendung von Python [**Injector** ](https://injector.readthedocs.io/en/latest/) oder [**django_injector**](https://github.com/blubber/django_injector). Dies erlaubt es Ihnen, API-Dienste als Abhängigkeiten in APIController-Klassen zu injizieren und sie dort zu verwenden, wo sie benötigt werden.

---

### Versionsanforderungen
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


Für die vollständige Dokumentation [folgen Sie diesem Link](https://django-ninja.cn/django-ninja-extra/).

## Installation

```
pip install django-ninja-extra
```
Fügen Sie nach der Installation `ninja_extra` zu Ihrer `INSTALLED_APPS` hinzu

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## Verwendung

Erstellen Sie in Ihrem Django-Projekt eine neue Datei `api.py` neben `urls.py`:

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

Gehen Sie nun zu `urls.py` und fügen Sie Folgendes hinzu:

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### Interaktive API-Dokumentation

Rufen Sie nun <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> auf

Sie sehen die automatische, interaktive API-Dokumentation (betrieben von <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

![Swagger UI](images/ui_swagger_preview_readme.gif)

## Tutorials
- [django-ninja - Using django-ninja-extra permissions, controllers and throttling!](https://www.youtube.com/watch?v=yQqig-c2dd4) - Erfahren Sie, wie man die Berechtigungen, Controller und das Throttling von django-ninja-extra verwendet
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - Ein Beispielprojekt, das die Verwendung von django-ninja-extra mit ninja schema und ninja-jwt demonstriert

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
