---
comments: true
---
# Pagination

**Django Ninja** pagination support के साथ आता है। यह आपको बड़े result sets को अलग-अलग pages में विभाजित करने की अनुमति देता है।


किसी function पर pagination लागू करने के लिए — बस `paginate` decorator लगाएँ:

```python hl_lines="1 4"
from ninja.pagination import paginate

@api.get('/users', response=List[UserSchema])
@paginate
def list_users(request):
    return User.objects.all()
```


बस हो गया!

अब आप `limit` और `offset` GET parameters का उपयोग करके users query कर सकते हैं

```
/api/users?limit=10&offset=0
```

डिफ़ॉल्ट रूप से, limit `100` सेट होता है (आप इसे अपनी settings.py में `NINJA_PAGINATION_PER_PAGE` का उपयोग करके बदल सकते हैं)


## Built-in Pagination Classes

### LimitOffsetPagination (डिफ़ॉल्ट)

यह डिफ़ॉल्ट pagination class है (आप इसे अपनी settings.py में `NINJA_PAGINATION_CLASS` को किसी class के path की ओर इशारा करके बदल सकते हैं)

```python hl_lines="1 4"
from ninja.pagination import paginate, LimitOffsetPagination

@api.get('/users', response=List[UserSchema])
@paginate(LimitOffsetPagination)
def list_users(request):
    return User.objects.all()
```

Example query:
```
/api/users?limit=10&offset=0
```

इस class के दो input parameters हैं:

 - `limit` - एक page पर querysets की संख्या परिभाषित करता है (डिफ़ॉल्ट = 100, NINJA_PAGINATION_PER_PAGE के माध्यम से बदला जा सकता है)
 - `offset` - page window का offset सेट करता है (डिफ़ॉल्ट: 0, indexing 0 से शुरू होती है)


### PageNumberPagination
```python hl_lines="1 4"
from ninja.pagination import paginate, PageNumberPagination

@api.get('/users', response=List[UserSchema])
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.all()
```

Example query:
```
/api/users?page=2
```

इस class में एक parameter `page` है और यह डिफ़ॉल्ट रूप से प्रति page 100 querysets आउटपुट करती है (settings.py के माध्यम से बदली जा सकती है)

Page numbering 1 से शुरू होती है।

आप प्रत्येक view के लिए अलग से एक custom page size मान भी सेट कर सकते हैं:

```python hl_lines="2"
@api.get("/users")
@paginate(PageNumberPagination, page_size=50)
def list_users(...
```



## View Function में Pagination Parameters तक पहुँच

यदि आपको अपने view function में pagination के लिए उपयोग किए गए `Input` parameters तक पहुँच की आवश्यकता है — तो `pass_parameter` argument का उपयोग करें

उस स्थिति में, input data `**kwargs` में उपलब्ध होगा:

```python hl_lines="2 4"
@api.get("/someview")
@paginate(pass_parameter="pagination_info")
def someview(request, **kwargs):
    page = kwargs["pagination_info"].page
    return ...
```


## एक Custom Pagination Class बनाना

एक custom pagination class बनाने के लिए, आपको `ninja.pagination.PaginationBase` से inherit करना चाहिए और `Input` व `Output` schema classes के साथ-साथ `paginate_queryset(self, queryset, request, **params)` method को भी override करना चाहिए:

 - `Input` schema एक schema class है जो paginator को पास किए जाने वाले parameters (जैसे page number या limit/offset मान) का वर्णन करती है।
 - `Output` schema page आउटपुट की schema का वर्णन करती है (जैसे count/next/items, आदि)।
 - `paginate_queryset` method प्रारंभिक queryset प्राप्त करता है और उसे केवल अनुरोधित page के data को रखने वाला एक iterable लौटाना चाहिए। Method निम्नलिखित parameters स्वीकार करता है:
    - `queryset`: API function द्वारा लौटाया गया queryset (या iterable)।
    - `pagination` - paginator.Input parameters (parsed और validated)
    - `**params`: keyword arguments जिनमें decorated function द्वारा प्राप्त सभी arguments होंगे।


उदाहरण:

```python hl_lines="7 11 16 26"
from ninja.pagination import paginate, PaginationBase
from ninja import Schema


class CustomPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip: int


    class Output(Schema):
        items: List[Any] # `items` is a default attribute
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            'items': queryset[skip : skip + 5],
            'total': queryset.count(),
            'per_page': 5,
        }


@api.get('/users', response=List[UserSchema])
@paginate(CustomPagination)
def list_users(request):
    return User.objects.all()
```

Tip: आप parameters से request object प्राप्त कर सकते हैं:

```python
def paginate_queryset(self, queryset, pagination: Input, **params):
    request = params["request"]
```

#### Async Pagination

Standard **Django Ninja** pagination classes async का समर्थन करती हैं। यदि आप एक custom pagination class के साथ async requests संभालना चाहते हैं, तो आपको `ninja.pagination.AsyncPaginationBase` से inherit करना चाहिए और `apaginate_queryset(self, queryset, request, **params)` method को override करना चाहिए।

### Output Attributes

डिफ़ॉल्ट रूप से, page items `'items'` attribute में रखे जाते हैं। इस व्यवहार को override करने के लिए, आप `items_attribute` का उपयोग कर सकते हैं:

```python hl_lines="4 8"
class CustomPagination(PaginationBase):
    ...
    class Output(Schema):
        results: List[Any]
        total: int
        per_page: int

    items_attribute: str = "results"

```


## एक साथ कई Operations पर Pagination लागू करना

अक्सर ऐसा मामला होता है जब आपको उन सभी views में pagination जोड़नी होती है जो querysets या lists लौटाते हैं

आप built-in router class (`RouterPaginated`) का उपयोग कर सकते हैं जो `response=List[SomeSchema]` के साथ परिभाषित सभी operations में स्वचालित रूप से pagination inject करेगा:

```python hl_lines="1 3 6 10"
from ninja.pagination import RouterPaginated

router = RouterPaginated()


@router.get("/items", response=List[MySchema])
def items(request):
    return MyModel.objects.all()

@router.get("/other-items", response=List[OtherSchema])
def ohter_items(request):
    return OtherModel.objects.all()

```

इस उदाहरण में, दोनों operations पर pagination सक्षम होगी।

मुख्य `api` instance पर pagination लागू करने के लिए, आप `default_router` argument का उपयोग कर सकते हैं:


```python
api = NinjaAPI(default_router=RouterPaginated())

@api.get(...
```

!!! done

    अगले अध्याय पर जाएँ! **[Response Renderers](response-renderers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
