---
comments: true
---
# **Ordering**

**Django Ninja Extra** Django-Ninja-Extra ordering module के `ordering` decorator का उपयोग करके एक intuitive ordering model प्रदान करता है। यह route function result से एक queryset या list की अपेक्षा करता है।

> यह feature [DRF OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter) से प्रेरित था

## **Attributes**

`def ordering(func_or_ordering_class: Any = NOT_SET, **ordering_params: Any) -> Callable[..., Any]:`

- func_or_ordering_class: एक route function या एक ordering class define करता है। डिफ़ॉल्ट: `ninja_extra.ordering.Ordering`
- ordering_params: ordering class को initialize करने के लिए उपयोग किए जाने वाले अतिरिक्त parameters

### डिफ़ॉल्ट Ordering Class बदलें

डिफ़ॉल्ट ordering class बदलने के लिए, आपको `settings.py` में key `ORDERING_CLASS` के साथ एक `NINJA_EXTRA` variable जोड़ने की आवश्यकता है और ordering class के path को परिभाषित करने वाला एक मान देना होगा।

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'ORDERING_CLASS': 'someapp.somemodule.CustomOrdering'
}
```

## **उपयोग**

- यदि आप `ordering_fields` parameter निर्दिष्ट नहीं करते हैं, तो queryset के सभी fields का उपयोग ordering के लिए किया जाएगा।
- उदाहरण के लिए, users को username के आधार पर order करने के लिए
  > http://example.com/api/users?ordering=username
- Client field name से पहले `-` लगाकर reverse ordering भी निर्दिष्ट कर सकता है, उदाहरण के लिए:
  > http://example.com/api/users?ordering=-username
- कई orderings भी निर्दिष्ट की जा सकती हैं:
  > http://example.com/api/users?ordering=username,email

```python
from typing import List
from ninja_extra.ordering import ordering, Ordering
from ninja_extra import api_controller, route, NinjaExtraAPI
from ninja import ModelSchema
from django.contrib.auth import get_user_model

user_model = get_user_model()


class UserSchema(ModelSchema):
    class Config:
        model = user_model
        model_fields = ['username', 'email']


@api_controller('/users')
class UserController:
    @route.get('', response=List[UserSchema])
    @ordering(Ordering, ordering_fields=['username', 'email'])
    def get_users(self):
        return user_model.objects.all()

    @route.get('/all-sort', response=List[UserSchema])
    @ordering
    def get_users_with_all_field_ordering(self):
        return [u for u in user_model.objects.all()]


api = NinjaExtraAPI(title='Ordering Test')
api.register_controllers(UserController)
```

## Note

> यदि आप `paginate` decorator और `ordering` decorator दोनों का उपयोग करते हैं, तो `paginate` decorator को `ordering` decorator के ऊपर होना चाहिए, क्योंकि data पहले sort किया जाता है और फिर paginate किया जाता है, उदाहरण के लिए:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
