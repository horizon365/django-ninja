
Ninja JWT には、トークンのブラックリスト機能を提供するアプリケーションが同梱されています。
このアプリケーションを使うには、`settings.py` のインストール済みアプリケーションのリストに追加してください：

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

また、アプリケーションのマイグレーションを実行するために `python manage.py migrate` を実行することを忘れないでください。

`INSTALLED_APPS` でブラックリストアプリケーションが検出されると、Ninja JWT は生成されたすべての refresh トークンや sliding トークンを outstanding トークンリストに追加します。
さらに、refresh トークンや sliding トークンを有効と判定する前に、そのトークンがトークンブラックリストに登録されていないことを確認します。

Ninja JWT のブラックリストアプリケーションは、outstanding トークンリストとブラックリストトークンリストを実装するために、`OutstandingToken` と `BlacklistedToken` という 2 つのモデルを使用します。
両方のモデルにはモデルアドミンが定義されています。トークンをブラックリストに追加するには、アドミンで対応する `OutstandingToken` レコードを見つけ、
次に再度アドミンを使って、その `OutstandingToken` レコードを指す `BlacklistedToken` レコードを作成します。

あるいは、`BlacklistMixin` のサブクラスのインスタンスを作成し、そのインスタンスの `blacklist` メソッドを呼び出すことでもトークンをブラックリストに追加できます：

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

これにより、トークンの `jti` クレーム（または `JTI_CLAIM` 設定で指定されたクレーム）に対して、一意の outstanding トークンとブラックリストレコードが作成されます。

ブラックリストアプリケーションは、管理コマンド `flushexpiredtokens` も提供しており、期限切れのトークンを outstanding リストとブラックリストの両方から削除します。
このコマンドを毎日実行する cron ジョブを、サーバーやホスティングプラットフォームに設定しておくとよいでしょう。

!!! success

    次の章 **[開発とコントリビューション](development_and_contributing.md)** に進みましょう。


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
