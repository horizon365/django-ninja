---
comments: true
---
# Error handling

**Django Ninja** आपको custom exception handlers इंस्टॉल करने की अनुमति देता है ताकि यह नियंत्रित किया जा सके कि errors या संभाले गए exceptions होने पर responses कैसे लौटाए जाएँ।

## Custom exception handlers

मान लीजिए आप एक ऐसा API बना रहे हैं जो किसी external service पर निर्भर है जिसे कुछ क्षणों में अनुपलब्ध रहने के लिए डिज़ाइन किया गया है। आप उस error को संभाल सकते हैं और client को कुछ अनुकूल response लौटा सकते हैं (उन्हें बाद में वापस आने को कहते हुए), exception होने पर डिफ़ॉल्ट 500 error फेंकने के बजाय।
इसे प्राप्त करने के लिए, आपको:

 - 1) कोई exception बनानी है (या किसी मौजूदा का उपयोग करना है)
 - 2) api.exception_handler decorator का उपयोग करना है


उदाहरण:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

Exception handler function 2 arguments लेता है:

 - **request** - Django की HTTP request
 - **exc** - वास्तविक exception

Function को एक HTTP response लौटाना चाहिए

## डिफ़ॉल्ट exception handlers को override करें

डिफ़ॉल्ट रूप से, **Django Ninja** निम्नलिखित exception handlers इनिशियलाइज़ करता है:


#### `ninja.errors.AuthenticationError`

Authentication data अमान्य होने पर thrown होती है

#### `ninja.errors.ValidationError`

Request data validation में विफल होने पर thrown होती है

#### `ninja.errors.HttpError`

Code में कहीं से भी status code के साथ HTTP error फेंकने के लिए उपयोग की जाती है
#### `django.http.Http404`

Django की डिफ़ॉल्ट 404 exception (उदाहरण के लिए, get_object_or_404 का उपयोग करके लौटाई जा सकती है)
#### `Exception`

कोई भी अन्य exception जो application द्वारा संभाली नहीं गई हो।
डिफ़ॉल्ट व्यवहार

  - **यदि `settings.DEBUG` `True` है** - plain text में traceback लौटाता है (console या Swagger UI में debug करते समय उपयोगी)
  - **अन्यथा** - Django के डिफ़ॉल्ट exception handling तंत्र का उपयोग करता है (error logging, ADMINS को emails भेजना)


### डिफ़ॉल्ट handlers को override करें

यदि आपको validation errors के डिफ़ॉल्ट आउटपुट को बदलना है - ValidationError exception handler को override करें:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## Exceptions के माध्यम से HTTP responses फेंकना

एक custom exception बनाने और उसके लिए handler लिखने के विकल्प के रूप में - आप एक HTTP exception भी फेंक सकते हैं, जिसके परिणामस्वरूप वांछित code के साथ एक HTTP response लौटाया जाएगा

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    अगले भाग पर जाएँ **[Reversing URLs](urls.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
