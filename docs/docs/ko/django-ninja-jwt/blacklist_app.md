
Ninja JWT는 토큰 블랙리스트 기능을 제공하는 애플리케이션과 함께 제공됩니다.
이 애플리케이션을 사용하려면 `settings.py`의 설치된 애플리케이션 목록에 포함시키세요:

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

또한 애플리케이션의 마이그레이션을 실행하도록 `python manage.py migrate`를 실행해야 합니다.

`INSTALLED_APPS`에서 블랙리스트 애플리케이션이 감지되면, Ninja JWT는 생성된 모든 refresh 토큰 또는 sliding 토큰을 outstanding 토큰 목록에 추가합니다.
또한 refresh 토큰이나 sliding 토큰을 유효한 것으로 간주하기 전에, 해당 토큰이 토큰 블랙리스트에 없는지 확인합니다.

Ninja JWT 블랙리스트 애플리케이션은 `OutstandingToken`과 `BlacklistedToken` 두 모델을 사용하여 outstanding 및 블랙리스트 토큰 목록을 구현합니다.
두 모델 모두에 대해 모델 어드민이 정의되어 있습니다. 토큰을 블랙리스트에 추가하려면 어드민에서 해당 토큰의 `OutstandingToken` 레코드를 찾은 다음,
다시 어드민을 사용하여 해당 `OutstandingToken` 레코드를 가리키는 `BlacklistedToken` 레코드를 생성합니다.

또는 `BlacklistMixin` 서브클래스의 인스턴스를 생성하고 해당 인스턴스에서 `blacklist` 메서드를 호출하여 토큰을 블랙리스트에 추가할 수 있습니다:

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

이렇게 하면 토큰의 `jti` 클레임(또는 `JTI_CLAIM` 설정으로 지정된 클레임)에 대해 고유한 outstanding 토큰과 블랙리스트 레코드가 생성됩니다.

블랙리스트 애플리케이션은 또한 관리 명령 `flushexpiredtokens`를 제공하며, 이는 outstanding 목록과 블랙리스트 모두에서 만료된 토큰을 제거합니다.
서버나 호스팅 플랫폼에서 이 명령을 매일 실행하는 cron 작업을 설정해야 합니다.

!!! success

    다음 장 **[개발 및 기여](development_and_contributing.md)**으로 계속 진행하세요.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
