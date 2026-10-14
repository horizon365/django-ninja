---
comments: true
---
# **Pagination**

**Django Ninja Extra** Django-Ninja-Extra pagination module के `paginate` decorator का उपयोग करके एक intuitive pagination model प्रदान करता है। यह route function result से एक list या queryset की अपेक्षा करता है।

## **Attributes**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: एक route function या एक pagination class define करता है। डिफ़ॉल्ट: `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: pagination class को initialize करने के लिए उपयोग किए जाने वाले अतिरिक्त parameters

### **Ninja LimitOffsetPagination का उपयोग करना**
`ninja_extra.pagination.LimitOffsetPagination` का उपयोग करते समय, आपको pagination response schema wrapper के रूप में `NinjaPaginationResponseSchema` का उपयोग करना चाहिए।

उदाहरण के लिए: 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **डिफ़ॉल्ट Pagination Class बदलें**
डिफ़ॉल्ट pagination class बदलने के लिए, आपको `settings.py` में key `PAGINATION_CLASS` के साथ एक `NINJA_EXTRA` variable जोड़ने की आवश्यकता है और pagination class के path को परिभाषित करने वाला एक मान देना होगा।
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **उपयोग**
```python
from typing import List
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)
from ninja_extra import api_controller, route, NinjaExtraAPI
from ninja import ModelSchema
from django.contrib.auth import get_user_model

user_model = get_user_model()


class UserSchema(ModelSchema):
    class Config:
        model = user_model
        model_fields = ['username', 'email']

        
@api_controller('/users')
class UserController:
    @route.get('', response=PaginatedResponseSchema[UserSchema])
    @paginate(PageNumberPaginationExtra, page_size=50)
    def get_users(self):
        return user_model.objects.all()
    
    @route.get('/limit', response=List[UserSchema])
    @paginate
    def get_users_with_limit(self):
        # this will use default paginator class - ninja_extra.pagination.LimitOffsetPagination
        return user_model.objects.all()

    
api = NinjaExtraAPI(title='Pagination Test')
api.register_controllers(UserController)
```

![Preview](../images/pagination_example.gif)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
