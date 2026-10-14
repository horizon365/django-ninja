![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Documentation de Django Ninja Extra

**Django Ninja Extra** fournit une approche **basée sur les classes** ainsi que des fonctionnalités supplémentaires qui accéléreront votre développement d'API RESTful avec [**Django Ninja**](https://django-ninja.cn).

**Fonctionnalités clés :**

Toutes les fonctionnalités de **Django-Ninja** :

- **Simple** : Conçu pour être facile à utiliser et intuitif.
- **Exécution rapide** : Grâce à **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** et **<a href="/async-support/">à la prise en charge de l'async</a>, il offre des performances très élevées.**
- **Codage rapide** : Les annotations de types et la documentation automatique vous permettent de vous concentrer sur la logique métier.
- **Basé sur les standards** : Basé sur les standards : **OpenAPI** (anciennement Swagger) et **JSON Schema**.
- **Ami de Django** : (Évidemment) bien intégré avec le cœur de Django et l'ORM.

Plus les fonctionnalités **Extra** :

- **Basé sur les classes** : Concevez vos APIs de manière basée sur les classes.
- **Permissions** : Sécurisez facilement l'accès aux endpoints via des permissions et une authentification définies au niveau de la route ou du contrôleur.
- **Injection de dépendances** : Les classes de contrôleur prennent en charge l'utilisation de [**Injector** ](https://injector.readthedocs.io/en/latest/) ou [**django_injector**](https://github.com/blubber/django_injector) Python. Cela vous permet d'injecter des services de dépendance d'API dans les classes APIController et de les utiliser là où c'est nécessaire.

---

### Exigences de version
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


Pour la documentation complète, [visitez ce lien](https://django-ninja.cn/django-ninja-extra/).

## Installation

```
pip install django-ninja-extra
```
Après l'installation, ajoutez `ninja_extra` à votre `INSTALLED_APPS`

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## Utilisation

Dans votre projet Django, créez un nouveau fichier `api.py` à côté de `urls.py` :

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

Maintenant, allez dans `urls.py` et ajoutez ce qui suit :

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### Documentation API interactive

Maintenant, allez sur <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Vous verrez la documentation API interactive automatique (propulsée par <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>) :

![Swagger UI](images/ui_swagger_preview_readme.gif)

## Tutoriels
- [django-ninja - Utilisation des permissions, contrôleurs et throttling de django-ninja-extra !](https://www.youtube.com/watch?v=yQqig-c2dd4) - Apprenez à utiliser les permissions, contrôleurs et throttling de django-ninja-extra
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - Un exemple de projet démontrant comment utiliser django-ninja-extra avec ninja schema et ninja-jwt

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
