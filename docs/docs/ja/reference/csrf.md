---
comments: true
---
# CSRF（クロスサイトリクエストフォージェリ）

## クロスサイトリクエストフォージェリとは？
> [クロスサイトリクエストフォージェリ](https://en.wikipedia.org/wiki/Cross-site_request_forgery) とは、悪意のある Web サイトが、（その悪意のあるサイトをブラウザーで訪れた）ログイン済みユーザーの資格情報を使って、あなたの Web サイト（またはこのドキュメントで扱う範囲外の場所）に対して何らかの操作を実行させるリンク、フォームのボタン、あるいは JavaScript を仕込むことで発生します。


## Django Ninja でクロスサイトリクエストフォージェリから防御する方法
### リクエストに自動的に組み込まれない認証方法を使う
クロスサイトリクエストフォージェリ攻撃は、[Cookie](https://en.wikipedia.org/wiki/HTTP_cookie) や [Basic 認証](https://en.wikipedia.org/wiki/Basic_access_authentication) のように、他の Web サイトから発信されるリクエストに自動的に含まれる認証方法に依存しています。
`Authorization: Bearer` のように自動的に組み込まれない認証方法を使うことで、この攻撃を緩和できます。


### Django の組み込みクロスサイトリクエストフォージェリ保護を使う
Cookie を利用する Django のデフォルト認証を使っている場合は、デフォルトの [Django クロスサイトリクエストフォージェリ保護](https://docs.djangoproject.com/en/4.2/ref/csrf/) も使う必要があります。


デフォルトでは、**Django Ninja** はすべての操作に対してクロスサイトリクエストフォージェリ保護が **OFF** になっています。
有効にするには、NinjaAPI クラスの `csrf` 引数を使います：

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">警告</span>: Cookie ベースの認証を、クロスサイトリクエストフォージェリ保護を無効にしたまま使うのは安全ではありません！（例：`CookieKey` や `django_auth`）


**Django Ninja** は、Cookie ベースの認証に対してクロスサイトリクエストフォージェリ保護を自動的に有効にします。


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


または django-auth ベースの場合（Cookie ベースの認証を継承しています）：

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Django の `ensure_csrf_cookie` デコレーター
保護されていないルートに対して Django の [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) デコレーターを使うと、そのルートがクロスサイトリクエストフォージェリトークン用の `Set-Cookie` ヘッダーを含むようになります。注意点：
- ルートのデコレーターは [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) デコレーターより先に（つまり上に）実行される必要があります。
- そのルートには `csrf_exempt` を指定する必要があります。
- `ensure_csrf_cookie` デコレーターは Django の `HttpResponse` に対してのみ機能し、多くの Django Ninja デコレーターのように辞書に対しては機能しません。
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
このルートへのリクエストは、適切な `Set-Cookie` ヘッダーを含む Django からのレスポンスを引き起こします。


#### フロントエンドコード
[How to use Django's CSRF protection](https://docs.djangoproject.com/en/4.2/howto/csrf/) の [Using CSRF protection with AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) と [Setting the token on the AJAX request](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) のセクションを参照して、フロントエンドコードでクロスサイトリクエストフォージェリ保護トークンを扱う方法を学べます。


## CORS について
フロントエンドと API を別のサイトに設置したい場合もあるでしょう（その場合は [django-cors-headers](https://github.com/adamchainz/django-cors-headers) を参照してください）。
クロスサイトリクエストフォージェリとは直接関係ありませんが、フロントエンドが使うサイトとは別のサイトにクロスサイトリクエストフォージェリ用の Cookie を定義する場合、[同一オリジンポリシー](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) ではデフォルトで許可されていないため、CORS（Cross-Origin Resource Sharing）が役立ちます。
その場合は [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme) を参照してください。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
