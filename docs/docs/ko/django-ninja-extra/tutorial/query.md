---
comments: true
---
Django-Ninja는 경로 매개변수가 아닌 함수 매개변수를 쿼리 매개변수로 간주합니다.

예를 들어:

```python hl_lines="7 10"
from ninja import constants
from ninja_extra import api_controller, route


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    weapons = ["Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"]
    
    @route.get("/weapons")
    def list_weapons(self, limit: int = 10, offset: int = 0):
        return self.weapons[offset: offset + limit]
```

이를 쿼리하려면 다음과 같은 URL을 사용합니다:
```
    http://localhost:8000/api/weapons?offset=0&limit=10
```

!!! info
    [더 알아보기](https://django-ninja.cn/guides/input/query-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
