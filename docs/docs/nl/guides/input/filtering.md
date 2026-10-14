---
comments: true
---
# Filtering

Als je gebruikers wilt toestaan om je querysets te filteren op meerdere verschillende attributen, is het zinvol om je filters in te kapselen in een `FilterSchema` class.
`FilterSchema` is een gewone `Schema`, dus het gebruikt alle benodigde mogelijkheden van Pydantic, maar het voegt ook enkele gemakken toe
om gebruiksvriendelijke filterparameters eenvoudig om te zetten naar databasequery's.

Definieer eerst een subclass van `FilterSchema`:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


Gebruik vervolgens dit schema samen met `Query` in je API handler:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Zoals beschreven in [Een Schema gebruiken om queryparameters te definiëren](./query-params.md#using-schema), zet Django Ninja de velden die zijn gedefinieerd in `BookFilterSchema` om naar queryparameters.
Je kunt de verkorte one-liner `.filter()` gebruiken om deze filters toe te passen op je queryset:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Onder de motorkap zet `FilterSchema` zijn velden om naar [Q expressies](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects), combineert ze en gebruikt ze om je queryset te filteren.


Als alternatief kun je, in plaats van de methode `.filter` te gebruiken, de voorbereide `Q` expressie ophalen en zelf de filtering uitvoeren.
Dit kan nuttig zijn wanneer je aanvullende queryset-filtering hebt bovenop wat je aan gebruikers blootstelt via de API:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

Standaard gedragen de filters zich als volgt:

* `None` waarden worden genegeerd en er wordt geen filtering toegepast;
* Elk niet-`None` veld wordt omgezet naar een `Q` expressie volgens de `Field` definitie van elk veld;
* Alle `Q` expressies worden gecombineerd tot één met de logische operator `AND`;
* De resulterende `Q` expressie wordt gebruikt om de queryset te filteren, en je krijgt een queryset terug waarop de `.filter` clausule is toegepast.

## Aangepaste velden
Standaard gebruikt `FilterSet` de veldnaam om de Q expressie te genereren:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
Het veld `name` wordt omgezet naar een `Q(name=...)` expressie.

Wanneer je database lookup complexer is dan dit, kun je deze expliciet opgeven met het keyword argument `"q"` in de velddefinitie:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
Je kunt zelfs meerdere lookup keyword argument namen opgeven als lijst:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
Standaard worden expressies op veldniveau gecombineerd met de connector `"OR"`, dus met de bovenstaande configuratie zoekt een queryparameter `?search=foobar` naar boeken die "foobar" bevatten in hun naam, auteur of uitgever.


## Expressies combineren
Standaard,

* worden expressies op veldniveau gecombineerd met de operator `OR`.
* worden de velden zelf gecombineerd met de operator `AND`.

Dus voor het volgende `FilterSchema`...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...en de volgende queryparameters van een gebruiker
```
http://localhost:8000/api/books?search=harry&popular=true
```
Zal de `FilterSchema` instantie zoeken naar populaire boeken die `harry` bevatten in de naam van het boek _of_ van de auteur.


Je kunt dit gedrag aanpassen met de parameter `expression_connector` in definities op veldniveau en op classniveau:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

De expression connector kan de waarden `"OR"`, `"AND"` en `"XOR"` aannemen, maar de laatste wordt alleen [ondersteund](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) in Django 4.1.

Nu zoekt een verzoek met deze queryparameters
```
http://localhost:8000/api/books?name=harry&active=true
```
...naar boeken die `harry` in hun naam hebben _of_ zelf actief zijn en gepubliceerd door een actieve uitgever.


## Filteren op Nones
Je kunt ervoor zorgen dat `FilterSchema` `None` als geldige waarde behandelt waarop filtering moet worden uitgevoerd.

Dit kan op veldniveau via het keyword argument `ignore_none`:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

Op deze manier zal het filter, wanneer de gebruiker geen andere waarde opgeeft voor `"tag"`, altijd de conditie `tag=None` opnemen.

Je kunt dit ook voor alle velden tegelijk opgeven in de configuratie:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## Aangepaste expressies
Soms heb je complexe filterscenario's die niet kunnen worden afgehandeld door een enkele veldannotatie.
Voor zulke gevallen kun je je veldfilterlogica implementeren als aangepaste methode. Definieer gewoon een methode genaamd `filter_<fieldname>` die een filterwaarde accepteert en een Q expressie teruggeeft:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
Zulke veldmethoden hebben voorrang op wat is opgegeven in de `Field()` definitie van het bijbehorende veld.
Als dat niet genoeg is, kun je je eigen aangepaste filterlogica implementeren voor de hele `FilterSet` class in de methode `custom_expression`:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    popular: Optional[bool] = None

    def custom_expression(self) -> Q:
        q = Q()
        if self.name:
            q &= Q(name__icontains=self.name)
        if self.popular:
            q &= (
                Q(view_count__gt=1000) |
                Q(downloads__gt=100) |
                Q(tag='popular')
            )
        return q
```
De methode `custom_expression` heeft voorrang op elke andere hierboven beschreven definitie, inclusief de methoden `filter_<fieldname>`.

!!! done

    De reeks over inputparameters is compleet! Ga verder naar de volgende sectie **[Responses verwerken](../response/index.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
