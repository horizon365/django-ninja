---
comments: true
---
Если вы не знаете, как обрабатывать POST-запросы с типами содержимого вроде `application/x-www-form-urlencoded` или `multipart/form-data` в django-ninja-extra, то это руководство будет вам полезно.
Django-Ninja уже охватывает большинство сценариев использования [здесь](https://django-ninja.cn/tutorial/form-params/), но здесь я приведу краткий обзор.

### Данные формы в качестве параметров

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
Здесь следует отметить два момента:

- Вам нужно импортировать `Form` из модуля `ninja`
- Используйте `Form` в качестве значения по умолчанию для ваших параметров


!!! info
    Для получения дополнительной информации посетите [руководство по формам Django-Ninja](https://django-ninja.cn/guides/input/form-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
