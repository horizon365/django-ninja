---
comments: true
---
# Path Parameters

आप Python formatted strings के समान syntax का उपयोग करके path "parameters" घोषित कर सकते हैं (जो, सौभाग्य से, <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">OpenAPI path parameters</a> से भी मेल खाता है):

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

Path parameter `item_id` का मान आपके function को `item_id` argument के रूप में पास किया जाएगा।

तो, यदि आप यह उदाहरण चलाते हैं और <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> पर जाते हैं, तो आपको यह response दिखाई देगा:

```JSON
{"item_id":"foo"}
```


### Types के साथ Path Parameters

आप अपने function में standard Python type annotations का उपयोग करके path parameter का type घोषित कर सकते हैं:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

इस स्थिति में, `item_id` एक **`int`** के रूप में घोषित है। इससे आपको error checking, code completion, आदि के लिए editor और linter समर्थन मिलता है।

यदि आप यह code browser में <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a> का उपयोग करके चलाते हैं, तो आपको यह response दिखाई देगा:
```JSON
{"item_id":3}
```

!!! tip
    ध्यान दें कि आपके function को मिलने वाला (और लौटाया जाने वाला) मान एक Python `int` के रूप में **3** है — string `"3"` नहीं।
    तो, बस इतनी सी type घोषणा के साथ, **Django Ninja** आपको automatic request "parsing" और validation प्रदान करता है。



### Data Validation

दूसरी ओर, यदि आप browser में <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(यहाँ `"foo"` एक int नहीं है)*</small> पर जाते हैं, तो आपको इस तरह का एक HTTP error दिखाई देगा:

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Django Path Converters

Path को parse करने में मदद के लिए आप [Django path converters](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters) का उपयोग कर सकते हैं:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

इस स्थिति में, `item_id` एक **`int`** के रूप में parse किया जाएगा। यदि `item_id` एक मान्य `int` नहीं है, तो URL मैच नहीं करेगा।
(उदाहरण के लिए, यदि कोई अन्य route मैच नहीं करता, तो 404 Not Found लौटाया जाएगा।)

!!! tip
    ध्यान दें कि चूँकि **Django Ninja** annotation किए गए बिना वाले parameters के लिए डिफ़ॉल्ट `str` type का उपयोग करता है, ऊपर दिया गया function जो मान प्राप्त करता है (और लौटाता है) वह `"3"` है,
    एक Python `str` के रूप में — पूर्णांक **3** नहीं। एक `int` प्राप्त करने के लिए, बस हमेशा की तरह function definition में `item_id` को `int` type annotation के साथ घोषित करें:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```

#### Slashes के साथ Path Parameters

Django का `path` converter path-जैसे parameters को संभालने की अनुमति देता है:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
आप इस operation को `/dir/some/path/with-slashes` के साथ query कर सकते हैं, और आपका `value` `some/path/with-slashes` के बराबर होगा

### कई Parameters

आप `path` को जितने चाहें variables पास कर सकते हैं — बस अद्वितीय नामों का उपयोग करना याद रखें, और अपने function arguments में वही नाम उपयोग करना न भूलें।

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Schema का उपयोग करना

आप आपस में जुड़े path parameters को समाहित करने के लिए (और उन्हें एक समूह के रूप में validate करने के लिए) भी एक schema का उपयोग कर सकते हैं:


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    ध्यान दें कि यहाँ हम **Django Ninja** को यह बताने के लिए `Path` source hint का उपयोग करते हैं कि यह schema path parameters पर लागू होगा।

### दस्तावेज़ीकरण

अब, जब आप browser में <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> खोलेंगे, तो आपको automatic, इंटरैक्टिव API दस्तावेज़ीकरण दिखाई देगा।
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    अगले अध्याय पर जाएँ! **[Query Parameters](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
