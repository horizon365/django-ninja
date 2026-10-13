---
comments: true
---
# Tutorial - Handling responses

## Defining response schemas

**Django Ninja** lets you define response schemas for validation and documentation purposes.

We will create a third operation that returns information about the current Django user.

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

This will convert Django's `User` object into a dictionary containing only the defined fields.

### Multiple response types

Let's return a different response if the current user is not authenticated.

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

As you can see, you can return a two-part tuple that will be interpreted as the HTTP response code and the data.

!!! success

    This is the end of the tutorial! Check out the **[other tutorials](other/crud.md)** or the **[How-to guides](../guides/input/operations.md)** for more information.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
