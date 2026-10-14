---
comments: true
---
# Paginering

**Django Ninja** wordt geleverd met ondersteuning voor paginering. Hiermee kun je grote resultatensets opsplitsen in afzonderlijke pagina's.


Om paginering toe te passen op een functie — pas simpelweg de decorator `paginate` toe:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


Dat is alles!

Nu kun je gebruikers bevragen met de GET parameters `limit` en `offset`

```
/api/users?limit=10&offset=0
```

Standaard is de limit ingesteld op `100` (je kunt dit wijzigen in je settings.py met `NINJA_PAGINATION_PER_PAGE`)


## Ingebouwde Paginering Classes

### LimitOffsetPagination (standaard)

Dit is de standaard paginering class (je kunt deze wijzigen in je settings.py door `NINJA_PAGINATION_CLASS` te laten verwijzen naar het path van een class)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

Voorbeeldquery:
```
/api/users?limit=10&offset=0
```

Deze class heeft twee input parameters:

 - `limit` - definieert het aantal querysets op een pagina (standaard = 100, te wijzigen via NINJA_PAGINATION_PER_PAGE)
 - `offset` - stelt de paginavenster-offset in (standaard: 0, indexering begint bij 0)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

Voorbeeldquery:
```
/api/users?page=2
```

Deze class heeft één parameter `page` en geeft standaard 100 querysets per pagina als output (te wijzigen via settings.py)

Paginanummering begint bij 1.

Je kunt ook een aangepaste paginagrootte instellen voor elke view afzonderlijk:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## Toegang Tot Paginering Parameters in een Viewfunctie

Als je toegang nodig hebt tot de `Input` parameters die voor de paginering worden gebruikt in je viewfunctie — gebruik dan het argument `pass_parameter`

In dat geval zijn de input data beschikbaar in `**kwargs`:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## Een Aangepaste Paginering Class Maken

Om een aangepaste paginering class te maken, moet je overerven van `ninja.pagination.PaginationBase` en de schema classes `Input` en `Output` evenals de methode `paginate_queryset(self, queryset, request, **params)` overriden:

 - Het `Input` schema is een schema class die de parameters beschrijft die aan de paginator moeten worden doorgegeven (zoals paginanummer of limit/offset waarden).
 - Het `Output` schema beschrijft het schema van de pagina-output (zoals count/next/items, enz.).
 - De methode `paginate_queryset` ontvangt de initiële queryset en moet een iterable teruggeven die alleen de data in de opgevraagde pagina bevat. De methode accepteert de volgende parameters:
    - `queryset`: de queryset (of iterable) die wordt teruggegeven door de API functie.
    - `pagination` - de paginator.Input parameters (geparst en gevalideerd)
    - `**params`: keyword argumenten die alle argumenten bevatten die de gedecoreerde functie ontvangt.


Voorbeeld:

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

Tip: je kunt het request object uit de parameters halen:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### Async Paginering

De standaard paginering classes van **Django Ninja** ondersteunen async. Als je asynchrone verzoeken wilt afhandelen met een aangepaste paginering class, moet je overerven van `ninja.pagination.AsyncPaginationBase` en de methode `apaginate_queryset(self, queryset, request, **params)` overriden.

### Output Attributen

Standaard worden pagina-items geplaatst in het attribuut `'items'`. Om dit gedrag te overriden, kun je `items_attribute` gebruiken:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## Paginering Toepassen op Meerdere Operaties Tegelijk

Vaak is er een geval waarin je paginering wilt toevoegen aan alle views die querysets of lijsten teruggeven

Je kunt de ingebouwde router class gebruiken (`RouterPaginated`) die automatisch paginering injecteert in alle operaties die zijn gedefinieerd met `response=List[SomeSchema]`:

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

In dit voorbeeld hebben beide operaties paginering ingeschakeld.

Om paginering toe te passen op de hoofd-`api` instantie, kun je het argument `default_router` gebruiken:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    Ga verder naar het volgende hoofdstuk! **[Response Renderers](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
