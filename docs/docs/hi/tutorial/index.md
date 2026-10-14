---
comments: true
---
# Tutorial - पहले कदम

यह tutorial आपको दिखाता है कि **Django Ninja** की ज़्यादातर features का इस्तेमाल कैसे करें।

यह tutorial मानता है कि आप <a href="https://www.djangoproject.com/" target="_blank">Django framework</a> की कम से कम basics जानते हैं, जैसे project कैसे बनाया जाता है और कैसे चलाया जाता है।

## Installation

```console
pip install django-ninja
```

!!! note

    यह ज़रूरी नहीं है, लेकिन आप `ninja` को `INSTALLED_APPS` में भी जोड़ सकते हैं।
    ऐसे में OpenAPI/Swagger UI (या Redoc) bundled JavaScript package से load होगा (जो तेज़ है) (अन्यथा JavaScript bundle एक CDN से आता है)

## एक Django project बनाएँ

एक नया Django project शुरू करें (या, अगर आपके पास पहले से कोई मौजूदा Django project है, तो अगले step पर जाएँ)।

```
django-admin startproject myproject
```

## एक API बनाएँ

आइए अपने API के लिए एक module बनाएँ। अपने Django project के root `urls.py` की उसी जगह एक `api.py` file बनाएँ:

```python
from ninja import NinjaAPI

api = NinjaAPI()
```

अब `urls.py` में जाएँ और निम्नलिखित जोड़ें:

```python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## हमारा पहला operation

**Django Ninja** हर HTTP method (`GET`, `POST`,
`PUT`, आदि) के लिए एक decorator के साथ आता है। अपनी `api.py` file में, आइए एक साधारण "hello world" operation जोड़ें।

```python hl_lines="5-7"
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"
```

अब browser में जाकर <a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> खोलें, जो एक साधारण JSON response return करेगा:
```json
"Hello world"
```

!!! success

    अगले chapter **[Input parameters को handle करना](step2.md)** पर बढ़ें।
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
