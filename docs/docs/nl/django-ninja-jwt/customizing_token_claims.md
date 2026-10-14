Als je de claims die zijn opgenomen in de web tokens die worden gegenereerd door de views `NinjaJWTDefaultController` en `NinjaJWTSlidingController` wilt aanpassen, maak dan een subklasse voor de gewenste controller samen met de bijbehorende serializer. Hier is een voorbeeld:

!!! info
Als je geïnteresseerd bent in de asynchrone versie van de klasse, gebruik dan `AsyncNinjaJWTDefaultController` en `AsyncNinjaJWTSlidingController`.
Let ook op dat dit alleen werkt met Django-versies die asynchrone operaties ondersteunen.

```python
from ninja_jwt.schema import TokenObtainPairInputSchema
from ninja_jwt.controller import TokenObtainPairController
from ninja_extra import api_controller, route
from ninja import Schema


class UserSchema(Schema):
    first_name: str
    email: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema


class MyTokenObtainPairSchema(TokenObtainPairInputSchema):
    def output_schema(self):
        out_dict = self.get_response_schema_init_kwargs()
        out_dict.update(user=UserSchema.from_orm(self._user))
        return MyTokenObtainPairOutSchema(**out_dict)


@api_controller('/token', tags=['Auth'])
class MyTokenObtainPairController(TokenObtainPairController):
    @route.post(
        "/pair", response=MyTokenObtainPairOutSchema, url_name="token_obtain_pair"
    )
    def obtain_token(self, user_token: MyTokenObtainPairSchema):
        return user_token.output_schema()

```

Zoals bij de standaardcontroller moet je ook de controller registreren zoals getoond in [Aan de Slag](getting_started.md)

#### Using Django Ninja Router

Als je geïnteresseerd bent in het gebruik van functies in plaats van klassen, is dat ook mogelijk. Hier is een voorbeeld

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

Registreer de `router` als volgt bij de `api` van django-ninja:

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

Als je geïnteresseerd bent in het aanpassen van token-claims, kun je dat doen door subklassen te maken van `TokenObtainPairInputSchema` en `TokenObtainPairController`. Zie [Controller Schema Swapping](#controller-schema-swapping)

Daarnaast is het belangrijk om te weten dat `NinjaExtra` een handler registreert voor de klasse `APIException` die niet beschikbaar is in `NinjaAPI`-instanties.
Om dit te omzeilen heb je de volgende extra code nodig:

```python
from ninja import NinjaAPI
from ninja_extra import exceptions

api = NinjaAPI()
api.add_router('', tags=['Auth'], router=router)

def api_exception_handler(request, exc):
    headers = {}

    if isinstance(exc.detail, (list, dict)):
        data = exc.detail
    else:
        data = {"detail": exc.detail}

    response = api.create_response(request, data, status=exc.status_code)
    for k, v in headers.items():
        response.setdefault(k, v)

    return response

api.exception_handler(exceptions.APIException)(api_exception_handler)
```

### Controller Schema Swapping

Je kunt nu controller-schema's wisselen in de `NINJA_JWT`-instellingen zonder de functionaliteit van de Ninja JWT-controller te erven of te overschrijven.

Alle input-schema's van controllers moeten erven van `ninja_jwt.schema.InputSchemaMixin`, en schema's die tokens genereren moeten erven van
 `ninja_jwt.schema.TokenObtainInputSchemaBase` of `ninja_jwt.schema.TokenInputSchemaMixin` als je meer controle wilt.

Met behulp van het bovenstaande voorbeeld:

```python
# project/schema.py
from typing import Type, Dict
from ninja_jwt.schema import TokenObtainInputSchemaBase
from ninja import Schema
from ninja_jwt.tokens import RefreshToken

class UserSchema(Schema):
    first_name: str
    email: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema


class MyTokenObtainPairInputSchema(TokenObtainInputSchemaBase):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return MyTokenObtainPairOutSchema

    @classmethod
    def get_token(cls, user) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        values.update(user=UserSchema.from_orm(user)) # this will be needed when creating output schema
        return values
```

In `MyTokenObtainPairInputSchema` overschrijven we de methode `get_token` om ons token te definiëren, evenals enkele gegevens die door het output-schema nodig zijn.
We overschrijven ook de methode `get_response_schema` om ons output-schema `MyTokenObtainPairOutSchema` te definiëren.

Vervolgens passen we het schema `MyTokenObtainPairInputSchema` toe op de controller. Dit kan eenvoudig in de `NINJA_JWT`-instellingen.

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
Andere vervangbare schema's kunnen als volgt worden ingesteld
```python
# project/settings.py

NINJA_JWT = {
    # FOR OBTAIN PAIR
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': "project.schema.MyTokenObtainPairInputSchema",
    'TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA': "for.obtain_pair.refresh_input.schema",
    # FOR SLIDING TOKEN
    'TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA':  "for.obtain_sliding.input.schema",
    'TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA': "for.obtain_pair.refresh_input.schema",

    'TOKEN_BLACKLIST_INPUT_SCHEMA':  "for.blacklist_input.schema",
    'TOKEN_VERIFY_INPUT_SCHEMA':  "for.verify_input.schema",
}
```

![token_customization_git](./img/token_customize.gif)

!!! note
   `Controller Schema Swapping` is alleen beschikbaar in **v5.2.4** en hoger

!!! success

    Ga verder naar het volgende hoofdstuk **[Handmatig Tokens Aanmaken](creating_tokens_manually.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
