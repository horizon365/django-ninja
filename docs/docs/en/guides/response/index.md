---
comments: true
---
# Response Schema

**Django Ninja** allows you to define response schemas for validation and documentation purposes.

Imagine you need to create an API operation that creates a user. The **input** parameters will be **username+password**, but the **output** of this operation should be **id+username** (**without** the password).

Let's create the input schema:

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

Now let's define the output schema and pass it as the `response` argument to the `@api.post` decorator:

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

**Django Ninja** will use the `response` schema to:

- Convert the output data to the declared schema
- Validate the data
- Add an OpenAPI schema definition
- It will be used by the automatic documentation system
- And, most importantly, it will **limit the output data** to only the fields defined in the schema.

## Nested Objects

It is also common to need to return responses with some nested/sub-objects.

Imagine we have a `Task` Django model with a `User` foreign key:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

Now let's output all tasks and, for each task, output some fields about the user.

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

If you execute this operation, you should get a response like this:

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

## Aliases

Instead of using nested responses, you may want to simply flatten the response output.
Ninja's `Schema` object extends Pydantic's `Field(..., alias="")` format to handle dotted responses.

Using the above model, let's create a schema that only includes the task owner's first name inline, and also uses `completed` instead of `is_completed`:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

Aliases also support Django template syntax variable access:

```python hl_lines="2"
class TaskSchema(Schema):
    last_message: str = Field(None, alias="message_set.0.text")
```

```python hl_lines="3"
class TaskSchema(Schema):
    type: str = Field(None)
    type_display: str = Field(None, alias="get_type_display") # callable will be executed
```

## Resolvers

You can also create computed fields via resolver methods based on field names.

The method must accept one argument, which will be the object the schema is resolving.

When creating the resolver as a standard method, `self` gives you access to other validated and formatted attributes in the schema.

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

### Accessing Extra Context

Pydantic v2 allows you to handle extra context passed to the serializer. In the following example, you can have a resolver that gets the request object from the passed `context` argument:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

If you use this schema for an incoming request — the request object will be automatically passed to the context.

You can also pass your own context:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## Returning a Queryset

In the previous example, we specifically converted the queryset to a list (and executed the SQL query during evaluation).

You can avoid this and return the queryset as the result, and it will be automatically evaluated as a list:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    If your operation is asynchronous, this example will not work, because ORM queries need to be called safely.
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    For more information, see [Async Support](../async-support.md#using-orm) .

## File Fields and Image Fields

**Django Ninja** turns files and images (declared using `FileField` or `ImageField`) into `string` URLs by default.

An example:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

If you need to output the image field to the response, declare a schema for it like this:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

Once you output this to the response, a URL will be automatically generated for each object:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## Multiple Response Schemas

Sometimes you need to define multiple response schemas.

For example, in the case of authentication, you might return:

- **200** successful -> token
- **401** -> Unauthorized
- **402** -> Payment required
- etc.

In fact, the [OpenAPI specification](https://swagger.io/docs/specification/describing-responses/) allows you to pass multiple response schemas.

You can pass a dictionary to the `response` argument, where:

- the keys are response codes
- the values are the schemas for each code

Also, when you return the result — you must also pass a status code to tell **Django Ninja** which schema should be used for validation and serialization.

An example:

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

## Multiple Response Codes

In the previous example, you saw that we basically repeated the `Message` schema twice:

```
...401: Message, 402: Message}
```

To avoid this duplication, you can use multiple response codes for a single schema:

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

**Django Ninja** comes with the following HTTP codes:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

You can also create your own ranges using a `frozenset`:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## Empty Responses

Some responses, such as [204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204), have no body.
To indicate that the response body is empty, mark the `response` argument with `None` instead of a schema:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## Error Responses

For more information, check out [Handling Errors](../errors.md) .

## Self-referencing Schemes

- Sometimes you need to create a schema that references itself or a tree-like structure object.

- To do this, you need to:

- wrap your schema type in quotes

- use the `update_forward_refs` method to apply the self-referencing type

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## Self-referencing Schemes Generated from `create_schema()`

To be able to use the `update_forward_refs()` method of a schema generated via `create_schema()`,
the "name" of the class needs to be in our namespace. In this case, it is important to pass the `name` argument to `create_schema()`.

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

## Serializing Outside of a View

You can directly serialize your objects in your code using the `.from_orm()` method on the schema object.

Consider the following model:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

It can be accessed using the following schema:
```python
class PersonSchema(Schema):
    name: str
```

Serialization can be performed directly using the `.from_orm()` method on the schema.
Once you have an instance of the schema object, the `.dict()` and `.json()` methods let you get a dictionary output and a string JSON version.

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

Multiple entries: or a queryset (or a list)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django HTTP Responses

It is also possible to return regular Django HTTP responses:

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

    Continue to the next chapter! **[Tweaking the Response](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
