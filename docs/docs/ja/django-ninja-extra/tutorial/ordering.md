---
comments: true
---
# **オーダリング（並び替え）**

**Django Ninja Extra** は、Django-Ninja-Extra の ordering モジュールから提供される `ordering` デコレータを使った、直感的なオーダリングモデルを提供します。ルート関数の結果として queryset またはリストを受け取ります。

> この機能は [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter) にインスパイアされました

## **属性**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: ルート関数またはオーダリングクラスを定義します。デフォルト： `ninja_extra.ordering.Ordering`
- ordering_params: オーダリングクラスの初期化に使用される追加パラメータ

### デフォルトのオーダリングクラスを変更する

デフォルトのオーダリングクラスを変更するには、`settings.py` に `NINJA_EXTRA` 変数を追加し、`ORDERING_CLASS` キーにオーダリングクラスへのパスを値として設定します。

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **使い方**

- `ordering_fields` パラメータを指定しない場合、queryset のすべてのフィールドがオーダリングに使用されます。
- たとえば、ユーザーを username 順に並べるには
  > http://example.com/api/users?ordering=username
- クライアントは、フィールド名の前に `-` を付けることで逆順のオーダリングも指定できます。例：
  > http://example.com/api/users?ordering=-username
- 複数のオーダリングを指定することもできます：
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

> `paginate` デコレータと `ordering` デコレータの両方を使用する場合は、`paginate` デコレータを `ordering` デコレータの上に置く必要があります。データはまずソートされ、その後にページネーションされるためです。例：
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
