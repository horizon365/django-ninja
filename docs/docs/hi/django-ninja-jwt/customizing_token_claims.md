यदि आप `NinjaJWTDefaultController` और `NinjaJWTSlidingController`
views द्वारा बनाए गए web tokens में शामिल claims को customize करना चाहते हैं, तो वांछित controller के लिए उसके संबंधित serializer के साथ एक subclass बनाएं। यहाँ एक उदाहरण है:

!!! info
यदि आप class के asynchronous version में रुचि रखते हैं, तो `AsyncNinjaJWTDefaultController` और `AsyncNinjaJWTSlidingController` का उपयोग करें।
साथ ही ध्यान दें कि यह केवल उन Django versions के साथ काम करता है जो asynchronous operations का समर्थन करते हैं।

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

Standard controller की तरह, आपको [Getting Started](getting_started.md) में दिखाए अनुसार controller को register करने की भी आवश्यकता है

#### Django Ninja Router का उपयोग करना

यदि आप classes के बजाय functions का उपयोग करने में रुचि रखते हैं, तो वह भी संभव है। यहाँ एक उदाहरण है

```python
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
```

`router` को django-ninja के `api` में इस प्रकार register करें:

```python
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/token', tags=['Auth'], router=obtain_pair_router)
...
```

यदि आप token claims को customize करने में रुचि रखते हैं, तो आप `TokenObtainPairInputSchema` और `TokenObtainPairController` के subclasses बनाकर ऐसा कर सकते हैं। देखें [Controller Schema Swapping](#controller-schema-swapping)

साथ ही, यह ध्यान रखना महत्वपूर्ण है कि `NinjaExtra`, `APIException` class के लिए एक handler register करता है जो `NinjaAPI` instances में उपलब्ध नहीं है।
इसके समाधान के लिए, आपको निम्नलिखित अतिरिक्त code की आवश्यकता है:

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

अब आप `NINJA_JWT` settings में controller schemas को swap कर सकते हैं, बिना Ninja JWT controller functionality को inherit या override किए।

सभी controller input schemas को `ninja_jwt.schema.InputSchemaMixin` से inherit होना चाहिए, और tokens बनाने वाले schemas को
 `ninja_jwt.schema.TokenObtainInputSchemaBase` या, यदि आप अधिक नियंत्रण चाहते हैं, तो `ninja_jwt.schema.TokenInputSchemaMixin` से inherit होना चाहिए।

ऊपर दिए गए उदाहरण का उपयोग करते हुए:

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

`MyTokenObtainPairInputSchema` में हम अपने token को परिभाषित करने के लिए `get_token` method को override करते हैं और साथ ही output schema के लिए आवश्यक कुछ data भी।
हम `get_response_schema` method को भी override करते हैं ताकि अपना output schema `MyTokenObtainPairOutSchema` परिभाषित कर सकें।

इसके बाद, हम `MyTokenObtainPairInputSchema` schema को controller पर लागू करते हैं। इसे बस `NINJA_JWT` settings में किया जा सकता है।

```python
# project/settings.py

NINJA_JWT = {
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'project.schema.MyTokenObtainPairInputSchema',
}
```
अन्य swappable schemas निम्नानुसार सेट किए जा सकते हैं
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
   `Controller Schema Swapping` केवल **v5.2.4** और उससे ऊपर में उपलब्ध है

!!! success

    अगले अध्याय **[Creating Tokens Manually](creating_tokens_manually.md)** पर जारी रखें।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
