---
comments: true
---
# URLs को reverse करना

Django Ninja schema (या `Router`) का प्रत्येक method एक reverse URL name बनाता है।

## URLs कैसे बनते हैं

ये URLs सभी एक namespace के भीतर होते हैं, जिसका डिफ़ॉल्ट `"api-1.0.0"` है, और प्रत्येक URL name उस function से मेल खाता है जिसे वह decorate करता है।

उदाहरण के लिए:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

यह implicit URL name केवल प्रत्येक API path के पहले operation के लिए सेट किया जाता है। यदि आप नहीं चाहते कि कोई implicit reverse URL name बने, तो बस method decorator पर `url_name=""` (एक खाली string) निर्दिष्ट करें।

### URL name बदलें

डिफ़ॉल्ट URL name का उपयोग करने के बजाय, आप इसे method decorator पर एक property के रूप में स्पष्ट रूप से निर्दिष्ट कर सकते हैं।
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

यह इस API path के लिए किसी भी implicit URL name को override कर देगा।


#### डिफ़ॉल्ट URL name को override करें

आप `get_operation_url_name` method को override करके implicit URL naming को भी override कर सकते हैं:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### Custom namespace

डिफ़ॉल्ट URL namespace schema के version के आगे `"api-"` prefix लगाकर बनता है, हालाँकि आप NinjaAPI schema class की `urls_namespace` attribute को override करके namespace स्पष्ट रूप से निर्दिष्ट कर सकते हैं।
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    अगले भाग पर जाएँ **[Async support](async-support.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
