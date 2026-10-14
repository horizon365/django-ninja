---
comments: true
---
# 操作のパラメータ

## OpenAPI スキーマに関連するパラメータ

以下のパラメータは、OpenAPI スキーマ（およびドキュメント）が生成される方法に影響します。

### `tags` 引数

`tags` 引数（`list[str]`）を使うと、API 操作をグループ化できます。
```python hl_lines="6"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}


@api.post("/orders/", tags=["orders"])
def create_order(request, order: Order):
    return {"success": True}
```

タグ付けされた操作は、さまざまなツールやライブラリによって異なる扱いを受けます。たとえば、Swagger UI はタグを使って表示される操作をグループ化します。

![Summary`](../img/operation_tags.png)

#### Router のタグ

`tags` 引数を使うと、router で宣言されたすべての操作にタグを適用できます：

```python
api.add_router("/events/", events_router, tags=["events"])

# or using constructor: 

router = Router(tags=["events"])
```


### `summary` 引数

操作の人間が読める名前です。

デフォルトでは、操作の関数名を大文字に変換したものが生成されます：

```python hl_lines="2"
@api.get("/hello/")
def hello(request, name: str):
    return {"hello": name}
```

![Summary`](../img/operation_summary_default.png)

上書きしたい場合や他の言語に翻訳したい場合は、`api` デコレーターで `summary` 引数を使えます。

```python hl_lines="1"
@api.get("/hello/", summary="Say Hello")
def hello(request, name: str):
    return {"hello": name}
```

![`Summary`](../img/operation_summary.png)

### `description` 引数

操作に関するより多くの情報を提供するには、`description` 引数または Python のプレーンな docstring を使えます：

```python hl_lines="1"
@api.post("/orders/", description="Creates an order and updates stock")
def create_order(request, order: Order):
    return {"success": True}
```

![`Summary`](../img/operation_description.png)

長い複数行の説明を提供したい場合は、関数定義に Python の `docstrings` を使えます：

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


### `operation_id` 引数

OpenAPI の `operationId` は、操作を識別するために使われるオプションの一意な文字列です。指定する場合、これらの ID は API に記述されたすべての操作の中で一意でなければなりません。

デフォルトでは、**Django Ninja** はこれを `モジュール名` + `関数名` に設定します。

操作ごとに個別に設定したい場合は、`operation_id` 引数を使えます：

```python hl_lines="2"
...
@api.post("/tasks", operation_id="create_task")
def new_task(request):
    ...
```

グローバルな動作を上書きしたい場合は、NinjaAPI インスタンスをサブクラス化して、`get_openapi_operation_id` メソッドをオーバーライドできます。

このメソッドは定義されたすべての操作に対して呼び出されるため、独自の命名ロジックを次のように設定できます：
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

### `deprecated` 引数

操作を削除せずに非推奨としてマークするには、`deprecated` 引数を使います：

```python hl_lines="1"
@api.post("/make-order/", deprecated=True)
def some_old_method(request, order: str):
    return {"success": True}
```

操作は JSON スキーマおよび対話型の OpenAPI ドキュメントの中で非推奨としてマークされます：

![Deprecated](../img/deprecated.png)

### `include_in_schema` 引数

特定の操作を OpenAPI スキーマに含めたり除外したりする必要がある場合は、`include_in_schema` 引数を使えます：

```python hl_lines="1"
@api.post("/hidden", include_in_schema=False)
def some_hidden_operation(request):
    pass
```

## `openapi_extra` 引数
特定のエンドポイント向けに OpenAPI スキーマをカスタマイズできます（詳細は [OpenAPI customization options](https://swagger.io/docs/specification/about/) を参照してください）
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


## レスポンス出力のオプション

レスポンスの出力を調整できる引数がいくつかあります：
### `by_alias`

レスポンスのキーとしてフィールドのエイリアスを使うかどうか（デフォルトは `False`）。

### `exclude_unset`

スキーマ作成時に設定されず、デフォルト値を持つフィールドをレスポンスから除外するかどうか（デフォルトは `False`）。
### `exclude_defaults`

デフォルト値と等しいフィールド（設定されたかどうかに関係なく）をレスポンスから除外するかどうか（デフォルトは `False`）。
### `exclude_none`

`None` と等しいフィールドをレスポンスから除外するかどうか（デフォルトは `False`）。

## url_name
API エンドポイントの URL 名を設定できます（[Django の URL 名の逆引き](https://docs.djangoproject.com/en/stable/topics/http/urls/#reversing-namespaced-urls) を利用します）
```python hl_lines="1 7"
@api.post("/tasks", url_name='tasks')
def some_operation(request):
    pass

# then you can get the url with

reverse('api-1.0.0:tasks')
```

詳細については、[URL の逆引き](../guides/urls.md) ガイドを参照してください。


## サーバーの指定
OpenAPI 仕様に 1 つまたは複数のサーバーを指定したい場合は、NinjaAPI インスタンスの初期化時に `servers` を使えます：
```python hl_lines="4 5 6 7"
from ninja import NinjaAPI

api = NinjaAPI(
        servers=[
            {"url": "https://stag.example.com", "description": "Staging env"},
            {"url": "https://prod.example.com", "description": "Production env"},
        ]
)
```
これにより、対話型の OpenAPI ドキュメントを使用する際に環境を切り替えられるようになります：
![Servers](../img/servers.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
