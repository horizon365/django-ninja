
Ninja JWT は、認証を証明するために使用できる 2 種類の異なるトークンタイプを提供しています。
トークンのペイロードでは、そのタイプはトークンタイプクレームの値で識別できます。デフォルトでは `token_type` です。
ただし、この値は `access`、`sliding`、`refresh` のいずれかになりますが、
現在のところ refresh トークンは有効な認証トークンとして扱われません。タイプの保存に使用されるクレーム名は、`TOKEN_TYPE_CLAIM` 設定を変更することでカスタマイズできます。

デフォルトでは、Ninja JWT は `access` トークンによる認証の証明を期待します。
認証に使用できるトークンタイプは `AUTH_TOKEN_CLASSES` 設定の値によって決まります。
この設定には、トークンクラスを指すドットパスのリストが含まれます。デフォルトでは `'ninja_jwt.tokens.AccessToken'` のドットパスが含まれており、
`'ninja_jwt.tokens.SlidingToken'` のドットパスを含めることもできます。
これらのドットパスの一方または両方を認証トークンクラスのリストに含めることができます。
両方が存在する場合、両方のトークンタイプを認証の証明に使用できます。

Sliding Tokens（スライディングトークン）
==============

スライディングトークンはトークンユーザーにより便利な体験を提供しますが、その代償としてセキュリティが低下し、blacklist アプリを使用している場合はパフォーマンスも低下します。
スライディングトークンとは、有効期限（expiration）クレームとリフレッシュ有効期限（refresh expiration）クレームの両方を含むトークンです。スライディングトークンの有効期限クレーム内のタイムスタンプがまだ経過していない限り、
認証の証明に使用できます。さらに、リフレッシュ有効期限クレーム内のタイムスタンプがまだ経過していない限り、
リフレッシュビューに送信して、有効期限クレームを更新した自分自身のコピーを取得することもできます。

スライディングトークンを使用したい場合は、`AUTH_TOKEN_CLASSES` 設定を `('ninja_jwt.tokens.SlidingToken',)` に変更してください。
（または、両方のトークンタイプで認証を許可したい場合は、`AUTH_TOKEN_CLASSES` 設定に `ninja_jwt.tokens` モジュール内の `AccessToken` と `SlidingToken` トークンクラスを指すドットパスを含めることもできます）

さらに、`NinjaJWTSlidingController` を `api` に登録します。
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

blacklist アプリを使用している場合、Ninja JWT は認証付きのすべてのリクエストに対して、すべてのスライディングトークンをブラックリストと照合して検証することに注意してください。
これにより、認証が必要な API ビューのパフォーマンスが低下します。

!!! success

    次の章 **[Blacklist App](blacklist_app.md)** に進みましょう。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
