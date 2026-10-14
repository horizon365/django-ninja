---
comments: true
---
# Schéma de réponse

**Django Ninja** vous permet de définir des schémas de réponse à des fins de validation et de documentation.

Imaginez que vous devez créer une opération d'API qui crée un utilisateur. Les paramètres d'**entrée** seront **username+password**, mais la **sortie** de cette opération devrait être **id+username** (**sans** le mot de passe).

Créons le schéma d'entrée :

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

Définissons maintenant le schéma de sortie et passons-le comme argument `response` au décorateur `@api.post` :

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

**Django Ninja** utilisera le schéma `response` pour :

- Convertir les données de sortie vers le schéma déclaré
- Valider les données
- Ajouter une définition de schéma OpenAPI
- Il sera utilisé par le système de documentation automatique
- Et, plus important encore, il **limitera les données de sortie** aux seuls champs définis dans le schéma.

## Objets imbriqués

Il est également fréquent d'avoir besoin de renvoyer des réponses avec des sous-objets/objets imbriqués.

Imaginez que nous ayons un model Django `Task` avec une clé étrangère `User` :

```python hl_lines="6"
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", null=True, blank=True)
```

Sortons maintenant toutes les tâches et, pour chaque tâche, affichons certains champs concernant l'utilisateur.

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

Si vous exécutez cette opération, vous devriez obtenir une réponse comme celle-ci :

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

## Alias

Au lieu d'utiliser des réponses imbriquées, vous pouvez souhaiter simplement aplatir la sortie de la réponse.
L'objet `Schema` de Ninja étend le format `Field(..., alias="")` de Pydantic pour gérer les réponses avec points (dotted).

En utilisant le model ci-dessus, créons un schéma qui n'inclut que le prénom du propriétaire de la tâche en ligne, et utilise également `completed` au lieu de `is_completed` :

```python hl_lines="1 7-9"
from ninja import Field, Schema


class TaskSchema(Schema):
    id: int
    title: str
    # The first Field argument is the default value; use ... for required fields.
    completed: bool = Field(..., alias="is_completed")
    owner_first_name: str = Field(None, alias="owner.first_name")
```

Les alias prennent également en charge l'accès aux variables selon la syntaxe des templates Django :

```python hl_lines="2"
class TaskSchema(Schema):
    last_message: str = Field(None, alias="message_set.0.text")
```

```python hl_lines="3"
class TaskSchema(Schema):
    type: str = Field(None)
    type_display: str = Field(None, alias="get_type_display") # callable will be executed
```

## Résolveurs

Vous pouvez également créer des champs calculés via des méthodes résolveurs (resolver) basées sur les noms de champs.

La méthode doit accepter un argument, qui sera l'objet que le schéma est en train de résoudre.

Lorsque vous créez le résolveur comme une méthode standard, `self` vous donne accès aux autres attributs validés et formatés du schéma.

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

### Accès au contexte supplémentaire

Pydantic v2 vous permet de gérer un contexte supplémentaire passé au sérialiseur. Dans l'exemple suivant, vous pouvez avoir un résolveur qui récupère l'objet request à partir de l'argument `context` passé :
```python hl_lines="6"
class Data(Schema):
    a: int
    path: str = ""

    @staticmethod
    def resolve_path(obj, context):
        request = context["request"]
        return request.path
```

Si vous utilisez ce schéma pour une requête entrante — l'objet request sera automatiquement passé au contexte.

Vous pouvez également passer votre propre contexte :

```python
data = Data.model_validate({'some': 1}, context={'request': MyRequest()})
```

## Renvoi d'un Queryset

Dans l'exemple précédent, nous avons spécifiquement converti le queryset en liste (et exécuté la requête SQL lors de l'évaluation).

Vous pouvez éviter cela et renvoyer le queryset comme résultat, il sera automatiquement évalué en liste :

```python hl_lines="3"
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()
```

!!! warning

    Si votre opération est asynchrone, cet exemple ne fonctionnera pas, car les requêtes ORM doivent être appelées de manière sûre.
    ```python hl_lines="2"
    @api.get("/tasks", response=List[TaskSchema])
    async def tasks(request):
        return Task.objects.all()
    ```

    Pour plus d'informations, consultez [Prise en charge asynchrone](../async-support.md#using-orm) .

## FileField et ImageField

**Django Ninja** convertit par défaut les fichiers et les images (déclarés à l'aide de `FileField` ou `ImageField`) en URL de type `string`.

Un exemple :

```python hl_lines="3"
class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
```

Si vous devez afficher le champ image dans la réponse, déclarez un schéma pour celui-ci comme ceci :

```python hl_lines="3"
class PictureSchema(Schema):
    title: str
    image: str
```

Une fois que vous l'avez affiché dans la réponse, une URL sera automatiquement générée pour chaque objet :

```JSON
{
    "title": "Zebra",
    "image": "/static/images/zebra.jpg"
}
```

## Plusieurs schémas de réponse

Parfois, vous devez définir plusieurs schémas de réponse.

Par exemple, dans le cas d'une authentification, vous pourriez renvoyer :

- **200** succès -> token
- **401** -> Unauthorized
- **402** -> Payment required
- etc.

En fait, la [spécification OpenAPI](https://swagger.io/docs/specification/describing-responses/) permet de passer plusieurs schémas de réponse.

Vous pouvez passer un dictionnaire à l'argument `response`, où :

- les clés sont les codes de réponse
- les valeurs sont les schémas pour chaque code

Aussi, lorsque vous renvoyez le résultat — vous devez également passer un code de statut pour indiquer à **Django Ninja** quel schéma doit être utilisé pour la validation et la sérialisation.

Un exemple :

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

## Plusieurs codes de réponse

Dans l'exemple précédent, vous avez vu que nous avons essentiellement répété deux fois le schéma `Message` :

```
...401: Message, 402: Message}
```

Pour éviter cette duplication, vous pouvez utiliser plusieurs codes de réponse pour un seul schéma :

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

**Django Ninja** est livré avec les codes HTTP suivants :

```python
from ninja.responses import codes_1xx
from ninja.responses import codes_2xx
from ninja.responses import codes_3xx
from ninja.responses import codes_4xx
from ninja.responses import codes_5xx
```

Vous pouvez également créer vos propres plages à l'aide d'un `frozenset` :

```python
my_codes = frozenset({416, 418, 425, 429, 451})

@api.post('/login', response={200: Token, my_codes: Message})
def login(request, payload: Auth):
    ...
```

## Réponses vides

Certaines réponses, telles que [204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204), n'ont pas de corps.
Pour indiquer que le corps de la réponse est vide, marquez l'argument `response` avec `None` au lieu d'un schéma :

```python hl_lines="1 3"
@api.post("/no_content", response={204: None})
def no_content(request):
    return 204, None
```

## Réponses d'erreur

Pour plus d'informations, consultez [Gestion des erreurs](../errors.md) .

## Schémas auto-référencés

- Parfois, vous devez créer un schéma qui se référence lui-même ou un objet de structure arborescente.

- Pour ce faire, vous devez :

- encapsuler votre type de schéma entre guillemets

- utiliser la méthode `update_forward_refs` pour appliquer le type auto-référencé

```python hl_lines="3 6"
class Organization(Schema):
    title: str
    part_of: 'Organization' = None     #!! Note that the type here needs to be in quotes!! !!


Organization.update_forward_refs()  # !!! this line is important


@api.get('/organizations', response=List[Organization])
def list_organizations(request):
    ...
```

## Schémas auto-référencés générés à partir de `create_schema()`

Pour pouvoir utiliser la méthode `update_forward_refs()` d'un schéma généré via `create_schema()`,
le « nom » de la classe doit se trouver dans notre espace de noms. Dans ce cas, il est important de passer l'argument `name` à `create_schema()`.

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

## Sérialisation en dehors d'une vue

Vous pouvez sérialiser directement vos objets dans votre code à l'aide de la méthode `.from_orm()` sur l'objet schéma.

Considérons le model suivant :

```python
class Person(models.Model):
    name = models.CharField(max_length=50)
```

Il peut être accessible à l'aide du schéma suivant :
```python
class PersonSchema(Schema):
    name: str
```

La sérialisation peut être effectuée directement à l'aide de la méthode `.from_orm()` sur le schéma.
Une fois que vous avez une instance de l'objet schéma, les méthodes `.dict()` et `.json()` vous permettent d'obtenir une sortie dictionnaire et une version JSON sous forme de chaîne.

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

Entrées multiples : ou un queryset (ou une liste)

```python
>>> persons = Person.objects.all()
>>> data = [PersonSchema.from_orm(i).dict() for i in persons]
[{'id':1, 'name':'Mr. Smith'},{'id': 2, 'name': 'Mrs. Smith'}...]
```

## Réponses HTTP Django

Il est également possible de renvoyer des réponses HTTP Django ordinaires :

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

    Poursuivez avec le chapitre suivant ! **[Ajustement de la réponse](temporal_response.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
