---
comments: true
---
# 改变响应

有时你会想要在响应即将被提供之前对其进行更改，例如添加一个头部或修改一个 cookie。

要做到这一点，只需声明一个函数参数，类型为 `HttpResponse`:

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## 临时响应对象

这个响应对象用于 Django Ninja 构建的所有响应的基础，包括错误响应。
如果一个 Django `HttpResponse` 对象直接由一个操作返回，那么这个对象就 *不会* 被使用。

显然这个响应对象还不会包含内容，但它确实设置了 `content_type` （但你可能不想去更改它）。

`status_code` 将根据返回值被覆盖（默认是 200，如果返回一个两部分的元组，则是该状态码）。


## 改变基础响应对象

你可以通过覆盖 `NinjaAPI.create_temporal_response` 方法来改变这个临时响应对象。

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```