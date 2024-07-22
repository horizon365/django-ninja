
Ninja JWT 的一些行为可以通过在 `settings.py` 中的设置变量来进行自定义:

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

以上，展示了这些设置的默认值。

## `ACCESS_TOKEN_LIFETIME`（访问令牌有效期）

一个 `datetime.timedelta` 对象，它指定访问令牌的有效时长。
在令牌生成期间，这个 `timedelta` 值会被添加到当前的 UTC 时间，以获得令牌默认的 `exp` 声明值。

## `REFRESH_TOKEN_LIFETIME`（刷新令牌有效期）

一个 `datetime.timedelta` 对象，它指定刷新令牌的有效时长。
在令牌生成期间，这个 `timedelta` 值会被添加到当前的 UTC 时间，以获得令牌默认的 `exp` 声明值。

### ``BLACKLIST_AFTER_ROTATION``（旋转后列入黑名单）
----------------------------
当设置为 ``True`` 时，如果黑名单应用程序在使用中且 ``ROTATE_REFRESH_TOKENS`` 设置为 ``True``，
提交给 ``TokenRefreshView`` 的刷新令牌将被添加到黑名单中。
你需要在设置文件中将 ``'ninja_jwt.token_blacklist'``, 添加到你的 ``INSTALLED_APPS`` 中才能使用此设置。


了解更多关于 `/blacklist_app`{.interpreted-text role="doc"} 的信息。

## `UPDATE_LAST_LOGIN`（更新最后登录）

当设置为 `True` 时，在登录（TokenObtainPairView）时会更新 auth_user 表中的 last_login 字段。

    警告：更新最后登录将极大地增加数据库事务的数量。
    滥用视图的人可能会减慢服务器速度，这可能是一个安全漏洞。
    如果你确实想要这样做，至少要用 DRF 限制端点。

## `ALGORITHM`（算法）

将从 PyJWT 库中用于对令牌执行签名/验证操作的算法。
要使用对称 HMAC 签名和验证，可以使用以下算法: ``'HS256'``, ``'HS384'``,``'HS512'``。
当选择 HMAC 算法时，``SIGNING_KEY`` 设置将同时用作签名密钥和验证密钥。
在这种情况下，``VERIFYING_KEY`` 设置将被忽略。
要使用非对称 RSA 签名和验证，可以使用以下算法：``'RS256'``、``'RS384'``、``'RS512'``。
当选择 RSA 算法时，``SIGNING_KEY`` 设置必须设置为包含 RSA 私钥的字符串。
同样，``VERIFYING_KEY`` 设置必须设置为包含 RSA 公钥的字符串。

## `SIGNING_KEY`（签名密钥）

用于对生成令牌的内容进行签名的签名密钥。
对于 HMAC 签名，这应该是一个具有至少与签名协议所需数据位数相同的随机字符串。
对于 RSA 签名，这应该是一个包含 2048 位或更长 RSA 私钥的字符串。
由于 Simple JWT 默认使用 256 位 HMAC 签名，`SIGNING_KEY` 设置默认为您的 Django 项目的 `SECRET_KEY` 设置的值。
尽管这是 Simple JWT 可以提供的最合理的默认值，但建议开发人员将此设置更改为独立于 Django 项目秘密密钥的值。
这将在令牌使用的签名密钥受到损害的情况下更容易更改签名密钥。

## `VERIFYING_KEY`（验证密钥）

用于验证生成令牌内容的验证密钥。如果 ``ALGORITHM`` 设置指定了 HMAC 算法，
则 ``VERIFYING_KEY`` 设置将被忽略，而使用 ``SIGNING_KEY`` 的值。
如果 ``ALGORITHM`` 设置指定了 RSA 算法，则 ``VERIFYING_KEY`` 设置必须设置为包含 RSA 公钥的字符串。

## `AUDIENCE`（受众）

要包含在生成令牌中和/或在解码令牌中验证的受众声明。
当设置为 ``None`` 时，此字段将从令牌中排除且不进行验证。

## `ISSUER`（发行人）

要包含在生成令牌中和/或在解码令牌中验证的发行人声明。
当设置为 ``None`` 时，此字段将从令牌中排除且不进行验证。

### ``JWK_URL``（JWK 网址）
----------

JWK_URL 用于动态解析验证令牌签名所需的公钥。
例如，使用 Auth0 时，您可能将其设置为 'https://yourdomain.auth0.com/.well-known/jwks.json' 。
当设置为 ``None`` 时，此字段将从令牌后端排除且在验证期间不使用

### ``LEEWAY``（宽限期）
----------

宽限期用于给到期时间一些余量。这可以是秒的整数或 ``datetime.timedelta``。
请参考 https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp 以获取更多信息。

###``AUTH_HEADER_TYPES`` (认证头类型)
---------------------

将被接受用于需要认证的视图的授权头类型。例如，值为 ``'Bearer'`` 意味着需要认证的视图将寻找具有以下格式的头：
``Authorization: Bearer <token>``。 此设置也可以包含可能的头类型的列表或元组（例如 ``('Bearer', 'JWT')``)。
如果以这种方式使用列表或元组，且认证失败，集合中的第一项将用于在响应中构建“WWW-Authenticate”头。

###``AUTH_HEADER_NAME``(认证头名称)
----------------------------

用于认证的授权头名称。默认是 `HTTP_AUTHORIZATION`，它将接受请求中的 `Authorization` 头。
例如，如果您想在您的请求头中使用 `X_Access_Token`，请在您的设置中指定 `AUTH_HEADER_NAME` 为 `HTTP_X_ACCESS_TOKEN`。


###``USER_ID_FIELD``
-----------------

用户模型中的数据库字段，将包含在生成的令牌中以识别用户。
建议此设置的值指定一个通常一旦其初始值被选择就不会改变的字段。
例如，指定一个“username”或“email”字段将是一个糟糕的选择，
因为一个账户的用户名或电子邮件可能根据给定服务中的账户管理如何设计而改变。
这可能允许使用旧用户名创建一个新账户，而使用该用户名作为用户标识符的现有令牌仍然有效。

###``USER_ID_CLAIM``
-----------------

在生成的令牌中用于存储用户标识符的声明。例如，设置值为 ```“user_id”`` 意味着生成的令牌包含一个“user_id”声明，
其中包含用户的标识符。

###``USER_AUTHENTICATION_RULE``
----------------------------

用于确定用户是否被允许认证的可调用对象。此规则在有效令牌被处理后应用。用户对象作为参数传递给可调用对象。
默认规则是检查 ``is_active`` 标志仍然是``True``。
可调用对象必须返回一个布尔值，``True``表示授权，``False``否则导致 401 状态码。

###``AUTH_TOKEN_CLASSES``
----------------------

一个点路径列表，指向指定允许用于证明认证的令牌类型的类。更多信息在下面的“令牌类型”部分。

###``TOKEN_TYPE_CLAIM``
--------------------

用于存储令牌类型的声明名称。更多信息在下面的“令牌类型”部分。

###``JTI_CLAIM``
-------------

用于存储令牌唯一标识符的声明名称。这个标识符用于在黑名单应用中识别已撤销的令牌。
在某些情况下，可能有必要使用除默认“jti”声明之外的另一个声明来存储这样的值。

###``TOKEN_USER_CLASS``
--------------------

一个由已验证令牌支持的无状态用户对象。仅用于 JWTStatelessUser 认证后端。
值是指向你对 ``“rest_framework_simplejwt.models.TokenUser”`` 的子类的点路径，这也是默认值。

###``SLIDING_TOKEN_LIFETIME``
--------------------------

一个 ``datetime.timedelta`` 对象，它指定滑动令牌在多长时间内有效以证明认证。
在令牌生成期间，这个 ``timedelta`` 值会添加到当前 UTC 时间以获得令牌默认的“exp”声明值。
更多信息在下面的“滑动令牌”部分。

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

一个 ``datetime.timedelta`` 对象，它指定滑动令牌在多长时间内有效可被刷新。
在令牌生成期间，这个 `timedelta` 值会添加到当前 UTC 时间以获得令牌默认的“exp”声明值。
更多信息在下面的“滑动令牌”部分。

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

用于存储滑动令牌刷新周期的到期时间的声明名称。更多信息在下面的“滑动令牌”部分。

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
