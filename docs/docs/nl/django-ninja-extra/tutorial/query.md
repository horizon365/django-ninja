---
comments: true
---
Django-Ninja gaat ervan uit dat functieparameters die geen padparameters zijn, queryparameters zijn.

Bijvoorbeeld:

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

Om dit te raadplegen, gebruik je een URL als deze:
```
    http://localhost:8000/api/weapons?offset=0&limit=10
```

!!! info
    Lees [meer](https://django-ninja.cn/guides/input/query-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
