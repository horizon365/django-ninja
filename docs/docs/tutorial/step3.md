# 教程 - 处理响应

## 定义响应模式

**Django Ninja** 允许您出于验证和文档目的定义响应的模式。

我们将创建第三个操作，该操作将返回有关当前 Django 用户的信息。

```python
from ninja import Schema

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # 未经过身份验证的用户没有以下字段，因此提供默认值。
    email: str = None
    first_name: str = None
    last_name: str = None

@api.get("/me", response=UserSchema)
def me(request):
    return request.user
```

这将把 Django 的 `用户` 对象转换为仅包含定义字段的字典。

### 这将把 Django 的“用户”对象转换为仅包含定义字段的字典。

如果当前用户未经过身份验证，让我们返回不同的响应。

```python hl_lines="2-5 7-8 10 12-13"
class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 
```

如您所见，您可以返回一个由两部分组成的元组，该元组将被解释为 HTTP 响应码和数据。

!!! 大功告成

    本教程到此结束！查看 **其他教程** 或 ** 操作指南 ** 以获取更多信息。