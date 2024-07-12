---
comments: true
---
# **分页**

**Django Ninja Extra** 使用来自 Django-Ninja-Extra 分页模块的　`paginate`　装饰器提供了一个直观的分页模型。它期望从路由函数结果中得到一个列表或查询集。

## **属性**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: 定义一个路由函数或一个分页类。默认： `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: 用于初始化分页类的额外参数

### **使用 Ninja LimitOffsetPagination**
当使用 `ninja_extra.pagination.LimitOffsetPagination`　时, 你应该使用 `NinjaPaginationResponseSchema` 作为分页响应模式包装器。

例如: 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **更改默认分页类**
要更改默认分页类，你需要在  `settings.py` 中添加　`NINJA_EXTRA`　变量，带有键 `PAGINATION_CLASS` 以及定义分页类路径的值。
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **用法**
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

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
