---
comments: true
---
# **Custom Exceptions**
**Django-Ninja** एक intuitive तरीका प्रदान करता है custom exceptions को handle करने का, जिसमें किसी exception type के लिए एक function (handler) register किया जाता है, जैसा कि Flask applications में किया जाता है।

इस संदर्भ में, **Django-Ninja-Extra** में एक `APIException` exception type है जो DRF के `APIException` का उपयोग करने के आदी लोगों के लिए समान functionality प्रदान करता है।

उदाहरण के लिए:
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
