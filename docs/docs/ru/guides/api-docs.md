---
comments: true
---
# Документация API

## OpenAPI-документация

После того как вы настроили свой Ninja API и запустили runserver — откройте <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Вы увидите автоматическую интерактивную документацию API (на базе <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a>)


## CDN и статические файлы

Вам не нужно добавлять django ninja в `INSTALLED_APPS`. В этом случае интерактивный интерфейс будет размещаться с CDN.

Чтобы размещать документацию (Js/css) на собственном сервере — просто добавьте `"ninja"` в INSTALLED_APPS — в этом случае её будет размещать стандартный механизм хостинга статических файлов Django.

## Переключение на Redoc


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
После этого вы увидите другую автогенерируемую документацию (на базе <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>).

## Изменение настроек отображения документации
Чтобы задать пользовательские настройки для Swagger или Redoc, вы можете использовать аргумент `settings` класса документации.

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

О других настройках смотрите в документации:

 - [Конфигурация Swagger](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Конфигурация Redoc](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## Скрыть документацию

Если вам не нужно показывать интерактивную документацию — установите для аргумента `docs_url` значение `None`

```python
api = NinjaAPI(docs_url=None)
```

## Защита документации

Чтобы использовать аутентификацию (или любой другой декоратор для любых целей), используйте аргумент `docs_decorator`:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## Расширение схемы OpenAPI пользовательскими атрибутами

Вы можете расширить схему OpenAPI пользовательскими атрибутами, например добавить `termsOfService`

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

## Формирование URL документации

Вы можете построить (reverse) URL представления документации API, обратившись к имени представления `openapi-view`.

В коде Python, например:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

В шаблонах Django, например:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## Создание собственного просмотрщика документации

Чтобы создать собственное представление OpenAPI — создайте класс, наследующийся от DocsBase, и переопределите метод `render_page`:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    Перейдите к следующему разделу **[Обработка ошибок](errors.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
