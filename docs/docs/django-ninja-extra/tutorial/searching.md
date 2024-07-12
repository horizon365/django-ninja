---
comments: true
---
# **检索**

**Django Ninja Extra** 使用来自 Django-Ninja-Extra 搜索模块的　`searching` 装饰器提供了一个直观的搜索模型。 它期望从路由函数结果中得到一个查询集或列表。

> 这个特性的灵感来自于 [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

## **属性**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: 定义一个路由函数或一个搜索类。默认值: `ninja_extra.searching.Searching`
- searching_params: 用于初始化搜索类的额外参数

### 更改默认搜索类

要更改默认搜索类，你需要在　`settings.py`　中添加一个 `NINJA_EXTRA` 变量，其中一个包含键 `SEARCHING_CLASS` 和定义搜索类路径的值

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **用法**

- 如果你不指定 `search_fields` 参数，将返回未改变的结果。
- 例如，要按用户名或电子邮件搜索用户：
  > http://example.com/api/users?search=someuser
- 你还可以使用查找 API 双下划线表示法对外键或多对多字段进行相关查找：
  > search_fields = ['username', 'email', 'profile__profession']
- 默认情况下，搜索将使用不区分大小写的部分匹配。搜索参数可以包含多个搜索项，这些项应该用空格和/或逗号分隔。如果使用多个搜索项，那么只有当提供的所有项都匹配时，对象才会在列表中返回。可以通过在 `search_fields`　前添加各种字符来限制搜索行为。

  * '^' 以开头进行搜索。
  * '=' 精确匹配。
  * '@' 全文搜索。(目前仅支持 Django 的　[PostgreSQL backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
  * '$' 正则搜索。

  例如:

    > search_fields = ['=username', '=email']

```python
from typing import List
from ninja_extra.searching import searching, Searching
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
    @searching(Searching, search_fields=['username', 'email'])
    def get_users(self):
        return user_model.objects.all()

    @route.get('/iexact-email', response=List[UserSchema])
    @searching(search_fields=['=email'])
    def get_users_with_search_iexact_email(self):
        return [u for u in user_model.objects.all()]


api = NinjaExtraAPI(title='Searching Test')
api.register_controllers(UserController)
```

## 注意

> 如果你同时使用 `paginate` 装饰器, `ordering` 装饰器和 `searching` 装饰器，那么 `paginate` 应该在 `ordering` 装饰器之上， `ordering` 装饰器应该在 `searching` 装饰器之上。 因为首先对数据进行过滤，然后对数据进行排序，最后进行分页，例如:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    @searching(Searching, search_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
