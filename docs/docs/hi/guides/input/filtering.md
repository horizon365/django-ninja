---
comments: true
---
# Filtering

यदि आप users को आपके querysets को कई अलग-अलग attributes द्वारा filter करने की अनुमति देना चाहते हैं, तो अपने filters को एक `FilterSchema` class में समाहित करना समझदारी है।
`FilterSchema` एक सामान्य `Schema` है, इसलिए यह Pydantic की सभी आवश्यक सुविधाओं का उपयोग करता है, लेकिन यह user-facing filtering parameters को database queries में आसानी से बदलने के लिए कुछ सुविधाएँ भी जोड़ता है।

सबसे पहले, `FilterSchema` का एक subclass परिभाषित करें:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


फिर, अपने API handler में इस schema का उपयोग `Query` के साथ करें:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

ठीक वैसे जैसा [Using a Schema to Define Query Parameters](./query-params.md#using-schema) में वर्णित है, Django Ninja `BookFilterSchema` में परिभाषित fields को query parameters में बदल देता है।
आप शॉर्टहैंड one-liner `.filter()` का उपयोग करके इन filters को अपने queryset पर लागू कर सकते हैं:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

भीतर की परत में, `FilterSchema` अपने fields को [Q expressions](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects) में बदलता है, फिर उन्हें जोड़ता है और आपके queryset को filter करने के लिए उपयोग करता है।


वैकल्पिक रूप से, `.filter` method का उपयोग करने के बजाय, आप तैयार `Q` expression प्राप्त कर सकते हैं और filtering स्वयं कर सकते हैं।
यह तब उपयोगी होता है जब आपके पास API के माध्यम से users को दिखाए जाने वाले filters के अलावा कुछ अतिरिक्त queryset filtering हो:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)

    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

डिफ़ॉल्ट रूप से, filters इस प्रकार व्यवहार करेंगे:

* `None` मानों को अनदेखा किया जाएगा और कोई filtering लागू नहीं होगी;
* प्रत्येक non-`None` field को उस field की `Field` definition के अनुसार एक `Q` expression में बदला जाएगा;
* सभी `Q` expressions को `AND` logical operator का उपयोग करके एक में जोड़ा जाएगा;
* परिणामी `Q` expression का उपयोग queryset को filter करने के लिए किया जाता है, और `.filter` clause लागू किया हुआ एक queryset आपको लौटा दिया जाता है।

## Custom Fields
डिफ़ॉल्ट रूप से, `FilterSet` Q expression बनाने के लिए field का नाम उपयोग करता है:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
`name` field एक `Q(name=...)` expression में बदल जाएगा।

जब आपका database lookup इससे अधिक जटिल हो, तो आप field definition में `"q"` keyword argument का उपयोग करके इन्हें स्पष्ट रूप से निर्दिष्ट कर सकते हैं:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
```
आप lookup keyword argument नामों की एक सूची भी निर्दिष्ट कर सकते हैं:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains'])
```
डिफ़ॉल्ट रूप से, field-level expressions को `"OR"` connector का उपयोग करके जोड़ा जाता है, इसलिए ऊपर दी गई सेटअप के साथ, एक query parameter `?search=foobar` उन books को खोजेगा जिनके नाम, author या publisher में से किसी एक में "foobar" हो।


## Expressions को जोड़ना
डिफ़ॉल्ट रूप से,

* field-level expressions को `OR` operator का उपयोग करके जोड़ा जाता है।
* fields स्वयं `AND` operator का उपयोग करके जोड़े जाते हैं।

तो, निम्नलिखित `FilterSchema` के लिए...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...और user से निम्नलिखित query parameters
```
http://localhost:8000/api/books?search=harry&popular=true
```
`FilterSchema` instance उन popular books को खोजेगा जिनके book के _या_ author के नाम में `harry` हो।


आप field-level और class-level दोनों definitions में `expression_connector` parameter का उपयोग करके इस व्यवहार को कस्टमाइज़ कर सकते हैं:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')

    class Config:
        expression_connector = 'OR'
```

Expression connector `"OR"`, `"AND"`, और `"XOR"` मान ले सकता है, लेकिन अंतिम वाला केवल Django 4.1 में [supported](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) है।

अब, इन query parameters के साथ एक request
```
http://localhost:8000/api/books?name=harry&active=true
```
...उन books को खोजेगा जिनके नाम में `harry` हो _या_ जो स्वयं active हों और एक active publisher द्वारा publish की गई हों।


## Nones द्वारा Filtering
आप `FilterSchema` को `None` को एक मान्य मान के रूप में व्यवहार करने के लिए बना सकते हैं जिसके लिए filtering की जानी चाहिए।

यह field स्तर पर `ignore_none` keyword argument के माध्यम से किया जा सकता है:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

इस तरह, जब user `"tag"` के लिए कोई अन्य मान प्रदान नहीं करता, तो filter में हमेशा `tag=None` शर्त शामिल होगी।

आप इसे configuration में सभी fields के लिए एक साथ भी निर्दिष्ट कर सकते हैं:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)

    class Config:
        ignore_none = False
```


## Custom Expressions
कभी-कभी आपके पास ऐसे जटिल filtering परिदृश्य हो सकते हैं जिन्हें एक single field annotation संभाल नहीं सकता।
ऐसे मामलों के लिए, आप अपनी field filtering logic को एक custom method के रूप में implement कर सकते हैं। बस `filter_<fieldname>` नाम की एक method परिभाषित करें जो एक filtering मान स्वीकार करे और एक Q expression लौटाए:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None

    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
ऐसे field methods संबंधित field की `Field()` definition में निर्दिष्ट चीज़ों पर प्राथमिकता रखते हैं।
यदि वह पर्याप्त नहीं है, तो आप `custom_expression` method में पूरी `FilterSet` class के लिए अपनी स्वयं की custom filtering logic implement कर सकते हैं:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    popular: Optional[bool] = None

    def custom_expression(self) -> Q:
        q = Q()
        if self.name:
            q &= Q(name__icontains=self.name)
        if self.popular:
            q &= (
                Q(view_count__gt=1000) |
                Q(downloads__gt=100) |
                Q(tag='popular')
            )
        return q
```
`custom_expression` method ऊपर वर्णित किसी भी अन्य definition पर प्राथमिकता रखता है, जिसमें `filter_<fieldname>` methods शामिल हैं।

!!! done

    Input parameter श्रृंखला पूरी हो गई है! अगले भाग पर जाएँ **[Handling Responses](../response/index.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
