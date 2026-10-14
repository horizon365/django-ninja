---
comments: true
---
# Paramètres des opérations

## Liés au schéma OpenAPI

Les paramètres suivants interagissent avec la manière dont le schéma OpenAPI (et la documentation) est généré.

### L'argument `tags`

Vous pouvez utiliser l'argument `tags` (`list[str]`) pour regrouper des opérations d'API.
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

Les opérations étiquetées peuvent être traitées différemment par divers outils et bibliothèques. Par exemple, Swagger UI utilise les tags pour regrouper les opérations affichées.

![Summary`](../img/operation_tags.png)

#### Tags de router

Vous pouvez utiliser l'argument `tags` pour appliquer des tags à toutes les opérations déclarées dans un router :

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### L'argument `summary`

Un nom lisible par l'humain pour votre opération.

Par défaut, il est généré en mettant en majuscule le nom de la fonction de votre opération :

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

Si vous souhaitez le remplacer ou le traduire dans une autre langue, vous pouvez utiliser l'argument `summary` dans le décorateur `api`.

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### L'argument `description`

Pour fournir plus d'informations sur votre opération, vous pouvez utiliser l'argument `description` ou une docstring Python simple :

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

Lorsque vous devez fournir une description longue et multi-lignes, vous pouvez utiliser des `docstrings` Python pour la définition de la fonction :

```python hl_lines="4 5 6 7"
@api.post("/orders/")
def create_order(request, order: Order):
    """
    To create an order please provide:
     - **first_name**
     - **last_name**
     - and **list of Items** *(product + amount)*
    """
    return {"success": True}

```

![`Summary`](../img/operation_description_docstring.png)


### L'argument `operation_id`

Le `operationId` d'OpenAPI est une chaîne de caractères unique et optionnelle utilisée pour identifier une opération. Si fournis, ces identifiants doivent être uniques parmi toutes les opérations décrites dans votre API.

Par défaut, **Django Ninja** le définit comme `nom du module` + `nom de la fonction`.

Si vous souhaitez le définir pour chaque opération individuellement, vous pouvez utiliser l'argument `operation_id` :

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

Si vous souhaitez remplacer le comportement global, vous pouvez dériver de l'instance NinjaAPI et redéfinir la méthode `get_openapi_operation_id`.

Elle sera appelée pour chaque opération que vous définissez, vous pouvez ainsi définir votre logique de nommage personnalisée de cette manière :
```python hl_lines="5 6 7 9"
from ninja import NinjaAPI

class MySuperApi(NinjaAPI):

    def get_openapi_operation_id(self, operation):
        # here you can access operation ( .path , .view_func, etc) 
        return ...

api = MySuperApi()

@api.get(...)
...
```

### L'argument `deprecated`

Marquez une opération comme dépréciée sans la supprimer en utilisant l'argument `deprecated` :

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

Elle sera marquée comme dépréciée dans le schéma JSON ainsi que dans la documentation OpenAPI interactive :

![Deprecated](../img/deprecated.png)

### L'argument `include_in_schema`

Si vous avez besoin d'inclure/d'exclure certaines opérations du schéma OpenAPI, vous pouvez utiliser l'argument `include_in_schema` :

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## L'argument `openapi_extra`
Vous pouvez personnaliser votre schéma OpenAPI pour un endpoint spécifique (voir [OpenAPI customization options](https://swagger.io/docs/specification/about/) pour plus de détails)
```python hl_lines="1 26"
# You can set requestBody from openapi_extra
@api.get(
    "/tasks",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["email"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "phone": {"type": "number"},
                            "email": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        }
    },
)
def some_operation(request):
    pass
    
# You can add additional responses to the automatically generated schema
@api.post(
    "/tasks",
    openapi_extra={
        "responses": {
            400: {
                "description": "Error Response",
            },
            404: {
                "description": "Not Found Response",
            },
        },
    },
)
def some_operation_2(request):
    pass

```


## Options de sortie de la réponse

Quelques arguments vous permettent d'ajuster la sortie de la réponse :
### `by_alias`

Indique si les alias de champs doivent être utilisés comme clés dans la réponse (par défaut `False`).

### `exclude_unset`

Indique si les champs qui n'ont pas été définis lors de la création du schéma et qui ont leur valeur par défaut doivent être exclus de la réponse (par défaut `False`).
### `exclude_defaults`

Indique si les champs qui sont égaux à leur valeur par défaut (qu'ils aient été définis ou non) doivent être exclus de la réponse (par défaut `False`).
### `exclude_none`

Indique si les champs qui sont égaux à `None` doivent être exclus de la réponse (par défaut `False`).

## url_name
Permet de définir le nom d'URL de l'endpoint d'API (en utilisant [l'inversion des noms d'URL de Django](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls))
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

Pour plus de détails, consultez le guide [Inverser les URLs](../guides/urls.md).


## Spécifier des serveurs
Si vous souhaitez spécifier un ou plusieurs serveurs pour la spécification OpenAPI, vous pouvez utiliser `servers` lors de l'initialisation de l'instance NinjaAPI :
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
Cela permettra de basculer entre les environnements lors de l'utilisation de la documentation OpenAPI interactive :
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
