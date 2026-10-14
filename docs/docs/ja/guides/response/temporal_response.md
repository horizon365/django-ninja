---
comments: true
---
# レスポンスの調整

レスポンスが返される直前にレスポンスを変更したい場合があります。たとえばヘッダーを追加したり Cookie を変更したりする場合です。

これを行うには、`HttpResponse` 型の関数引数を宣言するだけです:

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## テンポラリレスポンスオブジェクト

このレスポンスオブジェクトは、エラーレスポンスを含む Django Ninja が構築するすべてのレスポンスの基底として使用されます。
オペレーションが Django の `HttpResponse` オブジェクトを直接返した場合、このオブジェクトは使用*されません*。

当然ながら、このレスポンスオブジェクトにはまだコンテンツは含まれていませんが、`content_type` は設定されています（変更したいとは思わないでしょうが）。

`status_code` は戻り値に基づいてオーバーライドされます（デフォルトは 200、2 要素のタプルが返された場合はそのステータスコード）。


## 基底レスポンスオブジェクトの変更

このテンポラリレスポンスオブジェクトは、`NinjaAPI.create_temporal_response` メソッドをオーバーライドすることで変更できます。

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    次の章に進みましょう！ **[Django モデルからのスキーマ生成](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
