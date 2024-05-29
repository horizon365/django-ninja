# 欢迎来到 Django Ninja 1.0


要开始使用，请使用以下命令安装最新版本：
```
pip install -U django-ninja
```

django-ninja v1 与 Python 3.7 及以上版本兼容。


Django ninja 0.x 系列仍然受支持，但将仅接收安全更新和关键错误修复。


# Django Ninja 1.0 中的新特性

## 对 Pydantic2 的支持

Pydantic 版本 2 用 Rust 重写，包含了许多改进和特性，如：

 - 更安全的类型。
 - 更好的可扩展性。
 - 更好的性能。

根据我们的测试，平均项目可以平均获得约 10%的性能提升，而在某些边缘解析/序列化情况下可以给你带来 4 倍的提升。
另一方面，它引入了破坏性变化，pydantic 1 和 2 不是非常兼容 - 但我们尽力使这个过渡尽可能容易。
所以如果你使用了 'Schema' 类，迁移到 ninja v1 应该很容易。否则，请遵循  [pydantic 迁移指南](https://docs.pydantic.dev/latest/migration/)


一些 pydantic2 提供的新特性

### pydantic 上下文

Pydantic 现在在验证和序列化期间支持上下文，Django ninja 在请求和响应工作期间传递“请求”对象。
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

在响应期间，“response_code”也传递到上下文。

## Schema.Meta

Pydantic 现在弃用了 BaseModel.Config 类。但为了与所有其他 Django 部分保持一致，我们为 ModelSchema 引入了“Meta”类 - 它的工作方式与 Django 的 ModelForms 类似：
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

（“Config”类仍然支持，但已处于弃用状态）


## 更短/更简洁的参数语法

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

而不是

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

或

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


而不是

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



以及在编辑器中的所有自动完成功能。


另一方面， **旧语法仍然被支持** ，因此你可以轻松地将你的项目移植到最新的 django-ninja 版本而不费吹灰之力。


#### + Annotated

typing.Annotated 也已经被支持:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Async auth 异步身份验证支持

异步身份验证器终于得到支持。你所要做的只是在你的 `authenticate` 方法中添加 `async`:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## 更改的 CSRF 行为


`csrf=True` 不再是必须的，如果你使用了基于 cookie 的身份验证。 相反，CSRF 保护自动启用。这也允许你混合受 CSRF 保护的身份验证器和其他不需要 Cookie 的方法：

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## 文档

文档查看器现在是可配置和可插拔的。默认情况下，django-ninja 带有 Swagger 和 Redoc：
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

用户现在能够通过继承 `DocsBase` 类创建自定义文档查看器。

## 路由器

add_router 支持字符串路径：

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## 装饰器

当 django-ninja 用.get/.post 等装饰视图时，它会包装函数的结果（在大多数情况下不是 HttpResponse - 而是一些可序列化的对象），因此不太可能使用一些内置或第三方装饰器，如：
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- 将不起作用！
def test_view(request):
    return {"some": "Complex data"}
```
这个例子将不起作用。

现在 django-ninja 引入了一个装饰器 decorate_view，允许注入与 http 响应一起工作的装饰器：
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## 分页

`paginate_queryset` 方法现在接受 `request` 对象


#### 不向后兼容的内容
 - resolve_xxx(self, ...) - 支持 (self) 的解析被弃用，转而支持 pydantic 内置功能。
 - pydantic v1 不再支持
 - python 3.6 不再支持

顺便说一句 - 如果你喜欢这个项目并且还没有给它一个 Github 星标 - 请这样做！[github star](img/github-star.png)
