---
comments: true
---
# バージョニング

## 異なる API バージョン

**Django Ninja** を使えば、単一の Django プロジェクトから複数の API バージョンを簡単に運用できます。
必要なのは、異なる `version` 引数を持つ 2 つ以上の NinjaAPI インスタンスを作成することだけです:

**api_v1.py**:

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='1.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V1'}

```


api_**v2**.py:

```python hl_lines="4"
from ninja import NinjaAPI


api = NinjaAPI(version='2.0.0')

@api.get('/hello')
def hello(request):
    return {'message': 'Hello from V2'}
```


そして **urls.py** で:

```python hl_lines="8 9"
...
from api_v1 import api as api_v1
from api_v2 import api as api_v2


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
]

```


これで、バージョンごとに異なる OpenAPI ドキュメントページにアクセスできます:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## 異なるビジネスロジック

同じように、異なるコンポーネントやドメインに対して異なる API を定義できます:
```python hl_lines="4 7"
...


api = NinjaAPI(auth=token_auth, urls_namespace='public_api')
...

api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/', api.urls),
    path('internal-api/', api_private.urls),
]

```
!!! note
    異なる **NinjaAPI** インスタンスを使用する場合は、異なる `version` または異なる `urls_namespace` を定義する必要があります。

!!! success

    How-to シリーズが完了しました！

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
