---
comments: true
---
# **排序**

**Django Ninja Extra** 使用来自 Django-Ninja-Extra 排序模块的 `ordering` 装饰器提供了一个直观的排序模型。它期望从路由函数结果得到一个查询集或列表。

> 此功能的灵感来自于 [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

## **属性**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: 定义一个路由函数或一个排序类。默认: `ninja_extra.ordering.Ordering`
- ordering_params: 用于初始化排序类的额外参数

### 更改默认排序类

要更改默认排序类，您需要在 `settings.py`　中添加　`NINJA_EXTRA` 变量 ，其中包含键　`ORDERING_CLASS` 和定义排序类路径的值。

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **用法**

- 如果您未指定 `ordering_fields` 参数, 则查询集的所有字段都将用于排序。
- 例如，要按用户名对用户进行排序
  > http://example.com/api/users?ordering=username
- 客户端还可以通过在字段名称前加上 ｀-｀ 来指定反向排序，例如：
  > http://example.com/api/users?ordering=-username
- 也可以指定多个排序：
  > http://example.com/api/users?ordering=username,email

```python
from typing import List
from ninja_extra.ordering import ordering, Ordering
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
    @route.get('', response=List[UserSchema])
    @ordering(Ordering, ordering_fields=['username', 'email'])
    def get_users(self):
        return user_model.objects.all()

    @route.get('/all-sort', response=List[UserSchema])
    @ordering
    def get_users_with_all_field_ordering(self):
        return [u for u in user_model.objects.all()]


api = NinjaExtraAPI(title='Ordering Test')
api.register_controllers(UserController)
```

## 注意

> 如果您同时使用 `paginate` 装饰器和 `ordering` 装饰器,  `paginate` 装饰器应该在 `ordering` 装饰器之上，因为首先对数据进行排序，然后对数据进行分页，例如：
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
