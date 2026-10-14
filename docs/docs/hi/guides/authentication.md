---
comments: true
---
# Authentication

## परिचय

**Django Ninja** कई tools प्रदान करता है जिनकी मदद से आप authentication और authorization को आसानी से, तेज़ी से और मानक तरीके से संभाल सकते हैं, बिना <a href="https://swagger.io/docs/specification/authentication/" target="_blank">सभी security specifications</a> को पढ़ने और सीखने की ज़रूरत के।

मुख्य विचार यह है कि जब आप किसी API operation का वर्णन करते हैं, तो आप एक authentication object परिभाषित कर सकते हैं।
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

इस उदाहरण में, client केवल तभी `pets` method को कॉल कर पाएगा जब वह Django session authentication (जो डिफ़ॉल्ट रूप से cookie-आधारित है) का उपयोग करे, अन्यथा एक HTTP-401 error लौटाया जाएगा।
यदि आप केवल superusers को authorize करना चाहते हैं, तो आप `from ninja.security import django_auth_superuser` का उपयोग कर सकते हैं।
## Automatic OpenAPI schema

यहाँ एक उदाहरण है जिसमें client को authenticate करने के लिए एक header पास करनी होती है:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

अब <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> दस्तावेज़ीकरण पर जाएँ।


![Swagger UI Auth](../img/auth-swagger-ui.png)

अब, जब आप **Authorize** बटन पर क्लिक करेंगे, तो आपसे अपना authentication token दर्ज करने के लिए कहा जाएगा।

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

जब आप कोई test कॉल करेंगे, तो हर request authorization header पास करेगी।

## Global authentication

यदि आपको अपनी API की **सभी** methods की सुरक्षा करनी है, तो आप `NinjaAPI` constructor को `auth` argument पास कर सकते हैं:


```python hl_lines="11 19"
from ninja import NinjaAPI, Form
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI(auth=GlobalAuth())

# @api.get(...)
# def ...

# @api.post(...)
# def ...
```

और, यदि आपको कुछ methods को override करने की आवश्यकता है, तो आप इसे `auth` argument पास करके operation स्तर पर फिर से कर सकते हैं। इस उदाहरण में, `/token` operation के लिए authentication अक्षम हो जाएगा:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## उपलब्ध authentication विकल्प

### Custom function


"`auth=`" argument किसी भी callable को स्वीकार करता है। **NinjaAPI** तभी authentication पास करेगा जब callable कोई ऐसा मान लौटाए जो **truthy** हो (boolean `True` में बदलता हो)। यह return मान `request.auth` attribute को सौंप दिया जाएगा।

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API keys

कुछ APIs authorization के लिए API keys का उपयोग करती हैं। एक API key एक token है जिसे client API call करते समय खुद की पहचान करने के लिए प्रदान करता है। Key को query string में भेजा जा सकता है:
```
GET /something?api_key=abcdef12345
```

या request header के रूप में:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

या cookie के रूप में:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** इन स्थितियों को संभालने में आपकी मदद के लिए built-in classes के साथ आता है।


#### Query में

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

इस उदाहरण में, हम `GET['api_key']` से एक token प्राप्त करते हैं और database में संबंधित `Client` ढूँढते हैं। Client instance को `request.auth` attribute के रूप में सेट किया जाएगा।

Note: **`param_name`** उस GET parameter का नाम है जिसकी जाँच की जाएगी। यदि सेट नहीं किया गया है, तो डिफ़ॉल्ट `"key"` का उपयोग किया जाता है।


#### Header में

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### Cookie में

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### HTTP Basic authentication

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## Multiple authenticators

**`auth`** argument के साथ आप कई authenticators भी पास कर सकते हैं:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

इस स्थिति में, **Django Ninja** पहले `GET` से API key की जाँच करेगा, और यदि वह सेट नहीं है या अमान्य है, तो यह `header` key की जाँच करेगा।
यदि दोनों अमान्य हैं, तो यह response में एक authentication error उठाएगा।


## Router authentication

Router पर `auth` argument का उपयोग करें ताकि उसमें घोषित सभी operations पर एक authenticator लागू हो:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

या router constructor का उपयोग करते हुए
```python
router = Router(auth=BasicAuth())
```


## Custom exceptions

ऐसा exception उठाना जिसका एक exception handler हो, operation की तरह ही उस handler का response लौटाएगा:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## Async authentication

**Django Ninja** asynchronous authentication के लिए बुनियादी समर्थन रखता है। हालाँकि डिफ़ॉल्ट authentication classes async-संगत नहीं हैं, फिर भी आप अपना कस्टम async authentication callable परिभाषित कर सकते हैं और उसे `auth` के साथ पास कर सकते हैं।

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


अधिक जानकारी के लिए, [Error handling](errors.md) देखें।

!!! success

    अगले भाग पर जाएँ **[Testing](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
