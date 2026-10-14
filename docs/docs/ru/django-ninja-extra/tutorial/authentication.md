---
comments: true
---
# **Аутентификация**

**Django Ninja Extra** предоставляет тот же API, что и **Django Ninja**, в части авторизации и аутентификации, обеспечивая согласованность и простоту использования между этими двумя пакетами.

## **Автоматическая OpenAPI Schema**

Вот пример, в котором клиент должен передавать заголовок для аутентификации:

`Authorization: Bearer supersecret`

```Python
from ninja.security import HttpBearer
from ninja_extra import api_controller, route
from ninja.constants import NOT_SET


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    def bearer(self):
        return {"token": self.context.request.auth}

```

## **Глобальная аутентификация** 

Если вам нужно защитить **все** методы маршрутов, определённые в `api` и APIController, вы можете передать параметр `auth` в конструктор `NinjaExtraAPI`:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
Подробнее об [аутентификации](https://django-ninja.cn/guides/authentication/) в django-ninja.

## Классы асинхронной аутентификации

Ninja Extra добавляет поддержку async для всех базовых классов `Auth`, предоставляемых Django Ninja, в пакете `ninja_extra.security`,
сохраняя аналогичный интерфейс. Важно отметить, что при использовании этих классов асинхронной аутентификации обработчик эндпоинта **должен** быть async-функцией.

Например, перепишем первый пример аутентификации с использованием класса `AsyncHttpBearer`.

```Python
from ninja_extra import api_controller, route
from ninja_extra.security import AsyncHttpBearer
from ninja.constants import NOT_SET


class AuthBearer(AsyncHttpBearer):
    async def authenticate(self, request, token):
        # await some actions
        if token == "supersecret":
            return token


@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    async def bearer(self):
        return {"token": self.context.request.auth}

```
В приведённом выше примере мы заменили `HttpBearer` на `AsyncHttpBearer` и сделали bearer асинхронным (`async`) эндпоинтом. 
Если `AuthBearer` применяется для **аутентификации** `MyController`, то все обработчики маршрутов внутри `MyController` должны быть асинхронными обработчиками маршрутов.


## **JWT-аутентификация**
Если вы хотите использовать JWT-аутентификацию. См. [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
