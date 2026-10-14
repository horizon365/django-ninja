
Ninja JWT एक application के साथ आता है जो token blacklist functionality प्रदान करता है।
इस application का उपयोग करने के लिए, इसे `settings.py` में installed applications की list में शामिल करें:

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

साथ ही, application की migrations चलाने के लिए `python manage.py migrate` चलाना सुनिश्चित करें।

यदि blacklist application `INSTALLED_APPS` में detect किया जाता है, तो Ninja JWT कोई भी बनाए गए refresh tokens या sliding tokens outstanding token list में जोड़ देगा।
यह किसी भी refresh token या sliding token को valid मानने से पहले यह भी जाँच करेगा कि token token blacklist में नहीं है।

Ninja JWT blacklist application अपनी outstanding और blacklist token lists को implement करने के लिए दो models का उपयोग करता है: `OutstandingToken` और `BlacklistedToken`।
दोनों models के लिए model admins परिभाषित हैं। एक token को blacklist में जोड़ने के लिए, admin में उसके संबंधित `OutstandingToken` record को खोजें,
फिर admin का पुनः उपयोग करके एक `BlacklistedToken` record बनाएं जो उस `OutstandingToken` record की ओर इशारा करे।

वैकल्पिक रूप से, आप `BlacklistMixin` subclass का एक instance बनाकर और उस instance पर `blacklist` method को कॉल करके एक token को blacklist कर सकते हैं:

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

यह token के `jti` claim, या `JTI_CLAIM` setting द्वारा निर्दिष्ट किसी भी claim के लिए एक unique outstanding token और blacklist record बनाएगा।

Blacklist application एक management command `flushexpiredtokens` भी प्रदान करता है, जो outstanding list और blacklist दोनों से किसी भी expired tokens को हटा देगा।
आपको अपने server या hosting platform पर एक cron job सेट अप करना चाहिए जो इस command को दैनिक रूप से चलाए।

!!! success

    अगले अध्याय **[Development and Contributing](development_and_contributing.md)** पर जारी रखें।


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
