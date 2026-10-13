---
comments: true
---
The _parameters_ of the route path are declared as Python formatted strings.
For example:

```python hl_lines="7 8"
from ninja_extra import api_controller, route
from ninja import constants


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.get('/users/{user_id}')
    def get_user_by_id(self, user_id: int):
        return {'user_id': user_id}
```

The value of the path parameter `user_id` will be passed to your function as the parameter `user_id`.

!!! info
    Read [more](https://django-ninja.cn/guides/input/path-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
