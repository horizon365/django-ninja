---
comments: true
---
라우트 경로의 _매개변수_는 Python 포맷 문자열로 선언됩니다.
예를 들어:

```python hl_lines="7 8"
from ninja_extra import api_controller, route
from ninja import constants


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @route.get('/users/{user_id}')
    def get_user_by_id(self, user_id: int):
        return {'user_id': user_id}
```

경로 매개변수 `user_id`의 값은 함수에 매개변수 `user_id`로 전달됩니다.

!!! info
    [더 알아보기](https://django-ninja.cn/guides/input/path-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
