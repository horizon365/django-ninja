---
comments: true
---
# Response Schema 响应模式

**Django Ninja** 允许你为验证和文档目的定义响应的模式。

想象一下，你需要创建一个创建用户的 API 操作。 **input** 参数将是 **username+password**, 但这个操作的 **输出** 应该是 **id+username** (**不包含** 密码).

让我们创建输入模式：

```python hl_lines="3 5"
from ninja import Schema

class UserIn(Schema):
    username: str
    password: str


@api.post("/users/")
def create_user(request, data: UserIn):
    user = User(username=data.username) # User 类来自 django auth.User
    user.set_password(data.password)
    user.save()
    # ... return ?
```

现在让我们定义输出模式，并将其作为 `response` 参数传递给 `@api.post` 装饰器:

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

**Django Ninja** 将使用 `response` 模式来:

- 将输出数据转换为声明的模式
- 验证数据
- 添加一个 OpenAPI 模式定义
- 它将被自动文档系统使用
- 并且，最重要的是，它将 **限制输出数据**  为仅在模式中定义的字段。

## 嵌套对象

也经常有需要返回带有一些嵌套/子对象的响应。

想象我们有一个带有 `User` 外键的 `Task` Django 模型:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

现在让我们输出所有任务，并为每个任务输出一些关于用户的字段。

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
    owner: UserSchema = None  # ! None - 标记使它非必填


@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    queryset = Task.objects.select_related("owner")
    return list(queryset)
```

如果你执行这个操作，你应该得到这样的响应：

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

## 别名

与其使用嵌套响应，您可能希望仅展平响应输出。
Ninja 的 `Schema` 对象扩展了 Pydantic 的 `Field(..., alias="")` 格式，以处理带点的响应。

使用上面的模型，让我们创建一个模式，该模式仅内联包含任务所有者的名字，并且还使用 `completed` 而不是 `is_completed`:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # 第一个 Field 参数是默认值，对于必填字段使用...。
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

别名也支持 Django 模板语法变量访问：

```python hl_lines="2"
class TaskSchema(Schema):
    last_message: str = Field(None, alias="message_set.0.text")
```

```python hl_lines="3"
class TaskSchema(Schema):
    type: str = Field(None)
    type_display: str = Field(None, alias="get_type_display") # callable 将要被执行
```

## 解析器

您还可以通过基于字段名称的解析方法创建计算字段。

该方法必须接受一个参数，该参数将是模式要解析的对象。

当将解析器创建为标准方法时，`self` 使您能够访问模式中的其他经过验证和格式化的属性。

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

### 访问额外上下文

Pydantic v2 允许您处理传递给序列化器的额外上下文。在以下示例中，您可以有一个解析器，该解析器从传递的 `context` 参数中获取请求对象：
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

如果您将此模式用于传入请求 - 请求对象将自动传递到上下文。

您也可以传递自己的上下文：

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## 返回查询集

在上一个示例中，我们专门将查询集转换为列表（并在评估期间执行 SQL 查询）。

您可以避免这种情况并返回查询集作为结果，它将自动评估为列表：

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! 警告

    如果您的操作是异步的，此示例将不起作用，因为 ORM 查询需要安全地调用。
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    有关更多信息，请参阅 [异步支持](../async-support.md#using-orm) 。

## 文件字段和图像字段

**Django Ninja** 默认将文件和图像 (使用 `FileField` 或 `ImageField`声明) 转换成 `字符串`  URL.

一个例子：

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

如果您需要将图像字段输出到响应中，为其声明一个模式如下：

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

一旦您将此输出到响应中，将为每个对象自动生成 URL：

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## 多个响应模式

有时您需要定义多个响应模式。

例如，在身份验证的情况下，您可以返回：

- **200** successful -> token
- **401** -> Unauthorized
- **402** -> Payment required
- 等等..

实际上， [OpenAPI 规范](https://swagger.io/docs/specification/describing-responses/) 允许您传递多个响应模式。

您可以将一个字典传递给 `response` 参数，其中:

- 键是响应码
- 值是该代码的 schema 模式

此外，当您返回结果时 - 您还必须传递一个状态代码以告诉 **Django Ninja** 应该使用哪个模式进行验证和序列化。

一个示例:

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

## 多种响应代码

在前面的示例中，你看到我们基本上将 `Message` 模式重复了两次：

```
...401: Message, 402: Message}
```

为避免这种重复，你可以对一个模式使用多种响应代码：

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

**Django Ninja** 带有以下 HTTP 代码：

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

你也可以使用 `frozenset` 创建自己的范围:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## 空响应

有些响应，如 [204 无内容](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204)，没有主体。
要表示响应主体为空，用 `None` 而不是 Schema 模式来标记 `response` 参数 :

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## 错误响应

有关更多信息，请查看 [处理错误](../errors.md) 。

## Self-referencing schemes

- 有时你需要创建一个模式，该模式引用自身或树状结构对象。

- 要做到这一点，你需要：

- 将你的模式类型用引号括起来

- 使用 `update_forward_refs` 方法应用自引用类型

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! 注意这里的类型需要放在引号中！！ !!


Organization.update_forward_refs()  # !!! 这一行很重要


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## 从 `create_schema()` 生成的自引用模式

为了能够使用通过 `create_schema()` 生成的模式的 `update_forward_refs()` 方法 ,
类的 "name" 需要在我们的命名空间中。 在这种情况下，将 `name` 参数传递给 `create_schema()` 非常重要。

```python hl_lines="3"
UserSchema = create_schema(
    User,
    name='UserSchema',  # !!! 这对 update_forward_refs() 很重要
    fields=['id', 'username']
    custom_fields=[
        ('manager', 'UserSchema', None),
    ]
)
UserSchema.update_forward_refs()
```

## 在视图之外进行序列化

可以通过在模式对象上使用 `.from_orm()` 方法直接在代码中对你的对象进行序列化。

考虑以下模型：

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

可以使用以下模式进行访问：
```python
class PersonSchema(Schema):
    name: str
```

可以使用模式上的 `.from_orm()` 方法直接进行序列化。
一旦你有了模式对象的实例， `.dict()` 和 `.json()` 方法允许你获得字典输出和字符串 JSON 版本。

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

多个条目：或查询集（或列表）

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django HTTP 响应

也可以返回常规的 django http 响应:

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
