---
comments: true
---
# Filterung

Wenn Sie Benutzern erlauben möchten, Ihre Querysets nach mehreren unterschiedlichen Attributen zu filtern, ist es sinnvoll, Ihre Filter in einer `FilterSchema`-Klasse zu kapseln.
`FilterSchema` ist ein gewöhnliches `Schema`, nutzt also alle notwendigen Features von Pydantic, fügt aber zusätzlich einige Annehmlichkeiten hinzu,
um benutzerseitige Filterparameter einfach in Datenbankabfragen umzuwandeln.

Definieren Sie zunächst eine Unterklasse von `FilterSchema`:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


Verwenden Sie dieses Schema anschließend zusammen mit `Query` in Ihrem API-Handler:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Genauso wie unter [Ein Schema zum Definieren von Query-Parametern verwenden](./query-params.md#using-schema) beschrieben verwandelt Django Ninja die in `BookFilterSchema` definierten Felder in Query-Parameter.
Mit der Kurzform `.filter()` in einer Zeile können Sie diese Filter auf Ihr Queryset anwenden:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Unter der Haube wandelt `FilterSchema` seine Felder in [Q-Ausdrücke](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects) um, kombiniert sie und filtert damit Ihr Queryset.


Alternativ können Sie, statt die Methode `.filter` zu verwenden, den vorbereiteten `Q`-Ausdruck abrufen und die Filterung selbst durchführen.
Das kann nützlich sein, wenn Sie zusätzlich zu dem, was Sie Benutzern über die API zugänglich machen, noch weitere Filterungen am Queryset vornehmen:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

Standardmäßig verhalten sich die Filter wie folgt:

* `None`-Werte werden ignoriert, es wird dann keine Filterung angewendet;
* Jedes Feld, das nicht `None` ist, wird gemäß der `Field`-Definition des jeweiligen Felds in einen `Q`-Ausdruck umgewandelt;
* Alle `Q`-Ausdrücke werden mit dem logischen Operator `AND` zu einem Ausdruck kombiniert;
* Der resultierende `Q`-Ausdruck wird zum Filtern des Querysets verwendet, und Sie erhalten ein Queryset zurück, auf das die `.filter`-Klausel angewendet wurde.

## Benutzerdefinierte Felder
Standardmäßig verwendet `FilterSet` den Feldnamen, um den Q-Ausdruck zu generieren:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
Das Feld `name` wird in einen Ausdruck `Q(name=...)` umgewandelt.

Wenn Ihre Datenbankabfrage komplexer ist als das, können Sie sie explizit über das Schlüsselwortargument `"q"` in der Felddefinition angeben:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
Sie können sogar mehrere Lookup-Schlüsselwortargument-Namen als Liste angeben:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
Standardmäßig werden die Ausdrücke auf Feldebene mit dem Verbund „`OR`" kombiniert, daher sucht bei der obigen Konfiguration der Query-Parameter `?search=foobar` nach Büchern, die „foobar" in ihrem Namen, ihrem Autor oder ihrem Verlag enthalten.


## Ausdrücke kombinieren
Standardmäßig

* werden Ausdrücke auf Feldebene mit dem Operator `OR` kombiniert.
* werden die Felder selbst mit dem Operator `AND` kombiniert.

Für das folgende `FilterSchema` also...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
... und die folgenden Query-Parameter eines Benutzers
```
http://localhost:8000/api/books?search=harry&popular=true
```
sucht die `FilterSchema`-Instanz nach beliebten Büchern, die `harry` entweder im Namen des Buchs _oder_ im Namen des Autors enthalten.


Dieses Verhalten können Sie über den Parameter `expression_connector` sowohl auf Feld- als auch auf Klassenebene anpassen:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

Der Expression-Connector kann die Werte `"OR"`, `"AND"` und `"XOR"` annehmen, wobei Letzterer erst ab Django 4.1 [unterstützt](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) wird.

Ein Request mit diesen Query-Parametern
```
http://localhost:8000/api/books?name=harry&active=true
```
... sucht also nach Büchern, die `harry` in ihrem Namen enthalten _oder_ selbst aktiv sind und von einem aktiven Verlag veröffentlicht wurden.


## Filtern nach None-Werten
Sie können `FilterSchema` anweisen, `None` als gültigen Wert zu behandeln, für den ebenfalls gefiltert wird.

Auf Feldebene lässt sich das über das Schlüsselwortargument `ignore_none` erreichen:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

Auf diese Weise enthält der Filter immer die Bedingung `tag=None`, wenn der Benutzer keinen anderen Wert für „`tag`" angibt.

Sie können dies auch für alle Felder auf einmal in der Konfiguration festlegen:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## Benutzerdefinierte Ausdrücke
Manchmal gibt es komplexe Filterszenarien, die sich nicht durch eine einzelne Feldannotation abbilden lassen.
Für solche Fälle können Sie Ihre Filterlogik für ein Feld als benutzerdefinierte Methode implementieren. Definieren Sie dazu einfach eine Methode mit dem Namen `filter_<fieldname>`, die einen Filterwert entgegennimmt und einen Q-Ausdruck zurückgibt:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
Solche Feldmethoden haben Vorrang vor dem, was in der `Field()`-Definition des jeweiligen Felds angegeben ist.
Falls das nicht ausreicht, können Sie Ihre eigene benutzerdefinierte Filterlogik für die gesamte `FilterSet`-Klasse in der Methode `custom_expression` implementieren:

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
Die Methode `custom_expression` hat Vorrang vor allen anderen oben beschriebenen Definitionen, einschließlich der Methoden `filter_<fieldname>`.

!!! done

    Die Reihe zu Eingabeparametern ist abgeschlossen! Fahren Sie mit dem nächsten Abschnitt fort: **[Responses verarbeiten](../response/index.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
