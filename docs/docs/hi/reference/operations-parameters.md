---
comments: true
---
# Operations parameters

## OpenAPI schema से संबंधित

निम्नलिखित parameters इस बात के साथ interact करते हैं कि OpenAPI schema (और documentation) कैसे generate होती है।

### `tags` argument

आप API operations को group करने के लिए `tags` argument (`list[str]`) का इस्तेमाल कर सकते हैं।
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

Tag किए गए operations को विभिन्न tools और libraries अलग तरीके से handle कर सकती हैं। उदाहरण के लिए, Swagger UI दिखाए जाने वाले operations को group करने के लिए tags का इस्तेमाल करता है।

![Summary`](../img/operation_tags.png)

#### Router tags

आप किसी router में declare किए गए सभी operations पर tags लागू करने के लिए `tags` argument का इस्तेमाल कर सकते हैं:

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### `summary` argument

आपके operation का एक human-readable नाम।

डिफ़ॉल्ट रूप से, यह आपके operation के function नाम को capitalize करके generate किया जाता है:

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

अगर आप इसे override करना चाहते हैं या किसी दूसरी भाषा में translate करना चाहते हैं, तो आप `api` decorator में `summary` argument का इस्तेमाल कर सकते हैं।

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### `description` argument

अपने operation के बारे में अधिक जानकारी देने के लिए, आप `description` argument या एक साधारण Python docstring का इस्तेमाल कर सकते हैं:

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

जब आपको एक लंबा, multi-line description देना हो, तो आप function definition के लिए Python `docstrings` का इस्तेमाल कर सकते हैं:

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


### `operation_id` argument

OpenAPI का `operationId` एक optional, unique string होता है जिसका इस्तेमाल किसी operation की पहचान करने के लिए किया जाता है। अगर इसे दिया जाता है, तो ये IDs आपके API में वर्णित सभी operations में unique होनी चाहिए।

डिफ़ॉल्ट रूप से, **Django Ninja** इसे `module name` + `function name` पर set करता है।

अगर आप इसे हर operation के लिए अलग-अलग set करना चाहते हैं, तो आप `operation_id` argument का इस्तेमाल कर सकते हैं:

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

अगर आप global behavior को override करना चाहते हैं, तो आप NinjaAPI instance को subclass करके `get_openapi_operation_id` method को override कर सकते हैं।

इसे आपके द्वारा परिभाषित हर operation के लिए call किया जाएगा, इसलिए आप इस तरह अपनी custom naming logic set कर सकते हैं:
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

### `deprecated` argument

किसी operation को हटाए बिना deprecated के रूप में mark करने के लिए `deprecated` argument का इस्तेमाल करें:

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

JSON schema में और साथ ही interactive OpenAPI documentation में इसे deprecated के रूप में mark किया जाएगा:

![Deprecated](../img/deprecated.png)

### `include_in_schema` argument

अगर आपको OpenAPI schema में कुछ operations को include/exclude करना है, तो आप `include_in_schema` argument का इस्तेमाल कर सकते हैं:

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## `openapi_extra` argument
आप किसी specific endpoint के लिए अपना OpenAPI schema customize कर सकते हैं (विवरण के लिए [OpenAPI customization options](https://swagger.io/docs/specification/about/) देखें)
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


## Response output options

कुछ arguments ऐसे हैं जिनसे आप response के output को adjust कर सकते हैं:
### `by_alias`

क्या response में keys के रूप में field aliases का इस्तेमाल किया जाना चाहिए (डिफ़ॉल्ट `False` है)।

### `exclude_unset`

क्या उन fields को response से exclude किया जाए जो schema बनाते समय set नहीं किए गए थे और जिनकी value default है (डिफ़ॉल्ट `False` है)।
### `exclude_defaults`

क्या उन fields को response से exclude किया जाए जो अपनी default value के बराबर हैं (भले ही वे set किए गए हों) (डिफ़ॉल्ट `False` है)।
### `exclude_none`

क्या उन fields को response से exclude किया जाए जो `None` के बराबर हैं (डिफ़ॉल्ट `False` है)।

## url_name
आपको API endpoint का URL name set करने की सुविधा देता है ([Django के URL name reversing](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls) का इस्तेमाल करके)
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

अधिक जानकारी के लिए [Reversing URLs](../guides/urls.md) guide देखें।


## Servers specify करें
अगर आप OpenAPI specification के लिए एक या कई servers specify करना चाहते हैं, तो NinjaAPI instance initialize करते समय आप `servers` का इस्तेमाल कर सकते हैं:
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
इससे interactive OpenAPI documentation का इस्तेमाल करते समय environments के बीच switch करना संभव होगा:
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
