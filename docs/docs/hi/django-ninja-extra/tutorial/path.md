---
comments: true
---
Route path के _parameters_ Python formatted strings के रूप में घोषित किए जाते हैं।
उदाहरण के लिए:

```python hl_lines="7 8"
from ninja_extra import api_controller, route
from ninja import constants


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.get('/users/{user_id}')
    def get_user_by_id(self, user_id: int):
        return {'user_id': user_id}
```

Path parameter `user_id` का मान आपके function को `user_id` parameter के रूप में पास किया जाएगा।

!!! info
    [अधिक](https://django-ninja.cn/guides/input/path-params/) पढ़ें
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
