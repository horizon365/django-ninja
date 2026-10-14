---
comments: true
---
# **정렬(Ordering)**

**Django Ninja Extra**는 Django-Ninja-Extra ordering 모듈의 `ordering` 데코레이터를 사용하는 직관적인 정렬 모델을 제공합니다. 라우트 함수 결과에서 queryset이나 리스트를 기대합니다.

> 이 기능은 [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)에서 영감을 받았습니다

## **속성**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: 라우트 함수 또는 ordering 클래스를 정의합니다. 기본값: `ninja_extra.ordering.Ordering`
- ordering_params: ordering 클래스를 초기화하는 데 사용되는 추가 매개변수

### 기본 Ordering 클래스 변경하기

기본 ordering 클래스를 변경하려면 `settings.py`에 `NINJA_EXTRA` 변수를 추가하고, `ORDERING_CLASS` 키에 ordering 클래스의 경로를 값으로 지정해야 합니다.

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **사용법**

- `ordering_fields` 매개변수를 지정하지 않으면 queryset의 모든 필드가 정렬에 사용됩니다.
- 예를 들어, 사용자를 username으로 정렬하려면
  > http://example.com/api/users?ordering=username
- 클라이언트는 필드 이름 앞에 `-`를 붙여 역순 정렬을 지정할 수도 있습니다. 예를 들어:
  > http://example.com/api/users?ordering=-username
- 여러 정렬 기준을 지정할 수도 있습니다:
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

## 참고

> `paginate` 데코레이터와 `ordering` 데코레이터를 함께 사용하는 경우, 데이터가 먼저 정렬된 후 페이징되기 때문에 `paginate` 데코레이터가 `ordering` 데코레이터 위에 있어야 합니다. 예를 들어:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
