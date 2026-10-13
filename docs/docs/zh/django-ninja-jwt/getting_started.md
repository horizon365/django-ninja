
#### Requirements
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

这些是官方支持的 Python 版本和软件包版本。其他版本可能也会起作用。你可以自由修改 tox 配置并看看有哪些可能。

## 安装

Ninja JWT 能通过 pip 来安装:

    pip install django-ninja-jwt

此外，你需要向你的 Django-Ninja API 注册 `NinjaJWTDefaultController`控制器。

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` 带有三条路由 `obtain_token（获取令牌）`, `refresh_token（刷新令牌）` and `verify_token（验证令牌）`。
它是两个子类 `TokenVerificationController（令牌验证控制器）`和 `TokenObtainPairController（令牌获取对控制器）`的组合。
如果你希望自定义这些路由，你可以从这些控制器继承并更改其实现。

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """仅获取令牌和刷新令牌"""
...
api.register_controllers(MyCustomController)
```

如果你希望使用本地化/翻译，只需将 `ninja_jwt` 添加到 `INSTALLED_APPS`。

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## 用法

为了验证 Ninja JWT 正在工作，你可以使用 curl 发出几个测试请求：

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

你可以使用返回的访问令牌来证明对受保护视图的认证：

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

当这个短期访问令牌过期时，你可以使用长期的刷新令牌来获取另一个访问令牌：

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZX...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

Cryptographic Dependencies (Optional)
-------------------------------------

如果你计划使用某些数字签名算法（即 RSA 和 ECDSA；访问 PyJWT 以获取其他算法）来编码或解码令牌，
你将需要安装加密库 cryptography_ 。这可以明确地安装，或者作为 `django-ninja-jwt` 要求中的一个必填项进行安装：

    pip install django-ninja-jwt[crypto]

在使用 `Ninja JWT` 的项目的需求文件中，推荐使用 `django-ninja-jwt[crypto]` 格式，
因为单独的 `cryptography` 需求行之后可能会被误认为是未使用的需求并被删除。
[cryptography](https://cryptography.io)

!!! 大功告成

    继续下一章节 **[路由鉴权](auth_integration.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
