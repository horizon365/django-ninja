
Ninja JWT के कुछ व्यवहारों को `settings.py` में settings variables के माध्यम से customize किया जा सकता है:

```python
# Django project settings.py

from datetime import timedelta
from django.conf import settings
...

NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'ninja_jwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('ninja_jwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'ninja_jwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    
    # For Controller Schemas
    # FOR OBTAIN PAIR
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': "ninja_jwt.schema.TokenObtainPairInputSchema",
    'TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA': "ninja_jwt.schema.TokenRefreshInputSchema",
    # FOR SLIDING TOKEN
    'TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA': "ninja_jwt.schema.TokenObtainSlidingInputSchema",
    'TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA':"ninja_jwt.schema.TokenRefreshSlidingInputSchema",
    
    'TOKEN_BLACKLIST_INPUT_SCHEMA': "ninja_jwt.schema.TokenBlacklistInputSchema",
    'TOKEN_VERIFY_INPUT_SCHEMA': "ninja_jwt.schema.TokenVerifyInputSchema",
}
```

ऊपर, इन settings के डिफ़ॉल्ट मान दिखाए गए हैं।

## `ACCESS_TOKEN_LIFETIME`

एक `datetime.timedelta` object जो access tokens के lifetime को निर्दिष्ट करता है।
Token generation के दौरान, इस `timedelta` मान को current UTC time में जोड़ा जाता है ताकि token का डिफ़ॉल्ट `exp` claim मान प्राप्त हो सके।

## `REFRESH_TOKEN_LIFETIME`

एक `datetime.timedelta` object जो refresh tokens के lifetime को निर्दिष्ट करता है।
Token generation के दौरान, इस `timedelta` मान को current UTC time में जोड़ा जाता है ताकि token का डिफ़ॉल्ट `exp` claim मान प्राप्त हो सके।

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
जब इसे ``True`` सेट किया जाता है, यदि blacklist app उपयोग में है और ``ROTATE_REFRESH_TOKENS`` को ``True`` सेट किया गया है,
तो ``TokenRefreshView`` को submit किए गए refresh tokens blacklist में जोड़ दिए जाएंगे।
इस setting का उपयोग करने के लिए आपको अपनी settings file में ``'ninja_jwt.token_blacklist'`` को अपने ``INSTALLED_APPS`` में जोड़ने की आवश्यकता है।


`/blacklist_app`{.interpreted-text role="doc"} के बारे में अधिक जानें।

## `UPDATE_LAST_LOGIN`

जब इसे `True` सेट किया जाता है, तो login (TokenObtainPairView) के समय auth_user table में last_login field अपडेट हो जाता है।

    Warning: Updating last login will greatly increase the number of database transactions.
    Abusers of the view may slow down the server, which may be a security vulnerability.
    If you really want to do this, at least throttle the endpoint with DRF.

## `ALGORITHM`

वह algorithm जिसका उपयोग tokens पर signing/verification operations करने के लिए PyJWT library से किया जाता है।
Symmetric HMAC signing और verification का उपयोग करने के लिए, आप निम्नलिखित algorithms का उपयोग कर सकते हैं: ``'HS256'``, ``'HS384'``,``'HS512'``।
HMAC algorithm चुनने पर, ``SIGNING_KEY`` setting का उपयोग signing key और verification key दोनों के रूप में किया जाएगा।
इस स्थिति में, ``VERIFYING_KEY`` setting को नजरअंदाज किया जाता है।
Asymmetric RSA signing और verification का उपयोग करने के लिए, आप निम्नलिखित algorithms का उपयोग कर सकते हैं: ``'RS256'``, ``'RS384'``, ``'RS512'``।
RSA algorithm चुनने पर, ``SIGNING_KEY`` setting को एक ऐसी string पर सेट किया जाना चाहिए जिसमें एक RSA private key हो।
इसी तरह, ``VERIFYING_KEY`` setting को एक ऐसी string पर सेट किया जाना चाहिए जिसमें एक RSA public key हो।

## `SIGNING_KEY`

Signing key जिसका उपयोग बनाए गए tokens की सामग्री पर sign करने के लिए किया जाता है।
HMAC signing के लिए, यह signing protocol द्वारा आवश्यक जितने bits के data वाली कम से कम एक random string होनी चाहिए।
RSA signing के लिए, यह 2048-bit या उससे लंबी RSA private key वाली एक string होनी चाहिए।
चूँकि Simple JWT डिफ़ॉल्ट रूप से 256-bit HMAC signing का उपयोग करता है, `SIGNING_KEY` setting आपके Django project की `SECRET_KEY` setting के मान पर डिफ़ॉल्ट रहती है।
हालाँकि यह सबसे युक्तियुक्त डिफ़ॉल्ट है जो Simple JWT प्रदान कर सकता है, फिर भी developers को अनुशंसा की जाती है कि वे इस setting को Django project की secret key से स्वतंत्र किसी मान पर बदल दें।
इससे signing key से जुड़े tokens की सुरक्षा समझौता होने की स्थिति में signing key को बदलना आसान हो जाएगा।

## `VERIFYING_KEY`

Verifying key जिसका उपयोग बनाए गए tokens की सामग्री को verify करने के लिए किया जाता है। यदि ``ALGORITHM`` setting एक HMAC algorithm निर्दिष्ट करती है,
तो ``VERIFYING_KEY`` setting को नजरअंदाज किया जाता है और इसके बजाय ``SIGNING_KEY`` का मान उपयोग किया जाता है।
यदि ``ALGORITHM`` setting एक RSA algorithm निर्दिष्ट करती है, तो ``VERIFYING_KEY`` setting को एक ऐसी string पर सेट किया जाना चाहिए जिसमें एक RSA public key हो।

## `AUDIENCE`

बनाए गए tokens में शामिल करने के लिए और/या decoded tokens में verify करने के लिए audience claim।
जब इसे ``None`` सेट किया जाता है, तो इस field को token से exclude कर दिया जाता है और verify नहीं किया जाता।

## `ISSUER`

बनाए गए tokens में शामिल करने के लिए और/या decoded tokens में verify करने के लिए issuer claim।
जब इसे ``None`` सेट किया जाता है, तो इस field को token से exclude कर दिया जाता है और verify नहीं किया जाता।

### ``JWK_URL``
----------

JWK_URL का उपयोग token signatures को verify करने के लिए आवश्यक public key को dynamically resolve करने के लिए किया जाता है।
उदाहरण के लिए, Auth0 का उपयोग करते समय, आप इसे 'https://yourdomain.auth0.com/.well-known/jwks.json' पर सेट कर सकते हैं।
जब इसे ``None`` सेट किया जाता है, तो इस field को token backend से exclude कर दिया जाता है और verification के दौरान उपयोग नहीं किया जाता

### ``LEEWAY``
----------

Leeway का उपयोग expiration time को कुछ margin देने के लिए किया जाता है। यह सेकंडों का एक integer या एक ``datetime.timedelta`` हो सकता है।
अधिक जानकारी के लिए कृपया https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp देखें।

###``AUTH_HEADER_TYPES``
---------------------

Authentication की आवश्यकता वाले views के लिए स्वीकार किए जाने वाले authorization header type(s)। उदाहरण के लिए, ``'Bearer'`` मान का अर्थ है कि authentication की आवश्यकता वाले views निम्न format वाले header की तलाश करेंगे:
``Authorization: Bearer <token>``। यह setting संभावित header types की एक list या tuple भी हो सकती है (उदाहरण के लिए ``('Bearer', 'JWT')``)।
यदि इस तरह एक list या tuple का उपयोग किया जाता है, और authentication विफल हो जाता है, तो response में "WWW-Authenticate" header बनाने के लिए collection के पहले item का उपयोग किया जाएगा।

###``AUTH_HEADER_NAME``
----------------------------

Authentication के लिए उपयोग किए जाने वाले authorization header का नाम। डिफ़ॉल्ट `HTTP_AUTHORIZATION` है, जो requests से `Authorization` header स्वीकार करेगा।
उदाहरण के लिए, यदि आप अपने request headers में `X_Access_Token` का उपयोग करना चाहते हैं, तो अपनी settings में `AUTH_HEADER_NAME` को `HTTP_X_ACCESS_TOKEN` के रूप में निर्दिष्ट करें।


###``USER_ID_FIELD``
-----------------

User model का वह database field जिसे उपयोगकर्ता की पहचान करने के लिए बनाए गए tokens में शामिल किया जाएगा।
अनुशंसा की जाती है कि इस setting का मान ऐसे field को निर्दिष्ट करे जिसका प्रारंभिक मान चुने जाने के बाद आमतौर पर परिवर्तन नहीं होता।
उदाहरण के लिए, "username" या "email" field निर्दिष्ट करना एक खराब विकल्प होगा,
क्योंकि किसी account का username या email उस service में account management के design के आधार पर बदल सकता है।
इससे एक पुराने username के साथ एक नया account बनाया जा सकता है, जबकि उस username को user identifier के रूप में उपयोग करने वाले मौजूदा tokens valid बने रहते हैं।

###``USER_ID_CLAIM``
-----------------

वह claim जिसका उपयोग बनाए गए tokens में user identifier को संग्रहीत करने के लिए किया जाता है। उदाहरण के लिए, मान को ```"user_id"``` सेट करने का अर्थ है कि बनाया गया token एक "user_id" claim रखता है,
जिसमें उपयोगकर्ता का identifier होता है।

###``USER_AUTHENTICATION_RULE``
----------------------------

एक callable जिसका उपयोग यह निर्धारित करने के लिए किया जाता है कि उपयोगकर्ता को authenticate करने की अनुमति है या नहीं। यह rule एक valid token को process किए जाने के बाद लागू होता है। User object एक argument के रूप में callable को पास किया जाता है।
डिफ़ॉल्ट rule यह जाँचना है कि ``is_active`` flag अभी भी ``True`` है या नहीं।
Callable को एक boolean मान लौटाना चाहिए, ``True`` का अर्थ authorized है, अन्यथा ``False`` होने पर 401 status code आता है।

###``AUTH_TOKEN_CLASSES``
----------------------

Dotted paths की एक list जो उन classes की ओर इशारा करती है जो authentication सिद्ध करने के लिए अनुमत token types निर्दिष्ट करती हैं। नीचे "Token Types" section में अधिक जानकारी।

###``TOKEN_TYPE_CLAIM``
--------------------

वह claim का नाम जिसका उपयोग token type को संग्रहीत करने के लिए किया जाता है। नीचे "Token Types" section में अधिक जानकारी।

###``JTI_CLAIM``
-------------

वह claim का नाम जिसका उपयोग token के unique identifier को संग्रहीत करने के लिए किया जाता है। इस identifier का उपयोग blacklist app में revoked tokens को पहचानने के लिए किया जाता है।
कुछ मामलों में, ऐसा मान संग्रहीत करने के लिए डिफ़ॉल्ट "jti" claim के अलावा किसी अन्य claim का उपयोग करना आवश्यक हो सकता है।

###``TOKEN_USER_CLASS``
--------------------

एक verified token द्वारा समर्थित एक stateless user object। इसका उपयोग केवल JWTStatelessUser authentication backend द्वारा किया जाता है।
मान एक dotted path है जो आपकी ``"rest_framework_simplejwt.models.TokenUser"`` subclass की ओर इशारा करता है, जो डिफ़ॉल्ट भी है।

###``SLIDING_TOKEN_LIFETIME``
--------------------------

एक ``datetime.timedelta`` object जो निर्दिष्ट करता है कि एक sliding token authentication सिद्ध करने के लिए कितने समय तक valid रहता है।
Token generation के दौरान, इस ``timedelta`` मान को current UTC time में जोड़ा जाता है ताकि token का डिफ़ॉल्ट "exp" claim मान प्राप्त हो सके।
नीचे "Sliding Tokens" section में अधिक जानकारी।

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

एक ``datetime.timedelta`` object जो निर्दिष्ट करता है कि एक sliding token कितने समय तक refresh के लिए valid रहता है।
Token generation के दौरान, इस `timedelta` मान को current UTC time में जोड़ा जाता है ताकि token का डिफ़ॉल्ट "exp" claim मान प्राप्त हो सके।
नीचे "Sliding Tokens" section में अधिक जानकारी।

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

वह claim का नाम जिसका उपयोग एक sliding token के refresh अवधि के expiration time को संग्रहीत करने के लिए किया जाता है। नीचे "Sliding Tokens" section में अधिक जानकारी।

!!! success

    अगले अध्याय **[Customizing Token Claims](customizing_token_claims.md)** पर जारी रखें।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
