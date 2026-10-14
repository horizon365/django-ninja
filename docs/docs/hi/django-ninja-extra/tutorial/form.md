---
comments: true
---
यदि आप अनिश्चित हैं कि django-ninja-extra में `application/x-www-form-urlencoded` या `multipart/form-data` जैसे content types के साथ POST requests को कैसे handle किया जाए, तो यह guide आपके लिए उपयोगी होगी।
Django-Ninja अधिकांश use cases को पहले से [यहाँ](https://django-ninja.cn/tutorial/form-params/) कवर करता है, लेकिन मैं यहाँ आपको एक संक्षिप्त सारांश दूंगा।

### Parameters के रूप में Form Data

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
यहाँ दो बातें ध्यान देने योग्य हैं:

- आपको `ninja` module से `Form` import करने की आवश्यकता है
- अपने parameters के डिफ़ॉल्ट मान के रूप में `Form` का उपयोग करें


!!! info
    इसके बारे में अधिक जानकारी के लिए, [Django-Ninja Form Tutorial](https://django-ninja.cn/guides/input/form-params/) देखें
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
