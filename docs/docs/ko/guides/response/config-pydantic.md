---
comments: true
---
# Pydantic 설정 오버라이드

**Django Ninja `Schema`**에는 스키마의
[Pydantic `Config` 클래스](https://pydantic.com.cn/usage/model_config/)를 통해 사용할 수 있는 다양한 커스터마이즈 설정이 있습니다.

!!! note
    내부적으로 **Django Ninja**는 [Pydantic Models](https://pydantic.com.cn/usage/models/)와
    그 모든 기능과 이점을 사용합니다. Django models를 코드에서 다룰 때 혼란을 피하기 위해 `Schema`라는 별칭이 선택되었습니다.
    Pydantic의 model 클래스는 기본적으로 "Model"이라고 불리며, 이는 Django의 "Model" 클래스와 충돌하기 때문입니다.

## CamelCase Schema 예제

흥미로운 `Config` 속성으로는 [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator)가 있습니다.
**Django Ninja**에서 Pydantic을 사용하는 예제는 다음과 같을 수 있습니다:

```python hl_lines="12 13"
from ninja import Schema


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class CamelModelSchema(Schema):
    str_field_name: str
    float_field_name: float

    class Config(Schema.Config):
        alias_generator = to_camel
```

!!! note
    스키마의 `Config`를 오버라이드할 때는 기본 `Config` 클래스를 상속해야 합니다.

필드 이름의 출력(camelCase 등)을 수정하려는 경우 - `populate_by_name`과 `by_alias`도 함께 설정해야 한다는 점을 기억하세요

```python hl_lines="6 9"
class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "email"]
        alias_generator = to_camel
        populate_by_name = True  # !!!!!! <--------


@api.get("/users", response=list[UserSchema], by_alias=True) # !!!!!! <-------- by_alias
def get_users(request):
    return User.objects.all()

```

결과:

```JSON
[
  {
    "Id": 1,
    "Email": "tim@apple.com"
  },
  {
    "Id": 2,
    "Email": "sarah@smith.com"
  }
  ...
]

```

## Django Models에서 커스텀 설정 가져오기

[`create_schema`](django-pydantic-create-schema.md#create_schema)를 사용할 때, 생성된
스키마를 사용하여 커스텀 설정이 적용된 다른 클래스를 만들 수 있습니다. 예를 들면:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    다음 챕터로 계속 진행하세요! **[페이지네이션](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
