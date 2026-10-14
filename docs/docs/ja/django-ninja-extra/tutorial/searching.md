---
comments: true
---
# **サーチング（検索）**

**Django Ninja Extra** は、Django-Ninja-Extra の searching モジュールから提供される `searching` デコレータを使った、直感的なサーチングモデルを提供します。ルート関数の結果として queryset またはリストを受け取ります。

> この機能は [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter) にインスパイアされました

## **属性**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: ルート関数またはサーチングクラスを定義します。デフォルト： `ninja_extra.searching.Searching`
- searching_params: サーチングクラスの初期化に使用される追加パラメータ

### デフォルトのサーチングクラスを変更する

デフォルトのサーチングクラスを変更するには、`settings.py` に `NINJA_EXTRA` 変数を追加し、`SEARCHING_CLASS` キーにサーチングクラスへのパスを値として設定します

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **使い方**

- `search_fields` パラメータを指定しない場合、結果はそのままの形で返されます。
- たとえば、ユーザーを username または email で検索するには：
  > http://example.com/api/users?search=someuser
- ルックアップ API のダブルアンダースコア記法を使って、外部キーや多対多フィールドに対する関連ルックアップを行うこともできます：
  > search_fields = ['username', 'email', 'profile__profession']
- デフォルトでは、検索は大文字小文字を区別しない部分一致を使用します。search パラメータには複数の検索語を含めることができ、それらは空白やカンマで区切る必要があります。複数の検索語を使った場合、指定されたすべての検索語に一致するオブジェクトだけがリストとして返されます。検索の挙動は、`search_fields` の前にさまざまな文字を追加することで制限できます。

  * '^' 前方一致（starts-with）での検索。
  * '=' 完全一致。
  * '@' フルテキスト検索。（現在は Django の [PostgreSQL バックエンド](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/) のみでサポートされています。）
  * '$' 正規表現検索。

  例：

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

> `paginate` デコレータ、`ordering` デコレータ、`searching` デコレータを同時に使用する場合は、`paginate` を `ordering` デコレータの上に、`ordering` デコレータを `searching` デコレータの上に置く必要があります。データはまずフィルタリングされ、次にソートされ、最後にページネーションされるためです。例：
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
