
Ninja JWT, आपके API endpoints तक पहुँचने वाले उपयोगकर्ताओं को authenticate करने के तरीके के रूप में Django Ninja के `HttpBearer` का उपयोग करता है।
Authenticated उपयोगकर्ता को `request.user` या `request.auth` में पाया जा सकता है।

### Route Authentication - Class Based

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=JWTAuth())
    def some_endpoint(self):
        ...
```

### Route Authentication - Function Based

```python
from ninja import router
from ninja_jwt.authentication import JWTAuth

router = router('')

@router.get('/some-endpoint', auth=JWTAuth())
def some_endpoint(request):
    ...
```

Custom Authentication Implementation
-------
यदि आप `JWTAuth` का कोई अलग implementation उपयोग करना चाहते हैं, तो आपको `JWTBaseAuthentication` को subclass करने की आवश्यकता है।
यदि आप `bearer` के अलावा कुछ और उपयोग करना चाहते हैं, तो [Django Ninja - Authentication](https://django-ninja.rest-framework.com/tutorial/authentication/) के बारे में अधिक पढ़ें।

उदाहरण:
```python
from ninja.security import APIKeyHeader
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja import router

class ApiKey(APIKeyHeader, JWTBaseAuthentication):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        return self.jwt_authenticate(request, token=key)


header_key = ApiKey()
router = router('')

@router.get("/headerkey", auth=header_key)
def apikey(request):
    return f"Token = {request.auth}"

```

### Asynchronous Route Authentication
यदि आप asynchronous route authentication में रुचि रखते हैं, तो एक `AsyncJWTAuth` class उपलब्ध है

```python
from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

@api_controller
class MyController:
    @route.get('/some-endpoint', auth=AsyncJWTAuth())
    async def some_endpoint(self):
        ...
```
ध्यान दें: `some_endpoint` asynchronous होना चाहिए। `AsyncJWTAuth` से marked कोई भी endpoint function asynchronous होना चाहिए।

!!! warning
    Asynchronous functionality केवल Django versions > 3.0 के लिए उपलब्ध है।

!!! success

    अगले अध्याय **[Settings](settings.md)** पर जारी रखें।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
