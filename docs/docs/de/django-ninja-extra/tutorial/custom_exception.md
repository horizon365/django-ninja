---
comments: true
---
# **Eigene Ausnahmen (Custom Exceptions)**
**Django-Ninja** bietet einen intuitiven Weg, eigene Ausnahmen zu behandeln, indem eine Funktion (Handler) für einen Ausnahmetyp registriert wird – ähnlich wie in Flask-Anwendungen.

In dieser Hinsicht hat **Django-Ninja-Extra** einen Ausnahmetyp `APIException`, der ähnliche Funktionen für diejenigen bereitstellt, die die Verwendung von DRFs `APIException` gewohnt sind.

Zum Beispiel:
```python
from ninja_extra.exceptions import APIException
from ninja_extra import api_controller, route, NinjaExtraAPI, status
from ninja import constants


class CustomAPIException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'UnAuthorized'

    
@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyController:
    @route.get('/exception')
    def custom_exception(self):
        raise CustomAPIException()


api = NinjaExtraAPI(title='Exception Test')
api.register_controllers(MyController)
```
![Preview](../images/custom_exception.gif)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
