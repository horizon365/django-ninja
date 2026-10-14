---
comments: true
---
# ページネーション

**Django Ninja** にはページネーションのサポートが付属しています。これにより、大きな結果セットを個別のページに分割できます。


関数にページネーションを適用するには — 単に `paginate` デコレータを適用するだけです:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


これだけです！

これで、`limit` と `offset` の GET パラメータを使ってユーザーをクエリできます

```
/api/users?limit=10&offset=0
```

デフォルトでは、リミットは `100` に設定されています（settings.py の `NINJA_PAGINATION_PER_PAGE` で変更できます）


## 組み込みのページネーションクラス

### LimitOffsetPagination（デフォルト）

これはデフォルトのページネーションクラスです（settings.py の `NINJA_PAGINATION_CLASS` にクラスのパスを指定することで変更できます）

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

クエリの例:
```
/api/users?limit=10&offset=0
```

このクラスには 2 つの入力パラメータがあります:

 - `limit` - ページあたりのクエリセットの数を定義します（デフォルト = 100、NINJA_PAGINATION_PER_PAGE で変更可能）
 - `offset` - ページウィンドウのオフセットを設定します（デフォルト: 0、インデックスは 0 から始まります）


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

クエリの例:
```
/api/users?page=2
```

このクラスには `page` という 1 つのパラメータがあり、デフォルトではページあたり 100 件のクエリセットを出力します（settings.py で変更可能）

ページ番号は 1 から始まります。

ビューごとに個別のカスタムページサイズを設定することもできます:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## ビュー関数内でページネーションパラメータにアクセスする

ビュー関数内でページネーションに使用される `Input` パラメータにアクセスする必要がある場合は — `pass_parameter` 引数を使用します

その場合、入力データは `**kwargs` で利用可能になります:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## カスタムページネーションクラスの作成

カスタムページネーションクラスを作成するには、`ninja.pagination.PaginationBase` を継承し、`Input` と `Output` のスキーマクラス、および `paginate_queryset(self, queryset, request, **params)` メソッドをオーバーライドする必要があります:

 - `Input` スキーマは、ページネータに渡すべきパラメータ（ページ番号や limit/offset の値など）を記述するスキーマクラスです。
 - `Output` スキーマは、ページ出力のスキーマ（count/next/items など）を記述します。
 - `paginate_queryset` メソッドは初期のクエリセットを受け取り、リクエストされたページのデータのみを含むイテラブルを返す必要があります。このメソッドは次のパラメータを受け取ります:
    - `queryset`: API 関数が返したクエリセット（またはイテラブル）。
    - `pagination` - ページネータの Input パラメータ（パース・バリデーション済み）
    - `**params`: デコレートされた関数が受け取るすべての引数を含むキーワード引数。


例:

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

ヒント: パラメータからリクエストオブジェクトを取得できます:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### 非同期ページネーション

標準の **Django Ninja** ページネーションクラスは非同期をサポートしています。カスタムページネーションクラスで非同期リクエストを処理したい場合は、`ninja.pagination.AsyncPaginationBase` を継承し、`apaginate_queryset(self, queryset, request, **params)` メソッドをオーバーライドする必要があります。

### 出力属性

デフォルトでは、ページのアイテムは `'items'` 属性に配置されます。この動作をオーバーライドするには、`items_attribute` を使用します:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## 複数のオペレーションに一度にページネーションを適用する

クエリセットやリストを返すすべてのビューにページネーションを追加する必要があるケースはよくあります

組み込みのルータークラス（`RouterPaginated`）を使用できます。これは `response=List[SomeSchema]` で定義されたすべてのオペレーションに自動的にページネーションを注入します:

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

この例では、両方のオペレーションでページネーションが有効になります。

メインの `api` インスタンスにページネーションを適用するには、`default_router` 引数を使用します:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    次の章に進みましょう！ **[レスポンスレンダラー](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
