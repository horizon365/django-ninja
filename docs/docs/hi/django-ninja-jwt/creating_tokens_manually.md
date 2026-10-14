
कभी-कभी आप किसी उपयोगकर्ता के लिए मैन्युअल रूप से एक token बनाना चाह सकते हैं। इसे निम्नानुसार किया जा सकता है:

```python
from ninja_jwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

ऊपर दिया गया function `get_tokens_for_user` दिए गए उपयोगकर्ता के लिए एक नए refresh token और access token का serialized प्रतिनिधित्व लौटाएगा।
सामान्य तौर पर, `ninja_jwt.tokens.Token` के किसी भी subclass के tokens इस तरह बनाए जा सकते हैं।

!!! success

    अगले अध्याय **[Token Types](token_types.md)** पर जारी रखें।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
