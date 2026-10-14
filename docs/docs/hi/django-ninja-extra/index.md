![Test](https://github.com/eadwinCode/django-ninja-extra/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-extra.svg)](https://badge.fury.io/py/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/v/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/pyversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![PyPI version](https://img.shields.io/pypi/djversions/django-ninja-extra.svg)](https://pypi.python.org/pypi/django-ninja-extra)
[![Codecov](https://img.shields.io/codecov/c/gh/eadwinCode/django-ninja-extra)](https://codecov.io/gh/eadwinCode/django-ninja-extra)
[![Downloads](https://pepy.tech/badge/django-ninja-extra)](https://pepy.tech/project/django-ninja-extra)

# Django Ninja Extra Documentation

**Django Ninja Extra** [**Django Ninja**](https://django-ninja.cn) का उपयोग करके आपके RESTful API development को तेज़ करने वाली अतिरिक्त features के साथ एक **class-based** approach प्रदान करता है।

**मुख्य features:**

सभी **Django-Ninja** features:

- **सरल**: उपयोग में आसान और सहज बनाया गया।
- **तेज़ execution**: **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** और **<a href="/async-support/">async support</a> के कारण, यह बहुत उच्च performance प्रदान करता है।**
- **तेज़ coding**: Type hints और automatic documentation आपको business logic पर ध्यान केंद्रित करने देते हैं।
- **Standards-based**: Standards पर आधारित: **OpenAPI** (पूर्व में Swagger) और **JSON Schema**।
- **Django friendly**: (स्पष्ट रूप से) Django core और ORM के साथ अच्छी तरह integrated।

साथ ही **Extra**:

- **Class-based**: अपनी APIs को class-based तरीके से डिज़ाइन करें।
- **Permissions**: Route level या controller level पर परिभाषित permissions और authentication के माध्यम से access endpoints को आसानी से सुरक्षित करें।
- **Dependency injection**: Controller classes Python [**Injector** ](https://injector.readthedocs.io/en/latest/) या [**django_injector**](https://github.com/blubber/django_injector) का उपयोग करने का support करती हैं। यह आपको APIController classes में API dependency services inject करने और उन्हें आवश्यकता के स्थान पर उपयोग करने की अनुमति देता है।

---

### Version Requirements
- Python >= 3.6
- django >= 2.1 
- pydantic >= 1.6 
- Django-Ninja >= 0.16.1


पूर्ण documentation के लिए, [इस link पर जाएँ](https://django-ninja.cn/django-ninja-extra/)।

## Installation

```
pip install django-ninja-extra
```
Installation के बाद, `ninja_extra` को अपनी `INSTALLED_APPS` में जोड़ें

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```

## Usage

अपने Django project में, `urls.py` के बगल में एक नई `api.py` फ़ाइल बनाएं:

```Python
from ninja_extra import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()

# Function-based definition
@api.get("/add", tags=['Math'])
def add(request, a: int, b: int):
    return {"result": a + b}

# Class-based definition
@api_controller('/', tags=['Math'], permissions=[])
class MathAPI:

    @http_get('/subtract',)
    def subtract(self, a: int, b: int):
        """Subtracts a from b"""
        return {"result": a - b}

    @http_get('/divide',)
    def divide(self, a: int, b: int):
        """Divides a by b"""
        return {"result": a / b}
    
    @http_get('/multiple',)
    def multiple(self, a: int, b: int):
        """Multiples a with b"""
        return {"result": a * b}
    
api.register_controllers(
    MathAPI
)
```

अब `urls.py` पर जाएँ और निम्नलिखित जोड़ें:

```Python
...
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # <---------- !
]
```

### Interactive API documentation

अब <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a> पर जाएँ

आप automatic interactive API documentation देखेंगे (<a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a> द्वारा संचालित):

![Swagger UI](images/ui_swagger_preview_readme.gif)

## Tutorials
- [django-ninja - Using django-ninja-extra permissions, controllers and throttling!](https://www.youtube.com/watch?v=yQqig-c2dd4) - django-ninja-extra permissions, controllers और throttling का उपयोग करना सीखें
- [BookStore API](https://github.com/eadwinCode/bookstoreapi) - ninja schema और ninja-jwt के साथ django-ninja-extra का उपयोग प्रदर्शित करने वाला एक नमूना project

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
