
Some of Ninja JWT's behavior can be customized via settings variables in `settings.py`:

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

Above, the default values for these settings are shown.

## `ACCESS_TOKEN_LIFETIME`

A `datetime.timedelta` object that specifies the lifetime of access tokens.
During token generation, this `timedelta` value is added to the current UTC time to obtain the default `exp` claim value of the token.

## `REFRESH_TOKEN_LIFETIME`

A `datetime.timedelta` object that specifies the lifetime of refresh tokens.
During token generation, this `timedelta` value is added to the current UTC time to obtain the default `exp` claim value of the token.

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
When set to ``True``, if the blacklist app is in use and ``ROTATE_REFRESH_TOKENS`` is set to ``True``,
refresh tokens submitted to ``TokenRefreshView`` will be added to the blacklist.
You need to add ``'ninja_jwt.token_blacklist'`` to your ``INSTALLED_APPS`` in your settings file to use this setting.


Learn more about `/blacklist_app`{.interpreted-text role="doc"}.

## `UPDATE_LAST_LOGIN`

When set to `True`, the last_login field in the auth_user table is updated upon login (TokenObtainPairView).

    Warning: Updating last login will greatly increase the number of database transactions.
    Abusers of the view may slow down the server, which may be a security vulnerability.
    If you really want to do this, at least throttle the endpoint with DRF.

## `ALGORITHM`

The algorithm used from the PyJWT library to perform signing/verification operations on tokens.
To use symmetric HMAC signing and verification, you can use the following algorithms: ``'HS256'``, ``'HS384'``,``'HS512'``.
When selecting an HMAC algorithm, the ``SIGNING_KEY`` setting will be used as both the signing key and the verification key.
In this case, the ``VERIFYING_KEY`` setting is ignored.
To use asymmetric RSA signing and verification, you can use the following algorithms: ``'RS256'``, ``'RS384'``, ``'RS512'``.
When selecting an RSA algorithm, the ``SIGNING_KEY`` setting must be set to a string containing an RSA private key.
Likewise, the ``VERIFYING_KEY`` setting must be set to a string containing an RSA public key.

## `SIGNING_KEY`

The signing key used to sign the content of generated tokens.
For HMAC signing, this should be a random string with at least as many bits of data as required by the signing protocol.
For RSA signing, this should be a string containing a 2048-bit or longer RSA private key.
Since Simple JWT uses 256-bit HMAC signing by default, the `SIGNING_KEY` setting defaults to the value of your Django project's `SECRET_KEY` setting.
Although this is the most reasonable default that Simple JWT can provide, it is recommended that developers change this setting to a value independent of the Django project's secret key.
This will make it easier to change the signing key in the event that the signing key used for tokens is compromised.

## `VERIFYING_KEY`

The verifying key used to verify the content of generated tokens. If the ``ALGORITHM`` setting specifies an HMAC algorithm,
the ``VERIFYING_KEY`` setting is ignored and the value of ``SIGNING_KEY`` is used instead.
If the ``ALGORITHM`` setting specifies an RSA algorithm, the ``VERIFYING_KEY`` setting must be set to a string containing an RSA public key.

## `AUDIENCE`

The audience claim to include in generated tokens and/or to verify in decoded tokens.
When set to ``None``, this field is excluded from the token and not verified.

## `ISSUER`

The issuer claim to include in generated tokens and/or to verify in decoded tokens.
When set to ``None``, this field is excluded from the token and not verified.

### ``JWK_URL``
----------

The JWK_URL is used to dynamically resolve the public key needed to verify token signatures.
For example, when using Auth0, you might set this to 'https://yourdomain.auth0.com/.well-known/jwks.json'.
When set to ``None``, this field is excluded from the token backend and not used during verification

### ``LEEWAY``
----------

Leeway is used to give some margin to the expiration time. This can be an integer of seconds or a ``datetime.timedelta``.
Please refer to https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp for more information.

###``AUTH_HEADER_TYPES``
---------------------

The authorization header type(s) that will be accepted for views that require authentication. For example, a value of ``'Bearer'`` means that views requiring authentication will look for a header with the following format:
``Authorization: Bearer <token>``. This setting can also contain a list or tuple of possible header types (e.g. ``('Bearer', 'JWT')``).
If a list or tuple is used in this way, and authentication fails, the first item in the collection will be used to construct the "WWW-Authenticate" header in the response.

###``AUTH_HEADER_NAME``
----------------------------

The name of the authorization header used for authentication. The default is `HTTP_AUTHORIZATION`, which will accept the `Authorization` header from requests.
For example, if you want to use `X_Access_Token` in your request headers, specify `AUTH_HEADER_NAME` as `HTTP_X_ACCESS_TOKEN` in your settings.


###``USER_ID_FIELD``
-----------------

The database field in the user model that will be included in generated tokens to identify the user.
It is recommended that the value of this setting specify a field that typically does not change once its initial value is chosen.
For example, specifying a "username" or "email" field would be a poor choice,
since a account's username or email may change depending on how account management is designed in a given service.
This could allow a new account to be created with an old username, while existing tokens that use that username as the user identifier remain valid.

###``USER_ID_CLAIM``
-----------------

The claim used to store the user identifier in generated tokens. For example, setting the value to ```"user_id"``` means that the generated token contains a "user_id" claim,
which contains the user's identifier.

###``USER_AUTHENTICATION_RULE``
----------------------------

A callable used to determine whether the user is allowed to authenticate. This rule is applied after a valid token has been processed. The user object is passed as an argument to the callable.
The default rule is to check that the ``is_active`` flag is still ``True``.
The callable must return a boolean value, ``True`` meaning authorized, ``False`` otherwise resulting in a 401 status code.

###``AUTH_TOKEN_CLASSES``
----------------------

A list of dotted paths pointing to classes that specify the allowed token types for proving authentication. More information in the "Token Types" section below.

###``TOKEN_TYPE_CLAIM``
--------------------

The name of the claim used to store the token type. More information in the "Token Types" section below.

###``JTI_CLAIM``
-------------

The name of the claim used to store the token's unique identifier. This identifier is used to identify revoked tokens in the blacklist app.
In some cases, it may be necessary to use a claim other than the default "jti" claim to store such a value.

###``TOKEN_USER_CLASS``
--------------------

A stateless user object backed by a verified token. Only used by the JWTStatelessUser authentication backend.
The value is a dotted path pointing to your subclass of ``"rest_framework_simplejwt.models.TokenUser"``, which is also the default.

###``SLIDING_TOKEN_LIFETIME``
--------------------------

A ``datetime.timedelta`` object that specifies how long a sliding token is valid for proving authentication.
During token generation, this ``timedelta`` value is added to the current UTC time to obtain the default "exp" claim value of the token.
More information in the "Sliding Tokens" section below.

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

A ``datetime.timedelta`` object that specifies how long a sliding token is valid to be refreshed.
During token generation, this `timedelta` value is added to the current UTC time to obtain the default "exp" claim value of the token.
More information in the "Sliding Tokens" section below.

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

The name of the claim used to store the expiration time of a sliding token's refresh period. More information in the "Sliding Tokens" section below.

!!! success

    Continue to the next chapter **[Customizing Token Claims](customizing_token_claims.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
