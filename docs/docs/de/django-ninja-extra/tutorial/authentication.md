---
comments: true
---
# **Authentifizierung**

**Django Ninja Extra** bietet dieselbe API wie **Django Ninja** in Bezug auf Autorisierung und Authentifizierung, was für Konsistenz und einfache Handhabung zwischen den beiden Paketen sorgt.

## **Automatisches OpenAPI-Schema**

Hier ist ein Beispiel, bei dem der Client einen Header zur Authentifizierung übergeben muss:

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

## **Globale Authentifizierung** 

Wenn Sie **alle** in der `api` und im APIController definierten Routenmethoden schützen möchten, können Sie den Parameter `auth` an den Konstruktor `NinjaExtraAPI` übergeben:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
Mehr über [Authentifizierung](https://django-ninja.cn/guides/authentication/) bei django-ninja erfahren.

## Asynchrone Authentifizierungsklassen

Ninja Extra fügt allen von Django Ninja bereitgestellten `Auth`-Basisklassen im Paket `ninja_extra.security` asynchrone Unterstützung hinzu
und behält eine ähnliche Schnittstelle bei. Es ist wichtig zu beachten, dass der Endpoint-Handler bei Verwendung dieser asynchronen Authentifizierungsklassen **eine asynchrone Funktion sein muss**.

Lassen Sie uns beispielsweise das erste Authentifizierungsbeispiel mit der Klasse `AsyncHttpBearer` umschreiben.

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
Im obigen Beispiel haben wir `HttpBearer` durch `AsyncHttpBearer` ersetzt und bearer zu einem `async`-Endpoint geändert. 
Wenn `AuthBearer` auf die **Authentifizierung** von `MyController` angewendet werden soll, müssen alle Routen-Handler unter `MyController` asynchrone Routen-Handler sein.


## **JWT-Authentifizierung**
Wenn Sie die JWT-Authentifizierung verwenden möchten. Siehe [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
