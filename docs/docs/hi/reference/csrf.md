---
comments: true
---
# CSRF (Cross-Site Request Forgery)

## Cross-site request forgery क्या है?
> [Cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) तब होती है जब कोई दुर्भावनापूर्ण (malicious) website में ऐसा link, form button, या कुछ JavaScript होता है जो किसी logged-in user के credentials (जो अपने browser में उस malicious website पर जाता है) का इस्तेमाल करके आपकी website पर (या इस document में शामिल न की गई अन्य जगहों पर) कुछ action करवाना चाहता है।


## Django Ninja के साथ cross-site request forgery से कैसे बचें
### ऐसे authentication methods इस्तेमाल करें जो automatically requests में embed नहीं होते
Cross-site request forgery attacks उन authentication methods पर निर्भर करते हैं जो दूसरी websites से आने वाली requests में automatically शामिल हो जाते हैं, जैसे [cookies](https://en.wikipedia.org/wiki/HTTP_cookie) या [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)।
ऐसा authentication method इस्तेमाल करना जो automatically embed नहीं होता, जैसे `Authorization: Bearer`, इस attack को कम करता है।


### Django की built-in cross-site request forgery protection का इस्तेमाल करें
अगर आप cookies का इस्तेमाल करने वाली default Django authentication का इस्तेमाल कर रहे हैं, तो आपको default [Django cross-site request forgery protection](https://docs.djangoproject.com/en/4.2/ref/csrf/) का भी इस्तेमाल करना होगा।


डिफ़ॉल्ट रूप से, **Django Ninja** में सभी operations के लिए cross-site request forgery protection **OFF** रहती है।
इसे चालू करने के लिए, आपको NinjaAPI class के `csrf` argument का इस्तेमाल करना होगा:

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Warning</span>: Cross-site request forgery बंद रखकर cookie-आधारित authentication का इस्तेमाल करना असुरक्षित है! (जैसे `CookieKey`, या `django_auth`)।


**Django Ninja** cookie-आधारित authentication के लिए cross-site request forgery automatically enable कर देगा।


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


या django-auth पर आधारित (जो cookie-आधारित authentication से inherit करता है):

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Django `ensure_csrf_cookie` decorator
आप किसी unprotected route पर Django का [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) decorator इस्तेमाल कर सकते हैं ताकि वह route cross-site request forgery token के लिए एक `Set-Cookie` header include करे। ध्यान रखें:
- Route decorator को [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) decorator से पहले (यानी उसके ऊपर) execute होना चाहिए।
- आपको उस route को `csrf_exempt` करना होगा।
- `ensure_csrf_cookie` decorator केवल Django `HttpResponse` पर काम करता है, dictionary पर नहीं जैसा कि ज़्यादातर Django Ninja decorators के साथ होता है।
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
इस route को किया गया request Django से उचित `Set-Cookie` header वाला response trigger करेगा।


#### Front-end code
आप [AJAX के साथ CSRF protection का इस्तेमाल करना](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) और [AJAX request पर token set करना](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) sections को [Django की CSRF protection का इस्तेमाल कैसे करें](https://docs.djangoproject.com/en/4.2/howto/csrf/) से पढ़कर सीख सकते हैं कि अपने front-end code में cross-site request forgery protection token को कैसे handle करें।


## CORS के बारे में
आप शायद अपने front-end और API को अलग-अलग sites पर setup करना चाहें (ऐसे में आप [django-cors-headers](https://github.com/adamchainz/django-cors-headers) देख सकते हैं)।
हालाँकि यह सीधे तौर पर cross-site request forgery से संबंधित नहीं है, लेकिन CORS (Cross-Origin Resource Sharing) तब मददगार होता है जब आप front-end वाली site से अलग किसी site पर cross-site request forgery cookies define करते हैं, क्योंकि [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) इसकी डिफ़ॉल्ट रूप से इजाज़त नहीं देती।
फिर आप [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme) देख सकते हैं।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
