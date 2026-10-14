---
comments: true
---
# Tutorial - Erste Schritte

Dieses Tutorial zeigt Ihnen, wie Sie die meisten Funktionen von **Django Ninja** verwenden.

Dieses Tutorial setzt voraus, dass Sie mindestens die Grundlagen des <a href="https://www.djangoproject.com/" target="_blank">Django-Frameworks</a> kennen, z. B. wie man ein Projekt erstellt und ausführt.

## Installation

```console
pip install django-ninja
```

!!! note

    Dies ist nicht erforderlich, aber Sie können `ninja` auch zu `INSTALLED_APPS` hinzufügen.
    In diesem Fall wird die OpenAPI/Swagger-UI (oder Redoc) aus dem mitgelieferten JavaScript-Paket geladen (was schneller ist) (andernfalls kommt das JavaScript-Bündel von einem CDN)

## Ein Django-Projekt erstellen

Starten Sie ein neues Django-Projekt (oder, falls Sie bereits ein bestehendes Django-Projekt haben, springen Sie zum nächsten Schritt).

```
django-admin startproject myproject
```

## Eine API erstellen

Erstellen wir ein Modul für unsere API. Legen Sie eine Datei `api.py` am selben Speicherort an wie die Root-`urls.py` Ihres Django-Projekts:

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

Gehen Sie nun zu `urls.py` und fügen Sie Folgendes hinzu:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## Unsere erste Operation

**Django Ninja** wird mit einem Decorator für jede HTTP-Methode geliefert (`GET`, `POST`,
`PUT` usw.). Fügen wir in unserer Datei `api.py` eine einfache „Hello world"-Operation hinzu.

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

Öffnen Sie nun den Browser unter <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>, was eine einfache JSON-Antwort zurückgibt:
```json
"Hello world"
```

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Eingabeparameter verarbeiten](step2.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
