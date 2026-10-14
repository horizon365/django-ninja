
#### 요구 사항
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

이것들이 공식적으로 지원되는 Python과 패키지 버전입니다. 다른 버전도 동작할 수 있습니다. tox 설정을 자유롭게 수정해 보고 무엇이 가능한지 확인해 보세요.

## 설치

Ninja JWT는 pip을 통해 설치할 수 있습니다:

    pip install django-ninja-jwt

추가로 `NinjaJWTDefaultController` 컨트롤러를 Django-Ninja API에 등록해야 합니다.

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController`는 `obtain_token`, `refresh_token`, `verify_token` 세 개의 라우트를 제공합니다.
`TokenVerificationController`와 `TokenObtainPairController` 두 서브클래스의 조합입니다.
이 라우트들을 커스터마이즈하고 싶다면, 이 컨트롤러들을 상속하고 구현을 변경하면 됩니다.

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

현지화/번역을 사용하고 싶다면, `INSTALLED_APPS`에 `ninja_jwt`를 추가하기만 하면 됩니다.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## 사용법

Ninja JWT가 제대로 작동하는지 확인하려면, curl로 몇 가지 테스트 요청을 보낼 수 있습니다:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

반환된 access 토큰을 사용하여 보호된 뷰에 대한 인증을 증명할 수 있습니다:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

수명이 짧은 이 access 토큰이 만료되면, 수명이 더 긴 refresh 토큰을 사용하여 다른 access 토큰을 얻을 수 있습니다:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

암호화 의존성 (선택 사항)
-------------------------------------

특정 디지털 서명 알고리즘(예: RSA 및 ECDSA; 다른 알고리즘은 PyJWT 참조)을 사용하여 토큰을 인코딩하거나 디코딩할 계획이라면,
cryptography_ 라이브러리를 설치해야 합니다. 이는 명시적으로 설치하거나, `django-ninja-jwt` requirements의 필수 항목으로 설치할 수 있습니다:

    pip install django-ninja-jwt[crypto]

`Ninja JWT` 프로젝트의 requirements 파일을 사용할 때는 `django-ninja-jwt[crypto]` 형식이 권장됩니다,
별도의 `cryptography` requirement 줄은 나중에 사용되지 않는 requirement로 오해되어 제거될 수 있기 때문입니다.
[cryptography](https://cryptography.io)

!!! success

    다음 장 **[라우트 인증](auth_integration.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
