---
comments: true
---
# チュートリアル - レスポンスの扱い

## レスポンススキーマの定義

**Django Ninja** では、検証とドキュメント化の目的でレスポンススキーマを定義できます。

現在の Django ユーザーに関する情報を返す 3 つ目の操作を作成してみましょう。

```python
from ninja import Schema

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users do not have the following fields, so provide default values.
    email: str = None
    first_name: str = None
    last_name: str = None

@api.get("/me", response=UserSchema)
def me(request):
    return request.user
```

これにより、Django の `User` オブジェクトが、定義されたフィールドだけを含む辞書に変換されます。

### 複数のレスポンスタイプ

現在のユーザーが認証されていない場合に、別のレスポンスを返すようにしてみましょう。

```python hl_lines="2-5 7-8 10 12-13"
class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 
```

ご覧のとおり、2 つの要素を持つタプルを返すことができ、それは HTTP レスポンスコードとデータとして解釈されます。

!!! success

    これでチュートリアルは終わりです！ 詳しくは **[その他のチュートリアル](other/crud.md)** や **[ハウツーガイド](../guides/input/operations.md)** をチェックしてください。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
