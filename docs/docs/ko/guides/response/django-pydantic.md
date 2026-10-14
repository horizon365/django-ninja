---
comments: true
---
# Django Models로부터 Schema 생성하기


Schema는 검증 규칙과 응답을 정의하는 데 매우 유용하지만, 때로는 데이터베이스 모델을 스키마에 반영하고 변경 사항을 동기화 상태로 유지해야 합니다.
## ModelSchema

`ModelSchema`는 여러분의 모델로부터 스키마를 자동으로 생성할 수 있는 특별한 기본 클래스입니다.

필요한 작업은 스키마의 `Meta`에 `model`과 `fields`를 설정하는 것뿐입니다:


```python hl_lines="2 5 6 7"
from django.contrib.auth.models import User
from ninja import ModelSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
```

### 모든 Model 필드 사용

모델의 모든 필드를 사용하려면 - `fields`에 `__all__`을 전달하면 됩니다:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    __all__ 사용은 권장되지 않습니다.
    <br>
    원치 않는 데이터(위 예제의 해시된 비밀번호 같은)가 의도치 않게 노출되는 결과를 초래할 수 있습니다.
    <br>
    일반적인 권장 사항 - API에서 보이길 원하는 필드 목록을 `fields`로 명시적으로 정의하세요.

### Model 필드 제외

일부 필드를 **제외한** 모든 필드를 사용하려면 `exclude` 설정을 사용할 수 있습니다:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'user_permissions']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     email: str
#     is_superuser: bool
#     ... and the rest

```

### 필드 오버라이드

일부 필드의 기본 어노테이션을 변경하거나 새 필드를 추가하려면, 평소처럼 어노테이션이 지정된 속성을 사용하기만 하면 됩니다.
```python hl_lines="1 2 3 4 8"
class GroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSchema(ModelSchema):
    groups: List[GroupSchema] = []

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

```


### 필드를 선택적으로 만들기

PATCH API operation의 경우 일반적으로 스키마의 모든 필드를 선택적으로 만들어야 합니다. 이를 위해서는 fields_optional 설정을 사용할 수 있습니다

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

모든 필드 대신 일부 필드만 선택적으로 정의할 수도 있습니다:
```python
     fields_optional = ['description']
```

!!! done

    다음 챕터로 계속 진행하세요! **[동적으로 Schema 생성하기](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
