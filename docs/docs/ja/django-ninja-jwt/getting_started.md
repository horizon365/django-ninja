
#### 要件
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

これらは公式にサポートされている Python とパッケージのバージョンです。他のバージョンでも動作する場合があります。tox の設定を自由に変更して、何が可能か試してみてください。

## インストール

Ninja JWT は pip でインストールできます：

    pip install django-ninja-jwt

さらに、`NinjaJWTDefaultController` コントローラを Django-Ninja の API に登録する必要があります。

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` には `obtain_token`、`refresh_token`、`verify_token` という 3 つのルートが用意されています。
これは 2 つのサブクラス、`TokenVerificationController` と `TokenObtainPairController` を組み合わせたものです。
これらのルートをカスタマイズしたい場合は、これらのコントローラを継承して実装を変更できます。

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

ローカライズ/翻訳を使いたい場合は、`ninja_jwt` を `INSTALLED_APPS` に追加するだけです。

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## 使い方

Ninja JWT が正しく動作していることを確認するには、curl でいくつかのテストリクエストを送信できます：

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

返された access トークンを使って、保護されたビューに対する認証を証明できます：

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

この短命の access トークンが期限切れになったら、より長命の refresh トークンを使って新しい access トークンを取得できます：

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

暗号ライブラリの依存関係（任意）
-------------------------------------

特定のデジタル署名アルゴリズム（RSA や ECDSA など。その他のアルゴリズムは PyJWT を参照）を使ってトークンのエンコードやデコードを行う予定がある場合は、
cryptography_ ライブラリをインストールする必要があります。これは明示的にインストールするか、`django-ninja-jwt` の requirements の必須項目としてインストールできます：

    pip install django-ninja-jwt[crypto]

`Ninja JWT` プロジェクトの requirements ファイルを使う場合は、`django-ninja-jwt[crypto]` 形式が推奨されます。
独立した `cryptography` の require 行は、後で未使用の依存関係と誤認されて削除される可能性があるためです。
[cryptography](https://cryptography.io)

!!! success

    次の章 **[ルート認証](auth_integration.md)** に進みましょう。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
