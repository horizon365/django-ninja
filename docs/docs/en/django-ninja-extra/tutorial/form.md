---
comments: true
---
If you are unsure how to handle POST requests with content types like `application/x-www-form-urlencoded` or `multipart/form-data` in django-ninja-extra, then this guide will be useful to you.
Django-Ninja already covers most of the use cases here [here](https://django-ninja.cn/tutorial/form-params/), but I will give you a quick summary here.

### Form Data as Parameters

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
There are two things to note here:

- You need to import `Form` from the `ninja` module
- Use `Form` as the default value for your parameters


!!! info
    For more information about this, visit the [Django-Ninja Form Tutorial](https://django-ninja.cn/guides/input/form-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
