---
comments: true
---
# Django Ninja 1.0 में आपका स्वागत है


शुरू करने के लिए, निम्नलिखित command का इस्तेमाल करके latest version install करें:
```
pip install -U django-ninja
```

django-ninja v1, Python 3.7 और उससे ऊपर के versions के साथ compatible है।


Django Ninja की 0.x series अभी भी support की जाती है, लेकिन उसे केवल security updates और critical bug fixes ही मिलेंगे।


✨ Django Ninja 1.0 में नया क्या है

## Pydantic2 support

Pydantic version 2 को Rust में rewrite किया गया है और इसमें कई improvements और features शामिल हैं, जैसे:

 - अधिक सुरक्षित types.
 - बेहतर extensibility.
 - बेहतर performance.

हमारे tests के अनुसार, एक औसत project को औसतन लगभग 10% performance improvement मिल सकती है, जबकि कुछ edge parsing/serialization scenarios में आपको 4x तक का boost मिल सकता है।
दूसरी ओर, इसमें breaking changes भी हैं — pydantic 1 और 2 पूरी तरह compatible नहीं हैं — लेकिन हमने इस transition को जितना संभव हो सके आसान बनाने की कोशिश की है।
इसलिए अगर आपने 'Schema' class का इस्तेमाल किया है, तो ninja v1 में migrate करना सीधा-सरल होना चाहिए। अन्यथा, कृपया [pydantic migration guide](https://pydantic.com.cn/migration/) का पालन करें।


pydantic2 द्वारा प्रदान कुछ नए features

### pydantic context

Pydantic अब validation और serialization के दौरान context को support करता है, और Django Ninja request और response handling के दौरान "request" object को pass करता है।
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

Response phase के दौरान, "response_code" भी context को pass किया जाता है।

## Schema.Meta

Pydantic ने अब BaseModel.Config class को deprecate कर दिया है। हालाँकि, Django के बाकी सभी हिस्सों के साथ consistent रहने के लिए, हमने ModelSchema के लिए एक "Meta" class introduce की है — यह Django के ModelForms की तरह काम करती है:
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

("Config" class अभी भी support की जाती है, लेकिन अब यह deprecated है)


## छोटा/साफ parameter syntax

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

इसकी जगह

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

या

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


इसकी जगह

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



साथ ही आपके editor के सभी autocompletion features।

दूसरी ओर, **पुराना syntax अभी भी support किया जाता है**, इसलिए आप आसानी से अपने project को latest django-ninja version पर ले जा सकते हैं।


#### + Annotated

typing.Annotated अब भी support किया जाता है:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Async auth support

Async authenticators को आखिरकार support मिल गया है। आपको बस अपने `authenticate` method में `async` जोड़ना है:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## बदला गया CSRF behavior


अगर आप cookie-आधारित authentication का इस्तेमाल करते हैं, तो `csrf=True` की अब ज़रूरत नहीं है। इसकी जगह CSRF protection automatically enable हो जाती है। इससे आप CSRF-protected authenticators को अन्य ऐसे methods के साथ mix भी कर सकते हैं जिन्हें cookies की ज़रूरत नहीं है:

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Documentation

Documentation viewer अब configurable और pluggable है। डिफ़ॉल्ट रूप से, django-ninja Swagger और Redoc के साथ आता है:
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

Users अब `DocsBase` class को subclass करके custom documentation viewers बना सकते हैं।

## Router

add_router string paths को support करता है:

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Decorators

जब django-ninja किसी view को .get/.post आदि से decorate करता है, तो वह function के result को wrap करता है (ज़्यादातर मामलों में HttpResponse नहीं - बल्कि कोई serializable object), इसलिए यह कुछ built-in या third-party decorators के साथ काम नहीं करेगा, जैसे:
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
यह उदाहरण काम नहीं करेगा।

अब django-ninja एक decorate_view decorator introduce करता है जो http responses के साथ काम करने वाले decorators को inject करने की सुविधा देता है:
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Pagination

`paginate_queryset` method अब `request` object को accept करता है


#### Backward-incompatible items
 - resolve_xxx(self, ...) - (self) resolution का support deprecated है, इसकी जगह pydantic की built-in functionality का इस्तेमाल करें।
 - pydantic v1 अब support नहीं है
 - python 3.6 अब support नहीं है

वैसे - अगर आपको यह project पसंद है और आपने अभी तक इसे GitHub star नहीं दिया है - तो कृपया दे दीजिए! [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
