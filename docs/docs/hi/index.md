---
title: Django Ninja - तेज़ Django REST framework
template: home.html
comments: true
---

Django Ninja, Django और Python 3.6+ type hints के साथ API बनाने के लिए एक web framework है।

मुख्य विशेषताएँ:

 - **समझने में आसान**: इस्तेमाल में आसान और सहज (intuitive) बनाया गया है।
 - **तेज़ execution**: **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** और **<a href="guides/async-support/">async support</a>** की बदौलत, इसका performance बहुत बेहतरीन है।
 - **कोड लिखने में तेज़**: Django Ninja, Django और Python 3.6+ type hints के साथ API बनाने के लिए एक web framework है।
 - **मानकों (standards) पर आधारित**: मानकों पर आधारित: **OpenAPI** (पहले Swagger) और **JSON Schema**।
 - **Django friendly**: (ज़ाहिह तौर पर) Django core और ORM के साथ अच्छी तरह integrate होता है।
 - **Production ready**: कई कंपनियों द्वारा वास्तविक projects में इस्तेमाल किया जा रहा है (अगर आप Django Ninja इस्तेमाल करते हैं और अपनी feedback publish करना चाहते हैं, तो कृपया ppr.vitaly@gmail.com पर email करें)।

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">Benchmarks</a>:

![Django Ninja REST Framework](img/benchmark.png)

## Installation

```
pip install django-ninja
```

## Quick example

एक नया Django project शुरू करें (या किसी मौजूदा project का इस्तेमाल करें)
```
django-admin startproject apidemo
```

`urls.py` में

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

अब, इसे हमेशा की तरह चलाएँ:
```
./manage.py runserver
```

ध्यान दें: इसे काम करने के लिए आपको Django Ninja को अपनी installed apps में जोड़ने की ज़रूरत नहीं है।

## इसे check करें

अपना browser खोलें: <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

आपको JSON response ऐसा दिखेगा:
```JSON
{"result": 3}
```
अब आपने अभी-अभी एक ऐसा API बनाया है जो:

 - `/api/add` पर एक HTTP GET request receive करता है
 - GET parameters `a` और `b` को receive, validate और type-convert करता है
 - result को JSON के रूप में decode करता है
 - परिभाषित operation के लिए एक OpenAPI schema generate करता है

## Interactive API documentation

अब यहाँ जाएँ: <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

आपको automatic, interactive API documentation दिखेगी (जो <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> या <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> द्वारा प्रदान की गई है):

![Swagger UI](img/index-swagger-ui.png)


## सारांश

संक्षेप में, आप parameters, request body, आदि के types को **केवल एक बार** declare करते हैं, function arguments के रूप में।

आप यह मानक, आधुनिक Python types के साथ करते हैं।

आपको कोई नया syntax, किसी specific library के methods या classes, आदि सीखने की ज़रूरत नहीं है।

बस मानक **Python 3.6+**।

उदाहरण के लिए, एक `int` के लिए:

```python
a: int
```

या, एक अधिक जटिल `Item` model के लिए:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...इतनी-सी एक declaration से, आपको मिलता है:

* Editor support, जिसमें शामिल है:
    * Autocompletion
    * Type checking
* Data validation:
    * Data invalid होने पर automatic और स्पष्ट errors
    * गहराई तक nested JSON objects के लिए भी validation
* Network input data की <abbr title="इसे यह भी कहते हैं: serialization, parsing, marshalling">Serialization</abbr> और Python data output में conversion, और इनसे पढ़ना:
    * JSON
    * Path parameters
    * Query parameters
    * Cookies
    * Headers
    * Forms
    * Files
* Automatic, interactive API documentation

यह project <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> से बहुत अधिक प्रेरित (inspired) है।

!!! note

    जल्दी शुरुआत करने के लिए **[Tutorial](tutorial/index.md)** देखें।

    Django Ninja के आस-पास का ecosystem:

    1. [django-ninja](index.md): Django पर आधारित एक framework जो Django के सर्वोत्तम गुणों को Pydantic की शक्ति के साथ जोड़ता है — security और सुविधा के बीच संतुलन का सर्वोत्तम विकल्प।

    2. [django-ninja-crud](django-ninja-crud/index.md): django-ninja पर बना एक framework जो CRUD interface development को आसान बनाता है, जो declarative model viewsets और scenario-आधारित testing methods प्रदान करता है।

    3. [django-ninja-extra](django-ninja-extra/index.md): एक tool जो developers को लंबे-चौड़े Django documentation से बचाता है और न्यूनतम code के साथ तेज़ी से शक्तिशाली web applications और आधुनिक API interfaces बनाने देता है।

    4. [django-ninja-jwt](django-ninja-jwt/index.md): django-ninja के लिए एक JSON Web Token plugin जो authentication और संबंधित features implement करता है, जो एक लोकप्रिय Django Rest Framework plugin से fork किया गया है।
