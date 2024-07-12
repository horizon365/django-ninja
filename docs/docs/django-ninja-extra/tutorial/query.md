---
comments: true
---
Django-Ninja 假定不在路径参数中的函数参数为查询参数。

例如:

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

要查询此操作，你需使用类似这样的 URL:
```
    http://localhost:8000/api/weapons?offset=0&limit=10
```

!!! info
    阅读 [更多相关](https://django-ninja.cn/guides/input/query-params/)
<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
