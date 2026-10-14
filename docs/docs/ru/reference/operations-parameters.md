---
comments: true
---
# Параметры операций

## Связанные со схемой OpenAPI

Следующие параметры влияют на то, как генерируется схема OpenAPI (и документация).

### Аргумент `tags`

Вы можете использовать аргумент `tags` (`list[str]`) для группировки операций API.
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

Помеченные тегами операции могут по-разному обрабатываться различными инструментами и библиотеками. Например, Swagger UI использует теги для группировки отображаемых операций.

![Summary`](../img/operation_tags.png)

#### Теги роутера

Вы можете использовать аргумент `tags`, чтобы применить теги ко всем операциям, объявленным в роутере:

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### Аргумент `summary`

Понятное человеку название для вашей операции.

По умолчанию оно генерируется путём капитализации имени функции вашей операции:

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

Если вы хотите переопределить его или перевести на другой язык, вы можете использовать аргумент `summary` в декораторе `api`.

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### Аргумент `description`

Чтобы предоставить больше информации о вашей операции, вы можете использовать аргумент `description` или обычный Python-docstring:

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

Когда вам нужно предоставить длинное многострочное описание, вы можете использовать Python `docstrings` в определении функции:

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


### Аргумент `operation_id`

`operationId` в OpenAPI — это необязательная уникальная строка, используемая для идентификации операции. Если она указана, эти идентификаторы должны быть уникальными среди всех операций, описанных в вашем API.

По умолчанию **Django Ninja** устанавливает её как `имя модуля` + `имя функции`.

Если вы хотите задать её для каждой операции отдельно, вы можете использовать аргумент `operation_id`:

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

Если вы хотите переопределить глобальное поведение, вы можете создать подкласс NinjaAPI и переопределить метод `get_openapi_operation_id`.

Он будет вызываться для каждой определённой вами операции, так что вы можете задать свою собственную логику именования таким образом:
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

### Аргумент `deprecated`

Пометить операцию как устаревшую, не удаляя её, можно с помощью аргумента `deprecated`:

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

Операция будет помечена как устаревшая как в JSON-схеме, так и в интерактивной документации OpenAPI:

![Deprecated](../img/deprecated.png)

### Аргумент `include_in_schema`

Если вам нужно включить/исключить определённые операции из схемы OpenAPI, вы можете использовать аргумент `include_in_schema`:

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## Аргумент `openapi_extra`
Вы можете настроить схему OpenAPI для конкретного endpoint-а (подробнее см. [OpenAPI customization options](https://swagger.io/docs/specification/about/))
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


## Параметры вывода ответа

Есть несколько аргументов, которые позволяют настроить вывод ответа:
### `by_alias`

Следует ли использовать алиасы полей в качестве ключей в ответе (по умолчанию `False`).

### `exclude_unset`

Следует ли исключать из ответа поля, которые не были установлены при создании схемы и имеют значение по умолчанию (по умолчанию `False`).
### `exclude_defaults`

Следует ли исключать из ответа поля, равные значению по умолчанию (независимо от того, были ли они установлены) (по умолчанию `False`).
### `exclude_none`

Следует ли исключать из ответа поля, равные `None` (по умолчанию `False`).

## url_name
Позволяет задать имя URL для endpoint-а API (с использованием [Django's URL name reversing](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls))
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

Подробнее см. руководство [Reversing URLs](../guides/urls.md).


## Указание серверов
Если вы хотите указать один или несколько серверов для спецификации OpenAPI, вы можете использовать `servers` при инициализации экземпляра NinjaAPI:
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
Это позволит переключаться между окружениями при использовании интерактивной документации OpenAPI:
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
