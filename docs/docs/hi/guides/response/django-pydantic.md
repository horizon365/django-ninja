---
comments: true
---
# Django Models से Schemas बनाना


Schemas validation rules और responses परिभाषित करने के लिए बहुत उपयोगी हैं, लेकिन कभी-कभी आपको अपने database models को schemas में reflect करने और बदलावों को sync में रखने की आवश्यकता होती है।
## ModelSchema

`ModelSchema` एक विशेष base class है जो आपके model से स्वचालित रूप से एक schema बना सकती है।

आपको बस अपने schema की `Meta` पर `model` और `fields` सेट करना है:


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

### Model के सभी Fields का उपयोग करना

Model के सभी fields का उपयोग करने के लिए — आप `fields` को `__all__` पास कर सकते हैं:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    __all__ का उपयोग करने की सलाह नहीं दी जाती।
    <br>
    इससे अनचाहे data के आकस्मिक exposure का जोखिम हो सकता है (जैसे ऊपर दिए गए उदाहरण में hashed password)।
    <br>
    सामान्य सलाह - अपनी API में दिखाई देने वाले fields की सूची को स्पष्ट रूप से परिभाषित करने के लिए `fields` का उपयोग करें।

### Model Fields को exclude करना

सभी fields में से **चुनिंदा कुछ को छोड़कर** उपयोग करने के लिए, आप `exclude` configuration का उपयोग कर सकते हैं:

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

### Fields को override करना

कुछ fields के लिए डिफ़ॉल्ट annotations बदलने के लिए, या नए fields जोड़ने के लिए, बस हमेशा की तरह annotated properties का उपयोग करें।
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


### Fields को Optional बनाना

PATCH API operations के लिए, आपको आमतौर पर schema के सभी fields को optional बनाने की आवश्यकता होती है। इसके लिए, आप fields_optional configuration का उपयोग कर सकते हैं

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

आप सभी के बजाय केवल कुछ optional fields भी परिभाषित कर सकते हैं:
```python
     fields_optional = ['description']
```

!!! done

    अगले अध्याय पर जाएँ! **[Dynamically Generating a Schema](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
