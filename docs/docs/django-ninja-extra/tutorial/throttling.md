---
comments: true
---
# **节流*／速率控制*

节流可以被视为一种权限，用于确定请求是否应该被授权。
它表示用于控制客户端对 API 可以发出请求的速率的临时状态。

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # 这将应用默认的节流类 [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! 注意
    上述示例不会被节流，因为　`UserRateThrottle` 和 `AnonRateThrottle`　默认范围是　`none`

## **多种节流**
Django-ninja-extra 节流支持多种节流 ，这对于在 API 上施加不同的约束非常有用，
这些约束可以是突发节流速率或持续节流速率。
例如，你可能希望将用户限制为每分钟最多 60 个请求，每天最多 1000 个请求。

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle
api = NinjaExtraAPI()

class User60MinRateThrottle(UserRateThrottle):
    rate = "60/min"
    scope = "minutes"


class User1000PerDayRateThrottle(UserRateThrottle):
    rate = "1000/day"
    scope = "days"

@api.get('/users')
@throttle(User60MinRateThrottle, User1000PerDayRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'

```
## **节流策略设置**
你可以在项目的 `settings.py` 中通过覆盖以下键来全局设置默认的节流类和速率：
```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        "ninja_extra.throttling.AnonRateThrottle",
        "ninja_extra.throttling.UserRateThrottle",
    ],
    'THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
    },
    'NUM_PROXIES': None
}
```
在 `THROTTLE_RATES` 中使用的速率描述可以包括 `second`, `minute`, `hour` 或 `day` 作为节流周期。

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **客户端识别**
客户端通过 HTTP 头中的 x-Forwarded-For 和 WSGI 变量 REMOTE_ADDR 来识别。
这些是用于识别用于节流的客户端 IP 地址的独特标识。
`X-Forwarded-For` 比 `REMOTE_ADDR` 更优先，并被如此使用。

#### **限制客户端代理**
如果你需要严格识别独特的客户端 IP 地址， 你首先需要通过设置 `NUM_PROXIES` 设置来配置 API 背后运行的应用程序代理的数量。这个设置应该是一个零或更大的整数。
如果设置为非零，那么一旦首先排除了任何应用程序代理 IP 地址，客户端 IP 将被识别为 X-Forwarded-For 头中的最后一个 IP 地址。如果设置为零，那么 REMOTE_ADDR 值将始终被用作识别 IP 地址。
重要的是要理解，如果你配置了 `NUM_PROXIES` ， 那么在一个独特的 [网络地址转换（NAT）](https://en.wikipedia.org/wiki/Network_address_translation) 网关后面的所有客户端将被视为一个单一客户端。

!!! 注意
    关于 X-Forwarded-For 头如何工作以及识别远程客户端 IP 的更多上下文可以在这里找到。

## **节流模型缓存设置**
django-ninja-extra 中使用的节流模型利用 Django 缓存后端。它使用 [`LocMemCache`]() 的 `default` 值。
有关更多详细信息，请参阅 Django 的 [缓存文档](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) 。

如果你不想使用节流模型中定义的默认缓存，这里有一个示例，说明如何为节流模型定义不同的缓存：
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
# **API 参考**

## **匿名速率节流**
`AnonRateThrottle` 模型用于使用未认证用户的 IP 地址作为键进行节流限制。

它适用于限制来自未知来源的请求速率。

请求权限由以下因素确定：
- 在派生类中定义的 `rate` 
- 在 `settings.py` 中的 `NINJA_EXTRA` 设置中的 `THROTTLE_RATES` 定义的 `anon` 范围。

## **用户速率节流**
`UserRateThrottle` 模型用于使用已认证用户的用户 ID 或主键生成一个键来进行节流限制。
未认证请求将回退到使用传入请求的 IP 地址来生成一个独特的键进行节流限制。

请求权限由以下因素确定：
- 在派生类中定义的 `rate`
- 在 `settings.py` 中的 `NINJA_EXTRA` 设置中的 `THROTTLE_RATES` 定义的 `user` 范围。


你可以为 `UserRateThrottle` 模型使用多个用户节流速率，例如：
```python
# example/throttles.py
from ninja_extra.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        'example.throttles.BurstRateThrottle',
        'example.throttles.SustainedRateThrottle'
    ],
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```
## **动态速率节流**
`DynamicRateThrottle` 模型用于以与 `UserRateThrottle` 类似的方式对已认证和未认证用户进行节流。
它的关键特性在于能够动态设置其使用时的 `scope` 。
例如:
我们可以在设置中定义一个范围。

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```

```python
# api.py
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api.get('/users')
@throttle(DynamicRateThrottle, scope='burst')
def get_users(request):
    return 'foo'

@api.get('/users/<int:id>')
@throttle(DynamicRateThrottle, scope='sustained')
def get_user_by_id(request, id: int):
    return 'foo'
```
在这里，我们分别动态地将 `sustained (持续)` 速率和 `burst (突发)` 速率应用于 `get_users` 和 `get_user_by_id`。


!!! 注意 “在 v0.15.8 中新增”
    你可以在控制器类级别对所有控制器端点操作进行节流。

## **控制器节流**

```python
# api.py
from ninja_extra import (
    NinjaExtraAPI, throttle, api_controller, ControllerBase,
    http_get
)
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api_controller("/throttled-controller")
class ThrottlingControllerSample(ControllerBase):
    throttling_classes = [
        DynamicRateThrottle,
    ]
    throttling_init_kwargs = dict(scope="sustained")

    @http_get("/endpoint_1")
    @throttle(DynamicRateThrottle, scope='burst')
    def endpoint_1(self, request):
        # this will override the generally throttling applied at the controller
        return "foo"

    @http_get("/endpoint_2")
    def endpoint_2(self, request):
        return "foo"

    @http_get("/endpoint_3")
    def endpoint_3(self, request):
        return "foo"


api.register_controllers(ThrottlingControllerSample)
```