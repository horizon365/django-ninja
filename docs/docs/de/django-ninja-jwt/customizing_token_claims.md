Wenn Sie die in den von den Views `NinjaJWTDefaultController` und `NinjaJWTSlidingController` generierten Web-Tokens enthaltenen Claims anpassen möchten, erstellen Sie eine Unterklasse für den gewünschten Controller zusammen mit dem zugehörigen Serializer. Hier ist ein Beispiel:

!!! info
Wenn Sie an der asynchronen Version der Klasse interessiert sind, verwenden Sie `AsyncNinjaJWTDefaultController` und `AsyncNinjaJWTSlidingController`.
Beachten Sie außerdem, dass dies nur mit Django-Versionen funktioniert, die asynchrone Operationen unterstützen.

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

Wie beim Standard-Controller müssen Sie auch den Controller registrieren, wie in [Erste Schritte](getting_started.md) gezeigt

#### Verwendung des Django-Ninja-Routers

Wenn Sie lieber Funktionen anstelle von Klassen verwenden möchten, ist auch das möglich. Hier ist ein Beispiel

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

Registrieren Sie den `router` wie folgt an der `api` von django-ninja:

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

Wenn Sie Token-Claims anpassen möchten, können Sie dies tun, indem Sie Unterklassen von `TokenObtainPairInputSchema` und `TokenObtainPairController` erstellen. Siehe [Controller-Schema-Austausch](#controller-schema-swapping)

Zusätzlich ist wichtig zu wissen, dass `NinjaExtra` einen Handler für die Klasse `APIException` registriert, der in `NinjaAPI`-Instanzen nicht verfügbar ist.
Um dies zu umgehen, benötigen Sie den folgenden zusätzlichen Code:

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

### Controller-Schema-Austausch

Sie können jetzt Controller-Schemas in den `NINJA_JWT`-Einstellungen austauschen, ohne die Funktionalität der Ninja-JWT-Controller zu erben oder zu überschreiben.

Alle Controller-Eingabeschemas müssen von `ninja_jwt.schema.InputSchemaMixin` erben, und Schemas, die Token generieren, sollten von
 `ninja_jwt.schema.TokenObtainInputSchemaBase` oder `ninja_jwt.schema.TokenInputSchemaMixin` erben, wenn Sie mehr Kontrolle wünschen.

Verwendung des obigen Beispiels:

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

In `MyTokenObtainPairInputSchema` überschreiben wir die Methode `get_token`, um unser Token sowie einige Daten zu definieren, die vom Ausgabeschema benötigt werden.
Außerdem überschreiben wir die Methode `get_response_schema`, um unser Ausgabeschema `MyTokenObtainPairOutSchema` zu definieren.

Als Nächstes wenden wir das Schema `MyTokenObtainPairInputSchema` auf den Controller an. Dies kann einfach in den `NINJA_JWT`-Einstellungen erfolgen.

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
Weitere austauschbare Schemas können wie folgt gesetzt werden
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
   `Controller Schema Swapping` ist nur in **v5.2.4** und höher verfügbar

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Token manuell erstellen](creating_tokens_manually.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
