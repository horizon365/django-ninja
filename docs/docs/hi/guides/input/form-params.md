---
comments: true
---
# Form Data

**Django Ninja** `request.POST` data को parse और validate करने की भी अनुमति देता है
(यानी, `application/x-www-form-urlencoded` या `multipart/form-data`)।

## Form Data parameters के रूप में

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

निम्नलिखित बातों पर ध्यान दें:

1) आपको `Form` class को `ninja` से import करना होगा
```python
from ninja import Form
```

2) Parameter के डिफ़ॉल्ट मान के रूप में `Form` का उपयोग करें:
```python
username: Form[str]
```

## Schema का उपयोग करना

[Request Body](body.md#declare-it-as-a-parameter) की तरह, आप अपने parameters को व्यवस्थित करने के लिए एक schema का उपयोग कर सकते हैं।

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Request Form + Path + Query Parameters

[Request Body](body.md#request-body-path-query-parameters) की तरह, आप form data को अन्य parameter स्रोतों के साथ जोड़ सकते हैं।

आप query parameters **और** path parameters **और** form fields, **आदि** एक साथ घोषित कर सकते हैं।

**Django Ninja** पहचान लेगा कि path parameters से मेल खाते function parameters **path से लिए जाएँगे**,
जबकि `Form(...)` के साथ घोषित function parameters **request form fields से लिए जाएँगे**, और इसी तरह आगे।

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## खाली Form Fields को डिफ़ॉल्ट मानों पर मैप करना

Optional form fields अक्सर खाली मानों के साथ भेजे जाते हैं। इस मान को एक खाली string के रूप में व्याख्यायित किया जाता है, इसलिए `int` या `bool` जैसे fields के लिए यह validation में विफल हो सकता है।

जैसा कि Pydantic दस्तावेज़ीकरण में वर्णित है, इसे [generic classes as types](https://pydantic.com.cn/usage/types/#generic-classes-as-types) का उपयोग करके हल किया जा सकता है।

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    अगले अध्याय पर जाएँ! **[File Uploads](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
