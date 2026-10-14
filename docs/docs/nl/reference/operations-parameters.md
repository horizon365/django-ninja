---
comments: true
---
# Parameters voor operaties

## Gerelateerd aan het OpenAPI-schema

De volgende parameters hebben invloed op de manier waarop het OpenAPI-schema (en de documentatie) wordt gegenereerd.

### Het argument `tags`

Je kunt het argument `tags` (`list[str]`) gebruiken om API-operaties te groeperen.
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

Getagde operaties kunnen door verschillende tools en bibliotheken anders worden behandeld. Swagger UI gebruikt tags bijvoorbeeld om de getoonde operaties te groeperen.

![Summary`](../img/operation_tags.png)

#### Router-tags

Je kunt het argument `tags` gebruiken om tags toe te passen op alle operaties die in een router zijn gedeclareerd:

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### Het argument `summary`

Een voor mensen leesbare naam voor je operatie.

Standaard wordt deze gegenereerd door de functienaam van je operatie met een hoofdletter te beginnen:

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

Als je deze wilt overschrijven of naar een andere taal wilt vertalen, kun je het argument `summary` in de `api`-decorator gebruiken.

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### Het argument `description`

Om meer informatie over je operatie te geven, kun je het argument `description` gebruiken of een gewone Python docstring:

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

Wanneer je een lange beschrijving over meerdere regels wilt geven, kun je Python `docstrings` gebruiken bij de functiedefinitie:

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


### Het argument `operation_id`

De `operationId` van OpenAPI is een optionele, unieke tekenreeks die wordt gebruikt om een operatie te identificeren. Indien opgegeven, moeten deze ID's uniek zijn voor alle operaties die in je API worden beschreven.

Standaard stelt **Django Ninja** dit in op `module name` + `function name`.

Als je dit per operatie afzonderlijk wilt instellen, kun je het argument `operation_id` gebruiken:

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

Als je het globale gedrag wilt overschrijven, kun je een subklasse van de NinjaAPI-instantie maken en de methode `get_openapi_operation_id` overschrijven.

Deze wordt aangeroepen voor elke operatie die je definieert, zodat je op deze manier je eigen naamgevingslogica kunt instellen:
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

### Het argument `deprecated`

Markeer een operatie als verouderd zonder deze te verwijderen, door het argument `deprecated` te gebruiken:

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

Deze wordt gemarkeerd als verouderd in het JSON-schema en in de interactieve OpenAPI-documentatie:

![Deprecated](../img/deprecated.png)

### Het argument `include_in_schema`

Als je bepaalde operaties wilt opnemen in/uitsluiten van het OpenAPI-schema, kun je het argument `include_in_schema` gebruiken:

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## Het argument `openapi_extra`
Je kunt je OpenAPI-schema voor een specifiek endpoint aanpassen (zie [OpenAPI customization options](https://swagger.io/docs/specification/about/) voor details)
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


## Opties voor de response-uitvoer

Er zijn enkele argumenten waarmee je de uitvoer van de response kunt aanpassen:
### `by_alias`

Of veld-aliassen als sleutels in de response moeten worden gebruikt (standaard is `False`).

### `exclude_unset`

Of velden die niet zijn ingesteld bij het aanmaken van het schema en de standaardwaarde hebben, moeten worden uitgesloten van de response (standaard is `False`).
### `exclude_defaults`

Of velden die gelijk zijn aan hun standaardwaarde (ongeacht of ze zijn ingesteld) moeten worden uitgesloten van de response (standaard is `False`).
### `exclude_none`

Of velden die gelijk zijn aan `None` moeten worden uitgesloten van de response (standaard is `False`).

## url_name
Hiermee kun je de URL-naam van het API-endpoint instellen (met behulp van [Django's URL name reversing](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls))
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

Zie voor meer details de handleiding [Reversing URLs](../guides/urls.md).


## Servers opgeven
Als je een of meerdere servers wilt opgeven voor de OpenAPI-specificatie, kun je `servers` gebruiken bij het initialiseren van de NinjaAPI-instantie:
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
Dit maakt het mogelijk om te schakelen tussen omgevingen bij gebruik van de interactieve OpenAPI-documentatie:
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
