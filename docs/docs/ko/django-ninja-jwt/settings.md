
Ninja JWT의 일부 동작은 `settings.py`의 설정 변수를 통해 커스터마이즈할 수 있습니다:

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

위에서 이 설정들의 기본값이 표시되어 있습니다.

## `ACCESS_TOKEN_LIFETIME`

access 토큰의 수명을 지정하는 `datetime.timedelta` 객체입니다.
토큰 생성 시 이 `timedelta` 값이 현재 UTC 시간에 더해져 토큰의 기본 `exp` 클레임 값이 됩니다.

## `REFRESH_TOKEN_LIFETIME`

refresh 토큰의 수명을 지정하는 `datetime.timedelta` 객체입니다.
토큰 생성 시 이 `timedelta` 값이 현재 UTC 시간에 더해져 토큰의 기본 `exp` 클레임 값이 됩니다.

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
``True``로 설정하면, 블랙리스트 앱이 사용 중이고 ``ROTATE_REFRESH_TOKENS``가 ``True``로 설정된 경우,
``TokenRefreshView``에 제출된 refresh 토큰이 블랙리스트에 추가됩니다.
이 설정을 사용하려면 설정 파일의 ``INSTALLED_APPS``에 ``'ninja_jwt.token_blacklist'``를 추가해야 합니다.


`/blacklist_app`{.interpreted-text role="doc"}에서 더 알아보세요.

## `UPDATE_LAST_LOGIN`

`True`로 설정하면 로그인 시(TokenObtainPairView) auth_user 테이블의 last_login 필드가 업데이트됩니다.

    경고: last_login을 업데이트하면 데이터베이스 트랜잭션 수가 크게 증가합니다.
    이 뷰를 남용하면 서버가 느려질 수 있으며, 이는 보안 취약점이 될 수 있습니다.
    정말 이렇게 하고 싶다면 최소한 DRF로 엔드포인트에 스로틀을 적용하세요.

## `ALGORITHM`

PyJWT 라이브러리에서 토큰에 대한 서명/검증 작업을 수행하는 데 사용되는 알고리즘입니다.
대칭 HMAC 서명 및 검증을 사용하려면 ``'HS256'``, ``'HS384'``,``'HS512'`` 알고리즘을 사용할 수 있습니다.
HMAC 알고리즘을 선택하면 ``SIGNING_KEY`` 설정이 서명 키와 검증 키 모두로 사용됩니다.
이 경우 ``VERIFYING_KEY`` 설정은 무시됩니다.
비대칭 RSA 서명 및 검증을 사용하려면 ``'RS256'``, ``'RS384'``, ``'RS512'`` 알고리즘을 사용할 수 있습니다.
RSA 알고리즘을 선택하면 ``SIGNING_KEY`` 설정은 RSA 개인 키를 포함하는 문자열로 설정되어야 합니다.
마찬가지로 ``VERIFYING_KEY`` 설정은 RSA 공개 키를 포함하는 문자열로 설정되어야 합니다.

## `SIGNING_KEY`

생성된 토큰의 내용에 서명하는 데 사용되는 서명 키입니다.
HMAC 서명의 경우 서명 프로토콜에 요구되는 만큼의 데이터 비트를 가진 임의 문자열이어야 합니다.
RSA 서명의 경우 2048비트 이상의 RSA 개인 키를 포함하는 문자열이어야 합니다.
Simple JWT는 기본적으로 256비트 HMAC 서명을 사용하므로, `SIGNING_KEY` 설정의 기본값은 Django 프로젝트의 `SECRET_KEY` 설정 값입니다.
이것이 Simple JWT가 제공할 수 있는 가장 합리적인 기본값이지만, 개발자가 이 설정을 Django 프로젝트의 시크릿 키와 독립적인 값으로 변경하는 것이 권장됩니다.
이렇게 하면 토큰에 사용되는 서명 키가 유출되었을 때 서명 키를 변경하기가 더 쉬워집니다.

## `VERIFYING_KEY`

생성된 토큰의 내용을 검증하는 데 사용되는 검증 키입니다. ``ALGORITHM`` 설정이 HMAC 알고리즘을 지정하면,
``VERIFYING_KEY`` 설정은 무시되고 대신 ``SIGNING_KEY``의 값이 사용됩니다.
``ALGORITHM`` 설정이 RSA 알고리즘을 지정하면, ``VERIFYING_KEY`` 설정은 RSA 공개 키를 포함하는 문자열로 설정되어야 합니다.

## `AUDIENCE`

생성된 토큰에 포함하거나 디코딩된 토큰에서 검증할 audience 클레임입니다.
``None``으로 설정하면 이 필드는 토큰에서 제외되고 검증되지 않습니다.

## `ISSUER`

생성된 토큰에 포함하거나 디코딩된 토큰에서 검증할 issuer 클레임입니다.
``None``으로 설정하면 이 필드는 토큰에서 제외되고 검증되지 않습니다.

### ``JWK_URL``
----------

JWK_URL은 토큰 서명을 검증하는 데 필요한 공개 키를 동적으로 확인하는 데 사용됩니다.
예를 들어 Auth0를 사용할 때 이 값을 'https://yourdomain.auth0.com/.well-known/jwks.json'으로 설정할 수 있습니다.
``None``으로 설정하면 이 필드는 토큰 백엔드에서 제외되고 검증 시 사용되지 않습니다

### ``LEEWAY``
----------

Leeway는 만료 시간에 약간의 여유를 주는 데 사용됩니다. 초 단위의 정수 또는 ``datetime.timedelta``일 수 있습니다.
자세한 내용은 https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp 를 참고하세요.

###``AUTH_HEADER_TYPES``
---------------------

인증이 필요한 뷰에서 허용될 인증 헤더 타입입니다. 예를 들어 ``'Bearer'`` 값은 인증이 필요한 뷰가 다음 형식의 헤더를 찾는다는 의미입니다:
``Authorization: Bearer <token>``. 이 설정은 가능한 헤더 타입의 리스트나 튜플(예: ``('Bearer', 'JWT')``)을 포함할 수도 있습니다.
이런 방식으로 리스트나 튜플이 사용되고 인증에 실패하면, 컬렉션의 첫 번째 항목이 응답의 "WWW-Authenticate" 헤더를 구성하는 데 사용됩니다.

###``AUTH_HEADER_NAME``
----------------------------

인증에 사용되는 인증 헤더의 이름입니다. 기본값은 `HTTP_AUTHORIZATION`이며, 요청의 `Authorization` 헤더를 받아들입니다.
예를 들어 요청 헤더에서 `X_Access_Token`을 사용하고 싶다면, 설정에서 `AUTH_HEADER_NAME`을 `HTTP_X_ACCESS_TOKEN`으로 지정합니다.


###``USER_ID_FIELD``
-----------------

생성된 토큰에 사용자를 식별하기 위해 포함될 사용자 모델의 데이터베이스 필드입니다.
이 설정의 값으로 초기 값이 정해진 후에는 일반적으로 변경되지 않는 필드를 지정하는 것이 권장됩니다.
예를 들어 "username"이나 "email" 필드를 지정하는 것은 좋지 않은 선택입니다,
특정 서비스에서 계정 관리가 어떻게 설계되었는지에 따라 계정의 사용자 이름이나 이메일은 변경될 수 있기 때문입니다.
이로 인해 해당 사용자 이름을 사용자 식별자로 사용하는 기존 토큰이 여전히 유효한 상태에서, 오래된 사용자 이름으로 새 계정이 생성될 수 있습니다.

###``USER_ID_CLAIM``
-----------------

생성된 토큰에 사용자 식별자를 저장하는 데 사용되는 클레임입니다. 예를 들어 값을 ```"user_id"```로 설정하면 생성된 토큰에 "user_id" 클레임이 포함되며,
이 클레임에는 사용자의 식별자가 담깁니다.

###``USER_AUTHENTICATION_RULE``
----------------------------

사용자가 인증을 허용받았는지 여부를 결정하는 데 사용되는 호출 가능 객체(callable)입니다. 이 규칙은 유효한 토큰이 처리된 후에 적용됩니다. 사용자 객체가 인수로 호출 가능 객체에 전달됩니다.
기본 규칙은 ``is_active`` 플래그가 여전히 ``True``인지 확인하는 것입니다.
호출 가능 객체는 불리언 값을 반환해야 하며, ``True``는 승인됨을, ``False``는 그렇지 않음을 의미하여 401 상태 코드가 발생합니다.

###``AUTH_TOKEN_CLASSES``
----------------------

인증을 증명하기 위해 허용되는 토큰 타입을 지정하는 클래스들의 dotted path 목록입니다. 자세한 내용은 아래의 "토큰 타입" 섹션을 참고하세요.

###``TOKEN_TYPE_CLAIM``
--------------------

토큰 타입을 저장하는 데 사용되는 클레임의 이름입니다. 자세한 내용은 아래의 "토큰 타입" 섹션을 참고하세요.

###``JTI_CLAIM``
-------------

토큰의 고유 식별자를 저장하는 데 사용되는 클레임의 이름입니다. 이 식별자는 블랙리스트 앱에서 취소된 토큰을 식별하는 데 사용됩니다.
경우에 따라 이러한 값을 저장하기 위해 기본 "jti" 클레임이 아닌 다른 클레임을 사용해야 할 수도 있습니다.

###``TOKEN_USER_CLASS``
--------------------

검증된 토큰으로 뒷받침되는 상태 없는(stateless) 사용자 객체입니다. JWTStatelessUser 인증 백엔드에서만 사용됩니다.
값은 ``"rest_framework_simplejwt.models.TokenUser"``의 서브클래스를 가리키는 dotted path이며, 이것이 기본값이기도 합니다.

###``SLIDING_TOKEN_LIFETIME``
--------------------------

sliding 토큰이 인증 증명에 유효한 기간을 지정하는 ``datetime.timedelta`` 객체입니다.
토큰 생성 시 이 ``timedelta`` 값이 현재 UTC 시간에 더해져 토큰의 기본 "exp" 클레임 값이 됩니다.
자세한 내용은 아래의 "Sliding Tokens" 섹션을 참고하세요.

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

sliding 토큰이 갱신될 수 있는 기간을 지정하는 ``datetime.timedelta`` 객체입니다.
토큰 생성 시 이 `timedelta` 값이 현재 UTC 시간에 더해져 토큰의 기본 "exp" 클레임 값이 됩니다.
자세한 내용은 아래의 "Sliding Tokens" 섹션을 참고하세요.

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

sliding 토큰의 갱신 기간 만료 시간을 저장하는 데 사용되는 클레임의 이름입니다. 자세한 내용은 아래의 "Sliding Tokens" 섹션을 참고하세요.

!!! success

    다음 장 **[토큰 클레임 커스터마이즈](customizing_token_claims.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
