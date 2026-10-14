Если вы хотите настроить claims (утверждения), включаемые в веб-токены, генерируемые представлениями `NinjaJWTDefaultController` и `NinjaJWTSlidingController`,
создайте подкласс нужного контроллера вместе с соответствующим сериализатором. Вот пример:

!!! info
Если вас интересует асинхронная версия класса, используйте `AsyncNinjaJWTDefaultController` и `AsyncNinjaJWTSlidingController`.
Также обратите внимание, что это работает только с версиями Django, поддерживающими асинхронные операции.

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

Как и со стандартным контроллером, вам также нужно зарегистрировать контроллер, как показано в [Getting Started](getting_started.md)

#### Использование Django Ninja Router

Если вы хотите использовать функции, а не классы, это тоже возможно. Вот пример

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

Зарегистрируйте `router` в `api` django-ninja следующим образом:

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

Если вы хотите настроить claims токена, вы можете сделать это, создав подклассы `TokenObtainPairInputSchema` и `TokenObtainPairController`. См. [Подмена схем контроллера](#controller-schema-swapping)

Кроме того, важно отметить, что `NinjaExtra` регистрирует обработчик для класса `APIException`, который недоступен в экземплярах `NinjaAPI`.
Чтобы обойти это, вам нужен следующий дополнительный код:

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

### Подмена схем контроллера

Теперь вы можете подменять схемы контроллеров в настройках `NINJA_JWT` без наследования или переопределения функциональности контроллеров Ninja JWT.

Все входные схемы контроллеров должны наследоваться от `ninja_jwt.schema.InputSchemaMixin`, а схемы, генерирующие токены, должны наследоваться от
 `ninja_jwt.schema.TokenObtainInputSchemaBase` или `ninja_jwt.schema.TokenInputSchemaMixin`, если вам нужен больший контроль.

Используя приведённый выше пример:

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

В `MyTokenObtainPairInputSchema` мы переопределяем метод `get_token`, чтобы определить наш токен, а также некоторые данные, необходимые выходной схеме.
Мы также переопределяем метод `get_response_schema`, чтобы определить нашу выходную схему `MyTokenObtainPairOutSchema`.

Далее мы применяем схему `MyTokenObtainPairInputSchema` к контроллеру. Это можно сделать просто в настройках `NINJA_JWT`.

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
Другие подменяемые схемы можно задать следующим образом
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
   `Controller Schema Swapping` доступно только в **v5.2.4** и выше

!!! success

    Перейдите к следующей главе **[Создание токенов вручную](creating_tokens_manually.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
