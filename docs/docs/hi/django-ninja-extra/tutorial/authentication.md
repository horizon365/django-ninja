---
comments: true
---
# **Authentication**

**Django Ninja Extra**, authorization और authentication के मामले में **Django Ninja** के समान API प्रदान करता है, जिससे दोनों packages के बीच consistency और उपयोग में आसानी सुनिश्चित होती है।

## **Automatic OpenAPI Schema**

यहाँ एक उदाहरण दिया गया है जहाँ client को authentication के लिए एक header पास करने की आवश्यकता होती है:

`Authorization: Bearer supersecret`

```Python
from ninja.security import HttpBearer
from ninja_extra import api_controller, route
from ninja.constants import NOT_SET


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    def bearer(self):
        return {"token": self.context.request.auth}

```

## **Global Authentication** 

यदि आपको `api` और APIController में परिभाषित **सभी** route methods को protect करने की आवश्यकता है, तो आप `NinjaExtraAPI` constructor को `auth` parameter पास कर सकते हैं:


```Python
from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaExtraAPI(auth=GlobalAuth())

```
Django-Ninja पर [authentication](https://django-ninja.cn/guides/authentication/) के बारे में अधिक पढ़ें।

## Async Authentication Classes

Ninja Extra, Django Ninja द्वारा `ninja_extra.security` package में प्रदान की गई सभी `Auth` base classes में async support जोड़ता है,
और एक समान interface बनाए रखता है। यह ध्यान रखना महत्वपूर्ण है कि इन async authentication classes का उपयोग करते समय, endpoint handler **एक async function होना चाहिए**।

उदाहरण के लिए, आइए पहले authentication example को `AsyncHttpBearer` class के साथ दोबारा लिखें।

```Python
from ninja_extra import api_controller, route
from ninja_extra.security import AsyncHttpBearer
from ninja.constants import NOT_SET


class AuthBearer(AsyncHttpBearer):
    async def authenticate(self, request, token):
        # await some actions
        if token == "supersecret":
            return token


@api_controller(tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyController:
    @route.get("/bearer", auth=AuthBearer())
    async def bearer(self):
        return {"token": self.context.request.auth}

```
ऊपर दिए गए उदाहरण में, हमने `HttpBearer` को `AsyncHttpBearer` में बदला और bearer को एक `async` endpoint में बदल दिया। 
यदि `AuthBearer` को `MyController` की **authentication** पर लागू किया जाना है, तो `MyController` के अंतर्गत सभी route handlers async route handlers होने चाहिए।


## **JWT Authentication**
यदि आप JWT authentication का उपयोग करना चाहते हैं। देखें [ninja-jwt](https://pypi.org/project/django-ninja-jwt/)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
