---
comments: true
---
# フィルタリング

ユーザーに複数の異なる属性でクエリセットをフィルタリングできるようにしたい場合、フィルタを `FilterSchema` クラスにカプセル化すると便利です。
`FilterSchema` は通常の `Schema` なので、Pydantic の必要な機能をすべて利用できますが、さらにユーザー向けのフィルタリングパラメータをデータベースクエリに簡単に変換するための便利な機能も追加されています。

まず、`FilterSchema` のサブクラスを定義します:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


次に、このスキーマを API ハンドラ内で `Query` と組み合わせて使用します:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

[Schema を使ってクエリパラメータを定義する](./query-params.md#using-schema)で説明したように、Django Ninja は `BookFilterSchema` で定義されたフィールドをクエリパラメータに変換します。
省略形のワンライナーである `.filter()` を使用して、これらのフィルタをクエリセットに適用できます:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

内部的には、`FilterSchema` はそのフィールドを [Q 式](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects)に変換し、それらを結合してクエリセットのフィルタリングに使用します。


あるいは、`.filter` メソッドを使用する代わりに、準備された `Q` 式を取得して自分でフィルタリングを行うこともできます。
これは、API 経由でユーザーに公開する内容に加えて、追加のクエリセットフィルタリングを行いたい場合に役立ちます:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

デフォルトでは、フィルタは次のように動作します:

* `None` の値は無視され、フィルタリングは適用されません;
* `None` 以外の各フィールドは、各フィールドの `Field` 定義に従って `Q` 式に変換されます;
* すべての `Q` 式は `AND` 論理演算子を使って 1 つに結合されます;
* 結果の `Q` 式はクエリセットのフィルタリングに使用され、`.filter` 句が適用されたクエリセットが返されます。

## カスタムフィールド
デフォルトでは、`FilterSet` はフィールド名を使用して Q 式を生成します:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
`name` フィールドは `Q(name=...)` 式に変換されます。

データベースのルックアップがこれより複雑な場合は、フィールド定義内で `"q"` キーワード引数を使って明示的に指定できます:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
複数のルックアップキーワード引数名をリストとして指定することもできます:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
デフォルトでは、フィールドレベルの式は `"OR"` コネクタで結合されます。したがって、上記の設定では、クエリパラメータ `?search=foobar` は、名前・著者・出版社のいずれかに "foobar" を含む本を検索します。


## 式の結合
デフォルトでは、

* フィールドレベルの式は `OR` 演算子で結合されます。
* フィールド同士は `AND` 演算子で結合されます。

したがって、次の `FilterSchema` に対して...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...ユーザーから次のクエリパラメータが渡された場合
```
http://localhost:8000/api/books?search=harry&popular=true
```
`FilterSchema` インスタンスは、本の名前 _または_ 著者の名前に `harry` を含み、かつ人気（popular）の本を検索します。


この動作は、フィールドレベルとクラスレベルの両方の定義で `expression_connector` パラメータを使用してカスタマイズできます:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

expression コネクタには `"OR"`、`"AND"`、`"XOR"` の値を指定できますが、最後の `"XOR"` は Django 4.1 でのみ[サポートされています](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor)。

さて、次のクエリパラメータを含むリクエストは
```
http://localhost:8000/api/books?name=harry&active=true
```
...名前に `harry` を含む本 _または_、自分自身がアクティブでアクティブな出版社から出版されている本を検索します。


## None によるフィルタリング
`FilterSchema` に `None` を有効な値として扱わせ、その値に対してフィルタリングを行わせることができます。

これはフィールドレベルで `ignore_none` キーワード引数を使って設定できます:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

このようにすると、ユーザーが `"tag"` に別の値を指定しなかった場合でも、フィルタには常に `tag=None` の条件が含まれます。

設定ですべてのフィールドに対して一度に指定することもできます:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## カスタム式
単一のフィールドアノテーションでは処理できない複雑なフィルタリングのシナリオに遭遇することがあります。
そのような場合のために、フィールドのフィルタリングロジックをカスタムメソッドとして実装できます。フィルタリング値を受け取り Q 式を返す `filter_<fieldname>` という名前のメソッドを定義するだけです:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
このようなフィールドメソッドは、対応するフィールドの `Field()` 定義で指定された内容よりも優先されます。
それでも不十分な場合は、`custom_expression` メソッドで `FilterSet` クラス全体に対する独自のカスタムフィルタリングロジックを実装できます:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    popular: Optional[bool] = None

    def custom_expression(self) -> Q:
        q = Q()
        if self.name:
            q &= Q(name__icontains=self.name)
        if self.popular:
            q &= (
                Q(view_count__gt=1000) |
                Q(downloads__gt=100) |
                Q(tag='popular')
            )
        return q
```
`custom_expression` メソッドは、`filter_<fieldname>` メソッドを含む、上記で説明した他のすべての定義よりも優先されます。

!!! done

    入力パラメータのシリーズは完了です！ 次のセクション **[レスポンスの処理](../response/index.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
