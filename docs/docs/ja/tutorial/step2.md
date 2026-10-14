---
comments: true
---
# チュートリアル - 入力パラメータの扱い

## クエリ文字列からパラメータを渡す

URL のクエリ文字列から name を受け取るように操作を修正してみましょう。そのためには、関数に `name` 引数を追加するだけです。

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

名前付き引数を渡すと、期待どおりの（HTTP 200 の）レスポンスが得られます。

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a>：

```json
"Hello you"
```

### デフォルト値

パラメータを渡さないと、HTTP 422 のエラーレスポンスが返されます。

*[HTTP 422]: Unprocessable Entity（処理できないエンティティ）

<a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a>：

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

`name` 引数にデフォルト値を指定して、渡されなかった場合に備えることもできます：

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## 入力の型

**Django Ninja** は標準の [Python 型ヒント](https://docs.python.org/3/library/typing.html) を使って入力の型を指定します。型が指定されない場合は文字列とみなされます（ただし、すべての引数に型ヒントを付けるのがベストプラクティスです）。

整数で基本的な計算を行う 2 つ目の操作を追加してみましょう。

```python hl_lines="5-7"
@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

<a href="http://localhost:8000/api/math?a=2&b=3"
target="_blank">localhost:8000/api/math?a=2&b=3</a>：

```json
{
  "add": 5,
  "multiply": 6
}
```

## パス文字列からパラメータを渡す

Python のフォーマット文字列と同じ構文を使って、パスの「パラメータ」を宣言できます。

パス文字列の中で見つかったパラメータは、クエリ文字列から取得される代わりに、関数の引数として渡されます。

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

次に、<a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a> から math 操作にアクセスします。


## リクエストボディからパラメータを渡す

`hello` 操作を HTTP `POST` リクエストを使うように変更し、パラメータをリクエストボディから取得するようにします。

パラメータがリクエストボディから来ることを指定するには、schema を宣言する必要があります。

*[Schema]: Pydantic の "Model" を拡張したもの

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### セルフドキュメンティング API

次に <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> にアクセスすると、HTTP 405 のエラーレスポンスになります。この URL へのリクエストを POST タイプに変更する必要があるためです。

*[HTTP 405]: Method Not Allowed（許可されていないメソッド）

簡単な方法は、自動的に作成される Swagger ドキュメント（デフォルトでは API URL のルートに "/docs" が付加された URL）を使うことです。

1. <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a> にアクセスして、作成した操作を表示します
1. `/api/hello` 操作を開きます
2. "Try it out" をクリックします
3. リクエストボディを修正します
4. "Execute" をクリックします

!!! success

    次の章 **[レスポンスの扱い](step3.md)** に進みましょう。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
