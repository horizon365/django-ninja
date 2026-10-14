---
comments: true
---
# API Documentation

## OpenAPI docs

एक बार जब आप अपनी Ninja API कॉन्फ़िगर कर लें और runserver शुरू कर दें - तो <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> पर जाएँ

आपको स्वचालित, इंटरैक्टिव API दस्तावेज़ीकरण दिखाई देगा (<a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> द्वारा संचालित)


## CDN और static files

आपको `INSTALLED_APPS` में django ninja जोड़ने की आवश्यकता नहीं है। इस स्थिति में इंटरैक्टिव UI एक CDN से होस्ट किया जाएगा।

दस्तावेज़ीकरण (Js/css) को अपने ही server से होस्ट करने के लिए - बस `"ninja"` को INSTALLED_APPS में डालें - इस स्थिति में मानक django static files होस्टिंग तंत्र इसे होस्ट करेगा।

## Redoc पर स्विच करें


```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())

```
तब आपको एक और ऑटो-जेनरेटेड दस्तावेज़ीकरण दिखाई देगा (<a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> द्वारा संचालित)।

## दस्तावेज़ीकरण प्रदर्शन सेटिंग्स बदलें
Swagger या Redocs के लिए कुछ कस्टम सेटिंग्स सेट करने के लिए, आप docs class पर `settings` argument का उपयोग कर सकते हैं।

```python
from ninja import Redoc, Swagger

api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
...
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))

```

अन्य सेटिंग्स के लिए, दस्तावेज़ीकरण देखें:

 - [Swagger configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
 - [Redoc configuration](https://redocly.com/docs/api-reference-docs/configuration/functionality/)



## Docs छिपाएँ

यदि आपको इंटरैक्टिव दस्तावेज़ीकरण प्रदर्शित करने की आवश्यकता नहीं है - तो `docs_url` argument को `None` पर सेट करें

```python
api = NinjaAPI(docs_url=None)
```

## Docs की सुरक्षा करें

Authentication (या किसी भी उद्देश्य के लिए कोई अन्य decorator) का उपयोग करने के लिए, `docs_decorator` argument का उपयोग करें:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## OpenAPI schema को कस्टम attributes के साथ बढ़ाएँ

आप OpenAPI schema को कस्टम attributes के साथ बढ़ा सकते हैं, उदाहरण के लिए `termsOfService` जोड़ना

```python
api = NinjaAPI(
   openapi_extra={
       "info": {
           "termsOfService": "https://example.com/terms/",
       }
   },
   title="Demo API",
   description="This is a demo API with dynamic OpenAPI info section"
)
```

## दस्तावेज़ीकरण URL को resolve करना

आप view के नाम `openapi-view` का संदर्भ देकर API के दस्तावेज़ीकरण view का URL reverse कर सकते हैं।

Python code में, उदाहरण के लिए:
```python
from django.urls import reverse

reverse('api-1.0.0:openapi-view')

>>> '/api/docs'
```

Django templates में, उदाहरण के लिए:
```Html
<a href="{% url 'api-1.0.0:openapi-view' %}">API Docs</a>

<a href="/api/docs">API Docs</a>
```

## एक कस्टम docs viewer बनाएँ

अपना खुद का OpenAPI view बनाने के लिए - DocsBase से inherit करने वाली एक class बनाएँ और `render_page` method को override करें:



```python
from ninja.openapi.docs import DocsBase

class MyDocsViewer(DocsBase):
    def render_page(self, request, api):
        ... # return http response

...

api = NinjaAPI(docs=MyDocsViewer())

```

!!! success

    अगले भाग पर जाएँ **[Error handling](errors.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
