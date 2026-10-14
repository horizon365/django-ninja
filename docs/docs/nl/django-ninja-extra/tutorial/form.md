---
comments: true
---
Als je niet zeker weet hoe je POST-verzoeken met contenttypes zoals `application/x-www-form-urlencoded` of `multipart/form-data` moet afhandelen in django-ninja-extra, dan zal deze gids nuttig voor je zijn.
Django-Ninja behandelt de meeste use cases hier al [hier](https://django-ninja.cn/tutorial/form-params/), maar ik geef je hier een korte samenvatting.

### Formuliergegevens als Parameters

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
Er zijn hier twee dingen om op te letten:

- Je moet `Form` importeren uit de module `ninja`
- Gebruik `Form` als standaardwaarde voor je parameters


!!! info
    Voor meer informatie hierover ga je naar de [Django-Ninja Form Tutorial](https://django-ninja.cn/guides/input/form-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
