---
comments: true
---
# **Aangepaste Uitzonderingen**
**Django-Ninja** biedt een intuïtieve manier om aangepaste uitzonderingen af te handelen door een functie (handler) te registreren voor een uitzonderingstype, vergelijkbaar met wat wordt gedaan in Flask-applicaties.

In dit opzicht heeft **Django-Ninja-Extra** een uitzonderingstype `APIException` dat vergelijkbare functionaliteit biedt voor wie gewend is aan het gebruik van DRF's `APIException`.

Bijvoorbeeld:
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
