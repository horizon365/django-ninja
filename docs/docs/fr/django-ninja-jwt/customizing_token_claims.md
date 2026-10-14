Si vous souhaitez personnaliser les claims inclus dans les web tokens générés par les vues `NinjaJWTDefaultController` et `NinjaJWTSlidingController`,
créez une sous-classe pour le contrôleur souhaité ainsi que son serializer correspondant. Voici un exemple :

!!! info
Si la version asynchrone de la classe vous intéresse, utilisez `AsyncNinjaJWTDefaultController` et `AsyncNinjaJWTSlidingController`.
Notez également que cela ne fonctionne qu'avec les versions de Django prenant en charge les opérations asynchrones.

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

Comme pour le contrôleur standard, vous devez également enregistrer le contrôleur comme indiqué dans [Premiers pas](getting_started.md)

#### Utilisation du routeur Django Ninja

Si vous souhaitez utiliser des fonctions plutôt que des classes, c'est également possible. Voici un exemple

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

Enregistrez le `router` dans l'`api` de django-ninja comme ceci :

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

Si vous souhaitez personnaliser les claims des tokens, vous pouvez le faire en créant des sous-classes de `TokenObtainPairInputSchema` et `TokenObtainPairController`. Voir [Échange de schémas de contrôleur](#controller-schema-swapping)

De plus, il est important de noter que `NinjaExtra` enregistre un handler pour la classe `APIException` qui n'est pas disponible dans les instances `NinjaAPI`.
Pour contourner ce problème, vous avez besoin du code supplémentaire suivant :

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

### Échange de schémas de contrôleur

Vous pouvez désormais échanger les schémas des contrôleurs dans les paramètres `NINJA_JWT` sans hériter ni redéfinir les fonctionnalités des contrôleurs de Ninja JWT.

Tous les schémas d'entrée des contrôleurs doivent hériter de `ninja_jwt.schema.InputSchemaMixin`, et les schémas qui génèrent des tokens doivent hériter de
 `ninja_jwt.schema.TokenObtainInputSchemaBase` ou `ninja_jwt.schema.TokenInputSchemaMixin` si vous souhaitez plus de contrôle.

En utilisant l'exemple ci-dessus :

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

Dans `MyTokenObtainPairInputSchema`, nous redéfinissons la méthode `get_token` pour définir notre token ainsi que certaines données nécessaires au schéma de sortie.
Nous redéfinissons également la méthode `get_response_schema` pour définir notre schéma de sortie `MyTokenObtainPairOutSchema`.

Ensuite, nous appliquons le schéma `MyTokenObtainPairInputSchema` au contrôleur. Cela peut être fait simplement dans les paramètres `NINJA_JWT`.

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
Les autres schémas échangeables peuvent être définis comme suit
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
   `Controller Schema Swapping` n'est disponible qu'à partir de la version **v5.2.4**

!!! success

    Poursuivez avec le chapitre suivant **[Créer des tokens manuellement](creating_tokens_manually.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
