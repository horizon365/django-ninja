
Ninja JWT दो अलग-अलग token types प्रदान करता है जिनका उपयोग authentication सिद्ध करने के लिए किया जा सकता है।
Token के payload में, उसका प्रकार उसके token type claim के मान से पहचाना जा सकता है, जो डिफ़ॉल्ट रूप से `token_type` होता है।
हालाँकि, इसका मान `access`, `sliding`, या `refresh` हो सकता है,
लेकिन वर्तमान में refresh tokens को वैध authentication tokens नहीं माना जाता है। प्रकार को संग्रहीत करने के लिए उपयोग किए जाने वाले claim का नाम `TOKEN_TYPE_CLAIM` सेटिंग बदलकर कस्टमाइज़ किया जा सकता है।

डिफ़ॉल्ट रूप से, Ninja JWT authentication सिद्ध करने के लिए एक `access` token की अपेक्षा करता है।
अनुमत authentication token types `AUTH_TOKEN_CLASSES` सेटिंग के मान द्वारा निर्धारित होते हैं।
यह सेटिंग token classes की ओर इशारा करने वाले dotted paths की एक सूची रखती है। इसका डिफ़ॉल्ट `'ninja_jwt.tokens.AccessToken'` dotted path होता है,
लेकिन इसमें `'ninja_jwt.tokens.SlidingToken'` dotted path भी शामिल हो सकता है।
इनमें से कोई एक या दोनों dotted paths authentication token classes सूची में हो सकते हैं।
यदि दोनों मौजूद हैं, तो authentication सिद्ध करने के लिए दोनों token types का उपयोग किया जा सकता है।

Sliding Tokens
==============

Sliding tokens token उपयोगकर्ताओं के लिए अधिक सुविधाजनक अनुभव प्रदान करते हैं, लेकिन इसके बदले में कम सुरक्षा और, जब blacklist app उपयोग में हो, तो कम performance देते हैं।
Sliding token एक ऐसा token है जिसमें एक expiration claim और एक refresh expiration claim दोनों होते हैं। जब तक sliding token के expiration claim में दिया गया timestamp पार नहीं हुआ है,
इसे authentication सिद्ध करने के लिए उपयोग किया जा सकता है। इसके अलावा, जब तक उसके refresh expiration claim में दिया गया timestamp पार नहीं हुआ है,
इसे refresh view पर भी सबमिट किया जा सकता है ताकि अपडेटेड expiration claim के साथ इसकी एक प्रति प्राप्त की जा सके।

यदि आप sliding tokens का उपयोग करना चाहते हैं, तो `AUTH_TOKEN_CLASSES` सेटिंग को `('ninja_jwt.tokens.SlidingToken',)` में बदलें।
(वैकल्पिक रूप से, यदि आप authentication के लिए दोनों token types की अनुमति देना चाहते हैं, तो `AUTH_TOKEN_CLASSES` सेटिंग में `ninja_jwt.tokens` module के `AccessToken` और `SlidingToken` token classes की ओर इशारा करने वाले dotted paths शामिल हो सकते हैं)

इसके अतिरिक्त, `NinjaJWTSlidingController` को `api` के साथ रजिस्टर करें:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

ध्यान दें कि यदि आप blacklist app का उपयोग कर रहे हैं, तो Ninja JWT प्रत्येक authenticated request के लिए सभी sliding tokens को blacklist के विरुद्ध validate करेगा।
इससे authenticated API views की performance खराब होगी।

!!! success

    अगले अध्याय पर जाएँ **[Blacklist App](blacklist_app.md)**।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
