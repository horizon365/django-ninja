---
comments: true
---
# **검색(Searching)**

**Django Ninja Extra**는 Django-Ninja-Extra searching 모듈의 `searching` 데코레이터를 사용하는 직관적인 검색 모델을 제공합니다. 라우트 함수 결과에서 queryset이나 리스트를 기대합니다.

> 이 기능은 [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)에서 영감을 받았습니다

## **속성**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: 라우트 함수 또는 searching 클래스를 정의합니다. 기본값: `ninja_extra.searching.Searching`
- searching_params: searching 클래스를 초기화하는 데 사용되는 추가 매개변수

### 기본 Searching 클래스 변경하기

기본 searching 클래스를 변경하려면 `settings.py`에 `NINJA_EXTRA` 변수를 추가하고, `SEARCHING_CLASS` 키에 searching 클래스의 경로를 값으로 지정해야 합니다

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **사용법**

- `search_fields` 매개변수를 지정하지 않으면 변경되지 않은 결과가 그대로 반환됩니다.
- 예를 들어, username 또는 email로 사용자를 검색하려면:
  > http://example.com/api/users?search=someuser
- 외래 키(foreign key)나 다대다(many-to-many) 필드에 대한 관련 조회를 수행하기 위해 lookup API의 이중 언더스코어 표기법을 사용할 수도 있습니다:
  > search_fields = ['username', 'email', 'profile__profession']
- 기본적으로 검색은 대소문자를 구분하지 않는 부분 일치를 사용합니다. 검색 매개변수에는 여러 검색어가 포함될 수 있으며, 공백 및/또는 쉼표로 구분해야 합니다. 여러 검색어를 사용하면 제공된 모든 검색어와 일치하는 객체만 목록에 반환됩니다. `search_fields` 앞에 다양한 문자를 추가하여 검색 동작을 제한할 수 있습니다.

  * '^' 시작 문자 일치로 검색합니다.
  * '=' 정확한 일치입니다.
  * '@' 전문(full-text) 검색입니다. (현재 Django의 [PostgreSQL 백엔드](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/)에서만 지원됩니다.)
  * '$' 정규식 검색입니다.

  예를 들어:

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

## 참고

> `paginate` 데코레이터, `ordering` 데코레이터, `searching` 데코레이터를 동시에 사용하는 경우, `paginate`는 `ordering` 데코레이터 위에, `ordering` 데코레이터는 `searching` 데코레이터 위에 있어야 합니다. 데이터가 먼저 필터링되고, 그다음 정렬되고, 마지막으로 페이징되기 때문입니다. 예를 들어:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    @searching(Searching, search_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
