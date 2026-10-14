---
comments: true
---
# API-Dokumentation

## OpenAPI-Dokumentation

Sobald Sie Ihre Ninja-API konfiguriert und den Runserver gestartet haben – öffnen Sie <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Sie sehen die automatische, interaktive API-Dokumentation (betrieben mit <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a>)


## CDN und statische Dateien

Sie müssen django ninja nicht zu `INSTALLED_APPS` hinzufügen. In diesem Fall wird die interaktive UI über ein CDN ausgeliefert.

Um die Dokumentation (Js/CSS) von Ihrem eigenen Server auszuliefern – fügen Sie einfach `"ninja"` zu INSTALLED_APPS hinzu – in diesem Fall liefert der Standardmechanismus von Django für statische Dateien die Dokumentation aus.

## Zu Redoc wechseln


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
Dann sehen Sie eine weitere automatisch generierte Dokumentation (betrieben mit <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>).

## Anzeigeeinstellungen der Dokumentation ändern
Um benutzerdefinierte Einstellungen für Swagger oder Redoc vorzunehmen, können Sie das Argument `settings` der Docs-Klasse verwenden.

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

Weitere Einstellungen finden Sie in der Dokumentation:

 - [Swagger-Konfiguration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Redoc-Konfiguration](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## Dokumentation ausblenden

Wenn Sie die interaktive Dokumentation nicht anzeigen möchten – setzen Sie das Argument `docs_url` auf `None`

```python
api = NinjaAPI(docs_url=None)
```

## Dokumentation schützen

Um Authentifizierung zu verwenden (oder einen anderen Dekorator für beliebige Zwecke), nutzen Sie das Argument `docs_decorator`:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## OpenAPI-Schema um benutzerdefinierte Attribute erweitern

Sie können das OpenAPI-Schema um benutzerdefinierte Attribute erweitern, zum Beispiel um `termsOfService` hinzuzufügen

```python
api = NinjaAPI(
   openapi_extra={
       "info": {
           "termsOfService": "https://example.com/terms/",
       }
   },
   title="Demo API",
   description="This is a demo API with dynamic OpenAPI info section"
)
```

## Dokumentations-URL auflösen

Sie können die URL der Dokumentations-View Ihrer API über den Namen der View `openapi-view` reversen.

In Python-Code zum Beispiel:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

In Django-Templates zum Beispiel:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## Einen eigenen Docs-Viewer erstellen

Um Ihre eigene OpenAPI-View zu erstellen – erzeugen Sie eine Klasse, die von DocsBase erbt, und überschreiben Sie die Methode `render_page`:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    Fahren Sie mit dem nächsten Abschnitt fort: **[Fehlerbehandlung](errors.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
