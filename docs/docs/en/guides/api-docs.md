---
comments: true
---
# API Documentation

## OpenAPI docs

Once you have configured your Ninja API and started runserver - go to <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

You will see the automatic, interactive API documentation (powered by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a>)


## CDN and static files

You do not need to add django ninja to `INSTALLED_APPS`. In this case the interactive UI will be hosted from a CDN.

To host the documentation (Js/css) from your own server - simply put `"ninja"` into INSTALLED_APPS - in this case the standard django static files hosting mechanism will host it.

## Switch to Redoc


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
Then you will see another auto-generated documentation (powered by <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>).

## Change documentation display settings
To set some custom settings for Swagger or Redocs, you can use the `settings` argument on the docs class.

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

For other settings, refer to the documentation:

 - [Swagger configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Redoc configuration](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## Hide docs

If you do not need to display the interactive documentation - set the `docs_url` argument to `None`

```python
api = NinjaAPI(docs_url=None)
```

## Protect docs

To use authentication (or any other decorator for any purpose), use the `docs_decorator` argument:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## Extend OpenAPI schema with custom attributes

You can extend the OpenAPI schema with custom attributes, for example adding `termsOfService`

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

## Resolving the documentation URL

You can reverse the URL of the API's documentation view by referencing the view's name `openapi-view`.

In Python code, for example:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

In Django templates, for example:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## Create a custom docs viewer

To create your own OpenAPI view - create a class that inherits from DocsBase and override the `render_page` method:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    Continue to the next section **[Error handling](errors.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
