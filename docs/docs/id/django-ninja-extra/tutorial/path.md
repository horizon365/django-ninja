---
comments: true
---
_parameter_ dari path route dideklarasikan sebagai formatted string Python.
Sebagai contoh:

```python hl_lines="7 8"
from ninja_extra import api_controller, route
from ninja import constants


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.get('/users/{user_id}')
    def get_user_by_id(self, user_id: int):
        return {'user_id': user_id}
```

Nilai dari path parameter `user_id` akan diteruskan ke fungsi Anda sebagai parameter `user_id`.

!!! info
    Baca [selengkapnya](https://django-ninja.cn/guides/input/path-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
