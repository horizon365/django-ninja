---
comments: true
---
django-ninja-extra で `application/x-www-form-urlencoded` や `multipart/form-data` などのコンテンツタイプを含む POST リクエストの処理方法がわからない場合は、このガイドが役立ちます。
Django-Ninja 自体がそのほとんどのユースケースを [こちら](https://django-ninja.cn/tutorial/form-params/) でカバーしていますが、ここで簡単にまとめておきます。

### パラメータとしてのフォームデータ

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
ここで注意すべき点が 2 つあります：

- `ninja` モジュールから `Form` をインポートする必要があります
- パラメータのデフォルト値として `Form` を使用します


!!! info
    これについて詳しくは、[Django-Ninja フォームチュートリアル](https://django-ninja.cn/guides/input/form-params/) をご覧ください。
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
