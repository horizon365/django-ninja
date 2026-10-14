---
comments: true
---
# Documentation de l'API

## Documentation OpenAPI

Une fois votre API Ninja configurée et runserver démarré - rendez-vous sur <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Vous verrez la documentation automatique et interactive de l'API (propulsée par <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a>)


## CDN et fichiers statiques

Vous n'avez pas besoin d'ajouter django ninja à `INSTALLED_APPS`. Dans ce cas, l'interface interactive sera hébergée depuis un CDN.

Pour héberger la documentation (Js/css) depuis votre propre serveur - placez simplement `"ninja"` dans INSTALLED_APPS - dans ce cas, le mécanisme standard d'hébergement des fichiers statiques de django s'en chargera.

## Passer à Redoc


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
Vous verrez alors une autre documentation générée automatiquement (propulsée par <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>).

## Modifier les paramètres d'affichage de la documentation
Pour définir des paramètres personnalisés pour Swagger ou Redoc, vous pouvez utiliser l'argument `settings` de la classe de documentation.

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

Pour les autres paramètres, reportez-vous à la documentation :

 - [Configuration de Swagger](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Configuration de Redoc](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## Masquer la documentation

Si vous n'avez pas besoin d'afficher la documentation interactive - définissez l'argument `docs_url` sur `None`

```python
api = NinjaAPI(docs_url=None)
```

## Protéger la documentation

Pour utiliser l'authentification (ou tout autre décorateur à quelque fin que ce soit), utilisez l'argument `docs_decorator` :

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## Étendre le schéma OpenAPI avec des attributs personnalisés

Vous pouvez étendre le schéma OpenAPI avec des attributs personnalisés, par exemple en ajoutant `termsOfService`

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

## Résoudre l'URL de la documentation

Vous pouvez inverser (reverse) l'URL de la vue de documentation de l'API en référençant le nom de la vue `openapi-view`.

Dans du code Python, par exemple :
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

Dans les templates Django, par exemple :
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## Créer une visionneuse de documentation personnalisée

Pour créer votre propre vue OpenAPI - créez une classe qui hérite de DocsBase et redéfinissez la méthode `render_page` :



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    Poursuivez avec la section suivante **[Gestion des erreurs](errors.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
