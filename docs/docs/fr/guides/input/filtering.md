---
comments: true
---
# Filtrage

Si vous souhaitez permettre aux utilisateurs de filtrer vos querysets selon plusieurs attributs différents, il est judicieux d'encapsuler vos filtres dans une classe `FilterSchema`.
`FilterSchema` est un `Schema` ordinaire, il utilise donc toutes les fonctionnalités nécessaires de Pydantic, mais il ajoute également des commodités
pour convertir facilement les paramètres de filtrage destinés aux utilisateurs en requêtes de base de données.

Tout d'abord, définissez une sous-classe de `FilterSchema` :

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


Ensuite, utilisez ce schéma avec `Query` dans votre gestionnaire d'API :
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Tout comme décrit dans [Utiliser un Schema pour définir les paramètres de requête](./query-params.md#using-schema), Django Ninja transforme les champs définis dans `BookFilterSchema` en paramètres de requête.
Vous pouvez utiliser le raccourci d'une ligne `.filter()` pour appliquer ces filtres à votre queryset :
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Sous le capot, `FilterSchema` convertit ses champs en [expressions Q](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects), puis les combine et les utilise pour filtrer votre queryset.


Alternativement, au lieu d'utiliser la méthode `.filter`, vous pouvez récupérer l'expression `Q` préparée et effectuer le filtrage vous-même.
Cela peut être utile lorsque vous avez un filtrage de queryset supplémentaire au-delà de ce que vous exposez aux utilisateurs via l'API :
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)

    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

Par défaut, les filtres se comporteront comme suit :

* Les valeurs `None` seront ignorées et aucun filtrage ne sera appliqué ;
* Chaque champ non-`None` sera converti en une expression `Q` selon la définition `Field` de chaque champ ;
* Toutes les expressions `Q` seront combinées en une seule à l'aide de l'opérateur logique `AND` ;
* L'expression `Q` résultante est utilisée pour filtrer le queryset, et un queryset avec la clause `.filter` appliquée vous est renvoyé.

## Champs personnalisés
Par défaut, `FilterSet` utilise le nom du champ pour générer l'expression Q :
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
Le champ `name` sera converti en une expression `Q(name=...)`.

Lorsque votre recherche en base de données est plus complexe que cela, vous pouvez les spécifier explicitement à l'aide de l'argument mot-clé `"q"` dans la définition du champ :
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
```
Vous pouvez même spécifier plusieurs noms d'arguments mot-clés de recherche sous forme de liste :
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains'])
```
Par défaut, les expressions au niveau des champs sont combinées à l'aide du connecteur `"OR"`, donc avec la configuration ci-dessus, un paramètre de requête `?search=foobar` recherchera les livres contenant « foobar » dans leur nom, leur auteur ou leur éditeur.


## Combinaison des expressions
Par défaut,

* les expressions au niveau des champs sont combinées à l'aide de l'opérateur `OR`.
* les champs eux-mêmes sont combinés à l'aide de l'opérateur `AND`.

Ainsi, pour le `FilterSchema` suivant...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...et les paramètres de requête suivants d'un utilisateur
```
http://localhost:8000/api/books?search=harry&popular=true
```
L'instance `FilterSchema` recherchera les livres populaires contenant `harry` dans le nom du livre _ou_ de l'auteur.


Vous pouvez personnaliser ce comportement à l'aide du paramètre `expression_connector` dans les définitions au niveau des champs et au niveau de la classe :
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')

    class Config:
        expression_connector = 'OR'
```

Le connecteur d'expressions peut prendre les valeurs `"OR"`, `"AND"` et `"XOR"`, mais ce dernier n'est [pris en charge](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) qu'à partir de Django 4.1.

Désormais, une requête avec ces paramètres de requête
```
http://localhost:8000/api/books?name=harry&active=true
```
...recherchera les livres qui ont `harry` dans leur nom _ou_ qui sont eux-mêmes actifs et publiés par un éditeur actif.


## Filtrage par valeurs None
Vous pouvez faire en sorte que `FilterSchema` traite `None` comme une valeur valide pour laquelle le filtrage doit être effectué.

Cela peut être fait au niveau du champ via l'argument mot-clé `ignore_none` :
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

De cette façon, lorsque l'utilisateur ne fournit pas d'autre valeur pour `"tag"`, le filtre inclura toujours la condition `tag=None`.

Vous pouvez également le spécifier pour tous les champs à la fois dans la configuration :
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)

    class Config:
        ignore_none = False
```


## Expressions personnalisées
Parfois, vous pouvez avoir des scénarios de filtrage complexes qui ne peuvent pas être gérés par une simple annotation de champ.
Pour de tels cas, vous pouvez implémenter votre logique de filtrage de champ sous forme de méthode personnalisée. Définissez simplement une méthode nommée `filter_<nomduchamp>` qui accepte une valeur de filtrage et renvoie une expression Q :

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None

    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
Ces méthodes de champ ont la priorité sur ce qui est spécifié dans la définition `Field()` du champ correspondant.
Si cela ne suffit pas, vous pouvez implémenter votre propre logique de filtrage personnalisée pour l'ensemble de la classe `FilterSet` dans la méthode `custom_expression` :

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
La méthode `custom_expression` a la priorité sur toute autre définition décrite ci-dessus, y compris les méthodes `filter_<nomduchamp>`.

!!! done

    La série sur les paramètres d'entrée est terminée ! Poursuivez avec la section suivante **[Gestion des réponses](../response/index.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
