
Ninja JWT 包含一个提供令牌黑名单功能的应用程序。
要使用此应用程序，请将其包含在 `settings.py` 中的已安装应用程序列表中:

```python
# Django 项目 settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

同时，确保运行 `python manage.py migrate` 以运行该应用程序的迁移。

如果在 `INSTALLED_APPS` 中检测到黑名单应用程序，Ninja JWT 将把任何生成的刷新令牌或滑动令牌添加到未决令牌列表中。
它还将在认为任何刷新令牌或滑动令牌有效之前，检查该令牌是否未出现在令牌黑名单中。

Ninja JWT 黑名单应用程序使用两个模型：`OutstandingToken` 和 `BlacklistedToken` 来实现其未决和黑名单令牌列表。
为这两个模型都定义了模型管理员。要将令牌添加到黑名单中，在管理员中找到其相应的 `OutstandingToken` 记录，
然后再次使用管理员创建一个指向 `OutstandingToken` 记录的 `BlacklistedToken` 记录。

或者，你可以通过创建一个 `BlacklistMixin` 子类实例并调用该实例的 `blacklist` 方法来将令牌列入黑名单：

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

这将为令牌的 `jti` 声明或由 `JTI_CLAIM` 设置指定的任何声明创建唯一的未决令牌和黑名单记录。

黑名单应用程序还提供了一个管理命令 `flushexpiredtokens`，它将从未决列表和黑名单中删除任何已过期的令牌。
你应该在你的服务器或托管平台上设置一个每日运行此命令的 cron 作业。
