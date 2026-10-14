---
comments: true
---
## はじめに
JWT の存在はずっと以前から知っていましたが、実際に使ったことはありませんでした。最近、tus のレジュームアップロード（中断からの再開）プロトコルを調べているうちに、hooks-http のレベルまで踏み込みました。目的はファイルアップロード時の認証です。当然のことながら、`django-ninja-jwt` パッケージを思い浮かべました。簡単だろうと思っていましたが、[中国語ドキュメント](https://django-ninja.cn/django-ninja-jwt/)を読んでみると、簡単というよりは、驚くほど最低限の作りであることがわかりました。

## Getting Started

ガイドによれば、`dango-ninja-jwt` と `django-ninja-extra` をインストールし、`NinjaAPI` を `njaExtraAPI` に置き換えるだけで、たった 1 行で済みます。

```python
api.register_controllers(NinjaJWTDefaultController)
```

正直なところ、困惑させられます。

待ってください — まずはドキュメントを見てみましょう。3 つの新しいエンドポイントが現れます：`pair`、`refresh`、`verify` です。
![JWT swagger UI token](../img/jwt-token.png)
右上隅の鍵アイコンに注目してください。後で役に立ちます。`JWTAuth` 関数を使ったときにのみ表示されます。

### pair
最初は `pair` エンドポイントです。これは、ユーザー名とパスワードを提供すると、認証トークンとリフレッシュトークンが返されるという意味です。
リクエストボディの形式は次のとおりです：
```json
{
  "password": "string",
  "username": "string"
}
```
注意：ここでは `username` が下側に現れています。皆さんが想定しがちなものとは少し異なります。
Execute をクリックすると、次のようなものが得られます：
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
上記の `access` トークンは認証に使用できますが、デフォルトでは有効期限に制限があります。`refresh` トークンは `access` よりも長い有効期間を持ち、以前の `access` トークンの有効期限が切れた後に新しい `access` トークンを取得するために使用されます。
リフレッシュが行われると、以前の `access` トークンは無効化されます。

この時点で、`access` をコピーして右上隅の鍵アイコンに入力することができます。こうすることで、現在のページ上のすべてのエンドポイントでそれを使えるようになり、デバッグに便利です。
### verify
3 つ目のエンドポイント `verify` にアクセスして、`access` トークンが有効かどうかを確認できます。

全体として、`django-ninja-jwt` は単純に 3 つのエンドポイントを作ってくれるものであり、トークンの取得、リフレッシュ、テストを便利にしてくれます。

## カスタマイズ
これら 3 つのエンドポイントだけでは十分ではありません。少なくとも、自分たちの特定のエンドポイントに認証を追加する必要があります。
ここで必要なのは `JWTAuth` です。これを使って初めて鍵アイコンが表示されます。
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
そして `some` エンドポイントにも、独立した鍵アイコンが表示されます。
![JWT swagger UI token custom](../img/jwt-token-custom.png)
上記の `some` エンドポイントでは、認証に成功すると、現在ログインしているユーザーのユーザー名が応答として返されます。失敗した場合は 401 レスポンスが返されます。
バックエンド開発者は、フロントエンドチームにこの値を一緒に送るよう伝える必要があります。フロントエンド側は [pair](#pair) のセクションで取得し、定期的に [refresh](#refresh) でリフレッシュするようにします。

### トークンの有効期間を設定する

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### さらなるカスタマイズ
ninja のルートで `@route.get('/some', auth=JWTAuth())` を使うだけではニーズを満たせない場合、関数内で `authenticate` を呼び出すことができます。

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # 失敗した場合は内部で 401 が発生します
    if auth.authenticate(request, token):
        return request.auth.username

```
上記の `token` は、`request` オブジェクトから自分で取り出す必要があります。
