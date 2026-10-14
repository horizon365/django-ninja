---
comments: true
---
# **Authentification**

**Django Ninja Extra** fournit la même API que **Django Ninja** en matière d'autorisation et d'authentification, garantissant la cohérence et la facilité d'utilisation entre les deux packages.

## **Schéma OpenAPI automatique**

Voici un exemple dans lequel le client doit transmettre un en-tête pour l'authentification :

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

## **Authentification globale** 

Si vous avez besoin de protéger **toutes** les méthodes de route définies dans l'`api` et l'APIController, vous pouvez passer le paramètre `auth` au constructeur `NinjaExtraAPI` :


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
Pour en savoir plus sur l'[authentification](https://django-ninja.cn/guides/authentication/) dans django-ninja.

## Classes d'authentification asynchrones

Ninja Extra ajoute la prise en charge de l'asynchrone à toutes les classes de base `Auth` fournies par Django Ninja dans le package `ninja_extra.security`,
et maintient une interface similaire. Il est important de noter que lorsque vous utilisez ces classes d'authentification asynchrones, le gestionnaire d'endpoint **doit** être une fonction asynchrone.

Par exemple, réécrivons le premier exemple d'authentification avec la classe `AsyncHttpBearer`.

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
Dans l'exemple ci-dessus, nous avons remplacé `HttpBearer` par `AsyncHttpBearer` et transformé bearer en un endpoint `async`. 
Si `AuthBearer` doit être appliqué à l'**authentification** de `MyController`, alors tous les gestionnaires de route sous `MyController` doivent être des gestionnaires de route asynchrones.


## **Authentification JWT**
Si vous souhaitez utiliser l'authentification JWT. Consultez [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
