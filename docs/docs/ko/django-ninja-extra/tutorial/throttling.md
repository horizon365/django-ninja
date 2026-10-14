---
comments: true
---
# **스로틀링 / 속도 제어**

스로틀링(throttling)은 요청이 승인되어야 하는지를 결정하는 권한의 일종으로 볼 수 있습니다.
클라이언트가 API에 요청할 수 있는 속도를 제어하는 데 사용되는 임시 상태를 나타냅니다.

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    위 예제는 스로틀이 적용되지 않습니다. `UserRateThrottle`과 `AnonRateThrottle`의 기본 스코프가 `none`이기 때문입니다

## **다중 스로틀링**
Django-ninja-extra 스로틀링은 다중 스로틀을 지원하며, 이는 버스트(burst) 스로틀 비율이나 지속(sustained) 스로틀 비율처럼 API에 서로 다른 제약을 적용하는 데 유용합니다.
예를 들어, 사용자를 분당 최대 60회, 하루 최대 1000회 요청으로 제한하고 싶을 수 있습니다.

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
## **스로틀 정책 설정**
프로젝트의 `settings.py`에서 다음 키들을 재정의하여 기본 스로틀 클래스와 비율을 전역적으로 설정할 수 있습니다:
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
`THROTTLE_RATES`에 사용되는 비율 설명에는 스로틀 기간으로 `second`, `minute`, `hour`, 또는 `day`가 포함될 수 있습니다.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **클라이언트 식별**
클라이언트는 HTTP 헤더 X-Forwarded-For와 WSGI 변수 REMOTE_ADDR을 통해 식별됩니다.
이것들은 스로틀링을 위해 클라이언트 IP 주소를 식별하는 데 사용되는 고유 식별자입니다.
`X-Forwarded-For`가 `REMOTE_ADDR`보다 우선하며 그렇게 사용됩니다.

#### **클라이언트 프록시 제한**
고유한 클라이언트 IP 주소를 엄격하게 식별해야 하는 경우, 먼저 `NUM_PROXIES` 설정을 지정하여 API 뒤에서 실행 중인 애플리케이션 프록시의 수를 구성해야 합니다. 이 설정은 0 이상의 정수여야 합니다.
0이 아닌 값으로 설정하면, 애플리케이션 프록시 IP 주소를 먼저 제외한 후 클라이언트 IP가 X-Forwarded-For 헤더의 마지막 IP 주소로 식별됩니다. 0으로 설정하면 REMOTE_ADDR 값이 항상 식별 IP 주소로 사용됩니다.
`NUM_PROXIES`를 구성하면 하나의 고유한 [NAT(Network Address Translation)](https://en.wikipedia.org/wiki/Network_address_translation) 게이트웨이 뒤에 있는 모든 클라이언트가 단일 클라이언트로 취급된다는 점을 이해하는 것이 중요합니다.

!!! note
    X-Forwarded-For 헤더의 동작 방식과 원격 클라이언트 IP 식별에 대한 더 자세한 내용은 여기에서 찾을 수 있습니다.

## **스로틀 모델 캐시 설정**
django-ninja-extra에서 사용되는 스로틀 모델은 Django 캐시 백엔드를 활용합니다. [`LocMemCache`]()의 `default` 값을 사용합니다.
자세한 내용은 Django의 [캐시 문서](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache)를 참고하세요.

스로틀 모델에 정의된 기본 캐시를 사용하고 싶지 않다면, 스로틀 모델에 다른 캐시를 정의하는 방법의 예는 다음과 같습니다:
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **API 레퍼런스**

## **익명 사용자 속도 제한**
`AnonRateThrottle` 모델은 인증되지 않은 사용자의 IP 주소를 키로 사용하여 스로틀 제한을 적용하는 데 사용됩니다.

알 수 없는 출처의 요청 속도를 제한하는 데 적합합니다.

요청 권한은 다음에 의해 결정됩니다:
- 파생 클래스에 정의된 `rate`
- `settings.py`의 `NINJA_EXTRA` 설정 내 `THROTTLE_RATES`에 정의된 `anon` 스코프.

## **사용자 속도 제한**
`UserRateThrottle` 모델은 인증된 사용자의 사용자 ID 또는 기본 키를 사용하여 키를 생성함으로써 스로틀 제한을 적용하는 데 사용됩니다.
인증되지 않은 요청은 들어오는 요청의 IP 주소를 사용하여 스로틀 제한을 위한 고유 키를 생성하는 방식으로 대체(fallback)됩니다.

요청 권한은 다음에 의해 결정됩니다:
- 파생 클래스에 정의된 `rate`
- `settings.py`의 `NINJA_EXTRA` 설정 내 `THROTTLE_RATES`에 정의된 `user` 스코프.


`UserRateThrottle` 모델에는 여러 사용자 스로틀 비율을 사용할 수 있습니다. 예를 들어:
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
## **동적 속도 제한**
`DynamicRateThrottle` 모델은 `UserRateThrottle`과 유사한 방식으로 인증된 사용자와 인증되지 않은 사용자 모두를 스로틀하는 데 사용됩니다.
핵심 기능은 사용될 때 `scope`를 동적으로 설정할 수 있다는 것입니다.
예를 들어:
설정에 스코프를 정의할 수 있습니다.

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
여기서 우리는 `get_users`와 `get_user_by_id`에 각각 `sustained` 비율과 `burst` 비율을 동적으로 적용합니다.


!!! note "v0.15.8의 새 기능"
    컨트롤러 클래스 수준에서 모든 컨트롤러 엔드포인트 오퍼레이션에 스로틀을 적용할 수 있습니다.

## **컨트롤러 스로틀링**

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
