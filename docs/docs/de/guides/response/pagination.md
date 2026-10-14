---
comments: true
---
# Paginierung

**Django Ninja** wird mit Paginierungsunterstützung ausgeliefert. Dadurch können Sie große Ergebnismengen in einzelne Seiten aufteilen.


Um eine Funktion zu paginieren – wenden Sie einfach den Dekorator `paginate` an:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


Das war's!

Nun können Sie Benutzer über die GET-Parameter `limit` und `offset` abfragen

```
/api/users?limit=10&offset=0
```

Standardmäßig ist das Limit auf `100` gesetzt (in Ihrer settings.py können Sie es über `NINJA_PAGINATION_PER_PAGE` ändern)


## Integrierte Paginierungsklassen

### LimitOffsetPagination (Standard)

Dies ist die Standard-Paginierungsklasse (in Ihrer settings.py können Sie sie ändern, indem Sie `NINJA_PAGINATION_CLASS` auf den Pfad einer Klasse verweisen lassen)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

Beispielabfrage:
```
/api/users?limit=10&offset=0
```

Diese Klasse hat zwei Eingabeparameter:

 - `limit` – legt die Anzahl der Queryset-Einträge pro Seite fest (Standard = 100, änderbar über NINJA_PAGINATION_PER_PAGE)
 - `offset` – setzt das Offset des Seitenfensters (Standard: 0, die Indizierung beginnt bei 0)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

Beispielabfrage:
```
/api/users?page=2
```

Diese Klasse hat einen Parameter `page` und gibt standardmäßig 100 Queryset-Einträge pro Seite aus (änderbar über die settings.py)

Die Seitennummerierung beginnt bei 1.

Sie können auch eine eigene Seitengröße für jede View einzeln festlegen:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## Zugriff auf Paginierungsparameter in der View-Funktion

Wenn Sie in Ihrer View-Funktion auf die für die Paginierung verwendeten `Input`-Parameter zugreifen müssen – verwenden Sie das Argument `pass_parameter`

In diesem Fall sind die Eingabedaten in `**kwargs` verfügbar:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## Eine eigene Paginierungsklasse erstellen

Um eine eigene Paginierungsklasse zu erstellen, sollten Sie von `ninja.pagination.PaginationBase` erben und die Schema-Klassen `Input` und `Output` sowie die Methode `paginate_queryset(self, queryset, request, **params)` überschreiben:

 - Das `Input`-Schema ist eine Schema-Klasse, die die Parameter beschreibt, die an den Paginator übergeben werden sollen (wie Seitennummer oder limit/offset-Werte).
 - Das `Output`-Schema beschreibt das Schema der Seitenausgabe (wie count/next/items usw.).
 - Die Methode `paginate_queryset` erhält das anfängliche Queryset und sollte ein Iterable zurückgeben, das nur die Daten der angeforderten Seite enthält. Die Methode nimmt die folgenden Parameter entgegen:
    - `queryset`: das von der API-Funktion zurückgegebene Queryset (oder Iterable).
    - `pagination` – die paginator.Input-Parameter (geparst und validiert)
    - `**params`: Schlüsselwortargumente, die alle Argumente enthalten, die die dekorierte Funktion erhält.


Beispiel:

```python hl_lines="7 11 16 26"
from ninja.pagination import paginate, PaginationBase
from ninja import Schema


class CustomPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip: int
        

    class Output(Schema):
        items: List[Any] # `items` is a default attribute
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            'items': queryset[skip : skip + 5],
            'total': queryset.count(),
            'per_page': 5,
        }


@api.get('/users', response=List[UserSchema])
@paginate(CustomPagination)
def list_users(request):
    return User.objects.all()
```

Tipp: Auf das Request-Objekt können Sie über die Parameter zugreifen:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### Asynchrone Paginierung

Die Standard-Paginierungsklassen von **Django Ninja** unterstützen async. Wenn Sie asynchrone Requests mit einer eigenen Paginierungsklasse verarbeiten möchten, sollten Sie von `ninja.pagination.AsyncPaginationBase` erben und die Methode `apaginate_queryset(self, queryset, request, **params)` überschreiben.

### Output-Attribute

Standardmäßig werden die Seiteneinträge im Attribut `'items'` abgelegt. Um dieses Verhalten zu überschreiben, können Sie `items_attribute` verwenden:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## Paginierung auf mehrere Operationen auf einmal anwenden

Häufig kommt es vor, dass Sie alle Views, die Querysets oder Listen zurückgeben, mit einer Paginierung versehen möchten

Sie können die integrierte Router-Klasse (`RouterPaginated`) verwenden, die automatisch eine Paginierung in alle Operationen injiziert, die mit `response=List[SomeSchema]` definiert sind:

```python hl_lines="1 3 6 10"
from ninja.pagination import RouterPaginated

router = RouterPaginated()


@router.get("/items", response=List[MySchema])
def items(request):
    return MyModel.objects.all()

@router.get("/other-items", response=List[OtherSchema])
def ohter_items(request):
    return OtherModel.objects.all()

```

In diesem Beispiel ist die Paginierung für beide Operationen aktiviert.

Um die Paginierung auf die Haupt-`api`-Instanz anzuwenden, können Sie das Argument `default_router` verwenden:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    Weiter zum nächsten Kapitel! **[Response-Renderer](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
