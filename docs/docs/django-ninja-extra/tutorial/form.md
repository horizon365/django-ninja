---
comments: true
---
如果你不确定如何在 django-ninja-extra 中进行像 `application/x-www-form-urlencode` 或 `multipart/form-data` 这样的标点 POST 请求 , 那么本指南对你会很有用。
Django-Ninja 已经涵盖了这里的大多数用例 [在此](https://django-ninja.cn/tutorial/form-params/)，但我将在这里给你一个快速总结。

### 作为参数的表单数据

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post, router


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
这里有两件事需要注意：

- 你需要从　`ninja`　模块中导入 `Form`
- 使用 `Form` 作为你的参数的默认值


!!! 信息
    关于此的更多信息，访问 [Django-Ninja 表单教程](https://django-ninja.cn/guides/input/form-params/)
<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
