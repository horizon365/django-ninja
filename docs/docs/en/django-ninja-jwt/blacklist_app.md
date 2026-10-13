
Ninja JWT ships with an application that provides token blacklist functionality.
To use this application, include it in the list of installed applications in `settings.py`:

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

Also, make sure to run `python manage.py migrate` to run the application's migrations.

If the blacklist application is detected in `INSTALLED_APPS`, Ninja JWT will add any generated refresh tokens or sliding tokens to the outstanding token list.
It will also check, before considering any refresh token or sliding token valid, that the token does not appear in the token blacklist.

The Ninja JWT blacklist application uses two models: `OutstandingToken` and `BlacklistedToken` to implement its outstanding and blacklist token lists.
Model admins are defined for both models. To add a token to the blacklist, find its corresponding `OutstandingToken` record in the admin,
then use the admin again to create a `BlacklistedToken` record that points to the `OutstandingToken` record.

Alternatively, you can blacklist a token by creating an instance of a `BlacklistMixin` subclass and calling the `blacklist` method on that instance:

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

This will create a unique outstanding token and blacklist record for the token's `jti` claim, or for whatever claim is specified by the `JTI_CLAIM` setting.

The blacklist application also provides a management command `flushexpiredtokens`, which will remove any expired tokens from both the outstanding list and the blacklist.
You should set up a cron job on your server or hosting platform that runs this command daily.

!!! success

    Continue to the next chapter **[Development and Contributing](development_and_contributing.md)**.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
