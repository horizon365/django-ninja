# CSRF 跨站请求伪造

## 什么是跨站请求伪造？
> [跨站请求伪造](https://en.wikipedia.org/wiki/Cross-site_request_forgery) 发生在一个恶意网站包含一个链接、表单按钮或一些 JavaScript 时，旨在使用在其浏览器中访问恶意网站的已登录用户的凭证（或网络上未被本文档涵盖的位置）在您的网站上执行某些操作。


## 如何使用 Django Ninja 防范跨站请求伪造
### 使用非自动嵌入请求的身份验证方法
跨站请求伪造攻击依赖于自动包含在从其他网站发起的请求中的身份验证方法，如 [cookies](https://en.wikipedia.org/wiki/HTTP_cookie) 或 [基本访问身份验证](https://en.wikipedia.org/wiki/Basic_access_authentication).
使用不会自动嵌入的身份验证方法，例如 `Authorization: Bearer` ，可减轻这种攻击。


### 使用 Django 的内置跨站请求伪造保护
如果您使用的是默认的 Django 身份验证，该身份验证使用 Cookie，您还必须使用默认的 [Django 跨站请求伪造保护](https://docs.djangoproject.com/en/4.2/ref/csrf/)。


默认情况下， **Django Ninja** 对所有操作的跨站请求伪造保护都处于 **OFF** 状态。
要打开它，您需要使用 NinjaAPI 类的 `csrf` 参数 :

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Warning</span>: 在跨站请求伪造关闭的情况下使用基于 Cookie 的身份验证的 API 是不安全的！ (如 `CookieKey`, 或 `django_auth`)。


**Django Ninja** 将自动为基于 Cookie 的身份验证启用跨站请求伪造。


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


或者基于 django-auth 的（它继承自基于 Cookie 的身份验证）：

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Django `ensure_csrf_cookie` 装饰器
您可以在未受保护的路由上使用 Django [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) 装饰器，使其包含用于跨站请求伪造令牌的 `Set-Cookie`头，请注意:
- 路由装饰器必须在 [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) 装饰器之前（即之上）执行。
- 您必须对该路由进行 `csrf_exempt` 。
-  `ensure_csrf_cookie` 装饰器仅在 Django `HttpResponse` 上起作用，而不像大多数 Django Ninja 装饰器那样也在字典上起作用。
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
对该路由的请求会触发来自 Django 的带有适当 `Set-Cookie` 头的响应。


#### 前端代码
你可以使用 [使用 AJAX 进行 CSRF 保护 ](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) 和 [在 AJAX 请求上设置令牌](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) 部分的 [如何使用 Django’s CSRF 保护](https://docs.djangoproject.com/en/4.2/howto/csrf/) 以了解如何在您的前端代码中处理该跨站请求伪造保护令牌。


## 关于 CORS 的其它
您可能希望在不同的站点上设置前端和 API (在这种情况下，您可以查看 [django-cors-headers](https://github.com/adamchainz/django-cors-headers)).
虽然与跨站请求伪造没有直接关系，但 CORS (跨源资源共享) 在您在不同于前端使用的站点上定义跨站请求伪造 Cookie 时可能会有所帮助，因为这在默认情况下是不被 [同源策略](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)允许的。
然后您可以查看 [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme)。
