---
comments: true
---
# 동적으로 Schema 생성하기

내부적으로 [`ModelSchema`](django-pydantic.md#modelschema)는 `create_schema` 함수를 사용합니다.
이는 더 고급스러운(그리고 덜 안전한) 접근 방식입니다 - 신중하게 사용하세요.

## `create_schema`

**Django Ninja**는 헬퍼 함수 `create_schema`를 제공합니다:

```python
def create_schema(
    model, # django model
    name = "", # name for the generated class, if empty model names is used
    depth = 0, # if > 0 schema will also be created for the nested ForeignKeys and Many2Many (with the provided depth of lookup)
    fields: list[str] = None, # if passed - ONLY these fields will added to schema
    exclude: list[str] = None, # if passed - these fields will be excluded from schema
    optional_fields: list[str] | str = None, # if passed - these fields will not be required on schema (use '__all__' to mark ALL fields required)
    custom_fields: list[tuple(str, Any, Any)] = None, # if passed - this will override default field types (or add new fields)
)
```


이 예제를 살펴보세요:

```python hl_lines="2 4"
from django.contrib.auth.models import User
from ninja.orm import create_schema

UserSchema = create_schema(User)

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     password: str
#     last_login: datetime
#     is_superuser: bool
#     email: str
#     ... and the rest

```

!!! warning
    기본적으로 `create_schema`는 모든 model 필드를 사용해 스키마를 구성합니다.
    이는 원치 않는 데이터(위 예제의 해시된 비밀번호 같은)가 의도치 않게 노출되는 결과를 초래할 수 있습니다.
    <br>
    속성 목록을 명시적으로 정의하려면 **반드시** `fields` 또는 `exclude` 인자를 사용하세요.

### `fields` 사용

```python hl_lines="1"
UserSchema = create_schema(User, fields=['id', 'username'])

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str

```

### `exclude` 사용

```python hl_lines="1 2"
UserSchema = create_schema(User, exclude=[
    'password', 'last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions']
)

# Will create schema without excluded fields:
# 
# class UserSchema(Schema):
#    id: int
#    username: str
#    first_name: str
#    last_name: str
#    email: str
#    is_active: bool
#    date_joined: datetime
```

### `depth` 사용

`depth` 인자를 사용하면 Django model의 관련 필드(foreign key, one-to-one, many-to-many)를 인트로스펙션할 수 있습니다.

```python hl_lines="1 7"
UserSchema = create_schema(User, depth=1, fields=['username', 'groups'])

# Will create the following schema:
#
# class UserSchema(Schema):
#    username: str
#    groups: List[Group]
```

여기서 groups는 `List[Group]`이 됩니다 - many-to-many 필드가 1 레벨 깊이로 인트로스펙션되어 groups에 대한 스키마도 생성되었습니다:

```python
class Group(Schema):
    id: int
    name: str
    permissions: List[int]
```

!!! done

    다음 챕터로 계속 진행하세요! **[Pydantic 설정 오버라이드](config-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
