---
comments: true
---
# **Custom Exceptions**

**Django-Ninja** menyediakan cara yang intuitif untuk menangani custom exception dengan mendaftarkan sebuah fungsi (handler) untuk tipe exception tertentu, mirip dengan yang dilakukan di aplikasi Flask.

Dalam hal ini, **Django-Ninja-Extra** memiliki tipe exception `APIException` yang menyediakan fungsionalitas serupa bagi yang terbiasa menggunakan `APIException` milik DRF.

Sebagai contoh:
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
