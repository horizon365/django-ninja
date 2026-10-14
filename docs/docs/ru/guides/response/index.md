---
comments: true
---
# Схема ответа

**Django Ninja** позволяет определять схемы ответов для целей валидации и документирования.

Представьте, что вам нужно создать API-операцию, которая создаёт пользователя. **Входными** параметрами будут **username+password**, но **выводом** этой операции должны быть **id+username** (**без** пароля).

Создадим входную схему:

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

Теперь определим выходную схему и передадим её в качестве аргумента `response` декоратору `@api.post`:

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

**Django Ninja** будет использовать схему `response`, чтобы:

- Преобразовывать выходные данные в объявленную схему
- Проверять данные
- Добавлять определение схемы OpenAPI
- Она будет использоваться системой автоматической документации
- И, что самое важное, она будет **ограничивать выходные данные** только полями, определёнными в схеме.

## Вложенные объекты

Также часто требуется возвращать ответы с некоторыми вложенными/подобъектами.

Представьте, что у нас есть Django-модель `Task` с внешним ключом на `User`:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

Теперь выведем все задачи и для каждой задачи выведем некоторые поля о пользователе.

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

Если выполнить эту операцию, вы должны получить ответ следующего вида:

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

## Псевдонимы

Вместо использования вложенных ответов вы можете просто «выпрямить» вывод ответа.
Объект `Schema` в Ninja расширяет формат `Field(..., alias="")` из Pydantic для обработки точечных обращений.

Используя приведённую выше модель, создадим схему, которая включает только имя владельца задачи в строке, а также использует `completed` вместо `is_completed`:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

Псевдонимы также поддерживают доступ к переменным в синтаксисе шаблонов Django:

```python hl_lines="2"
class TaskSchema(Schema):
    last_message: str = Field(None, alias="message_set.0.text")
```

```python hl_lines="3"
class TaskSchema(Schema):
    type: str = Field(None)
    type_display: str = Field(None, alias="get_type_display") # callable will be executed
```

## Резолверы

Вы также можете создавать вычисляемые поля с помощью методов-резолверов на основе имён полей.

Метод должен принимать один аргумент — объект, который разрешает схема.

При создании резолвера как обычного метода `self` даёт вам доступ к другим проверенным и отформатированным атрибутам схемы.

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

### Доступ к дополнительному контексту

Pydantic v2 позволяет обрабатывать дополнительный контекст, передаваемый в сериализатор. В следующем примере вы можете иметь резолвер, который получает объект запроса из переданного аргумента `context`:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

Если вы используете эту схему для входящего запроса — объект запроса будет автоматически передан в контекст.

Вы также можете передать свой собственный контекст:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## Возврат queryset

В предыдущем примере мы специально преобразовали queryset в список (и выполнили SQL-запрос при вычислении).

Этого можно избежать и вернуть queryset в качестве результата, и он будет автоматически вычислен как список:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    Если ваша операция асинхронна, этот пример не сработает, потому что ORM-запросы должны вызываться безопасно.
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    Для получения дополнительной информации см. [Поддержка асинхронности](../async-support.md#using-orm) .

## Поля файлов и изображений

**Django Ninja** по умолчанию преобразует файлы и изображения (объявленные с помощью `FileField` или `ImageField`) в строковые (`string`) URL.

Пример:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

Если вам нужно вывести поле изображения в ответ, объявите для него схему следующим образом:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

Как только вы выведете это в ответ, для каждого объекта будет автоматически сгенерирован URL:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## Несколько схем ответа

Иногда нужно определить несколько схем ответа.

Например, в случае аутентификации вы можете возвращать:

- **200** успех -> токен
- **401** -> не авторизован
- **402** -> требуется оплата
- и т. д.

Фактически, [спецификация OpenAPI](https://swagger.io/docs/specification/describing-responses/) позволяет передавать несколько схем ответов.

Вы можете передать словарь в аргумент `response`, где:

- ключи — это коды ответов
- значения — схемы для каждого кода

Также при возврате результата вы должны передать код статуса, чтобы сообщить **Django Ninja**, какая схема должна использоваться для валидации и сериализации.

Пример:

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

## Несколько кодов ответа

В предыдущем примере вы видели, что мы фактически дважды повторили схему `Message`:

```
...401: Message, 402: Message}
```

Чтобы избежать этого дублирования, вы можете использовать несколько кодов ответа для одной схемы:

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

**Django Ninja** поставляется со следующими HTTP-кодами:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

Вы также можете создавать свои собственные диапазоны с помощью `frozenset`:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## Пустые ответы

Некоторые ответы, например [204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204), не имеют тела.
Чтобы указать, что тело ответа пустое, пометьте аргумент `response` как `None` вместо схемы:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## Ответы с ошибками

Для получения дополнительной информации см. [Обработка ошибок](../errors.md) .

## Самоссылочные схемы

- Иногда нужно создать схему, которая ссылается сама на себя или на древовидный объект.

- Для этого вам нужно:

- обернуть тип вашей схемы в кавычки

- использовать метод `update_forward_refs` для применения самоссылочного типа

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## Самоссылочные схемы, сгенерированные с помощью `create_schema()`

Чтобы иметь возможность использовать метод `update_forward_refs()` для схемы, сгенерированной через `create_schema()`,
«имя» класса должно быть в нашем пространстве имён. В этом случае важно передать аргумент `name` в `create_schema()`.

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

## Сериализация вне представления

Вы можете напрямую сериализовать ваши объекты в коде, используя метод `.from_orm()` объекта схемы.

Рассмотрим следующую модель:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

К ней можно получить доступ с помощью следующей схемы:
```python
class PersonSchema(Schema):
    name: str
```

Сериализация может быть выполнена напрямую с помощью метода `.from_orm()` на схеме.
Как только у вас есть экземпляр объекта схемы, методы `.dict()` и `.json()` позволяют получить вывод в виде словаря и строковой версии JSON.

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

Несколько записей: или queryset (или список)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## HTTP-ответы Django

Также возможно возвращать обычные HTTP-ответы Django:

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

    Переходите к следующей главе! **[Настройка ответа](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
