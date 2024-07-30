---
comments: true
---
# 认证

## 介绍

**Django Ninja** 提供了若干工具来帮助你轻松、快速、以标准方式处理认证和授权，而无需研究和学习 <a href="https://swagger.io/docs/specification/authentication/" target="_blank">所有安全规范</a>.

核心概念是，当你描述一个 API 操作时，你可以定义一个认证对象。
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

在这个例子中，如果客户端使用 Django 会话认证（默认是基于 cookie 的），它将只能调用 `pets` 方法，否则将返回一个 HTTP-401 错误。
如果你只需要授权超级用户，你可以使用 `from ninja.security import django_auth_superuser` 来代替。
## 自动 OpenAPI 模式

这里有一个例子，其中客户端为了进行认证需要传递一个头信息：

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

现在访问 <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> 文档。


![Swagger UI Auth](../img/auth-swagger-ui.png)

现在，当你点击 **Authorize** 按钮，你将得到一个输入你的认证令牌的提示。

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

当你进行测试调用时，每个请求都会传递授权头信息。

## 全局认证

如果你需要保护你的 API 的 **所有 **方法，你可以将 `auth` 参数传递给 `NinjaAPI` 构造函数:


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

并且，如果您需要否决其中一些方法，可以再次在操作级别通过传递 `auth` 参数来实现。在这个例子中，对于 `/token` 操作将禁用身份验证：
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## 可用的身份验证选项

### 自定义函数


"`auth=`" 参数参数接受任何可调用对象。只有当可调用对象返回一个可以 **转换为布尔值`True`的值** 时， **NinjaAPI** 才会传递身份验证。这个返回值将被分配给 `request.auth` 属性。

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API 密钥

一些 API 使用 API 密钥进行授权。API 密钥是客户端在进行 API 调用时提供的用于识别自身的令牌。该密钥可以在查询字符串中发送：
```
GET /something?api_key=abcdef12345
```

或者作为请求头：

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

或者作为一个 cookie：

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** 带有内置类来帮助您处理这些情况。


#### 在 Query 中

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

在这个例子中，我们从 `GET['api_key']` 获取一个令牌，并在数据库中找到与之对应的 `Client`。 Client 实例将被设置为 `request.auth` 属性。

注意: **`param_name`** 是将被检查的 GET 参数的名称。如果未设置，将使用默认的 "`key`" 。


#### 在 Header 中

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### 在 Cookie 中

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### HTTP 基本身份验证

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## 多个身份验证器

The **`auth`** 参数也允许您传递多个身份验证器：

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

在这种情况下， **Django Ninja** 将首先检查 API 密钥 `GET`，如果未设置或无效，将检查 `header`密钥。
如果两者都无效，它将向响应引发身份验证错误。


## 路由器身份验证

在路由器上使用 `auth` 参数， 将身份验证器应用于其中声明的所有操作：

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

或者使用路由器构造函数
```python
router = Router(auth=BasicAuth())
```


## 自定义异常

引发具有异常处理程序的异常将以与操作相同的方式返回该处理程序的响应：

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## 异步身份验证

**Django Ninja** 对异步身份验证有基本支持。虽然默认的身份验证类不是异步兼容的，但您仍然可以定义您的自定义异步身份验证可调用对象，并使用 `auth` 传递它们。

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


有关更多信息，请参阅 [处理错误](errors.md) 。

!!! 大功告成

    继续下一小节 **[测试](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
