
ユーザーに対してトークンを手動で作成したい場合があるでしょう。これは次のように行えます：

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

上の関数 `get_tokens_for_user` は、指定されたユーザーに対する新しい refresh トークンと access トークンのシリアライズ表現を返します。
一般に、`ninja_jwt.tokens.Token` の任意のサブクラスのトークンもこの方法で作成できます。

!!! success

    次の章 **[Token Types](token_types.md)** に進みましょう。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
