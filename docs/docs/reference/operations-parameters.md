---
comments: true
---
# 操作参数

## 与 OpenAPI 模式相关

以下参数与 OpenAPI 模式（及文档）的生成方式相互作用。

### 参数`tags`

你可以使用 `tags` 参数  (`list[str]`) 对 API 操作进行分组。
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

带标签的操作可能会被各种工具和库以不同方式处理。例如，Swagger UI 使用标签对显示的操作进行分组。

![Summary`](../img/operation_tags.png)

#### 路由器标签

你可以使用 `tags` 参数将标签应用于路由器声明的所有操作：

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### 参数`summary`

你的操作的一个人类可读的名称。

默认情况下，它是通过将你的操作函数名称大写生成的：

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

如果你想覆盖它或将其翻译成其他语言，可以在 `api` 装饰器中使用 `summary` 参数。

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### 参数`description`

要提供关于你的操作的更多信息，可以使用 `description` 参数或普通的 Python 文档字符串：

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

当你需要提供一个长的多行描述时，你可以为函数定义使用 Python `docstrings` :

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


### 参数`operation_id`

OpenAPI 的 `operationId` 是一个可选的唯一字符串，用于标识一个操作。如果提供，这些 ID 必须在你的 API 中描述的所有操作中是唯一的。

默认情况下， **Django Ninja** 将其设置为 `模块名称` + `函数名称`.

如果你想为每个操作单独设置，可以使用 `operation_id` 参数:

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

如果你想覆盖全局行为，你可以继承 NinjaAPI 实例并覆盖 `get_openapi_operation_id` 方法。

它将为你定义的每个操作调用，所以你可以这样设置你的自定义命名逻辑：
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

### 参数`deprecated`

通过使用 `deprecated` 参数标记一个操作已弃用而不删除它：

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

它将在 JSON 模式以及交互式 OpenAPI 文档中被标记为已弃用：

![Deprecated](../img/deprecated.png)

### 参数`include_in_schema`

如果你需要从 OpenAPI 模式中包含/排除某些操作，可以使用 `include_in_schema` 参数:

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## 参数 `openapi_extra`
您可以针对特定端点自定义您的 OpenAPI 模式(详细信息请参阅 [OpenAPI 自定义选项](https://swagger.io/docs/specification/about/))
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


## 响应输出选项

有几个参数可让您调整响应的输出：
### `by_alias`

字段别名是否应在响应中用作键（默认为 `False`）。

### `exclude_unset`

在创建模式时未设置且具有其默认值的字段是否应从响应中排除（默认为 `False`）。
### `exclude_defaults`

等于其默认值（无论是否设置）的字段是否应从响应中排除（默认为 `False`）。
### `exclude_none`

等于 `None` 的字段是否应从响应中排除（默认为 `False`）。

## url_name
允许您设置 API 端点网址名称 (使用 [django 路径的命名](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls))
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

有关更多详细信息，请参阅[网址的反向解析](../guides/urls.md) 指南。


## 指定服务器
如果您想为 OpenAPI 规范指定单个或多个服务器，在初始化 NinjaAPI 实例时可以使用 `servers`：
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
这将允许在使用交互式 OpenAPI 文档时在环境之间切换：
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
