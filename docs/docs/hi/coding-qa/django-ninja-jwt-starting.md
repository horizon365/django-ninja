---
comments: true
---
## परिचय
JWT के बारे में मैंने बहुत पहले सुना था लेकिन कभी वास्तव में इसका उपयोग नहीं किया था। हाल ही में, tus resumable upload protocol पर शोध करते समय, मैं hooks-http स्तर तक पहुँच गया, जिसका लक्ष्य file upload के दौरान authentication करना था। स्वाभाविक रूप से, मेरे दिमाग में `django-ninja-jwt` package आया। मुझे लगा कि यह सरल होना चाहिए, लेकिन [चीनी documentation](https://django-ninja.cn/django-ninja-jwt/) पढ़ने के बाद, मुझे पता चला कि यह केवल सरल नहीं — बल्कि एक चौंकाने वाली सीमा तक न्यूनतम (bare-bones) था।

## शुरू करना

Guide के अनुसार, आपको केवल `dango-ninja-jwt` और `django-ninja-extra` install करने की आवश्यकता है, फिर `NinjaAPI` को `njaExtraAPI` से बदलना है, और इसमें बस एक line लगती है।

```python
api.register_controllers(NinjaJWTDefaultController)
```

ईमानदारी से कहूँ तो यह हैरान करने वाला है।

रुकिए — पहले docs पर एक नज़र डालते हैं। तीन नए endpoints दिखाई देते हैं: `pair`, `refresh`, और `verify`।
![JWT swagger UI token](../img/jwt-token.png)
ऊपरी दाएँ कोने में lock icon पर ध्यान दें — यह बाद में काम आएगा। यह केवल तब दिखाई देता है जब आप `JWTAuth` function का उपयोग करते हैं।

### pair
पहला है `pair` endpoint। इसका अर्थ है कि जब आप username और password प्रदान करते हैं, तो यह authentication tokens और refresh tokens return करता है।
Request body का format इस प्रकार है:
```json
{
  "password": "string",
  "username": "string"
}
```
ध्यान दें: यहाँ `username` नीचे दिखाई देता है, जो आपकी धारणा से थोड़ा अलग हो सकता है।
Execute पर click करने के बाद, आपको इस तरह का आउटपुट मिलेगा:
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
ऊपर दिया गया `access` token authentication के लिए उपयोग किया जा सकता है, लेकिन डिफ़ॉल्ट रूप से इसकी lifetime सीमित होती है। `refresh` token की lifetime `access` से अधिक लंबी होती है, और इसका उपयोग पिछले token के समाप्त होने के बाद नया `access` token प्राप्त करने के लिए किया जाता है।
Refresh होने के बाद, पिछला `access` token invalid हो जाता है।

इस बिंदु पर, आप `access` को copy करके ऊपरी दाएँ कोने में lock icon में paste कर सकते हैं। इस तरह, वर्तमान page के प्रत्येक endpoint इसका उपयोग कर सकते हैं, जो debugging के लिए सुविधाजनक है।
### verify
आप तीसरे endpoint, `verify`, पर जाकर जाँच सकते हैं कि `access` token मान्य है या नहीं।

तो कुल मिलाकर, `django-ninja-jwt` बस आपके लिए तीन endpoints बना देता है, जिससे tokens प्राप्त करना, refresh करना और परखना आसान हो जाता है।

## Customization
केवल ये तीन endpoints पर्याप्त नहीं हैं — कम से कम, हमें अपने विशिष्ट endpoints पर authentication जोड़ने की आवश्यकता है।
यहाँ आपको जिस चीज़ की आवश्यकता है वह है `JWTAuth`; इसका उपयोग करने के बाद ही lock icon दिखाई देगा।
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
और `some` endpoint पर, एक अलग lock icon भी होता है।
![JWT swagger UI token custom](../img/jwt-token-custom.png)
ऊपर दिए गए `some` endpoint के लिए, यदि authentication सफल होता है, तो यह वर्तमान में logged-in user का username respond करता है। यदि विफल होता है, तो यह 401 response return करता है।
Backend developers को frontend team को यह बताना होगा कि वे यह value अपने साथ भेजें — उन्हें [pair](#pair) section पर जाकर इसे प्राप्त करने दें, और समय-समय पर [refresh](#refresh) पर जाकर इसे refresh करने दें।

### Token Lifetime को Configure करें

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### आगे की Customization
यदि अपनी ninja route में `@route.get('/some', auth=JWTAuth())` का उपयोग करना आपकी आवश्यकताओं को पूरा नहीं करता, तो आप function के अंदर `authenticate` को call कर सकते हैं।

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # If it fails, a 401 is raised internally
    if auth.authenticate(request, token):
        return request.auth.username

```
ऊपर दिया गया `token` आपको स्वयं `request` object से extract करना होगा।
