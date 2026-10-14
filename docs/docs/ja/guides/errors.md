---
comments: true
---
# エラーハンドリング

**Django Ninja** では、カスタム例外ハンドラをインストールして、エラーやハンドルされた例外が発生した際のレスポンスの返し方を制御できます。

## カスタム例外ハンドラ

特定の時刻に利用不可になるように設計された外部サービスに依存する API を構築しているとします。例外が発生したときにデフォルトの 500 エラーを投げる代わりに、そのエラーを処理してクライアントに親切なレスポンス（後でもう一度来るように伝えるなど）を返すことができます。
これを実現するには、次のようにします:

 - 1) 何らかの例外を作成する（または既存のものを使用する）
 - 2) api.exception_handler デコレータを使用する


例:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

例外ハンドラ関数は 2 つの引数を受け取ります:

 - **request** - Django の HTTP リクエスト
 - **exc** - 実際の例外

この関数は HTTP レスポンスを返す必要があります

## デフォルトの例外ハンドラをオーバーライドする

デフォルトでは、**Django Ninja** は次の例外ハンドラを初期化します:


#### `ninja.errors.AuthenticationError`

認証データが無効な場合に発生します

#### `ninja.errors.ValidationError`

リクエストデータがバリデーションに失敗した場合に発生します

#### `ninja.errors.HttpError`

コードのどこからでもステータスコード付きの HTTP エラーを発生させるために使用します
#### `django.http.Http404`

Django のデフォルトの 404 例外（たとえば get_object_or_404 を使用して返せます）
#### `Exception`

アプリケーションで処理されなかったその他のすべての例外。
デフォルトの動作

  - **`settings.DEBUG` が `True` の場合** - プレーンテキストでトレースバックを返します（コンソールや Swagger UI でのデバッグに便利）
  - **それ以外** - Django のデフォルトの例外処理メカニズムを使用します（エラーログの記録、ADMINS へのメール送信）


### デフォルトハンドラのオーバーライド

バリデーションエラーのデフォルト出力を変更する必要がある場合は - ValidationError 例外ハンドラをオーバーライドします:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## 例外による HTTP レスポンスの送出

カスタム例外を作成してハンドラを書く代わりの方法として - HTTP 例外を発生させることもできます。これにより、望みのコードを持つ HTTP レスポンスが返されます

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    次のセクション **[URL の逆引き](urls.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
