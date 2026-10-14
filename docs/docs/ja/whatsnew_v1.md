---
comments: true
---
# Django Ninja 1.0 へようこそ


はじめに、次のコマンドで最新バージョンをインストールしてください：
```
pip install -U django-ninja
```

django-ninja v1 は Python 3.7 以上と互換性があります。


Django Ninja 0.x 系列は引き続きサポートされますが、セキュリティアップデートと重大なバグ修正のみが提供されます。


✨ Django Ninja 1.0 の新機能

## Pydantic2 サポート

Pydantic バージョン 2 は Rust で書き直され、次のような多くの改善と機能が含まれています：

 - より安全な型。
 - より優れた拡張性。
 - より高いパフォーマンス。

私たちのテストによると、平均的なプロジェクトでは平均して約 10% のパフォーマンス向上が見込め、一部のエッジケースのパース/シリアライゼーションシナリオでは 4 倍の高速化が得られます。
一方で、破壊的な変更ももたらされます — pydantic 1 と 2 は完全には互換性がありません — しかし、私たちはこの移行をできる限り簡単にするよう努めました。
'Schema' クラスを使っていたのであれば、ninja v1 への移行は簡単なはずです。そうでない場合は、[pydantic の移行ガイド](https://pydantic.com.cn/migration/) に従ってください。


pydantic2 が提供するいくつかの新機能

### pydantic コンテキスト

Pydantic は検証およびシリアライゼーション時にコンテキストをサポートするようになりました。Django Ninja はリクエストとレスポンスの処理中に "request" オブジェクトを渡します。
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

レスポンスフェーズでは、"response_code" もコンテキストに渡されます。

## Schema.Meta

Pydantic は BaseModel.Config クラスを非推奨にしました。しかし、Django の他の部分との一貫性を保つため、ModelSchema 向けに "Meta" クラスを導入しました — Django の ModelForms と同様に動作します：
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

（"Config" クラスは引き続きサポートされていますが、非推奨になりました）


## より短く/よりクリーンなパラメータ構文

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

これは次の代わりに使えます：

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

または

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


これは次の代わりに使えます：

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



さらに、エディターでの自動補完機能もすべて利用できます。


一方で、**古い構文も引き続きサポートされています** ので、プロジェクトを最新の django-ninja バージョンへ簡単に移行できます。


#### + Annotated

typing.Annotated もサポートされるようになりました：

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## 非同期認証のサポート

ついに非同期の認証クラスがサポートされました。必要なのは `authenticate` メソッドに `async` を追加するだけです：

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## CSRF の動作変更


Cookie ベースの認証を使う場合、`csrf=True` は不要になりました。代わりに、CSRF 保護が自動的に有効化されます。これにより、CSRF 保護付きの認証クラスと、Cookie を必要としない他の認証方法を混在させることもできます：

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## ドキュメント

ドキュメントビューアーが設定可能かつプラグイン可能になりました。デフォルトでは、django-ninja には Swagger と Redoc が同梱されています：
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

ユーザーは `DocsBase` クラスを継承して、カスタムのドキュメントビューアーを作成できるようになりました。

## Router

add_router は文字列パスをサポートするようになりました：

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## デコレーター

django-ninja が .get/.post などでビューをデコレートするとき、関数の結果をラップします（ほとんどの場合 HttpResponse ではなく、シリアライズ可能なオブジェクトです）。そのため、一部の組み込みやサードパーティのデコレーターとは動作しない可能性があります。たとえば：
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
この例は動作しません。

現在の django-ninja では、HTTP レスポンスと連携するデコレーターを注入できる decorate_view デコレーターが導入されました：
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## ページネーション

`paginate_queryset` メソッドが `request` オブジェクトを受け取れるようになりました


#### 後方互換性のない変更
 - resolve_xxx(self, ...) - (self) の解決のサポートは非推奨となり、pydantic の組み込み機能が推奨されます。
 - pydantic v1 はサポートされなくなりました
 - python 3.6 はサポートされなくなりました

ちなみに - このプロジェクトを気に入っていて、まだ GitHub スターを付けていないなら、ぜひ付けてください！ [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
