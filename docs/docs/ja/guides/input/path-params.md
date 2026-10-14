---
comments: true
---
# パスパラメータ

パスの "parameters"（パラメータ）は、Python のフォーマット文字列と同じ構文で宣言できます（幸い、この構文は <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">OpenAPI のパスパラメータ</a>とも一致します）:

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

パスパラメータ `item_id` の値は、引数 `item_id` として関数に渡されます。

したがって、この例を実行して <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> にアクセスすると、次のレスポンスが表示されます:

```JSON
{"item_id":"foo"}
```


### 型付きのパスパラメータ

パスパラメータの型は、関数内で標準的な Python の型アノテーションを使って宣言できます:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

この場合、`item_id` は **`int`** として宣言されています。これにより、エラーチェックやコード補完などのエディタ・リンターのサポートが得られます。

ブラウザで <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a> を使ってこのコードを実行すると、次のレスポンスが表示されます:
```JSON
{"item_id":3}
```

!!! tip
    関数が受け取り（返す）値は、Python の `int` としての **3** であり、文字列 `"3"` ではないことに注意してください。
    つまり、たったこれだけの型宣言で、**Django Ninja** は自動的なリクエストの "パース" とバリデーションを提供します。



### データバリデーション

一方、ブラウザで <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*（`"foo"` は int ではない）*</small> にアクセスすると、次のような HTTP エラーが表示されます:

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Django のパスコンバータ

[Django のパスコンバータ](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters)を使用して、パスのパースを支援できます:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

この場合、`item_id` は **`int`** としてパースされます。`item_id` が有効な `int` でない場合、URL はマッチしません。
（たとえば、他にマッチするルートがない場合は、404 Not Found が返されます。）

!!! tip
    **Django Ninja** はアノテーションされていないパラメータにデフォルトの `str` 型を使用するため、上記の関数が受け取り（返す）値は、Python の `str` としての `"3"` であり、整数 **3** ではないことに注意してください。`int` を受け取るには、通常どおり関数定義で `item_id` に `int` 型のアノテーションを付けて宣言します:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```

#### スラッシュを含むパスパラメータ

Django の `path` コンバータを使用すると、パスのようなパラメータを処理できます:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
このオペレーションには `/dir/some/path/with-slashes` のようにクエリでき、`value` は `some/path/with-slashes` と等しくなります

### 複数のパラメータ

`path` には必要な数だけ変数を渡せます — 一意な名前を使用することと、関数の引数で同じ名前を使用することを忘れないでください。

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Schema の使用

相互に依存するパスパラメータをカプセル化する（そしてグループとしてバリデーションする）ために、スキーマを使用することもできます:


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    ここでは `Path` ソースヒントを使用して、このスキーマがパスパラメータに適用されることを **Django Ninja** に伝えていることに注意してください。

### ドキュメント

ブラウザで <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> を開くと、自動生成されたインタラクティブな API ドキュメントが表示されます。
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    次の章に進みましょう！ **[クエリパラメータ](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
