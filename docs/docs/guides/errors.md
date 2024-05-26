# 处理错误

**Django Ninja** 允许你安装自定义异常处理程序，以处理当错误或已处理的异常发生时如何返回响应。

## 自定义异常处理程序

假设你正在制作一个依赖于某些外部服务的 API，该服务被设计为在某些时刻不可用。你可以处理该错误并向客户端返回一些友好的响应（让其稍后回来），而不是在异常发生时抛出默认的 500 错误。
要实现这一点，你需要:

 - 1) 创建一些异常（或使用现有的异常）
 - 2) 使用 api.exception_handler 装饰器


示例:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

异常处理函数接受 2 个参数：

 - **request** - Django 的 HTTP 请求
 - **exc** - 实际的异常

函数必须返回 HTTP 响应

## 覆盖默认的异常处理程序

默认情况下，**Django Ninja** 初始化了以下异常处理程序：


#### `ninja.errors.AuthenticationError`

当认证数据无效时抛出

#### `ninja.errors.ValidationError`

当请求数据未通过验证时抛出

#### `ninja.errors.HttpError`

用于从代码的任何地方抛出带有状态码的 HTTP 错误
#### `django.http.Http404`
 
Django 的默认 404 异常（例如可以使用 get_object_or_404 返回）
#### `Exception`
 
应用程序未处理的任何其他异常。
默认行为
 
  - **如果 `settings.DEBUG` 为 `True`** - 在纯文本中返回一个跟踪信息（在控制台或 Swagger UI 中调试时很有用）
  - **else** - 使用默认的 Django 异常处理机制（错误日志记录，向 ADMINS 发送电子邮件）


### 覆盖默认处理程序

如果你需要更改验证错误的默认输出 - 覆盖 ValidationError 异常处理程序：

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## 通过异常抛出 HTTP 响应

作为自定义异常和为其编写处理程序的替代方案 - 你也可以抛出 HTTP 异常，这将导致返回带有所需代码的 HTTP 响应

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
