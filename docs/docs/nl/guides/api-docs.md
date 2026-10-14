---
comments: true
---
# API-documentatie

## OpenAPI docs

Zodra je je Ninja API hebt geconfigureerd en runserver hebt gestart - ga naar <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Je ziet daar de automatische, interactieve API-documentatie (mogelijk gemaakt door <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a>)


## CDN en statische bestanden

Je hoeft django ninja niet toe te voegen aan `INSTALLED_APPS`. In dat geval wordt de interactieve UI gehost vanaf een CDN.

Om de documentatie (Js/css) vanaf je eigen server te hosten - zet `"ninja"` gewoon in INSTALLED_APPS - in dat geval wordt het gehost via het standaard mechanisme voor statische bestanden van django.

## Overschakelen naar Redoc


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
Dan zie je een andere automatisch gegenereerde documentatie (mogelijk gemaakt door <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>).

## Weergave-instellingen van de documentatie wijzigen
Om aangepaste instellingen in te stellen voor Swagger of Redocs, kun je het argument `settings` op de docs class gebruiken.

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

Voor overige instellingen, raadpleeg de documentatie:

 - [Swagger configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Redoc configuration](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## Documentatie verbergen

Als je de interactieve documentatie niet hoeft weer te geven - stel het argument `docs_url` in op `None`

```python
api = NinjaAPI(docs_url=None)
```

## Documentatie beveiligen

Om authenticatie te gebruiken (of een andere decorator voor welk doel dan ook), gebruik je het argument `docs_decorator`:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## OpenAPI schema uitbreiden met aangepaste attributen

Je kunt het OpenAPI schema uitbreiden met aangepaste attributen, bijvoorbeeld door `termsOfService` toe te voegen

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

## De URL van de documentatie resolven

Je kunt de URL van de documentatieview van de API reverse-resolven door te verwijzen naar de naam van de view: `openapi-view`.

In Python code, bijvoorbeeld:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

In Django templates, bijvoorbeeld:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## Een eigen docs viewer maken

Om je eigen OpenAPI view te maken - maak een class die overerft van DocsBase en overschrijf de methode `render_page`:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    Ga verder naar de volgende sectie **[Foutafhandeling](errors.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
