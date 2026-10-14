`NinjaJWTDefaultController`와 `NinjaJWTSlidingController` 뷰에서 생성되는 웹 토큰에 포함된 클레임을 커스터마이즈하고 싶다면, 원하는 컨트롤러에 대한 서브클래스와 그에 상응하는 시리얼라이저를 생성합니다. 다음은 예제입니다:

!!! info
비동기 버전의 클래스에 관심이 있다면 `AsyncNinjaJWTDefaultController`와 `AsyncNinjaJWTSlidingController`를 사용하세요.
또한 비동기 작업을 지원하는 Django 버전에서만 작동한다는 점에 유의하세요.

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

표준 컨트롤러와 마찬가지로, [시작하기](getting_started.md)에서 보여준 것처럼 컨트롤러를 등록해야 합니다

#### Django Ninja Router 사용하기

클래스가 아닌 함수를 사용하는 것에 관심이 있다면, 그것도 가능합니다. 다음은 예제입니다

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

다음과 같이 `router`를 django-ninja의 `api`에 등록합니다:

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

토큰 클레임을 커스터마이즈하는 데 관심이 있다면, `TokenObtainPairInputSchema`와 `TokenObtainPairController`의 서브클래스를 만들어 수행할 수 있습니다. [컨트롤러 스키마 교체](#controller-schema-swapping)를 참고하세요

또한 `NinjaExtra`는 `NinjaAPI` 인스턴스에는 없는 `APIException` 클래스에 대한 핸들러를 등록한다는 점에 유의하는 것이 중요합니다.
이를 해결하려면 다음과 같은 추가 코드가 필요합니다:

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

### 컨트롤러 스키마 교체

이제 Ninja JWT 컨트롤러 기능을 상속하거나 오버라이드하지 않고도 `NINJA_JWT` 설정에서 컨트롤러 스키마를 교체할 수 있습니다.

모든 컨트롤러 입력 스키마는 `ninja_jwt.schema.InputSchemaMixin`을 상속해야 하며, 토큰을 생성하는 스키마는 더 많은 제어가 필요한 경우
 `ninja_jwt.schema.TokenObtainInputSchemaBase` 또는 `ninja_jwt.schema.TokenInputSchemaMixin`을 상속해야 합니다.

위의 예제를 사용하여:

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

`MyTokenObtainPairInputSchema`에서 우리는 `get_token` 메서드를 오버라이드하여 토큰과 출력 스키마에 필요한 일부 데이터를 정의합니다.
또한 `get_response_schema` 메서드를 오버라이드하여 출력 스키마인 `MyTokenObtainPairOutSchema`를 정의합니다.

다음으로 `MyTokenObtainPairInputSchema` 스키마를 컨트롤러에 적용합니다. 이는 `NINJA_JWT` 설정에서 간단히 수행할 수 있습니다.

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
다른 교체 가능한 스키마는 다음과 같이 설정할 수 있습니다
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
   `Controller Schema Swapping`은 **v5.2.4** 이상에서만 사용할 수 있습니다

!!! success

    다음 장 **[토큰 수동 생성](creating_tokens_manually.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
