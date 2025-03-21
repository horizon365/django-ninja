---
comments: true
---
## 前言
jwt 早就有耳闻，而没有实际用过。最近在调研 tus 的断点续传协议，进入到了 hooks-http 级别，目的是上传文件时候进行认证。自然而然想到了django-ninja-jwt 这个包。想着应该很简单，可翻了[中文文档](https://django-ninja.cn/django-ninja-jwt/)后发现，岂止简单，简直简陋到令人发指。

## 入门指南

根据指南，只需要安装 `dango-ninja-jwt` 和 `django-ninja-extra`，然后替换 NinjaAPI 为`njaExtraAPI` 后，只需要一行。

```python
api.register_controllers(NinjaJWTDefaultController)
```

真是让人懵逼啊。

别急，我们先去docs上看看。上面多出了3个接口，pair ，refresh, verify
![JWT swagger UI token](../img/jwt-token.png)
注意右上角的锁图标，后面还有用处，它只在你使用了 JWTAuth 函数时候才会出现 。

### pair
第一个是 pair 接口，这个意思是你传递用户名和密码后，会返回给你一些可认证的 token 和可刷新的 token。
请求体格式如下：
```json
{
  "password": "string",
  "username": "string"
}
```
注意： 我这里的username是在下方，和想当然的有点不一样。
点击Execute后，会得到类似如下的内容：
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
上面这个access 呢，就可以拿来认证用了，不过它默认是有时效的。而refresh的时效要比access长一些，用来在access失效后，重新refresh获取新的access。
一旦刷新后，前一个access就失效了。

这时候可以把access拷贝到右上角的锁图标那里。这样，你在当前页面的每个接口都能用上它，方便调试。
### verify
你可以去第3个接口verify中验证这个access是否有效。

所以总的来说，django-ninja-jwt就是快速给你建了3个接口，方便你来获取、刷新和测试。

## 自定义
光有这3个接口是不行的，起码我们需要给自己特定的接口加上认证。
这时需要用到的是 `JWTAuth`，用了之后，上面的锁图标才会出现。
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """方便在docs页面显示auth按钮"""
    return request.auth.username
```
并且，在somde这个端点上，也有一个单独的锁图标。
![JWT swagger UI token custom](../img/jwt-token-custom.png)
上面的 some 这个接口，如果认证成功了的话，会响应当前登录的用户名。如果不成功，在会返回 401 头。
后端同学需要告诉前端人员配合传递这个值，让他去 [pair](#pair) 部分获取，并定时去 [refresh](#refresh) 刷新。

### 配置有效期

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # 访问令牌有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # 刷新令牌有效期
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### 进一步的自定义
如果上方ninja在route中使用 @route.get('/some', auth=JWTAuth()) 不能满足你的需求，可以在函数中调用 authenticate

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # 如果不通过 ，会内置抛出401
    if auth.authenticate(request, token):
        return request.auth.username

```
上方的token需要自己从request对象中获取。
