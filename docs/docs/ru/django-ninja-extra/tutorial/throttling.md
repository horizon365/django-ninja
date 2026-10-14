---
comments: true
---
# **Троттлинг / Ограничение частоты запросов**

Троттлинг можно рассматривать как разрешение, определяющее, должен ли запрос быть авторизован.
Он представляет собой временное состояние, используемое для управления частотой, с которой клиенты могут отправлять запросы к API.

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    Приведённый выше пример не будет подвержен троттлингу, поскольку область видимости (scope) по умолчанию для `UserRateThrottle` и `AnonRateThrottle` — `none`

## **Множественный троттлинг**
Троттлинг в Django-ninja-extra поддерживает несколько ограничений одновременно, что полезно для применения разных ограничений к API,
таких как пиковые лимиты (burst) или продолжительные лимиты (sustained).
Например, вы можете захотеть ограничить пользователей максимум 60 запросами в минуту и 1000 запросами в день.

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
## **Настройка политик троттлинга**
Вы можете глобально задать классы троттлинга и лимиты по умолчанию в `settings.py` вашего проекта, переопределив следующие ключи:
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
Описания лимитов, используемые в `THROTTLE_RATES`, могут включать `second`, `minute`, `hour` или `day` в качестве периода троттлинга.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **Идентификация клиента**
Клиенты идентифицируются через HTTP-заголовок X-Forwarded-For и WSGI-переменную REMOTE_ADDR.
Это уникальные идентификаторы, используемые для определения IP-адреса клиента при троттлинге.
`X-Forwarded-For` имеет приоритет над `REMOTE_ADDR` и используется соответствующим образом.

#### **Ограничение прокси клиента**
Если вам нужно строго определять уникальные IP-адреса клиентов, сначала необходимо настроить количество прокси приложения, работающих за API, установив параметр `NUM_PROXIES`. Это значение должно быть целым числом, большим или равным нулю.
Если задано ненулевое значение, то после исключения IP-адресов прокси приложения IP-адресом клиента будет считаться последний IP-адрес в заголовке X-Forwarded-For. Если задан ноль, в качестве идентифицирующего IP-адреса всегда будет использоваться значение REMOTE_ADDR.
Важно понимать, что если вы настроите `NUM_PROXIES`, то все клиенты за одним уникальным шлюзом [Network Address Translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation) будут рассматриваться как один клиент.

!!! note
    Больше контекста о том, как работает заголовок X-Forwarded-For и как определяются IP-адреса удалённых клиентов, можно найти здесь.

## **Настройки кэша модели троттлинга**
Модель троттлинга, используемая в django-ninja-extra, опирается на кэш-бэкенд Django. Она использует значение `default` [`LocMemCache`]().
Для получения более подробной информации обратитесь к [документации Django по кэшированию](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache).

Если вы не хотите использовать кэш по умолчанию, определённый в модели троттлинга, вот пример того, как определить другой кэш для модели троттлинга:
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **Справочник API**

## **Анонимный троттлинг**
Модель `AnonRateThrottle` используется для ограничения частоты запросов с использованием IP-адреса неаутентифицированных пользователей в качестве ключа.

Она подходит для ограничения частоты запросов из неизвестных источников.

Права на запрос определяются:
- `rate`, определённой в производном классе
- областью видимости (scope) `anon`, определённой в `THROTTLE_RATES` в настройках `NINJA_EXTRA` в `settings.py`.

## **Троттлинг пользователей**
Модель `UserRateThrottle` используется для ограничения частоты запросов путём генерации ключа на основе ID пользователя или первичного ключа аутентифицированных пользователей.
Неаутентифицированные запросы будут использовать IP-адрес входящего запроса для генерации уникального ключа ограничения частоты.

Права на запрос определяются:
- `rate`, определённой в производном классе
- областью видимости (scope) `user`, определённой в `THROTTLE_RATES` в настройках `NINJA_EXTRA` в `settings.py`.


Вы можете использовать несколько лимитов для модели `UserRateThrottle`, например:
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
## **Динамический троттлинг**
Модель `DynamicRateThrottle` используется для троттлинга как аутентифицированных, так и неаутентифицированных пользователей аналогично `UserRateThrottle`.
Её ключевая особенность — возможность динамически задавать `scope` при использовании.
Например:
Мы можем определить scope в настройках.

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
Здесь мы динамически применяем лимит `sustained` и лимит `burst` к `get_users` и `get_user_by_id` соответственно.


!!! note "New in v0.15.8"
    Вы можете применять троттлинг ко всем операциям эндпоинтов контроллера на уровне класса контроллера.

## **Троттлинг контроллера**

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
