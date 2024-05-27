# 过滤

如果你想允许用户通过多个不同的属性来过滤你的查询集，那么将你的过滤器封装到一个 `FilterSchema` 类中是有意义的。
`FilterSchema` 是一个常规的 `Schema`，所以它使用了 Pydantic 的所有必要特性，但它也添加了一些便利功能，
以便将面向用户的过滤参数轻松转换为数据库查询。

首先定义一个 `FilterSchema` 的子类:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


接下来，在你的 API 处理程序中结合 `Query` 使用这个模式:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

就像在 [使用模式定义查询参数](./query-params.md#using-schema)中描述的那样, Django Ninja 将`BookFilterSchema` 中定义的字段转换为查询参数。
你可以使用一个简写的单行代码 `.filter()` 将这些过滤器应用到你的查询集：
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

在底层， `FilterSchema` 将其字段转换为 [Q 表达式](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects) ，然后将它们组合起来并用于过滤你的查询集。


或者，除了使用 `.filter` 方法，你也可以获取准备好的 `Q`表达式并自己进行过滤。
当你在通过 API 向用户公开的内容之上还有一些额外的查询集过滤时，这可能会很有用：
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

默认情况下，过滤器将按照以下方式运行：

* `None` 值将被忽略且不进行过滤；
* 每个非 `None` 字段将根据每个字段的 `Field` 定义转换为一个 `Q` 表达式；
* 所有的 `Q` 表达式将使用 `AND` 逻辑运算符合并为一个；
* 生成的 `Q`表达式用于过滤查询集，并返回一个应用了 `.filter` 子句的查询集给你。

## 自定义字段
默认情况下， `FilterSet` 将使用字段名称来生成 Q 表达式：
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
`name` 字段将被转换成 `Q(name=...)` 表达式。

当你的数据库查找比这更复杂时，你可以在字段定义中使用 `"q"` 关键字参数明确指定它们：
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
你甚至可以将多个查找关键字参数名称指定为一个列表：
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
默认情况下，字段级别的表达式使用 `"OR"` 连接器组合，所以使用上述设置，一个查询参数 `?search=foobar` 将搜索那些在其名称、作者或出版者中任何一个有 "foobar" 的书。


## 组合表达式
默认情况下，

* 字段级别的表达式使用 `OR` 运算符组合在一起。
* 字段本身使用 `AND` 运算符组合在一起。

因此，对于以下的 `FilterSchema`...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...以及来自用户的以下查询参数
```
http://localhost:8000/api/books?search=harry&popular=true
```
`FilterSchema` 实例将寻找在书籍的_或_作者的名字中包含 `harry` 的热门书籍。


你可以使用字段级别和类级别定义中的 `expression_connector` 参数自定义此行为：
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

表达式连接器可以取值为 `"OR"`, `"AND"` 和 `"XOR"`, 但后者仅在 Django 4.1 中 [受支持](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) 。

现在，具有这些查询参数的请求
```
http://localhost:8000/api/books?name=harry&active=true
```
...将寻找在其名字中包含 `harry` 的书籍 _或_ 自身是活跃的并且是由活跃的出版商出版的书籍。


## 通过 Nones 进行过滤
你可以让 `FilterSchema` 将 `None` 视为应该进行过滤的有效值。

这可以在字段级别通过 `ignore_none` 关键字参数来完成：
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

这样，当用户没有为 `"tag"` 提供其他值时，过滤将始终包括 `tag=None`条件。

你也可以在配置中同时为所有字段指定此设置：
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## 自定义表达式
有时你可能希望有复杂的过滤场景，这些场景无法通过单个字段注释来处理。
对于此类情况，你可以将你的字段过滤逻辑实现为自定义方法。只需定义一个名为 `filter_<fieldname>` 的方法，该方法接受一个过滤值并返回一个 Q 表达式：

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
此类字段方法优先于相应字段的 `Field()` 定义中指定的内容。
如果这还不够，你可以在 `custom_expression` 方法中为整个 `FilterSet` 类实现你自己的自定义过滤逻辑：

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
`custom_expression` 方法优先于前面描述的任何其他定义，包括 `filter_<fieldname>` 方法。
