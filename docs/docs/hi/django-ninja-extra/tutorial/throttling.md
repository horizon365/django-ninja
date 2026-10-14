---
comments: true
---
# **Throttling / Rate Control**

Throttling को एक permission के रूप में देखा जा सकता है जो यह निर्धारित करता है कि request को authorize किया जाना चाहिए या नहीं।
यह एक अस्थायी state का प्रतिनिधित्व करता है जिसका उपयोग clients द्वारा API को requests भेजने की दर को नियंत्रित करने के लिए किया जाता है।

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    ऊपर दिया गया उदाहरण throttle नहीं किया जाएगा, क्योंकि `UserRateThrottle` और `AnonRateThrottle` का डिफ़ॉल्ट scope `none` है

## **Multiple Throttling**
Django-ninja-extra throttling कई throttles का समर्थन करता है, जो एक API पर विभिन्न constraints लागू करने के लिए उपयोगी है,
जैसे burst throttle rates या sustained throttle rates।
उदाहरण के लिए, आप users को प्रति मिनट अधिकतम 60 requests और प्रति दिन 1000 requests तक सीमित करना चाह सकते हैं।

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
आप अपने project की `settings.py` में निम्नलिखित keys को override करके डिफ़ॉल्ट throttle classes और rates को globally सेट कर सकते हैं:
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
`THROTTLE_RATES` में उपयोग किए गए rate descriptions में throttle अवधि के रूप में `second`, `minute`, `hour`, या `day` शामिल हो सकते हैं।

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
Clients को HTTP header X-Forwarded-For और WSGI variable REMOTE_ADDR के माध्यम से पहचाना जाता है।
ये वे unique identifiers हैं जिनका उपयोग throttling के लिए client IP address को पहचानने के लिए किया जाता है।
`X-Forwarded-For`, `REMOTE_ADDR` पर प्राथमिकता रखता है और इसी तरह उपयोग किया जाता है।

#### **Client Proxies को प्रतिबंधित करना**
यदि आपको unique client IP addresses को सख्ती से पहचानने की आवश्यकता है, तो आपको पहले `NUM_PROXIES` setting सेट करके API के पीछे चल रहे application proxies की संख्या configure करने की आवश्यकता है। यह setting शून्य या उससे अधिक का एक integer होनी चाहिए।
यदि इसे एक non-zero मान पर सेट किया जाता है, तो एक बार किसी भी application proxy IP addresses को पहले exclude करने के बाद, client IP को X-Forwarded-For header में अंतिम IP address के रूप में पहचाना जाएगा। यदि इसे शून्य पर सेट किया जाता है, तो REMOTE_ADDR मान का उपयोग हमेशा पहचानने वाले IP address के रूप में किया जाएगा।
यह समझना महत्वपूर्ण है कि यदि आप `NUM_PROXIES` configure करते हैं, तो एक single unique [Network Address Translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation) gateway के पीछे के सभी clients को एक single client माना जाएगा।

!!! note
    X-Forwarded-For header कैसे काम करता है और remote client IPs की पहचान कैसे की जाती है, इसके बारे में अधिक जानकारी यहाँ मिल सकती है।

## **Throttle Model Cache Settings**
Django-ninja-extra में उपयोग किया गया throttle model Django cache backend का लाभ उठाता है। यह [`LocMemCache`]() के `default` मान का उपयोग करता है।
अधिक जानकारी के लिए, कृपया Django के [cache documentation](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) को देखें।

यदि आप throttle model में परिभाषित डिफ़ॉल्ट cache का उपयोग नहीं करना चाहते हैं, तो यहाँ throttle model के लिए एक अलग cache define करने का एक उदाहरण दिया गया है:
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **API Reference**

## **Anonymous Rate Throttling**
`AnonRateThrottle` model का उपयोग बिना authenticated उपयोगकर्ताओं के IP address को key के रूप में उपयोग करके throttle limiting के लिए किया जाता है।

यह अज्ञात स्रोतों से आने वाली requests की दर को सीमित करने के लिए उपयुक्त है।

Request permissions निम्न द्वारा निर्धारित होते हैं:
- Derived class में परिभाषित `rate`
- `settings.py` में `NINJA_EXTRA` settings में `THROTTLE_RATES` में परिभाषित `anon` scope।

## **User Rate Throttling**
`UserRateThrottle` model का उपयोग authenticated उपयोगकर्ताओं के user ID या primary key का उपयोग करके एक key बनाकर throttle limiting के लिए किया जाता है।
बिना authenticated requests वाले उपयोगकर्ता throttle limiting के लिए एक unique key बनाने के लिए incoming request के IP address का उपयोग करने पर वापस आ जाएंगे।

Request permissions निम्न द्वारा निर्धारित होते हैं:
- Derived class में परिभाषित `rate`
- `settings.py` में `NINJA_EXTRA` settings में `THROTTLE_RATES` में परिभाषित `user` scope।


आप `UserRateThrottle` model के लिए कई user throttle rates का उपयोग कर सकते हैं, उदाहरण के लिए:
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
`DynamicRateThrottle` model का उपयोग authenticated और बिना authenticated दोनों उपयोगकर्ताओं को `UserRateThrottle` के समान तरीके से throttle करने के लिए किया जाता है।
इसकी मुख्य विशेषता यह है कि इसके उपयोग के समय `scope` को dynamically सेट करने की क्षमता है।
उदाहरण के लिए:
हम settings में एक scope define कर सकते हैं।

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
यहाँ, हम `get_users` और `get_user_by_id` पर क्रमशः `sustained` rate और `burst` rate को dynamically लागू करते हैं।


!!! note "New in v0.15.8"
    आप controller class level पर सभी controller endpoint operations को throttle कर सकते हैं।

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
