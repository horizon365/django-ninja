---
comments: true
---
# Pagination

**Django Ninja** est livré avec la prise en charge de la pagination. Cela vous permet de diviser de grands ensembles de résultats en pages séparées.


Pour appliquer la pagination à une fonction — appliquez simplement le décorateur `paginate` :

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


C'est tout !

Vous pouvez maintenant interroger les utilisateurs à l'aide des paramètres GET `limit` et `offset`

```
/api/users?limit=10&offset=0
```

Par défaut, la limite est définie sur `100` (vous pouvez la modifier dans votre settings.py à l'aide de `NINJA_PAGINATION_PER_PAGE`)


## Classes de pagination intégrées

### LimitOffsetPagination (par défaut)

C'est la classe de pagination par défaut (vous pouvez la modifier dans votre settings.py en pointant `NINJA_PAGINATION_CLASS` vers le chemin d'une classe)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

Exemple de requête :
```
/api/users?limit=10&offset=0
```

Cette classe possède deux paramètres d'entrée :

 - `limit` - définit le nombre de querysets sur une page (par défaut = 100, modifiable via NINJA_PAGINATION_PER_PAGE)
 - `offset` - définit le décalage de la fenêtre de page (par défaut : 0, l'indexation commence à 0)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

Exemple de requête :
```
/api/users?page=2
```

Cette classe possède un paramètre `page` et affiche par défaut 100 querysets par page (modifiable via settings.py)

La numérotation des pages commence à 1.

Vous pouvez également définir une valeur de taille de page personnalisée pour chaque vue individuellement :

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## Accès aux paramètres de pagination dans une fonction de vue

Si vous devez accéder aux paramètres `Input` utilisés pour la pagination dans votre fonction de vue — utilisez l'argument `pass_parameter`

Dans ce cas, les données d'entrée seront disponibles dans `**kwargs` :

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## Création d'une classe de pagination personnalisée

Pour créer une classe de pagination personnalisée, vous devez hériter de `ninja.pagination.PaginationBase` et redéfinir les classes de schéma `Input` et `Output` ainsi que la méthode `paginate_queryset(self, queryset, request, **params)` :

 - Le schéma `Input` est une classe de schéma qui décrit les paramètres qui doivent être passés au pagineur (tels que le numéro de page ou les valeurs limit/offset).
 - Le schéma `Output` décrit le schéma de la sortie de page (tels que count/next/items, etc.).
 - La méthode `paginate_queryset` reçoit le queryset initial et doit renvoyer un itérable contenant uniquement les données de la page demandée. La méthode accepte les paramètres suivants :
    - `queryset` : le queryset (ou itérable) renvoyé par la fonction d'API.
    - `pagination` - les paramètres paginator.Input (analysés et validés)
    - `**params` : arguments mot-clés qui contiendront tous les arguments que la fonction décorée reçoit.


Exemple :

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

Astuce : vous pouvez récupérer l'objet request à partir des paramètres :

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### Pagination asynchrone

Les classes de pagination standard de **Django Ninja** prennent en charge l'async. Si vous souhaitez gérer des requêtes asynchrones avec une classe de pagination personnalisée, vous devez hériter de `ninja.pagination.AsyncPaginationBase` et redéfinir la méthode `apaginate_queryset(self, queryset, request, **params)`.

### Attributs de sortie

Par défaut, les éléments de page sont placés dans l'attribut `'items'`. Pour modifier ce comportement, vous pouvez utiliser `items_attribute` :

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int

    items_attribute: str = "results"

```


## Application de la pagination à plusieurs opérations à la fois

Il arrive souvent que vous ayez besoin d'ajouter la pagination à toutes les vues qui renvoient des querysets ou des listes

Vous pouvez utiliser la classe de routeur intégrée (`RouterPaginated`) qui injectera automatiquement la pagination dans toutes les opérations définies avec `response=List[SomeSchema]` :

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

Dans cet exemple, les deux opérations auront la pagination activée.

Pour appliquer la pagination à l'instance principale de l'`api`, vous pouvez utiliser l'argument `default_router` :


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    Poursuivez avec le chapitre suivant ! **[Renderers de réponse](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
