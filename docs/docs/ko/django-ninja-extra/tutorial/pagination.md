---
comments: true
---
# **페이징(Pagination)**

**Django Ninja Extra**는 Django-Ninja-Extra pagination 모듈의 `paginate` 데코레이터를 사용하는 직관적인 페이징 모델을 제공합니다. 라우트 함수 결과에서 리스트나 queryset을 기대합니다.

## **속성**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: 라우트 함수 또는 페이징 클래스를 정의합니다. 기본값: `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: 페이징 클래스를 초기화하는 데 사용되는 추가 매개변수

### **Ninja LimitOffsetPagination 사용하기**
`ninja_extra.pagination.LimitOffsetPagination`를 사용할 때는 `NinjaPaginationResponseSchema`를 페이징 응답 스키마 래퍼(wrapper)로 사용해야 합니다.

예를 들어: 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **기본 페이징 클래스 변경하기**
기본 페이징 클래스를 변경하려면 `settings.py`에 `NINJA_EXTRA` 변수를 추가하고, `PAGINATION_CLASS` 키에 페이징 클래스의 경로를 값으로 지정해야 합니다.
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **사용법**
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
