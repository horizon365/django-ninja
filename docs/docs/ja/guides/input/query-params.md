---
comments: true
---
# クエリパラメータ

パスパラメータの一部ではない関数パラメータを宣言すると、それらは自動的に "query"（クエリ）パラメータとして解釈されます。
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

このオペレーションをクエリするには、次のような URL を使用します:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
デフォルトでは、すべての GET パラメータは文字列です。関数パラメータに型を付けると、その型に変換され、その型に対してバリデーションされます。

パスパラメータと同じ利点は、クエリパラメータにも適用されます:

- エディタサポート（当然ながら）
- データの "パース"
- データのバリデーション
- 自動ドキュメント


!!! note
    パラメータに型アノテーションを付けない場合、それらは `str` 型として扱われます

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### デフォルト値

クエリパラメータはパスの固定部分ではないため、オプションであり、デフォルト値を持つことができます:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

上記の例では、`offset=0` と `limit=10` のデフォルト値を設定しています。

したがって、次の URL にアクセスすると:
```
http://localhost:8000/api/weapons
```
次の URL にアクセスした場合と同じになります:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
たとえば次の URL にアクセスした場合:
```
http://localhost:8000/api/weapons?offset=20
```

関数内のパラメータの値は次のようになります:

 - `offset=20`（URL で設定したため）
 - `limit=10`（デフォルト値であるため）


### 必須パラメータとオプションパラメータ

必須またはオプションの GET パラメータは、Python の関数パラメータを宣言するのと同じ方法で宣言できます:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

この場合、**Django Ninja** は GET リクエストで渡す `q` パラメータを常にバリデーションし、`offset` パラメータはオプションの整数として扱われます。

### GET パラメータの型変換

複数の型付きパラメータを宣言してみましょう:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
`str` 型はそのまま渡されます。

`bool` 型の場合、次のすべて:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
および大文字・先頭文字だけ大文字などの他の大文字小文字のバリエーションでも、パラメータ `b` は `bool` 値の `True` として関数に渡され、それ以外は `False` になります。

日付は、日付文字列と整数（Unix タイムスタンプ）を受け付けます:

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Schema の使用

GET パラメータをカプセル化するためにスキーマを使用することもできます:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

より複雑なフィルタリングのシナリオについては、[フィルタリング](./filtering.md)を参照してください。

!!! done

    次の章に進みましょう！ **[リクエストボディ](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
