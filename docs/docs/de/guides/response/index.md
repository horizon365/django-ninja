---
comments: true
---
# Response-Schema

**Django Ninja** erlaubt es Ihnen, Response-Schemata für Validierungs- und Dokumentationszwecke zu definieren.

Angenommen, Sie müssen eine API-Operation erstellen, die einen Benutzer anlegt. Die **Eingabe**-Parameter sind **username+password**, aber die **Ausgabe** dieser Operation sollte **id+username** sein (**ohne** das Passwort).

Erstellen wir das Eingabe-Schema:

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

Definieren wir nun das Ausgabe-Schema und übergeben es als Argument `response` an den Dekorator `@api.post`:

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

**Django Ninja** wird das `response`-Schema verwenden, um:

- die Ausgabedaten in das deklarierte Schema zu konvertieren
- die Daten zu validieren
- eine OpenAPI-Schema-Definition hinzuzufügen
- sie wird vom automatischen Dokumentationssystem verwendet
- und – am wichtigsten – sie **begrenzt die Ausgabedaten** auf die im Schema definierten Felder.

## Verschachtelte Objekte

Häufig müssen auch Responses mit verschachtelten Unterobjekten zurückgegeben werden.

Angenommen, wir haben ein Django-Modell `Task` mit einem `User`-Fremdschlüssel:

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

Geben wir nun alle Tasks aus und dazu für jeden Task einige Felder des Benutzers.

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

Wenn Sie diese Operation ausführen, sollten Sie eine Response wie diese erhalten:

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

## Aliase

Statt verschachtelter Responses möchten Sie die Response-Ausgabe vielleicht einfach flach halten. Das `Schema`-Objekt von Ninja erweitert Pydantics Format `Field(..., alias="")`, um verschachtelte Ausgaben mit Punktnotation zu verarbeiten.

Anhand des obigen Modells erstellen wir ein Schema, das nur den Vornamen des Task-Eigners inline ausgibt und außerdem `completed` statt `is_completed` verwendet:

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

Aliase unterstützen auch den Variablenzugriff der Django-Template-Syntax:

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

Sie können auch berechnete Felder über Resolver-Methoden erstellen, die auf den Feldnamen basieren.

Die Methode muss ein Argument entgegennehmen, das das Objekt ist, das das Schema auflöst.

Wenn Sie den Resolver als Standardmethode erstellen, gibt Ihnen `self` Zugriff auf andere validierte und formatierte Attribute im Schema.

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

### Zugriff auf zusätzlichen Kontext

Pydantic v2 erlaubt es, zusätzlichen Kontext zu verarbeiten, der an den Serializer übergeben wird. Im folgenden Beispiel kann ein Resolver das Request-Objekt aus dem übergebenen Argument `context` beziehen:
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

Wenn Sie dieses Schema für einen eingehenden Request verwenden – wird das Request-Objekt automatisch an den Kontext übergeben.

Sie können auch Ihren eigenen Kontext übergeben:

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## Rückgabe eines Querysets

Im vorherigen Beispiel haben wir das Queryset eigens in eine Liste konvertiert (und dabei die SQL-Abfrage bei der Auswertung ausgeführt).

Sie können das vermeiden und das Queryset direkt als Ergebnis zurückgeben; es wird automatisch als Liste ausgewertet:

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    Wenn Ihre Operation asynchron ist, funktioniert dieses Beispiel nicht, da ORM-Abfragen sicher aufgerufen werden müssen.
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    Weitere Informationen finden Sie unter [Asynchrone Unterstützung](../async-support.md#using-orm) .

## Datei- und Bildfelder

**Django Ninja** wandelt Dateien und Bilder (deklariert mit `FileField` oder `ImageField`) standardmäßig in `string`-URLs um.

Ein Beispiel:

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

Wenn Sie das Bildfeld in der Response ausgeben möchten, deklarieren Sie dafür ein Schema wie folgt:

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

Sobald Sie dies in der Response ausgeben, wird für jedes Objekt automatisch eine URL generiert:

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## Mehrere Response-Schemata

Manchmal müssen Sie mehrere Response-Schemata definieren.

Zum Beispiel könnten Sie im Fall der Authentifizierung Folgendes zurückgeben:

- **200** erfolgreich -> Token
- **401** -> Unauthorized
- **402** -> Payment required
- usw.

Tatsächlich erlaubt die [OpenAPI-Spezifikation](https://swagger.io/docs/specification/describing-responses/) die Übergabe mehrerer Response-Schemata.

Sie können ein Wörterbuch an das Argument `response` übergeben, wobei:

- die Schlüssel die Response-Codes sind
- die Werte die Schemata für den jeweiligen Code sind

Wenn Sie das Ergebnis zurückgeben, müssen Sie außerdem einen Statuscode übergeben, um **Django Ninja** mitzuteilen, welches Schema für Validierung und Serialisierung verwendet werden soll.

Ein Beispiel:

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

## Mehrere Response-Codes

Im vorherigen Beispiel haben Sie gesehen, dass wir im Grunde das Schema `Message` zweimal wiederholt haben:

```
...401: Message, 402: Message}
```

Um diese Duplikation zu vermeiden, können Sie mehrere Response-Codes für ein einzelnes Schema verwenden:

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

**Django Ninja** wird mit den folgenden HTTP-Codes ausgeliefert:

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

Sie können auch eigene Bereiche mit einem `frozenset` erstellen:

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## Leere Responses

Manche Responses, wie [204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204), haben keinen Body.
Um anzuzeigen, dass der Response-Body leer ist, markieren Sie das Argument `response` mit `None` statt mit einem Schema:

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## Fehler-Responses

Weitere Informationen finden Sie unter [Fehlerbehandlung](../errors.md) .

## Sich selbst referenzierende Schemata

- Manchmal müssen Sie ein Schema erstellen, das sich selbst referenziert oder ein baumartig strukturiertes Objekt darstellt.

- Dazu müssen Sie:

- Ihren Schema-Typ in Anführungszeichen setzen

- die Methode `update_forward_refs` verwenden, um den selbstreferenzierenden Typ anzuwenden

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## Sich selbst referenzierende Schemata, generiert mit `create_schema()`

Um die Methode `update_forward_refs()` eines Schemas verwenden zu können, das mit `create_schema()` generiert wurde,
muss der „Name" der Klasse in unserem Namensraum vorhanden sein. In diesem Fall ist es wichtig, das Argument `name` an `create_schema()` zu übergeben.

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

## Serialisierung außerhalb einer View

Sie können Ihre Objekte direkt in Ihrem Code serialisieren, indem Sie die Methode `.from_orm()` am Schema-Objekt verwenden.

Betrachten Sie das folgende Modell:

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

Es kann über das folgende Schema abgerufen werden:
```python
class PersonSchema(Schema):
    name: str
```

Die Serialisierung kann direkt mit der Methode `.from_orm()` am Schema durchgeführt werden.
Sobald Sie eine Instanz des Schema-Objekts haben, liefern Ihnen die Methoden `.dict()` und `.json()` eine Wörterbuch-Ausgabe bzw. eine JSON-String-Version.

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

Mehrere Einträge: oder ein Queryset (oder eine Liste)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Django-HTTP-Responses

Es ist auch möglich, reguläre Django-HTTP-Responses zurückzugeben:

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

    Weiter zum nächsten Kapitel! **[Die Response anpassen](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
