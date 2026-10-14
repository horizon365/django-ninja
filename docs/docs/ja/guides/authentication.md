---
comments: true
---
# 認証

## はじめに

**Django Ninja** は、<a href="https://swagger.io/docs/specification/authentication/" target="_blank">セキュリティ仕様のすべて</a>を学習することなく、認証と認可を標準的な方法で簡単かつ迅速に処理できるよう支援するツールを複数提供しています。

基本的な考え方は、API オペレーションを記述するときに認証オブジェクトを定義できるというものです。
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

この例では、クライアントは Django のセッション認証（デフォルトでは Cookie ベース）を使用した場合にのみ `pets` メソッドを呼び出すことができ、そうでない場合は HTTP-401 エラーが返されます。
スーパーユーザーのみを許可したい場合は、代わりに `from ninja.security import django_auth_superuser` を使用できます。
## 自動 OpenAPI スキーマ

次の例では、クライアントが認証のためにヘッダーを渡す必要があります:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

次に、<a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> のドキュメントにアクセスしてください。


![Swagger UI Auth](../img/auth-swagger-ui.png)

**Authorize** ボタンをクリックすると、認証トークンの入力を求められます。

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

テストコールを実行すると、すべてのリクエストに認証ヘッダーが付与されます。

## グローバル認証

API の**すべての**メソッドを保護する必要がある場合は、`auth` 引数を `NinjaAPI` コンストラクタに渡します:


```python hl_lines="11 19"
from ninja import NinjaAPI, Form
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI(auth=GlobalAuth())

# @api.get(...)
# def ...

# @api.post(...)
# def ...
```

また、一部のメソッドをオーバーライドする必要がある場合は、オペレーションレベルで `auth` 引数を渡すことで再度指定できます。この例では、`/token` オペレーションでは認証が無効になります:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## 利用可能な認証オプション

### カスタム関数


"`auth=`" 引数は任意の callable を受け付けます。**NinjaAPI** は、callable が **truthy**（ブール値の `True` に変換される）な値を返した場合にのみ認証を行います。この戻り値は `request.auth` 属性に割り当てられます。

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API キー

API によっては認可に API キーを使用するものがあります。API キーとは、クライアントが API 呼び出し時に自分自身を識別するために提供するトークンです。キーはクエリ文字列で送信できます:
```
GET /something?api_key=abcdef12345
```

またはリクエストヘッダーとして:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

または Cookie として:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** には、こうした状況に対応するための組み込みクラスが用意されています。


#### クエリ内（In Query）

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

この例では、`GET['api_key']` からトークンを取得し、データベース内の対応する `Client` を検索します。Client インスタンスは `request.auth` 属性として設定されます。

注: **`param_name`** はチェック対象の GET パラメータの名前です。設定しない場合、デフォルトの `"key"` が使用されます。


#### ヘッダー内（In Header）

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### Cookie 内（In Cookie）

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### HTTP Basic 認証

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## 複数の認証クラス

**`auth`** 引数には複数の認証クラスを渡すこともできます:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

この場合、**Django Ninja** はまず `GET` から API キーをチェックし、設定されていないか無効な場合は `header` キーをチェックします。
両方とも無効な場合は、認証エラーがレスポンスとして発生します。


## ルーターの認証

ルーターに `auth` 引数を使用すると、そのルーター内で宣言されたすべてのオペレーションに認証クラスを適用できます:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

またはルーターのコンストラクタでも指定できます
```python
router = Router(auth=BasicAuth())
```


## カスタム例外

例外ハンドラを持つ例外を発生させると、オペレーションと同じようにそのハンドラのレスポンスが返されます:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## 非同期認証

**Django Ninja** は非同期認証を基本的にサポートしています。デフォルトの認証クラスは非同期対応ではありませんが、独自の非同期認証 callable を定義して `auth` に渡すことは可能です。

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


詳細については、[エラーハンドリング](errors.md) を参照してください。

!!! success

    次のセクション **[テスト](testing.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
