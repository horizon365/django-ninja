---
comments: true
---
Wenn Sie sich nicht sicher sind, wie Sie in django-ninja-extra POST-Requests mit Content-Typen wie `application/x-www-form-urlencoded` oder `multipart/form-data` verarbeiten sollen, wird Ihnen dieser Leitfaden weiterhelfen.
Django-Ninja deckt die meisten Anwendungsfälle bereits [hier](https://django-ninja.cn/tutorial/form-params/) ab, aber ich gebe Ihnen hier eine kurze Zusammenfassung.

### Formulardaten als Parameter

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
Hier sind zwei Dinge zu beachten:

- Sie müssen `Form` aus dem Modul `ninja` importieren
- Verwenden Sie `Form` als Standardwert für Ihre Parameter


!!! info
    Weitere Informationen dazu finden Sie im [Django-Ninja-Formular-Tutorial](https://django-ninja.cn/guides/input/form-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
