---
comments: true
---
路由路径的 _parameters_ 是以 Python 格式化字符串的形式声明的。
例如:

```python hl_lines="7 8"
from ninja_extra import api_controller, route
from ninja import constants


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.get('/users/{user_id}')
    def get_user_by_id(self, user_id: int):
        return {'user_id': user_id}
```

路径参数 `user_id` 的值将作为参数 `user_id` 传递给你的函数。

!!! info
    Read [more](https://django-ninja.cn/guides/input/path-params/)
<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
