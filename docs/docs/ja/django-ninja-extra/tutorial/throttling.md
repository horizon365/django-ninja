---
comments: true
---
# **スロットリング / レート制限**

スロットリングは、リクエストを認可すべきかどうかを決めるパーミッションの一種と見なすことができます。
これは、クライアントが API に対してリクエストできるレートを制御するために使われる一時的な状態を表します。

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    上の例はスロットリングされません。`UserRateThrottle` と `AnonRateThrottle` のデフォルトのスコープは `none` だからです

## **複数のスロットリング**
django-ninja-extra のスロットリングは複数のスロットルをサポートしており、バースト時のスロットルレートや持続的なスロットルレートのように、API に対して異なる制約を適用するのに便利です。
たとえば、ユーザーを毎分最大 60 リクエスト、かつ 1 日あたり 1000 リクエストに制限したい場合があります。

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
## **スロットルポリシーの設定**
プロジェクトの `settings.py` で、次のキーを上書きすることにより、デフォルトのスロットルクラスとレートをグローバルに設定できます：
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
`THROTTLE_RATES` で使用されるレートの記述には、スロットル期間として `second`、`minute`、`hour`、`day` を含めることができます。

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **クライアントの識別**
クライアントは、HTTP ヘッダー X-Forwarded-For と WSGI 変数 REMOTE_ADDR を通じて識別されます。
これらは、スロットリングのためにクライアントの IP アドレスを識別するために使われる一意の識別子です。
`X-Forwarded-For` は `REMOTE_ADDR` よりも優先され、そのように使われます。

#### **クライアントプロキシの制限**
一意のクライアント IP アドレスを厳密に識別する必要がある場合は、まず `NUM_PROXIES` 設定をセットして、API の背後で動作しているアプリケーションプロキシの数を設定する必要があります。この設定は 0 以上の整数にする必要があります。
非ゼロの値を設定した場合、まずアプリケーションプロキシの IP アドレスが除外されたうえで、クライアントの IP は X-Forwarded-For ヘッダー内の最後の IP アドレスとして識別されます。ゼロを設定した場合は、REMOTE_ADDR の値が常に識別用の IP アドレスとして使われます。
`NUM_PROXIES` を設定した場合、単一の一意の [ネットワークアドレス変換（NAT）](https://en.wikipedia.org/wiki/Network_address_translation) ゲートウェイの背後にあるすべてのクライアントが 1 つのクライアントとして扱われることを理解しておくことが重要です。

!!! note
    X-Forwarded-For ヘッダーの仕組みやリモートクライアントの IP を識別する方法についての詳しい情報は、こちらをご覧ください。

## **スロットルモデルのキャッシュ設定**
django-ninja-extra で使われるスロットルモデルは、Django のキャッシュバックエンドを利用します。[`LocMemCache`]()` の `default` の値を使用します。
詳しくは、Django の [キャッシュドキュメント](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) を参照してください。

スロットルモデルで定義されたデフォルトのキャッシュを使いたくない場合は、スロットルモデルに別のキャッシュを定義する方法の例を以下に示します：
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **API リファレンス**

## **匿名レートスロットリング**
`AnonRateThrottle` モデルは、未認証ユーザーの IP アドレスをキーとして使ってスロットル制限を行うために使われます。

未知の送信元からのリクエストのレートを制限するのに適しています。

リクエストの許可は次によって決まります：
- 派生クラスで定義された `rate`
- `settings.py` の `NINJA_EXTRA` 設定にある `THROTTLE_RATES` で定義された `anon` スコープ。

## **ユーザーレートスロットリング**
`UserRateThrottle` モデルは、認証済みユーザーのユーザー ID またはプライマリキーを使ってキーを生成することでスロットル制限を行うために使われます。
未認証のリクエストは、受信リクエストの IP アドレスを使ってスロットル制限用の一意のキーを生成するフォールバックが行われます。

リクエストの許可は次によって決まります：
- 派生クラスで定義された `rate`
- `settings.py` の `NINJA_EXTRA` 設定にある `THROTTLE_RATES` で定義された `user` スコープ。


`UserRateThrottle` モデルには複数のユーザースロットルレートを使用できます。たとえば：
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
## **ダイナミックレートスロットリング**
`DynamicRateThrottle` モデルは、`UserRateThrottle` と同様の方法で、認証済みユーザーと未認証ユーザーの両方をスロットリングするために使われます。
その最大の特徴は、使用時に `scope` を動的に設定できることです。
たとえば：
設定にスコープを定義できます。

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
ここでは、`get_users` と `get_user_by_id` にそれぞれ `sustained` レートと `burst` レートを動的に適用しています。


!!! note "New in v0.15.8"
    コントローラクラスレベルで、そのコントローラのすべてのエンドポイントオペレーションをスロットリングできます。

## **コントローラのスロットリング**

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
