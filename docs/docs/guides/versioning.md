---
comments: true
---
# 版本控制

## 不同的 API 版本号

使用 **Django Ninja** ，从单个 Django 项目中运行多个 API 版本很容易。
你所要做的就是创建两个或更多具有不同 `version` 参数的 NinjaAPI 实例：

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


然后在 **urls.py** 中:

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


现在你可以为每个版本访问不同的 OpenAPI 文档页面：

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## 不同的业务逻辑

以同样的方式，你可以为不同的组件或领域定义不同的 API：
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
!!! 注意
    如果你使用不同的 **NinjaAPI** 实例，你需要定义不同的 `version` 或不同的 `urls_namespace`。
