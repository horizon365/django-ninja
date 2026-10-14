---
comments: true
---
# **Exceptions personnalisées**
**Django-Ninja** offre une manière intuitive de gérer les exceptions personnalisées en enregistrant une fonction (handler) pour un type d'exception, de manière similaire à ce qui se fait dans les applications Flask.

À cet égard, **Django-Ninja-Extra** dispose d'un type d'exception `APIException` qui fournit une fonctionnalité similaire pour ceux habitués à utiliser l'`APIException` de DRF.

Par exemple :
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
