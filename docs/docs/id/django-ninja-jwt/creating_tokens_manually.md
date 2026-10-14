
Terkadang Anda mungkin ingin membuat token untuk seorang user secara manual. Ini dapat dilakukan sebagai berikut:

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

Fungsi `get_tokens_for_user` di atas akan mengembalikan representasi terserialisasi dari refresh token dan access token baru untuk user yang diberikan.
Secara umum, token dari subclass mana pun dari `ninja_jwt.tokens.Token` dapat dibuat dengan cara ini.

!!! success

    Lanjutkan ke bab berikutnya **[Tipe Token](token_types.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
