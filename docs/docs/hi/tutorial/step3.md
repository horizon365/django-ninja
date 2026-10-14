---
comments: true
---
# Tutorial - Responses को handle करना

## Response schemas define करना

**Django Ninja** आपको validation और documentation के उद्देश्यों के लिए response schemas define करने देता है।

हम एक तीसरा operation बनाएँगे जो current Django user की जानकारी return करता है।

```python
from ninja import Schema

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users do not have the following fields, so provide default values.
    email: str = None
    first_name: str = None
    last_name: str = None

@api.get("/me", response=UserSchema)
def me(request):
    return request.user
```

यह Django के `User` object को केवल defined fields वाली एक dictionary में convert कर देगा।

### Multiple response types

आइए एक अलग response return करें अगर current user authenticated नहीं है।

```python hl_lines="2-5 7-8 10 12-13"
class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 
```

जैसा कि आप देख सकते हैं, आप एक two-part tuple return कर सकते हैं जिसे HTTP response code और data के रूप में interpret किया जाएगा।

!!! success

    Tutorial यहीं समाप्त होता है! अधिक जानकारी के लिए **[अन्य tutorials](other/crud.md)** या **[How-to guides](../guides/input/operations.md)** देखें।
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
