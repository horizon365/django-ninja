---
comments: true
---
# Tutoriel - Premiers pas

Ce tutoriel vous montre comment utiliser la plupart des fonctionnalités de **Django Ninja**.

Ce tutoriel suppose que vous connaissez au moins les bases du <a href="https://www.djangoproject.com/" target="_blank">framework Django</a>, comme la création d'un projet et son exécution.

## Installation

```console
pip install django-ninja
```

!!! note

    Ce n'est pas obligatoire, mais vous pouvez également ajouter `ninja` à `INSTALLED_APPS`.
    Dans ce cas, l'OpenAPI/Swagger UI (ou Redoc) sera chargé depuis le paquet JavaScript inclus (ce qui est plus rapide) (sinon le bundle JavaScript provient d'un CDN)

## Créer un projet Django

Démarrez un nouveau projet Django (ou, si vous avez déjà un projet Django existant, passez à l'étape suivante).

```
django-admin startproject myproject
```

## Créer une API

Créons un module pour notre API. Créez un fichier `api.py` au même endroit que le fichier `urls.py` racine de votre projet Django :

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

Allez maintenant dans `urls.py` et ajoutez ceci :

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## Notre première opération

**Django Ninja** est livré avec un décorateur pour chaque méthode HTTP (`GET`, `POST`,
`PUT`, etc.). Dans notre fichier `api.py`, ajoutons une simple opération « hello world ».

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

Allez maintenant dans le navigateur et ouvrez <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> qui renverra une simple réponse JSON :
```json
"Hello world"
```

!!! success

    Poursuivez avec le chapitre suivant **[Gérer les paramètres d'entrée](step2.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
