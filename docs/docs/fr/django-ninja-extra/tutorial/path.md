---
comments: true
---
Les _paramètres_ du chemin de la route sont déclarés sous forme de chaînes formatées Python.
Par exemple :

```python hl_lines="7 8"
from ninja_extra import api_controller, route
from ninja import constants


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.get('/users/{user_id}')
    def get_user_by_id(self, user_id: int):
        return {'user_id': user_id}
```

La valeur du paramètre de chemin `user_id` sera transmise à votre fonction en tant que paramètre `user_id`.

!!! info
    Consultez [la documentation](https://django-ninja.cn/guides/input/path-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
