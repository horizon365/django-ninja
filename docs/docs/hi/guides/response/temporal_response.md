---
comments: true
---
# Response को ढालना (Tweaking the Response)

कभी-कभी आप response को ठीक serve होने से ठीक पहले बदलना चाहेंगे, उदाहरण के लिए एक header जोड़ने या cookie बदलने के लिए।

इसके लिए, बस `HttpResponse` type का एक function argument घोषित करें:

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## Temporal Response Object

इस response object का उपयोग Django Ninja द्वारा बनाए जाने वाले सभी responses के आधार के रूप में किया जाता है, जिनमें error responses शामिल हैं।
यदि कोई Django `HttpResponse` object सीधे किसी operation द्वारा लौटाया जाता है, तो इस object का उपयोग *नहीं* किया जाता।

जाहिर है कि इस response object में अभी content नहीं होगा, लेकिन यह `content_type` सेट करता है (हालाँकि संभवतः आप इसे बदलना नहीं चाहेंगे)।

`status_code` return मान के आधार पर override किया जाएगा (डिफ़ॉल्ट 200 है, या यदि दो-भागों वाला tuple लौटाया जाए तो वह status code)।


## Base Response Object को बदलना

आप `NinjaAPI.create_temporal_response` method को override करके इस temporal response object को बदल सकते हैं।

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    अगले अध्याय पर जाएँ! **[Generating Schemas from Django Models](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
