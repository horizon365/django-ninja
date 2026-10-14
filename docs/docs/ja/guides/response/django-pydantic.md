---
comments: true
---
# Django モデルからのスキーマ生成


スキーマはバリデーションルールやレスポンスを定義するのに非常に便利ですが、データベースモデルをスキーマに反映し、変更を同期し続ける必要がある場合があります。
## ModelSchema

`ModelSchema` は、モデルからスキーマを自動生成できる特殊な基底クラスです。

必要なのは、スキーマの `Meta` に `model` と `fields` を設定することだけです:


```python hl_lines="2 5 6 7"
from django.contrib.auth.models import User
from ninja import ModelSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
```

### すべてのモデルフィールドを使用する

モデルのすべてのフィールドを使用するには — `fields` に `__all__` を渡します:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    __all__ の使用は推奨されません。
    <br>
    望まないデータ（上記の例ではハッシュ化されたパスワードなど）が誤って露出する可能性があります。
    <br>
    一般的な推奨事項 — API で表示したいフィールドのリストは `fields` を使って明示的に定義してください。

### モデルフィールドの除外

一部を**除く**すべてのフィールドを使用するには、`exclude` 設定を使用します:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'user_permissions']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     email: str
#     is_superuser: bool
#     ... and the rest

```

### フィールドのオーバーライド

一部のフィールドのデフォルトのアノテーションを変更したり、新しいフィールドを追加したりするには、通常どおりアノテーション付きのプロパティを使用します。
```python hl_lines="1 2 3 4 8"
class GroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSchema(ModelSchema):
    groups: List[GroupSchema] = []

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

```


### フィールドをオプションにする

PATCH の API オペレーションでは、通常スキーマのすべてのフィールドをオプションにする必要があります。これには fields_optional 設定を使用できます

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

すべてではなく一部のフィールドだけをオプションにすることもできます:
```python
     fields_optional = ['description']
```

!!! done

    次の章に進みましょう！ **[スキーマの動的生成](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
