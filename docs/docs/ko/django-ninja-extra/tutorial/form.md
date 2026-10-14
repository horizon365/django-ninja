---
comments: true
---
django-ninja-extra에서 `application/x-www-form-urlencoded`나 `multipart/form-data` 같은 콘텐츠 타입의 POST 요청을 처리하는 방법을 잘 모르겠다면, 이 가이드가 유용할 것입니다.
Django-Ninja는 이미 [여기](https://django-ninja.cn/tutorial/form-params/)에서 대부분의 사용 사례를 다루고 있지만, 여기서 간단히 요약해 드리겠습니다.

### 폼 데이터를 매개변수로 사용하기

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
여기서 주의할 두 가지가 있습니다:

- `ninja` 모듈에서 `Form`을 임포트해야 합니다
- 매개변수의 기본값으로 `Form`을 사용합니다


!!! info
    이에 대한 자세한 내용은 [Django-Ninja 폼 튜토리얼](https://django-ninja.cn/guides/input/form-params/)을 참고하세요
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
