---
comments: true
---
# **カスタム例外**
**Django-Ninja** は、Flask アプリケーションで行われるのと同様に、例外型に対して関数（ハンドラ）を登録することで、カスタム例外を処理する直感的な方法を提供します。

これに関連して、**Django-Ninja-Extra** には、DRF の `APIException` に慣れている人向けに同様の機能を提供する `APIException` 例外型があります。

例：
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
