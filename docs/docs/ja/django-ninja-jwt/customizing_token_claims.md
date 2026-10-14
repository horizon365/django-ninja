`NinjaJWTDefaultController` と `NinjaJWTSlidingController` のビューから生成される Web トークンに含まれるクレームをカスタマイズしたい場合は、
対象のコントローラと、それに対応するシリアライザのサブクラスを作成します。以下はその例です：

!!! info
非同期バージョンのクラスに興味がある場合は、`AsyncNinjaJWTDefaultController` と `AsyncNinjaJWTSlidingController` を使用してください。
なお、これは非同期操作をサポートする Django バージョンでのみ動作することに注意してください。

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

標準のコントローラと同様に、[はじめに](getting_started.md) で示したようにコントローラを登録する必要があります

#### Django Ninja Router の使用

クラスではなく関数を使いたい場合も可能です。以下はその例です

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

`router` を django-ninja の `api` に次のように登録します：

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

トークンクレームをカスタマイズしたい場合は、`TokenObtainPairInputSchema` と `TokenObtainPairController` のサブクラスを作成することで行えます。[コントローラスキーマのスワップ](#controller-schema-swapping) を参照してください

さらに、`NinjaExtra` は `NinjaAPI` インスタンスには存在しない `APIException` クラス用のハンドラを登録している点に注意することが重要です。
これに対処するには、次の追加コードが必要です：

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

### コントローラスキーマのスワップ

Ninja JWT のコントローラ機能を継承したりオーバーライドしたりすることなく、`NINJA_JWT` 設定でコントローラのスキーマをスワップできるようになりました。

すべてのコントローラ入力スキーマは `ninja_jwt.schema.InputSchemaMixin` を継承する必要があり、トークンを生成するスキーマは、
より細かい制御をしたい場合は `ninja_jwt.schema.TokenObtainInputSchemaBase` または `ninja_jwt.schema.TokenInputSchemaMixin` を継承する必要があります。

上の例を使うと：

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

`MyTokenObtainPairInputSchema` では、`get_token` メソッドをオーバーライドしてトークンと、出力スキーマが必要とするいくつかのデータを定義しています。
また、`get_response_schema` メソッドをオーバーライドして、出力スキーマ `MyTokenObtainPairOutSchema` を定義しています。

次に、`MyTokenObtainPairInputSchema` スキーマをコントローラに適用します。これは `NINJA_JWT` 設定で簡単に行えます。

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
その他のスワップ可能なスキーマは次のように設定できます
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
   `Controller Schema Swapping` は **v5.2.4** 以上でのみ利用可能です

!!! success

    次の章 **[トークンの手動作成](creating_tokens_manually.md)** に進みましょう。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
