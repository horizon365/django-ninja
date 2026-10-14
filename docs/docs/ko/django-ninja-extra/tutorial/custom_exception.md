---
comments: true
---
# **커스텀 예외**
**Django-Ninja**는 예외 타입에 대해 함수(핸들러)를 등록하는 방식으로 커스텀 예외를 처리하는 직관적인 방법을 제공합니다. Flask 애플리케이션에서 하는 것과 유사합니다.

이와 관련하여 **Django-Ninja-Extra**는 DRF의 `APIException`에 익숙한 사용자들을 위해 유사한 기능을 제공하는 `APIException` 예외 타입을 갖고 있습니다.

예를 들어:
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
