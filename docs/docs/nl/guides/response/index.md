---
comments: true
---
# Response Schema

**Django Ninja** stelt je in staat om response schemas te definiëren voor validatie- en documentatiedoeleinden.

Stel je voor dat je een API-operatie moet maken die een gebruiker aanmaakt. De **input** parameters zijn **username+password**, maar de **output** van deze operatie moet **id+username** zijn (**zonder** het wachtwoord).

Laten we het input schema maken:

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

Laten we nu het output schema definiëren en dit als argument `response` doorgeven aan de decorator `@api.post`:

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

**Django Ninja** zal het `response` schema gebruiken om:

- De output data te converteren naar het gedeclareerde schema
- De data te valideren
- Een OpenAPI schema definitie toe te voegen
- Het wordt gebruikt door het automatische documentatiesysteem
- En, het allerbelangrijkste: het **beperkt de output data** tot alleen de velden die in het schema zijn gedefinieerd.

## Geneste Objecten

Het komt ook vaak voor dat je responses met geneste/sub-objecten moet teruggeven.

Stel je voor dat we een Django model `Task` hebben met een foreign key naar `User`:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

Laten we nu alle taken als output geven en voor elke taak enkele velden over de gebruiker tonen.

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

Als je deze operatie uitvoert, zou je een response zoals deze moeten krijgen:

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

## Aliassen

In plaats van geneste responses te gebruiken, wil je de response-output misschien gewoon afvlakken (flatten).
Het `Schema` object van Ninja breidt het formaat van Pydantic `Field(..., alias="")` uit om responses met puntnotatie af te handelen.

Met het bovenstaande model maken we een schema dat alleen de voornaam van de taakeigenaar inline opneemt, en dat ook `completed` gebruikt in plaats van `is_completed`:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

Aliassen ondersteunen ook variabeletoegang met de syntax van Django templates:

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

Je kunt ook berekende velden maken via resolver-methoden op basis van veldnamen.

De methode moet één argument accepteren, dat het object is waarvoor het schema wordt geresolved.

Wanneer je de resolver als standaard methode maakt, geeft `self` je toegang tot andere gevalideerde en geformatteerde attributen in het schema.

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

### Toegang Tot Extra Context

Pydantic v2 maakt het mogelijk om extra context af te handelen die aan de serializer wordt doorgegeven. In het volgende voorbeeld kun je een resolver hebben die het request object haalt uit het doorgegeven argument `context`:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

Als je dit schema gebruikt voor een inkomend verzoek — wordt het request object automatisch doorgegeven aan de context.

Je kunt ook je eigen context doorgeven:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## Een Queryset Teruggeven

In het vorige voorbeeld hebben we de queryset specifiek naar een lijst geconverteerd (en de SQL query uitgevoerd tijdens de evaluatie).

Je kunt dit vermijden en de queryset als resultaat teruggeven; deze wordt automatisch als lijst geëvalueerd:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    Als je operatie asynchroon is, zal dit voorbeeld niet werken, omdat ORM query's veilig moeten worden aangeroepen.
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    Voor meer informatie, zie [Async Ondersteuning](../async-support.md#using-orm) .

## Bestandsvelden en Afbeeldingsvelden

**Django Ninja** zet bestanden en afbeeldingen (gedeclareerd met `FileField` of `ImageField`) standaard om naar `string` URLs.

Een voorbeeld:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

Als je het afbeeldingsveld naar de response wilt sturen, declareer je er als volgt een schema voor:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

Zodra je dit naar de response stuurt, wordt er automatisch een URL gegenereerd voor elk object:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## Meerdere Response Schemas

Soms moet je meerdere response schemas definiëren.

Bijvoorbeeld, in het geval van authenticatie kun je teruggeven:

- **200** succesvol -> token
- **401** -> Unauthorized
- **402** -> Payment required
- enz.

In feite staat de [OpenAPI specificatie](https://swagger.io/docs/specification/describing-responses/) toe om meerdere response schemas door te geven.

Je kunt een dictionary doorgeven aan het argument `response`, waarbij:

- de keys de response codes zijn
- de values de schemas zijn voor elke code

Ook moet je, wanneer je het resultaat teruggeeft — ook een statuscode doorgeven om **Django Ninja** te vertellen welk schema moet worden gebruikt voor validatie en serialisatie.

Een voorbeeld:

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

## Meerdere Response Codes

In het vorige voorbeeld zag je dat we in feite het schema `Message` twee keer herhaalden:

```
...401: Message, 402: Message}
```

Om deze duplicatie te voorkomen, kun je meerdere response codes gebruiken voor één schema:

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

**Django Ninja** wordt geleverd met de volgende HTTP codes:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

Je kunt ook je eigen reeksen maken met een `frozenset`:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## Lege Responses

Sommige responses, zoals [204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204), hebben geen body.
Om aan te geven dat de response body leeg is, markeer je het argument `response` met `None` in plaats van een schema:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## Fout Responses

Voor meer informatie, bekijk [Fouten Afhandelen](../errors.md) .

## Zelfverwijzende Schemas

- Soms moet je een schema maken dat naar zichzelf verwijst of een boomachtig structuurobject.

- Om dit te doen, moet je:

- je schematype tussen aanhalingstekens zetten

- de methode `update_forward_refs` gebruiken om het zelfverwijzende type toe te passen

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## Zelfverwijzende Schemas Gegenereerd vanuit `create_schema()`

Om de methode `update_forward_refs()` van een schema dat is gegenereerd via `create_schema()` te kunnen gebruiken,
moet de "name" van de class in onze namespace staan. In dit geval is het belangrijk om het argument `name` door te geven aan `create_schema()`.

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

## Serialiseren Buiten een View

Je kunt je objecten direct in je code serialiseren met de methode `.from_orm()` op het schema object.

Beschouw het volgende model:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

Het kan worden benaderd met het volgende schema:
```python
class PersonSchema(Schema):
    name: str
```

Serialisatie kan direct worden uitgevoerd met de methode `.from_orm()` op het schema.
Zodra je een instantie van het schema object hebt, geven de methoden `.dict()` en `.json()` je een dictionary-output en een JSON-versie als string.

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

Meerdere items: of een queryset (of een lijst)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django HTTP Responses

Het is ook mogelijk om reguliere Django HTTP responses terug te geven:

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

    Ga verder naar het volgende hoofdstuk! **[De Response Aanpassen](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
