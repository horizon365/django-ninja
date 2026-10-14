
Ninja JWT の一部の動作は、`settings.py` の設定変数を通じてカスタマイズできます：

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

上記は、これらの設定のデフォルト値です。

## `ACCESS_TOKEN_LIFETIME`

access トークンのライフタイムを指定する `datetime.timedelta` オブジェクトです。
トークン生成時には、この `timedelta` の値が現在の UTC 時刻に加算され、トークンのデフォルトの `exp` クレーム値が求められます。

## `REFRESH_TOKEN_LIFETIME`

refresh トークンのライフタイムを指定する `datetime.timedelta` オブジェクトです。
トークン生成時には、この `timedelta` の値が現在の UTC 時刻に加算され、トークンのデフォルトの `exp` クレーム値が求められます。

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
``True`` に設定した場合、ブラックリストアプリが使用中で、かつ ``ROTATE_REFRESH_TOKENS`` が ``True`` に設定されているときは、
``TokenRefreshView`` に送信された refresh トークンがブラックリストに追加されます。
この設定を使うには、設定ファイルの ``INSTALLED_APPS`` に ``'ninja_jwt.token_blacklist'`` を追加する必要があります。


`/blacklist_app`{.interpreted-text role="doc"} について詳しく学びましょう。

## `UPDATE_LAST_LOGIN`

`True` に設定すると、ログイン時（TokenObtainPairView）に auth_user テーブルの last_login フィールドが更新されます。

    Warning: Updating last login will greatly increase the number of database transactions.
    Abusers of the view may slow down the server, which may be a security vulnerability.
    If you really want to do this, at least throttle the endpoint with DRF.

## `ALGORITHM`

トークンの署名/検証操作を行うために PyJWT ライブラリから使用されるアルゴリズムです。
対称鍵の HMAC による署名と検証を使うには、次のアルゴリズムが利用できます： ``'HS256'``、``'HS384'``、``'HS512'``。
HMAC アルゴリズムを選択した場合、``SIGNING_KEY`` 設定が署名鍵と検証鍵の両方として使われます。
この場合、``VERIFYING_KEY`` 設定は無視されます。
非対称鍵の RSA による署名と検証を使うには、次のアルゴリズムが利用できます： ``'RS256'``、``'RS384'``、``'RS512'``。
RSA アルゴリズムを選択した場合、``SIGNING_KEY`` 設定には RSA 秘密鍵を含む文字列を設定しなければなりません。
同様に、``VERIFYING_KEY`` 設定には RSA 公開鍵を含む文字列を設定しなければなりません。

## `SIGNING_KEY`

生成されるトークンの内容に署名するために使われる署名鍵です。
HMAC 署名の場合、これは署名プロトコルが要求する以上のビット数のデータを含むランダムな文字列にする必要があります。
RSA 署名の場合、これは 2048 ビット以上の RSA 秘密鍵を含む文字列にする必要があります。
Simple JWT はデフォルトで 256 ビットの HMAC 署名を使用するため、`SIGNING_KEY` 設定のデフォルト値は Django プロジェクトの `SECRET_KEY` 設定の値になります。
これは Simple JWT が提供できる最も合理的なデフォルトですが、開発者にはこの設定を、Django プロジェクトの秘密鍵とは独立した値に変更することが推奨されます。
そうすることで、トークンの署名に使う鍵が漏洩した場合に、署名鍵をより簡単に変更できるようになります。

## `VERIFYING_KEY`

生成されるトークンの内容を検証するために使われる検証鍵です。``ALGORITHM`` 設定で HMAC アルゴリズムが指定された場合、
``VERIFYING_KEY`` 設定は無視され、代わりに ``SIGNING_KEY`` の値が使われます。
``ALGORITHM`` 設定で RSA アルゴリズムが指定された場合、``VERIFYING_KEY`` 設定には RSA 公開鍵を含む文字列を設定しなければなりません。

## `AUDIENCE`

生成されるトークンに含め、かつ/またはデコードされたトークンで検証される audience クレームです。
``None`` に設定した場合、このフィールドはトークンから除外され、検証もされません。

## `ISSUER`

生成されるトークンに含め、かつ/またはデコードされたトークンで検証される issuer クレームです。
``None`` に設定した場合、このフィールドはトークンから除外され、検証もされません。

### ``JWK_URL``
----------

JWK_URL は、トークン署名の検証に必要な公開鍵を動的に解決するために使われます。
たとえば、Auth0 を使用している場合、これを 'https://yourdomain.auth0.com/.well-known/jwks.json' に設定することがあります。
``None`` に設定した場合、このフィールドはトークンバックエンドから除外され、検証時にも使われません

### ``LEEWAY``
----------

Leeway（猶予時間）は、有効期限にある程度のマージンを与えるために使われます。秒数の整数または ``datetime.timedelta`` を指定できます。
詳しくは https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp を参照してください。

###``AUTH_HEADER_TYPES``
---------------------

認証を必要とするビューで受け付けられる認証ヘッダーのタイプです。たとえば、``'Bearer'`` という値は、認証を必要とするビューが次の形式のヘッダーを探すことを意味します：
``Authorization: Bearer <token>``。この設定には、あり得るヘッダータイプのリストやタプル（例： ``('Bearer', 'JWT')``）を指定することもできます。
このようにリストやタプルを使った場合に認証が失敗すると、コレクションの最初の要素がレスポンスの "WWW-Authenticate" ヘッダーの構築に使われます。

###``AUTH_HEADER_NAME``
----------------------------

認証に使用される認証ヘッダーの名前です。デフォルトは `HTTP_AUTHORIZATION` で、リクエストから `Authorization` ヘッダーを受け付けます。
たとえば、リクエストヘッダーで `X_Access_Token` を使いたい場合は、設定で `AUTH_HEADER_NAME` に `HTTP_X_ACCESS_TOKEN` を指定します。


###``USER_ID_FIELD``
-----------------

ユーザーを識別するために生成されるトークンに含める、ユーザーモデルのデータベースフィールドです。
この設定の値には、初期値が決まった後に通常変更されることのないフィールドを指定することが推奨されます。
たとえば、"username" や "email" フィールドを指定するのは良い選択とは言えません。
これは、アカウントの username や email は、サービスにおけるアカウント管理の設計によっては変更される可能性があるためです。
その結果、古い username で新しいアカウントが作成されても、その username をユーザー識別子として使う既存のトークンが有効なまま残る事態が起こり得ます。

###``USER_ID_CLAIM``
-----------------

生成されるトークン内でユーザー識別子を格納するために使われるクレームです。たとえば、値を ```"user_id"``` に設定すると、
生成されるトークンには "user_id" クレームが含まれ、そこにユーザーの識別子が格納されます。

###``USER_AUTHENTICATION_RULE``
----------------------------

ユーザーが認証を許可されているかどうかを判定するために使われる呼び出し可能オブジェクト（callable）です。このルールは、有効なトークンが処理された後に適用されます。ユーザーオブジェクトが引数として callable に渡されます。
デフォルトのルールは、``is_active`` フラグがまだ ``True`` であることを確認することです。
callable は真偽値を返さなければならず、``True`` は認証済みを、``False`` はそれ以外を意味し、401 ステータスコードが返されます。

###``AUTH_TOKEN_CLASSES``
----------------------

認証を証明するために許可されるトークンタイプを指定するクラスへのドット区切りパスのリストです。詳しくは後述の「Token Types」セクションを参照してください。

###``TOKEN_TYPE_CLAIM``
--------------------

トークンタイプを格納するために使われるクレームの名前です。詳しくは後述の「Token Types」セクションを参照してください。

###``JTI_CLAIM``
-------------

トークンの一意の識別子を格納するために使われるクレームの名前です。この識別子は、ブラックリストアプリで失効したトークンを識別するために使われます。
場合によっては、そのような値を格納するために、デフォルトの "jti" クレーム以外のクレームを使う必要があるかもしれません。

###``TOKEN_USER_CLASS``
--------------------

検証済みトークンによって支えられるステートレスなユーザーオブジェクトです。JWTStatelessUser 認証バックエンドでのみ使われます。
値は、``"rest_framework_simplejwt.models.TokenUser"`` のサブクラス（これがデフォルトでもあります）を指すドット区切りパスです。

###``SLIDING_TOKEN_LIFETIME``
--------------------------

sliding トークンが認証を証明するために有効である期間を指定する ``datetime.timedelta`` オブジェクトです。
トークン生成時には、この ``timedelta`` の値が現在の UTC 時刻に加算され、トークンのデフォルトの "exp" クレーム値が求められます。
詳しくは後述の「Sliding Tokens」セクションを参照してください。

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

sliding トークンがリフレッシュ可能な期間を指定する ``datetime.timedelta`` オブジェクトです。
トークン生成時には、この `timedelta` の値が現在の UTC 時刻に加算され、トークンのデフォルトの "exp" クレーム値が求められます。
詳しくは後述の「Sliding Tokens」セクションを参照してください。

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

sliding トークンのリフレッシュ期間の有効期限を格納するために使われるクレームの名前です。詳しくは後述の「Sliding Tokens」セクションを参照してください。

!!! success

    次の章 **[Token Claims のカスタマイズ](customizing_token_claims.md)** に進みましょう。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
