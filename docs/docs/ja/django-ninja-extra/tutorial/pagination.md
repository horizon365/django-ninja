---
comments: true
---
# **ページネーション**

**Django Ninja Extra** は、Django-Ninja-Extra の pagination モジュールから提供される `paginate` デコレータを使った、直感的なページネーションモデルを提供します。ルート関数の結果としてリストまたは queryset を受け取ります。

## **属性**

`def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable[..., Any]:`

- func_or_pgn_class: ルート関数またはページネーションクラスを定義します。デフォルト： `ninja_extra.pagination.LimitOffsetPagination`
- paginator_params: ページネーションクラスの初期化に使用される追加パラメータ

### **Ninja の LimitOffsetPagination を使う**
`ninja_extra.pagination.LimitOffsetPagination` を使用する場合は、ページネーションレスポンスのスキーマラッパーとして `NinjaPaginationResponseSchema` を使用する必要があります。

例： 
```python
from ninja_extra.schemas import NinjaPaginationResponseSchema

...

@route.get('', response=NinjaPaginationResponseSchema[UserSchema])
@paginate()
def list_items(self):
    return item_model.objects.all()
```
    

### **デフォルトのページネーションクラスを変更する**
デフォルトのページネーションクラスを変更するには、`settings.py` に `NINJA_EXTRA` 変数を追加し、`PAGINATION_CLASS` キーにページネーションクラスへのパスを値として設定します。
```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
```

## **使い方**
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
