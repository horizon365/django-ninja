---
comments: true
---
# **Tutorial / Reference**

यह tutorial आपको दिखाता है कि **Django Ninja Extra** और उसकी अधिकांश features का उपयोग कैसे करें।
विशेष रूप से, यह मानता है कि आप **Django Ninja** का उपयोग करना जानते हैं


!!! info
    यहाँ की अधिकांश सामग्री Django-Ninja से ली गई है। इसलिए यदि आप पहले Django-Ninja framework के बारे में सीखते हैं, तो इसमें से अधिकांश समझ में आ जाएगा।

## **Installation**

```
pip install django-ninja-extra
```

Installation के बाद, `ninja_extra` को `INSTALLED_APPS` में जोड़ें

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **एक Django Project बनाना**

(यदि आपके पास पहले से कोई मौजूदा Django project है, तो अगले चरण पर जाएं)।

एक नया Django project शुरू करें (या किसी मौजूदा का उपयोग करें)।

```
django-admin startproject myproject
```


## **पहला चरण**

आइए अपने API के लिए एक module बनाएं। **urls.py** के समान directory location में एक **api.py** फ़ाइल बनाएं:


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

अब **urls.py** पर जाएं और निम्नलिखित जोड़ें:


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **Operation methods परिभाषित करना**
एक "operation" HTTP "methods" में से एक हो सकता है:

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... और भी बहुत कुछ।

ये वे operations हैं जो Django-Ninja द्वारा API या Django-Ninja router पर परिभाषित किए जाते हैं।

वे ही operations `route` class के माध्यम से APIControllers को exposed किए जाते हैं।

`route` class एक अतिरिक्त decorator है जो APIController instance methods को route functions या endpoints में बदलता है।

दूसरी ओर, यहाँ `route`, `ControllerRouter` class का संक्षिप्त रूप है, जो एक adapter class है जो बस APIController को Django-Ninja router के अनुकूलित करती है। यह किसी भी APIController class में परिभाषित सभी routes पर global नियंत्रण भी प्रदान करता है।

```Python
from ninja_extra import (
    api_controller, 
    http_get, http_post, http_put, http_delete, http_patch, http_generic
)
from ninja.constants import NOT_SET

@api_controller('', tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyAPIController:
    @http_get("/path")
    def get_operation(self):
        ...
    
    @http_post("/path")
    def post_operation(self):
        ...
    
    @http_put("/path")
    def put_operation(self):
        ...
    
    @http_delete("/path")
    def delete_operation(self):
        ...
    
    @http_patch("/path")
    def patch_operation(self):
        ...
    
    # If you need to handle multiple methods with a single function, you can use the `generic` method as shown above
    @http_generic(["POST", "PATCH"]) 
    def mixed(request):
        ...

api.register_controllers(MyAPIController)
```
Controller setup को पूरा करने के लिए, आपको APIController को register करने से पहले `ControllerRouter` के साथ decorate करना होगा।


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
