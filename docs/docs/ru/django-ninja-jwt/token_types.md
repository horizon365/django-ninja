

Ninja JWT предоставляет два разных типа токенов, которые можно использовать для подтверждения аутентификации.
В полезной нагрузке (payload) токена его тип можно определить по значению claim типа токена, который по умолчанию называется `token_type`.
Однако его значение может быть `access`, `sliding` или `refresh`,
но в настоящее время refresh-токены не считаются валидными токенами аутентификации. Имя claim, используемое для хранения типа, можно изменить с помощью настройки `TOKEN_TYPE_CLAIM`.

По умолчанию Ninja JWT ожидает токен `access` для подтверждения аутентификации.
Разрешённые типы токенов аутентификации определяются значением настройки `AUTH_TOKEN_CLASSES`.
Эта настройка содержит список dotted-путей, указывающих на классы токенов. По умолчанию она содержит dotted-путь `'ninja_jwt.tokens.AccessToken'`,
но может также включать dotted-путь `'ninja_jwt.tokens.SlidingToken'`.
Любой из этих dotted-путей или оба могут присутствовать в списке классов токенов аутентификации.
Если присутствуют оба, то оба типа токенов могут использоваться для подтверждения аутентификации.

Sliding Tokens
==============

Sliding-токены обеспечивают более удобный опыт для пользователей токенов, но за счёт более низкой безопасности и, при использовании приложения blacklist, более низкой производительности.
Sliding-токен — это токен, который содержит и claim срока действия (expiration), и claim срока обновления (refresh expiration). Пока временная метка в claim срока действия sliding-токена не истекла,
его можно использовать для подтверждения аутентификации. Кроме того, пока временная метка в его claim срока обновления не истекла,
его также можно отправить в refresh-представление, чтобы получить копию этого токена с обновлённым claim срока действия.

Если вы хотите использовать sliding-токены, измените настройку `AUTH_TOKEN_CLASSES` на `('ninja_jwt.tokens.SlidingToken',)`.
(В качестве альтернативы, если вы хотите разрешить оба типа токенов для аутентификации, настройка `AUTH_TOKEN_CLASSES` может включать dotted-пути, указывающие на классы токенов `AccessToken` и `SlidingToken`
в модуле `ninja_jwt.tokens`)

Кроме того, зарегистрируйте `NinjaJWTSlidingController` в `api`:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

Обратите внимание, что если вы используете приложение blacklist, Ninja JWT будет проверять все sliding-токены на соответствие blacklist при каждом аутентифицированном запросе.
Это снизит производительность аутентифицированных API-представлений.

!!! success

    Перейдите к следующей главе **[Blacklist App](blacklist_app.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
