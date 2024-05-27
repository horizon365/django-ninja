# 分页

**Django Ninja** 带有分页支持。这允许你将大型结果集拆分为单独的页面。


要将分页应用于一个函数 - 只需应用 `paginate` 装饰器:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


就是这样！

现在你可以使用 `limit` 和 `offset` GET 参数查询用户

```
/api/users?limit=10&offset=0
```

默认情况下，限制设置为 `100` (你可以在你的 settings.py 中使用 `NINJA_PAGINATION_PER_PAGE` 来更改它)


## 内置分页类

### LimitOffsetPagination 限制偏移分页 (默认)

这是默认的分页类 (你可以在你的 settings.py 中使用 `NINJA_PAGINATION_CLASS` 指向一个类的路径来更改它)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

示例查询:
```
/api/users?limit=10&offset=0
```

这个类有两个输入参数：

 - `limit` - 定义页面上的查询集数量 (default = 100, 可以在 NINJA_PAGINATION_PER_PAGE 中修改)
 - `offset` - 设置页面窗口偏移量 (default: 0, 索引从 0 开始)


### PageNumberPagination 页码分页
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

示例查询:
```
/api/users?page=2
```

这个类有一个参数 `page` 并且默认每页输出 100 个查询集  (可以通过 settings.py 更改)

页面编号从 1 开始。

你也可以为每个视图单独设置自定义的页面大小值：

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## 在视图函数中访问分页参数

如果你需要在你的视图函数中访问用于分页的 `Input` 参数 - use `pass_parameter` 参数

在那种情况下，输入数据将在 `**kwargs` 中可用:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## 创建自定义分页类

要创建自定义分页类，你应该继承 `ninja.pagination.PaginationBase` 并覆盖 `Input` 和 `Output` 模式类以及 `paginate_queryset(self, queryset, request, **params)` 方法:

 - `Input` 模式是一个描述应传递给分页器的参数（例如页码或 limit/offset值 ）的模式类。
 - `Output` 模式描述页面输出的模式（例如计数/下一页/项目等）。
 - `paginate_queryset` 方法接收初始的查询集，并且应该返回一个仅包含所请求页面中数据的可迭代对象。该方法接受以下参数：
    - `queryset`: 由 API 函数返回的查询集（或可迭代对象）。
    - `pagination` -  paginator.Input 参数 (已解析和验证)
    - `**params`: 关键字参数，将包含装饰函数接收的所有参数。


示例:

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

提示：你可以从参数中获取请求对象：

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### 异步分页

标准的 **Django Ninja** 分页类支持异步。 如果你想用自定义分页类处理异步请求，你应该继承 `ninja.pagination.AsyncPaginationBase` 并覆盖 `apaginate_queryset(self, queryset, request, **params)` 方法。

### 输出属性

默认情况下页面项被放置在 `'items'` 属性中。 要覆盖此行为，可以使用  `items_attribute`:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int
    
    items_attribute: str = "results"

```


## 一次对多个操作应用分页

经常会有这样的情况，你需要对所有返回查询集或列表的视图添加分页

你可以使用内置的路由类 (`RouterPaginated`) 它会自动将分页注入到所有定义为 `response=List[SomeSchema]` 的操作中:

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

在这个例子中，这两个操作都将启用分页。

要将分页应用于主 `api` 实例，可以使用 `default_router` 参数:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```
