---
comments: true
---
# Operationsparameter

## Mit Bezug auf das OpenAPI-Schema

Die folgenden Parameter beeinflussen die Art und Weise, wie das OpenAPI-Schema (und die Dokumentation) generiert wird.

### Das Argument `tags`

Sie können das Argument `tags` (`list[str]`) verwenden, um API-Operationen zu gruppieren.
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

Operationen mit Tags können von verschiedenen Tools und Bibliotheken unterschiedlich behandelt werden. Beispielsweise verwendet Swagger UI Tags, um die angezeigten Operationen zu gruppieren.

![Summary`](../img/operation_tags.png)

#### Router-Tags

Sie können das Argument `tags` verwenden, um alle in einem Router deklarierten Operationen mit Tags zu versehen:

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### Das Argument `summary`

Ein menschenlesbarer Name für Ihre Operation.

Standardmäßig wird er erzeugt, indem der Funktionsname Ihrer Operation großgeschrieben wird:

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

Wenn Sie ihn überschreiben oder in eine andere Sprache übersetzen möchten, können Sie das Argument `summary` im `api`-Decorator verwenden.

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### Das Argument `description`

Um weitere Informationen zu Ihrer Operation bereitzustellen, können Sie das Argument `description` oder einen einfachen Python-Docstring verwenden:

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

Wenn Sie eine lange, mehrzeilige Beschreibung angeben müssen, können Sie Python-`docstrings` für die Funktionsdefinition verwenden:

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


### Das Argument `operation_id`

OpenAPIs `operationId` ist eine optionale, eindeutige Zeichenfolge zur Identifizierung einer Operation. Falls angegeben, müssen diese IDs über alle in Ihrer API beschriebenen Operationen hinweg eindeutig sein.

Standardmäßig setzt **Django Ninja** ihn auf `Modulname` + `Funktionsname`.

Wenn Sie ihn für jede Operation einzeln festlegen möchten, können Sie das Argument `operation_id` verwenden:

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

Wenn Sie das globale Verhalten überschreiben möchten, können Sie die NinjaAPI-Instanz ableiten und die Methode `get_openapi_operation_id` überschreiben.

Sie wird für jede von Ihnen definierte Operation aufgerufen, sodass Sie auf diese Weise Ihre eigene Namenslogik festlegen können:
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

### Das Argument `deprecated`

Markieren Sie eine Operation als veraltet, ohne sie zu entfernen, indem Sie das Argument `deprecated` verwenden:

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

Sie wird sowohl im JSON-Schema als auch in der interaktiven OpenAPI-Dokumentation als veraltet markiert:

![Deprecated](../img/deprecated.png)

### Das Argument `include_in_schema`

Wenn Sie bestimmte Operationen aus dem OpenAPI-Schema ein- oder ausschließen möchten, können Sie das Argument `include_in_schema` verwenden:

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## Das Argument `openapi_extra`
Sie können Ihr OpenAPI-Schema für einen bestimmten Endpoint anpassen (Details siehe [Anpassungsoptionen für OpenAPI](https://swagger.io/docs/specification/about/))
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


## Optionen für die Response-Ausgabe

Es gibt einige Argumente, mit denen Sie die Ausgabe der Response anpassen können:
### `by_alias`

Ob Feld-Aliase als Schlüssel in der Response verwendet werden sollen (Standard ist `False`).

### `exclude_unset`

Ob Felder, die beim Erstellen des Schemas nicht gesetzt wurden und deren Standardwert haben, aus der Response ausgeschlossen werden sollen (Standard ist `False`).
### `exclude_defaults`

Ob Felder, die ihrem Standardwert entsprechen (unabhängig davon, ob sie gesetzt wurden), aus der Response ausgeschlossen werden sollen (Standard ist `False`).
### `exclude_none`

Ob Felder, die `None` entsprechen, aus der Response ausgeschlossen werden sollen (Standard ist `False`).

## url_name
Ermöglicht das Festlegen des URL-Namens des API-Endpoints (unter Verwendung von [Djangos URL-Namen-Auflösung](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls))
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

Weitere Details finden Sie im Leitfaden [URLs auflösen](../guides/urls.md).


## Server angeben
Wenn Sie einen oder mehrere Server für die OpenAPI-Spezifikation angeben möchten, können Sie `servers` beim Initialisieren der NinjaAPI-Instanz verwenden:
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
Dies ermöglicht das Umschalten zwischen Umgebungen bei Verwendung der interaktiven OpenAPI-Dokumentation:
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
