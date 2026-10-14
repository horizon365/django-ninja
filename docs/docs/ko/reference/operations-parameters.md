---
comments: true
---
# Operations parameters

## OpenAPI schema 관련

다음 파라미터들은 OpenAPI schema(및 문서)가 생성되는 방식과 상호작용합니다.

### `tags` 인자

`tags` 인자(`list[str]`)를 사용하여 API operation을 그룹화할 수 있습니다.
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

태그가 지정된 operation은 다양한 도구와 라이브러리에서 다르게 처리될 수 있습니다. 예를 들어, Swagger UI는 태그를 사용하여 표시되는 operation을 그룹화합니다.

![Summary`](../img/operation_tags.png)

#### Router tags

`tags` 인자를 사용하여 router에 선언된 모든 operation에 태그를 적용할 수 있습니다:

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### `summary` 인자

operation을 위한 사람이 읽을 수 있는 이름입니다.

기본적으로 operation 함수 이름을 대문자로 시작하도록 변환하여 생성됩니다:

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

이를 재정의하거나 다른 언어로 번역하고 싶다면, `api` 데코레이터에서 `summary` 인자를 사용할 수 있습니다.

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### `description` 인자

operation에 대한 더 많은 정보를 제공하려면, `description` 인자나 일반 Python docstring을 사용할 수 있습니다:

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

길고 여러 줄에 걸친 설명이 필요할 때는, 함수 정의에 Python `docstrings`를 사용할 수 있습니다:

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


### `operation_id` 인자

OpenAPI의 `operationId`는 operation을 식별하는 데 사용되는 선택적인 고유 문자열입니다. 제공하는 경우, 이러한 ID는 API에 정의된 모든 operation에서 고유해야 합니다.

기본적으로 **Django Ninja**는 이를 `module name` + `function name`으로 설정합니다.

각 operation에 개별적으로 설정하려면 `operation_id` 인자를 사용할 수 있습니다:

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

전역 동작을 재정의하려면 NinjaAPI 인스턴스를 서브클래싱하고 `get_openapi_operation_id` 메서드를 재정의하면 됩니다.

이 메서드는 정의하는 모든 operation에 대해 호출되므로, 다음과 같이 커스텀 명명 로직을 설정할 수 있습니다:
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

### `deprecated` 인자

operation을 제거하지 않고 사용 중단(deprecated)으로 표시하려면 `deprecated` 인자를 사용하세요:

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

JSON schema와 인터랙티브 OpenAPI 문서 모두에서 사용 중단으로 표시됩니다:

![Deprecated](../img/deprecated.png)

### `include_in_schema` 인자

특정 operation을 OpenAPI schema에 포함하거나 제외해야 하는 경우, `include_in_schema` 인자를 사용할 수 있습니다:

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## `openapi_extra` 인자
특정 endpoint에 대해 OpenAPI schema를 커스터마이즈할 수 있습니다 (자세한 내용은 [OpenAPI customization options](https://swagger.io/docs/specification/about/) 참조)
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


## Response 출력 옵션

response의 출력을 조정할 수 있는 몇 가지 인자가 있습니다:
### `by_alias`

필드 별칭(alias)을 response의 키로 사용할지 여부입니다 (기본값은 `False`).

### `exclude_unset`

schema를 생성할 때 설정되지 않았고 기본값을 가지는 필드를 response에서 제외할지 여부입니다 (기본값은 `False`).
### `exclude_defaults`

기본값과 동일한 필드(설정 여부와 무관)를 response에서 제외할지 여부입니다 (기본값은 `False`).
### `exclude_none`

`None`과 동일한 필드를 response에서 제외할지 여부입니다 (기본값은 `False`).

## url_name
API endpoint의 URL 이름을 설정할 수 있습니다 ([Django의 URL name reversing](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls) 사용)
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

자세한 내용은 [Reversing URLs](../guides/urls.md) 가이드를 참조하세요.


## servers 지정하기
OpenAPI specification에 하나 또는 여러 개의 server를 지정하고 싶다면, NinjaAPI 인스턴스를 초기화할 때 `servers`를 사용할 수 있습니다:
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
이를 통해 인터랙티브 OpenAPI 문서를 사용할 때 환경 간 전환이 가능합니다:
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
