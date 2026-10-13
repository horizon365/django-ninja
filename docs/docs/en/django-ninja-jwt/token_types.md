
Ninja JWT provides two different token types that can be used to prove authentication.
In a token's payload, its type can be identified by the value of its token type claim, which by default is `token_type`.
However, this may have a value of `access`, `sliding`, or `refresh`,
but currently refresh tokens are not considered valid authentication tokens. The claim name used to store the type can be customized by changing the `TOKEN_TYPE_CLAIM` setting.

By default, Ninja JWT expects an `access` token to prove authentication.
The allowed authentication token types are determined by the value of the `AUTH_TOKEN_CLASSES` setting.
This setting contains a list of dotted paths pointing to token classes. It defaults to containing the `'ninja_jwt.tokens.AccessToken'` dotted path,
but may also include the `'ninja_jwt.tokens.SlidingToken'` dotted path.
Either or both of these dotted paths may appear in the authentication token classes list.
If both are present, then both token types can be used to prove authentication.

Sliding Tokens
==============

Sliding tokens provide a more convenient experience for token users, but trade off lower security and, when the blacklist app is in use, lower performance.
A sliding token is a token that contains both an expiration claim and a refresh expiration claim. As long as the timestamp in the sliding token's expiration claim has not yet passed,
it can be used to prove authentication. In addition, as long as the timestamp in its refresh expiration claim has not yet passed,
it can also be submitted to the refresh view to obtain a copy of itself with an updated expiration claim.

If you wish to use sliding tokens, change the `AUTH_TOKEN_CLASSES` setting to `('ninja_jwt.tokens.SlidingToken',)`.
(Alternatively, if you want to allow both token types for authentication, the `AUTH_TOKEN_CLASSES` setting may include dotted paths pointing to the `AccessToken` and `SlidingToken` token classes
in the `ninja_jwt.tokens` module)

In addition, register `NinjaJWTSlidingController` with the `api`:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

Note that if you are using the blacklist app, Ninja JWT will validate all sliding tokens against the blacklist for every authenticated request.
This will degrade the performance of authenticated API views.

!!! success

    Continue to the next chapter **[Blacklist App](blacklist_app.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
