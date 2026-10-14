---
comments: true
---
以下は、`django-ninja-jwt` を `tusd` の HTTP Hooks と統合してユーザー認証を行う方法を紹介する、Markdown ブログに適した技術解説記事です。

---

# django-ninja-jwt を使って tusd の HTTP Hooks と連携しユーザー認証を実現する

レジュームアップロード（中断からの再開）に対応した大容量ファイルアップロードサービスを構築する場合、[`tusd`](https://github.com/tus/tusd) は非常に人気のあるサーバーサイド実装です。Django プロジェクトでは、通常 [django-ninja](https://django-ninja.dev) フレームワークと [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) を組み合わせて API 開発と認証を行います。

本記事では、**tusd の HTTP Hooks** を `django-ninja-jwt` と組み合わせて、ユーザーの識別とアップロード権限の制御を実現する方法を紹介します。

---

## 1. tusd の HTTP Hooks の紹介

`tusd` は、アップロードのライフサイクルにおける様々な段階（`pre-create`、`post-finish` など）で Hooks をトリガーすることをサポートしています。`--hooks-http` パラメータを設定すると、Hook がトリガーされたときに `tusd` が HTTP リクエストを送信するようになります。

設定コマンドの例：

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

アップロード操作が行われると、tusd は指定されたアドレスに JSON ペイロードを POST します。これにはリクエストヘッダー（`Authorization` や `Cookie` など）とアップロードのメタデータが含まれます。

---

## 2. tus-js-client で JWT リクエストヘッダーを設定する

フロントエンド（たとえば Vue/Quasar アプリケーション）で `tus-js-client` を使用する場合、リクエストヘッダーに JWT Token を添付する必要があります：

```js
import tus from 'tus-js-client'

const upload = new tus.Upload(file, {
  endpoint: 'http://localhost:1080/files/',
  metadata: {
    filename: file.name,
    filetype: file.type
  },
  headers: {
    Authorization: 'Bearer ' + localStorage.getItem('access_token') // JWT token
  },
  withCredentials: false, // Do not use cookies; use the Authorization header
  onError: (error) => console.error(error),
  onSuccess: () => console.log('Upload succeeded')
})

upload.start()
```

---

## 3. バックエンド：Django で tusd の Hook を受け取り JWT を検証する

Django プロジェクトに Hook 受信用のエンドポイントを作成します：

```python
# views.py
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json

router = Router()

@router.post("/tusd-hook")
def tusd_hook(request):
    try:
        payload = json.loads(request.body)
        headers = payload.get("HTTPRequest", {}).get("Header", {})
        auth_header = headers.get("Authorization", [""])[0]

        if auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]

            # Use django-ninja-jwt's JWTAuth to parse the token
            user = JWTAuth().authenticate(request, token)

            if user is None:
                return JsonResponse({"error": "Invalid token"}, status=401)

            # user is an authenticated Django User instance
            print("Upload user:", user.username)

            # You can perform authorization or write to the database based on user info
            return JsonResponse({"status": "ok"})

        return JsonResponse({"error": "No token"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
```

---

## 4. ルートを登録する

```python
# urls.py
from django.urls import path
from ninja import NinjaAPI
from .views import router as tusd_router

api = NinjaAPI()
api.add_router("/", tusd_router)

urlpatterns = [
    path("tusd-hook/", api.urls),
]
```

---

## 5. tusd の Hook リクエスト（POST）の例

tusd はバックエンドに次のような JSON を送信します：

```json
{
  "Protocol": "http",
  "EventName": "pre-create",
  "Upload": {
    "ID": "123456",
    "Size": 1024000,
    "MetaData": {
      "filename": "example.pdf",
      "filetype": "application/pdf"
    }
  },
  "HTTPRequest": {
    "Method": "POST",
    "URI": "/files/",
    "Header": {
      "Authorization": ["Bearer <jwt-token>"]
    }
  }
}
```

---

## 6. まとめ

上記の設定を通じて、私たちは次のことを実現しました：

1. フロントエンドがファイルアップロード時に JWT を運ぶ；
2. tusd がリクエストヘッダーを HTTP hook に渡す；
3. バックエンドが django-ninja-jwt を使ってトークンを検証しユーザーを取得する；
4. アップロード権限の付与やファイル所有者の紐付けといった高度な機能を実装できる。

---

ファイルのデータベース記録、権限チェック、ユーザーのクォータ制限などの機能を追加したい場合は、この基盤の上にロジックを拡張することができます。

tus はまさに新時代のアップロードソリューションです。レジュームアップロードは本当に気持ちいいものです。最後に動画でのデモを添付します。
tus と django-ninja-jwt を組み合わせたレジュームアップロードのデモです。

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
