---
comments: true
---
# Учебник — Первые шаги

Этот учебник покажет вам, как использовать большинство возможностей **Django Ninja**.

Этот учебник предполагает, что вы знаете хотя бы основы <a href="https://www.djangoproject.com/" target="_blank">фреймворка Django</a>, например, как создать проект и запустить его.

## Установка

```console
pip install django-ninja
```

!!! note

    Это не обязательно, но вы также можете добавить `ninja` в `INSTALLED_APPS`.
    В этом случае OpenAPI/Swagger UI (или Redoc) будут загружены из встроенного JavaScript-пакета (что быстрее) (иначе JavaScript-бандл загружается с CDN)

## Создайте Django-проект

Создайте новый Django-проект (или, если у вас уже есть существующий Django-проект, переходите к следующему шагу).

```
django-admin startproject myproject
```

## Создайте API

Давайте создадим модуль для нашего API. Создайте файл `api.py` в том же каталоге, где находится корневой `urls.py` вашего Django-проекта:

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

Теперь откройте `urls.py` и добавьте следующее:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## Наша первая операция

**Django Ninja** поставляется с декоратором для каждого HTTP-метода (`GET`, `POST`,
`PUT` и т.д.). В нашем файле `api.py` давайте добавим простую операцию «hello world».

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

Теперь откройте в браузере <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> — он вернёт простой JSON-ответ:
```json
"Hello world"
```

!!! success

    Продолжайте со следующей главы **[Обработка входных параметров](step2.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
