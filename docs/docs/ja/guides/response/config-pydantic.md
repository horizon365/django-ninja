---
comments: true
---
# Pydantic 設定のオーバーライド

**Django Ninja の `Schema`** には、スキーマの [Pydantic `Config` クラス](https://pydantic.com.cn/usage/model_config/)を通じて利用できる多くのカスタマイズ設定があります。

!!! note
    内部的には、**Django Ninja** は [Pydantic Models](https://pydantic.com.cn/usage/models/) とそのすべての機能と利点を使用しています。
    Django モデルと一緒に作業するときのコードの混乱を避けるため、`Schema` というエイリアスが選ばれました。
    Pydantic のモデルクラスはデフォルトで "Model" という名前であり、Django の "Model" クラスと衝突するためです。

## CamelCase スキーマの例

興味深い `Config` 属性の 1 つが [`alias_generator`](https://pydantic.com.cn/usage/model_config/#alias-generator) です。
**Django Ninja** で Pydantic を使用した例は次のようになります:

```python hl_lines="12 13"
from ninja import Schema


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class CamelModelSchema(Schema):
    str_field_name: str
    float_field_name: float

    class Config(Schema.Config):
        alias_generator = to_camel
```

!!! note
    スキーマの `Config` をオーバーライドするときは、基底の `Config` クラスを継承する必要があります。

フィールド名の出力（camelCase など）を変更したい場合は、`populate_by_name` と `by_alias` も設定する必要があることに注意してください

```python hl_lines="6 9"
class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "email"]
        alias_generator = to_camel
        populate_by_name = True  # !!!!!! <--------


@api.get("/users", response=list[UserSchema], by_alias=True) # !!!!!! <-------- by_alias
def get_users(request):
    return User.objects.all()

```

結果:

```JSON
[
  {
    "Id": 1,
    "Email": "tim@apple.com"
  },
  {
    "Id": 2,
    "Email": "sarah@smith.com"
  }
  ...
]

```

## Django モデルからのカスタム設定

[`create_schema`](django-pydantic-create-schema.md#create_schema) を使用する場合、生成されたスキーマを使ってカスタム設定を持つ別のクラスを構築できます。たとえば:

```python hl_lines="10"
from django.contrib.auth.models import User
from ninja.orm import create_schema


BaseUserSchema = create_schema(User)


class UserSchema(BaseUserSchema):

    class Config(BaseUserSchema.Config):
        ...
```

!!! done

    次の章に進みましょう！ **[ページネーション](pagination.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
