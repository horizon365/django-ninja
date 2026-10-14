
Ninja JWT는 인증을 증명하는 데 사용할 수 있는 두 가지 토큰 타입을 제공합니다.
토큰의 페이로드에서는 토큰 타입 클레임(기본값은 `token_type`)의 값으로 토큰 타입을 식별할 수 있습니다.
이 값은 `access`, `sliding` 또는 `refresh`가 될 수 있지만,
현재 refresh 토큰은 유효한 인증 토큰으로 간주되지 않습니다. 타입을 저장하는 데 사용되는 클레임 이름은 `TOKEN_TYPE_CLAIM` 설정을 변경하여 커스터마이즈할 수 있습니다.

기본적으로 Ninja JWT는 `access` 토큰으로 인증을 증명하도록 기대합니다.
허용되는 인증 토큰 타입은 `AUTH_TOKEN_CLASSES` 설정 값에 따라 결정됩니다.
이 설정은 토큰 클래스를 가리키는 dotted path 목록을 포함하며, 기본적으로 `'ninja_jwt.tokens.AccessToken'` dotted path를 포함하지만,
`'ninja_jwt.tokens.SlidingToken'` dotted path도 포함할 수 있습니다.
이 두 dotted path 중 하나 또는 둘 다 인증 토큰 클래스 목록에 나타날 수 있습니다.
둘 다 존재하는 경우 두 토큰 타입 모두 인증 증명에 사용할 수 있습니다.

Sliding 토큰
==============

Sliding 토큰은 토큰 사용자에게 더 편리한 경험을 제공하지만, 그 대가로 낮은 보안성과, blacklist 앱을 사용하는 경우 낮은 성능을 감수해야 합니다.
Sliding 토큰은 만료(expiration) 클레임과 refresh 만료 클레임을 모두 포함하는 토큰입니다. sliding 토큰의 만료 클레임에 담긴 타임스탬프가 아직 지나지 않았다면,
이를 사용해 인증을 증명할 수 있습니다. 또한 refresh 만료 클레임의 타임스탬프가 아직 지나지 않았다면,
이 토큰을 refresh 뷰에 제출하여 만료 클레임이 갱신된 자기 자신의 복사본을 얻을 수도 있습니다.

Sliding 토큰을 사용하려면 `AUTH_TOKEN_CLASSES` 설정을 `('ninja_jwt.tokens.SlidingToken',)`으로 변경하세요.
(또는 두 토큰 타입을 모두 인증에 허용하고 싶다면, `AUTH_TOKEN_CLASSES` 설정에 `ninja_jwt.tokens` 모듈의 `AccessToken`과 `SlidingToken` 토큰 클래스를 가리키는 dotted path를 포함시킬 수 있습니다)

추가로 `NinjaJWTSlidingController`를 `api`에 등록하세요:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

blacklist 앱을 사용 중이라면, Ninja JWT는 인증이 필요한 모든 요청마다 모든 sliding 토큰을 blacklist와 대조하여 검증한다는 점에 유의하세요.
이는 인증된 API 뷰의 성능을 저하시킬 수 있습니다.

!!! success

    다음 챕터 **[Blacklist App](blacklist_app.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
