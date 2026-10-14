---
comments: true
---
# Response Schema

**Django Ninja** आपको validation और दस्तावेज़ीकरण के उद्देश्यों के लिए response schemas परिभाषित करने की अनुमति देता है।

कल्पना कीजिए कि आपको एक ऐसा API operation बनाना है जो एक user बनाता है। **Input** parameters **username+password** होंगे, लेकिन इस operation का **output** **id+username** होना चाहिए (**password के बिना**)।

आइए input schema बनाएँ:

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

अब आइए output schema परिभाषित करें और उसे `response` argument के रूप में `@api.post` decorator को पास करें:

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

**Django Ninja** `response` schema का उपयोग इन कार्यों के लिए करेगा:

- Output data को घोषित schema में बदलना
- Data को validate करना
- एक OpenAPI schema definition जोड़ना
- इसका उपयोग automatic दस्तावेज़ीकरण प्रणाली द्वारा किया जाएगा
- और, सबसे महत्वपूर्ण, यह **output data को सीमित करेगा** केवल schema में परिभाषित fields तक।

## Nested Objects

कुछ nested/sub-objects के साथ responses लौटाने की आवश्यकता भी आम बात है।

कल्पना कीजिए कि हमारे पास एक `Task` Django model है जिसमें `User` foreign key है:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

अब आइए सभी tasks आउटपुट करें और, प्रत्येक task के लिए, user के बारे में कुछ fields आउटपुट करें।

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

यदि आप यह operation निष्पादित करते हैं, तो आपको इस तरह का एक response मिलेगा:

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

Nested responses का उपयोग करने के बजाय, आप बस response आउटपुट को flatten करना चाह सकते हैं।
Ninja का `Schema` object dotted responses को संभालने के लिए Pydantic के `Field(..., alias="")` format को विस्तारित करता है।

ऊपर दिए गए model का उपयोग करते हुए, आइए एक ऐसा schema बनाएँ जिसमें task owner का first name inline शामिल हो, और जो `is_completed` के बजाय `completed` का उपयोग करे:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

Aliases Django template syntax variable access का भी समर्थन करते हैं:

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

आप field नामों पर आधारित resolver methods के माध्यम से computed fields भी बना सकते हैं।

Method को एक argument स्वीकार करना चाहिए, जो वह object होगा जिसे schema resolve कर रहा है।

Resolver को एक standard method के रूप में बनाते समय, `self` आपको schema में अन्य validated और formatted attributes तक पहुँच देता है।

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

### Extra Context तक पहुँच

Pydantic v2 आपको serializer को पास किए गए extra context को संभालने की अनुमति देता है। निम्नलिखित उदाहरण में, आपके पास एक ऐसा resolver हो सकता है जो पास किए गए `context` argument से request object प्राप्त करता है:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

यदि आप इस schema का उपयोग incoming request के लिए करते हैं — request object स्वचालित रूप से context में पास कर दिया जाएगा।

आप अपना खुद का context भी पास कर सकते हैं:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## एक Queryset लौटाना

पिछले उदाहरण में, हमने विशेष रूप से queryset को एक list में बदला (और मूल्यांकन के दौरान SQL query निष्पादित की)।

आप इससे बच सकते हैं और queryset को परिणाम के रूप में लौटा सकते हैं, और इसका मूल्यांकन स्वचालित रूप से एक list के रूप में होगा:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    यदि आपका operation asynchronous है, तो यह उदाहरण काम नहीं करेगा, क्योंकि ORM queries को सुरक्षित रूप से कॉल करने की आवश्यकता होती है।
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    अधिक जानकारी के लिए, [Async Support](../async-support.md#using-orm) देखें।

## File Fields और Image Fields

**Django Ninja** files और images (`FileField` या `ImageField` का उपयोग करके घोषित) को डिफ़ॉल्ट रूप से `string` URLs में बदल देता है।

एक उदाहरण:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

यदि आपको image field को response में आउटपुट करना है, तो इसके लिए एक schema इस तरह घोषित करें:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

इसे एक बार response में आउटपुट करने के बाद, प्रत्येक object के लिए एक URL स्वचालित रूप से बन जाएगा:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## Multiple Response Schemas

कभी-कभी आपको कई response schemas परिभाषित करने की आवश्यकता होती है।

उदाहरण के लिए, authentication के मामले में, आप लौटा सकते हैं:

- **200** सफल -> token
- **401** -> Unauthorized
- **402** -> Payment required
- आदि।

वास्तव में, [OpenAPI specification](https://swagger.io/docs/specification/describing-responses/) कई response schemas पास करने की अनुमति देती है।

आप `response` argument को एक dictionary पास कर सकते हैं, जहाँ:

- keys response codes हैं
- values प्रत्येक code के लिए schemas हैं

साथ ही, जब आप परिणाम लौटाते हैं — आपको **Django Ninja** को बताने के लिए एक status code भी पास करना होगा कि validation और serialization के लिए कौन सा schema उपयोग किया जाना चाहिए।

एक उदाहरण:

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

पिछले उदाहरण में, आपने देखा कि हमने मूल रूप से `Message` schema को दो बार दोहराया:

```
...401: Message, 402: Message}
```

इस duplication से बचने के लिए, आप एक single schema के लिए कई response codes का उपयोग कर सकते हैं:

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

**Django Ninja** निम्नलिखित HTTP codes के साथ आता है:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

आप एक `frozenset` का उपयोग करके अपनी खुद की ranges भी बना सकते हैं:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## खाली Responses

कुछ responses, जैसे [204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204), का कोई body नहीं होता।
यह इंगित करने के लिए कि response body खाली है, `response` argument को schema के बजाय `None` से चिह्नित करें:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## Error Responses

अधिक जानकारी के लिए, [Handling Errors](../errors.md) देखें।

## Self-referencing Schemes

- कभी-कभी आपको ऐसा schema बनाने की आवश्यकता होती है जो स्वयं का या एक tree-जैसी संरचना वाले object का संदर्भ दे।

- इसके लिए, आपको:

- अपने schema type को quotes में लपेटना है

- self-referencing type लागू करने के लिए `update_forward_refs` method का उपयोग करना है

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## `create_schema()` से बनाए गए Self-referencing Schemes

`create_schema()` के माध्यम से बनाए गए schema के `update_forward_refs()` method का उपयोग करने में सक्षम होने के लिए,
class का "name" हमारे namespace में होना चाहिए। इस स्थिति में, `name` argument को `create_schema()` को पास करना महत्वपूर्ण है।

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

## View के बाहर Serializing करना

आप schema object पर `.from_orm()` method का उपयोग करके अपने code में सीधे अपने objects को serialize कर सकते हैं।

निम्नलिखित model पर विचार करें:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

इसे निम्नलिखित schema का उपयोग करके access किया जा सकता है:
```python
class PersonSchema(Schema):
    name: str
```

Serialization सीधे schema पर `.from_orm()` method का उपयोग करके की जा सकती है।
एक बार जब आपके पास schema object का एक instance हो, तो `.dict()` और `.json()` methods आपको dictionary आउटपुट और एक string JSON संस्करण प्राप्त करने देते हैं।

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

कई entries: या एक queryset (या एक list)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django HTTP Responses

सामान्य Django HTTP responses लौटाना भी संभव है:

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

    अगले अध्याय पर जाएँ! **[Tweaking the Response](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
