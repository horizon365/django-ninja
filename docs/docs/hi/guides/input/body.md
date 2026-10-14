---
comments: true
---
# Request Body

Request body का उपयोग आमतौर पर "create" और "update" operations (POST, PUT, PATCH) के साथ होता है।
उदाहरण के लिए, POST या PUT के साथ कोई resource बनाते समय, request body में आमतौर पर बनाए जाने वाले resource का एक representation होता है।

Request body घोषित करने के लिए, आपको **Django Ninja का `Schema`** उपयोग करना होगा।

!!! note
    भीतर की परत में (under the hood), **Django Ninja** <a href="https://pydantic.com.cn/" class="external-link" target="_blank">Pydantic</a> Model की सारी शक्ति और सुविधाओं का उपयोग करता है।
    Django models के साथ काम करते समय code confusion से बचने के लिए `Schema` alias चुना गया था, क्योंकि Pydantic की model class डिफ़ॉल्ट रूप से `Model` नाम से जानी जाती है, जो Django की `Model` class से टकराव करती है।


## Schema import करना

सबसे पहले, आपको `ninja` से `Schema` import करना होगा:

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## अपना Data Model बनाना

फिर अपने data model को `Schema` से inherit करने वाली एक class के रूप में घोषित करें।

सभी attributes के लिए standard Python types का उपयोग करें:

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

Note: यदि आप किसी attribute का डिफ़ॉल्ट मान **`None`** सेट करते हैं, तो वह request body में optional हो जाता है। उदाहरण के लिए, ऊपर दिया गया model एक ऐसा JSON "`object`" (या Python `dict`) घोषित करता है:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...चूँकि `description` optional है (उसका डिफ़ॉल्ट मान `None` है), यह JSON "`object`" भी मान्य होगा:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## इसे Parameter के रूप में घोषित करना

इसे अपनी *path operation* में जोड़ने के लिए, इसे उसी तरह घोषित करें जिस तरह आप path और query parameters घोषित करते हैं:


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

... और उसका type अपने बनाए हुए `Item` model के रूप में घोषित करें।

## परिणाम

बस इतनी सी Python type घोषणा के साथ, **Django Ninja**:

* Request body को JSON के रूप में पढ़ेगा।
* उपयुक्त types में बदलेगा (यदि आवश्यक हो)।
* Data को validate करेगा।
    * यदि data अमान्य है, तो यह एक अनुकूल और अर्थपूर्ण error लौटाएगा जो गलत data के स्थान और सामग्री को सटीक रूप से बताएगा।
* आपको प्राप्त data `item` parameter में देगा।
    * चूँकि आपने function में उसका type `Item` घोषित किया है, आपको सभी attributes और उनके types के लिए editor समर्थन (autocomplete, आदि) भी मिलेगा।
* आपके model के लिए <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> definitions बनाएगा, जिनका उपयोग आप project में कहीं भी, जहाँ आवश्यकता हो, कर सकते हैं।
* ये schemas बनाए गए OpenAPI schema का हिस्सा बनेंगे और automatic दस्तावेज़ीकरण <abbr title="User Interfaces">UI</abbr> द्वारा उपयोग किए जाएँगे।

## Automatic दस्तावेज़ीकरण

आपके models के JSON Schemas आपके बनाए गए OpenAPI schema का हिस्सा बन जाएँगे और इंटरैक्टिव API दस्तावेज़ीकरण में प्रदर्शित होंगे:

![Openapi schema](../../img/body-schema-doc.png)

...और उनका उपयोग उन सभी *path operations* के लिए API दस्तावेज़ीकरण में भी किया जाएगा जिन्हें उनकी आवश्यकता होती है:

![Openapi schema](../../img/body-schema-doc2.png)

## Editor समर्थन

अपने editor में, function के भीतर, आपको हर जगह type hints और completion मिलेगी (यह तब नहीं होगा जब आप Schema object के बजाय `dict` का उपयोग करेंगे):

![Type hints](../../img/body-editor.gif)


पिछले screenshots में <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> का उपयोग हुआ है।

आपको <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> और अधिकांश अन्य Python editors में भी वही editor समर्थन मिलेगा।

## Request Body + Path Parameters

आप path parameters **और** request body एक साथ घोषित कर सकते हैं।


**Django Ninja** पहचान लेगा कि path parameters से मेल खाते function parameters **path से** लिए जाएँगे, जबकि `Schema` के साथ घोषित function parameters **request body से** लिए जाएँगे।

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## Request Body + Path + Query Parameters

आप **request body**, **path**, और **query** parameters भी एक साथ घोषित कर सकते हैं।

**Django Ninja** प्रत्येक parameter को पहचान लेगा और data को सही स्थान से लेगा।

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

Function parameters इस प्रकार पहचाने जाएँगे:

* यदि parameter **path** में भी घोषित है, तो उसे path parameter के रूप में उपयोग किया जाएगा।


* यदि parameter एक **single type** है (जैसे `int`, `float`, `str`, `bool`, आदि), तो उसे **query** parameter के रूप में व्याख्यायित किया जाएगा।
* यदि parameter **Schema** (या Pydantic `BaseModel`) type के रूप में घोषित है, तो उसे **request body** के रूप में व्याख्यायित किया जाएगा।

!!! done

    अगले अध्याय पर जाएँ! **[Form Data](form-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
