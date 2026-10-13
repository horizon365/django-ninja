---
comments: true
---
# **Versioning**

## **Different API Version Numbers**

Using **Django Ninja Extra**, it is very easy to run multiple API versions from a single Django project.

All you have to do is create two or more NinjaAPI instances with different `version` parameters:


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
You can reuse your API controllers and make changes to specific routes.

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


Then in **urls.py**:

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


Now you can access different OpenAPI documentation pages for each version:

 - http://127.0.0.1/api/**v1**/docs
 - http://127.0.0.1/api/**v2**/docs



## **Different Business Logic**

In the same way, you can define different APIs for different components or domains:

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
    If you use different **NinjaExtraAPI** instances, you need to define different `version`s or different `urls_namespace`s.
    This is the same for **NinjaAPI** instances.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
