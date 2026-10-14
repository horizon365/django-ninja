---
comments: true
---
# **バージョニング**

## **異なる API バージョン番号**

**Django Ninja Extra** を使えば、単一の Django プロジェクトから複数の API バージョンを非常に簡単に運用できます。

必要なのは、異なる `version` パラメータを持つ NinjaAPI インスタンスを 2 つ以上作成することだけです：


**`api_v1.py`**:

```Python
from ninja_extra import NinjaExtraAPI, route, api_controller

@api_controller
class MyV1Controller:
    @route.get('/hello')
    def hello(self):
        return {'message': 'Hello from V1'}
    
    @route.get('/example')
    def example(self):
        return {'message': 'Hello from V1 Example'}

    
api = NinjaExtraAPI(version='1.0.0')
api.register_controllers(MyV1Controller)
```


api_**v2**.py:
API コントローラを再利用しつつ、特定のルートだけ変更を加えることができます。

```Python
from ninja_extra import NinjaExtraAPI, route, api_controller
from .api_v1 import MyV1Controller

@api_controller
class MyV2Controller(MyV1Controller):
    @route.get('/example')
    def example(self):
        return {'message': 'Hello from V2 Example'}

    
api = NinjaExtraAPI(version='2.0.0')
api.register_controllers(MyV2Controller)
```


次に **urls.py** で：

```Python hl_lines="8 9"
...
from api_v1 import api as api_v1
from api_v2 import api as api_v2


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
]

```


これで、バージョンごとに異なる OpenAPI ドキュメントページにアクセスできるようになります：

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **異なるビジネスロジック**

同じやり方で、コンポーネントやドメインごとに異なる API を定義することもできます：

```Python
...


api = NinjaExtraAPI(auth=token_auth, urls_namespace='public_api')
...

api_private = NinjaExtraAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/', api.urls),
    path('internal-api/', api_private.urls),
]

```
!!! note
    異なる **NinjaExtraAPI** インスタンスを使用する場合は、異なる `version` か異なる `urls_namespace` を定義する必要があります。
    これは **NinjaAPI** インスタンスの場合も同様です。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
