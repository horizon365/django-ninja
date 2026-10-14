---
comments: true
---
# **Searching**

**Django Ninja Extra** Django-Ninja-Extra searching module के `searching` decorator का उपयोग करके एक intuitive searching model प्रदान करता है। यह route function result से एक queryset या list की अपेक्षा करता है।

> यह feature [DRF SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter) से प्रेरित था

## **Attributes**

`def searching(func_or_searching_class: Any = NOT_SET, **searching_params: Any) -> Callable[..., Any]:`

- func_or_searching_class: एक route function या एक searching class define करता है। डिफ़ॉल्ट: `ninja_extra.searching.Searching`
- searching_params: searching class को initialize करने के लिए उपयोग किए जाने वाले अतिरिक्त parameters

### डिफ़ॉल्ट Searching Class बदलें

डिफ़ॉल्ट searching class बदलने के लिए, आपको `settings.py` में key `SEARCHING_CLASS` के साथ एक `NINJA_EXTRA` variable जोड़ने की आवश्यकता है और searching class के path को परिभाषित करने वाला एक मान देना होगा

```python
# Django project settings.py
INSTALLED_APPS = [
    ...
]
NINJA_EXTRA={
    'SEARCHING_CLASS': 'someapp.somemodule.CustomSearching'
}
```

## **उपयोग**

- यदि आप `search_fields` parameter निर्दिष्ट नहीं करते हैं, तो अपरिवर्तित results लौटाए जाएंगे।
- उदाहरण के लिए, users को username या email के आधार पर search करने के लिए:
  > http://example.com/api/users?search=someuser
- आप foreign key या many-to-many fields पर related lookups करने के लिए lookup API double-underscore notation का भी उपयोग कर सकते हैं:
  > search_fields = ['username', 'email', 'profile__profession']
- डिफ़ॉल्ट रूप से, search case-insensitive partial matching का उपयोग करेगा। Search parameter में कई search terms हो सकते हैं, जिन्हें spaces और/या commas से अलग किया जाना चाहिए। यदि कई search terms का उपयोग किया जाता है, तो केवल वे objects list में लौटाए जाएंगे जो सभी दिए गए terms से match करते हैं। `search_fields` से पहले विभिन्न characters जोड़कर search behavior को प्रतिबंधित किया जा सकता है।

  * '^' Starts-with के आधार पर search।
  * '=' Exact match।
  * '@' Full-text search। (वर्तमान में केवल Django के [PostgreSQL backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/) द्वारा समर्थित।)
  * '$' Regex search।

  उदाहरण के लिए:

    > search_fields = ['=username', '=email']

```python
from typing import List
from ninja_extra.searching import searching, Searching
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
    @searching(Searching, search_fields=['username', 'email'])
    def get_users(self):
        return user_model.objects.all()

    @route.get('/iexact-email', response=List[UserSchema])
    @searching(search_fields=['=email'])
    def get_users_with_search_iexact_email(self):
        return [u for u in user_model.objects.all()]


api = NinjaExtraAPI(title='Searching Test')
api.register_controllers(UserController)
```

## Note

> यदि आप `paginate` decorator, `ordering` decorator और `searching` decorator का एक साथ उपयोग करते हैं, तो `paginate` को `ordering` decorator के ऊपर होना चाहिए, और `ordering` decorator को `searching` decorator के ऊपर होना चाहिए। क्योंकि data पहले filter किया जाता है, फिर sort किया जाता है, और अंत में paginate किया जाता है, उदाहरण के लिए:
>
> ```python
>    @route.get('', response=List[UserSchema])
>    @paginate
>    @ordering(Ordering, ordering_fields=['username', 'email'])
>    @searching(Searching, search_fields=['username', 'email'])
>    def get_users(self):
>        return user_model.objects.all()
> ```

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
