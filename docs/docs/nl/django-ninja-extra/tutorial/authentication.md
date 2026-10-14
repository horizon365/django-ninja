---
comments: true
---
# **Authenticatie**

**Django Ninja Extra** biedt dezelfde API als **Django Ninja** wat betreft autorisatie en authenticatie, wat zorgt voor consistentie en gebruiksgemak tussen de twee pakketten.

## **Automatisch OpenAPI Schema**

Hier is een voorbeeld waarin de client een header moet doorgeven voor authenticatie:

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

## **Globale Authenticatie** 

Als je **alle** routemethoden die zijn gedefinieerd in de `api` en APIController wilt beveiligen, kun je de parameter `auth` doorgeven aan de constructor `NinjaExtraAPI`:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
Lees meer over [authenticatie](https://django-ninja.cn/guides/authentication/) op django-ninja.

## Asynchrone Authenticatieklassen

Ninja Extra voegt async-ondersteuning toe aan alle `Auth`-basisklassen die Django Ninja biedt in het pakket `ninja_extra.security`, en behoudt een vergelijkbare interface. Het is belangrijk om op te merken dat bij het gebruik van deze asynchrone authenticatieklassen de endpoint-handler **moet** een asynchrone functie zijn.

Laten we bijvoorbeeld het eerste authenticatievoorbeeld herschrijven met de klasse `AsyncHttpBearer`.

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
In het bovenstaande voorbeeld hebben we `HttpBearer` gewijzigd in `AsyncHttpBearer` en bearer omgezet naar een `async`-endpoint. 
Als `AuthBearer` moet worden toegepast op de **authenticatie** van `MyController`, dan moeten alle route-handlers onder `MyController` asynchrone route-handlers zijn.


## **JWT Authenticatie**
Als je JWT-authenticatie wilt gebruiken. Zie [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
