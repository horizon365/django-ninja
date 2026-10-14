---
comments: true
---
# Response Schema

**Django Ninja**는 검증과 문서화 목적으로 response 스키마를 정의할 수 있게 해줍니다.

사용자를 생성하는 API operation을 만들어야 한다고 상상해 보세요. **입력** 파라미터는 **username+password**이지만, 이 operation의 **출력**은 **id+username**이어야 합니다(**비밀번호 제외**).

입력 스키마를 만들어 보겠습니다:

```python hl_lines="3 5"
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str


@api.post("/users/")
def create_user(request, data: UserIn):
    user = User(username=data.username) # User class comes from django auth.User
    user.set_password(data.password)
    user.save()
    # ... return ?
```

이제 출력 스키마를 정의하고 `@api.post` 데코레이터에 `response` 인자로 전달해 보겠습니다:

```python hl_lines="8 9 10 13 18"
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str


class UserOut(Schema):
    id: int
    username: str


@api.post("/users/", response=UserOut)
def create_user(request, data: UserIn):
    user = User(username=data.username)
    user.set_password(data.password)
    user.save()
    return user
```

**Django Ninja**는 `response` 스키마를 다음 목적으로 사용합니다:

- 출력 데이터를 선언된 스키마로 변환
- 데이터 검증
- OpenAPI 스키마 정의 추가
- 자동 문서화 시스템에서 사용
- 그리고 가장 중요하게, **출력 데이터를** 스키마에 정의된 필드로만 **제한**합니다.

## 중첩 객체

중첩/하위 객체가 포함된 응답을 반환해야 하는 경우도 흔합니다.

`User` foreign key를 가진 `Task` Django model이 있다고 상상해 보세요:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

이제 모든 task를 출력하고, 각 task에 대해 사용자에 관한 일부 필드를 출력해 보겠습니다.

```python hl_lines="13 16"
from typing import List
from ninja import Schema

class UserSchema(Schema):
    id: int
    first_name: str
    last_name: str

class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: UserSchema = None  # ! None - the marker makes it non-required


@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    queryset = Task.objects.select_related("owner")
    return list(queryset)
```

이 operation을 실행하면 다음과 같은 응답을 얻을 수 있습니다:

```JSON hl_lines="6 7 8 9 16"
[
    {
        "id": 1,
        "title": "Task 1",
        "is_completed": false,
        "owner": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
        }
    },
    {
        "id": 2,
        "title": "Task 2",
        "is_completed": false,
        "owner": null
    },
]
```

## 별칭(Aliases)

중첩 응답을 사용하는 대신, 응답 출력을 단순히 평탄화(flatten)하고 싶을 수 있습니다.
Ninja의 `Schema` 객체는 Pydantic의 `Field(..., alias="")` 형식을 확장하여 점(dotted) 응답을 처리합니다.

위 모델을 사용하여 task 소유자의 first name만 인라인으로 포함하고, `is_completed` 대신 `completed`를 사용하는 스키마를 만들어 보겠습니다:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

별칭은 Django 템플릿 문법의 변수 접근도 지원합니다:

```python hl_lines="2"
class TaskSchema(Schema):
    last_message: str = Field(None, alias="message_set.0.text")
```

```python hl_lines="3"
class TaskSchema(Schema):
    type: str = Field(None)
    type_display: str = Field(None, alias="get_type_display") # callable will be executed
```

## Resolver

필드 이름을 기반으로 하는 resolver 메서드를 통해 계산된(computed) 필드를 만들 수도 있습니다.

이 메서드는 하나의 인자를 받아야 하며, 이 인자는 스키마가 해석 중인 객체입니다.

resolver를 표준 메서드로 만들면 `self`를 통해 스키마의 다른 검증되고 포맷팅된 속성에 접근할 수 있습니다.

```python hl_lines="5 7-11"
class TaskSchema(Schema):
    id: int
    title: str
    is_completed: bool
    owner: Optional[str] = None
    lower_title: str

    @staticmethod
    def resolve_owner(obj):
        if not obj.owner:
            return
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def resolve_lower_title(self, obj):
        return self.title.lower()
```

### 추가 컨텍스트 접근

Pydantic v2는 serializer에 전달된 추가 컨텍스트를 처리할 수 있게 해줍니다. 다음 예제에서는 전달된 `context` 인자에서 request 객체를 가져오는 resolver를 만들 수 있습니다:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

들어오는 요청에 이 스키마를 사용하면 - request 객체가 자동으로 컨텍스트에 전달됩니다.

자신만의 컨텍스트를 전달할 수도 있습니다:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## Queryset 반환하기

이전 예제에서는 queryset을 의도적으로 리스트로 변환했습니다(평가 과정에서 SQL 쿼리가 실행됩니다).

이를 피하고 queryset을 결과로 반환할 수 있으며, 자동으로 리스트로 평가됩니다:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    operation이 비동기인 경우 이 예제는 동작하지 않습니다. ORM 쿼리는 안전하게 호출되어야 하기 때문입니다.
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    자세한 내용은 [비동기 지원](../async-support.md#using-orm)을 참조하세요.

## File 필드와 Image 필드

**Django Ninja**는 파일과 이미지(`FileField` 또는 `ImageField`로 선언됨)를 기본적으로 `string` URL로 변환합니다.

예제:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

image 필드를 응답으로 출력해야 하는 경우, 다음과 같이 스키마를 선언하세요:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

이를 응답으로 출력하면 각 객체에 대해 URL이 자동으로 생성됩니다:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## 다중 Response 스키마

때로는 여러 개의 response 스키마를 정의해야 하는 경우가 있습니다.

예를 들어, 인증의 경우 다음을 반환할 수 있습니다:

- **200** 성공 -> token
- **401** -> Unauthorized
- **402** -> Payment required
- etc.

실제로 [OpenAPI 스펙](https://swagger.io/docs/specification/describing-responses/)은 여러 response 스키마를 전달하는 것을 허용합니다.

`response` 인자에 딕셔너리를 전달할 수 있으며, 여기서:

- 키는 response 코드입니다
- 값은 각 코드에 대한 스키마입니다

또한 결과를 반환할 때 - 어떤 스키마가 검증과 직렬화에 사용되어야 하는지 **Django Ninja**에 알려주기 위해 상태 코드도 함께 전달해야 합니다.

예제:

```python hl_lines="9 12 14 16"
class Token(Schema):
    token: str
    expires: date

class Message(Schema):
    message: str


@api.post('/login', response={200: Token, 401: Message, 402: Message})
def login(request, payload: Auth):
    if auth_not_valid:
        return 401, {'message': 'Unauthorized'}
    if negative_balance:
        return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page.'}
    return 200, {'token': xxx, ...}
```

## 다중 Response 코드

이전 예제에서 `Message` 스키마가 사실상 두 번 반복되는 것을 보았습니다:

```
...401: Message, 402: Message}
```

이런 중복을 피하려면 단일 스키마에 여러 response 코드를 사용할 수 있습니다:

```python hl_lines="2 5 8 10"
...
from ninja.responses import codes_4xx


@api.post('/login', response={200: Token, codes_4xx: Message})
def login(request, payload: Auth):
    if auth_not_valid:
        return 401, {'message': 'Unauthorized'}
    if negative_balance:
        return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page.'}
    return 200, {'token': xxx, ...}
```

**Django Ninja**는 다음 HTTP 코드들을 제공합니다:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

`frozenset`을 사용하여 자신만의 범위를 만들 수도 있습니다:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## 빈 응답

[204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204) 같은 일부 응답은 body가 없습니다.
응답 body가 비어 있음을 나타내려면, 스키마 대신 `response` 인자를 `None`으로 마킹하세요:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## 에러 응답

자세한 내용은 [에러 처리](../errors.md)를 확인하세요.

## 자기 참조 스키마

- 때로는 자기 자신을 참조하는 스키마나 트리 형태의 구조 객체를 만들어야 하는 경우가 있습니다.

- 이를 위해 다음을 수행해야 합니다:

- 스키마 타입을 따옴표로 감쌉니다

- `update_forward_refs` 메서드를 사용하여 자기 참조 타입을 적용합니다

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## `create_schema()`로 생성된 자기 참조 스키마

`create_schema()`를 통해 생성된 스키마의 `update_forward_refs()` 메서드를 사용하려면,
클래스의 "name"이 네임스페이스에 존재해야 합니다. 이 경우 `create_schema()`에 `name` 인자를 전달하는 것이 중요합니다.

```python hl_lines="3"
UserSchema = create_schema(
    User,
    name='UserSchema',  # !!! this is important for update_forward_refs()
    fields=['id', 'username']
    custom_fields=[
        ('manager', 'UserSchema', None),
    ]
)
UserSchema.update_forward_refs()
```

## 뷰 외부에서 직렬화하기

스키마 객체의 `.from_orm()` 메서드를 사용하여 코드에서 객체를 직접 직렬화할 수 있습니다.

다음 모델을 살펴보세요:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

다음 스키마를 사용하여 접근할 수 있습니다:
```python
class PersonSchema(Schema):
    name: str
```

직렬화는 스키마의 `.from_orm()` 메서드를 사용하여 직접 수행할 수 있습니다.
스키마 객체의 인스턴스를 얻으면, `.dict()`와 `.json()` 메서드로 딕셔너리 출력과 문자열 JSON 버전을 얻을 수 있습니다.

```python
>>> person = Person.objects.get(id=1)
>>> data = PersonSchema.from_orm(person)
>>> data
PersonSchema(id=1, name='Mr. Smith')
>>> data.dict()
{'id':1, 'name':'Mr. Smith'}
>>> data.json()
'{"id":1, "name":"Mr. Smith"}'
```

여러 엔트리: 또는 queryset(또는 리스트)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django HTTP 응답

일반 Django HTTP 응답을 반환하는 것도 가능합니다:

```python
from django.http import HttpResponse
from django.shortcuts import redirect


@api.get("/http")
def result_django(request):
    return HttpResponse('some data')   # !!!!


@api.get("/something")
def some_redirect(request):
    return redirect("/some-path")  # !!!!
```

!!! done

    다음 챕터로 계속 진행하세요! **[응답 조정하기](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
