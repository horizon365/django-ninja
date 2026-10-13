---
comments: true
---
# **Throttling / Rate Control**

Throttling can be viewed as a permission that determines whether a request should be authorized.
It represents a temporary state used to control the rate at which clients can make requests to the API.

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    The above example will not be throttled, because the default scope of `UserRateThrottle` and `AnonRateThrottle` is `none`

## **Multiple Throttling**
Django-ninja-extra throttling supports multiple throttles, which is useful for applying different constraints on an API,
such as burst throttle rates or sustained throttle rates.
For example, you might want to limit users to a maximum of 60 requests per minute and 1000 requests per day.

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
## **Throttle Policy Settings**
You can globally set the default throttle classes and rates in your project's `settings.py` by overriding the following keys:
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
The rate descriptions used in `THROTTLE_RATES` may include `second`, `minute`, `hour`, or `day` as the throttle period.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **Client Identification**
Clients are identified through the HTTP header X-Forwarded-For and the WSGI variable REMOTE_ADDR.
These are the unique identifiers used to identify the client IP address for throttling.
`X-Forwarded-For` takes precedence over `REMOTE_ADDR` and is used as such.

#### **Restricting Client Proxies**
If you need to strictly identify unique client IP addresses, you first need to configure the number of application proxies running behind the API by setting the `NUM_PROXIES` setting. This setting should be an integer of zero or greater.
If set to a non-zero value, then once any application proxy IP addresses are excluded first, the client IP will be identified as the last IP address in the X-Forwarded-For header. If set to zero, the REMOTE_ADDR value will always be used as the identifying IP address.
It is important to understand that if you configure `NUM_PROXIES`, then all clients behind a single unique [Network Address Translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation) gateway will be treated as a single client.

!!! note
    More context on how the X-Forwarded-For header works and on identifying remote client IPs can be found here.

## **Throttle Model Cache Settings**
The throttle model used in django-ninja-extra leverages the Django cache backend. It uses the `default` value of [`LocMemCache`]().
For more details, please refer to Django's [cache documentation](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache).

If you don't want to use the default cache defined in the throttle model, here is an example of how to define a different cache for the throttle model:
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **API Reference**

## **Anonymous Rate Throttling**
The `AnonRateThrottle` model is used for throttle limiting using the IP address of unauthenticated users as the key.

It is suitable for limiting the rate of requests from unknown sources.

Request permissions are determined by:
- The `rate` defined in the derived class
- The `anon` scope defined in `THROTTLE_RATES` in the `NINJA_EXTRA` settings in `settings.py`.

## **User Rate Throttling**
The `UserRateThrottle` model is used for throttle limiting by generating a key using the user ID or primary key of authenticated users.
Unauthenticated requests will fall back to using the IP address of the incoming request to generate a unique key for throttle limiting.

Request permissions are determined by:
- The `rate` defined in the derived class
- The `user` scope defined in `THROTTLE_RATES` in the `NINJA_EXTRA` settings in `settings.py`.


You can use multiple user throttle rates for the `UserRateThrottle` model, for example:
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
## **Dynamic Rate Throttling**
The `DynamicRateThrottle` model is used to throttle both authenticated and unauthenticated users in a similar way to `UserRateThrottle`.
Its key feature is the ability to dynamically set the `scope` when it is used.
For example:
We can define a scope in the settings.

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
Here, we dynamically apply the `sustained` rate and the `burst` rate to `get_users` and `get_user_by_id` respectively.


!!! note "New in v0.15.8"
    You can throttle all controller endpoint operations at the controller class level.

## **Controller Throttling**

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
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
