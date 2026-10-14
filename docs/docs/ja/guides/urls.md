---
comments: true
---
# URL の逆引き

Django Ninja スキーマ（または `Router`）内の各メソッドは、逆引き URL 名を生成します。

## URL の生成方法

これらの URL はすべて名前空間（デフォルトは `"api-1.0.0"`）に含まれ、各 URL 名はそれが装飾する関数名と一致します。

たとえば:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

この暗黙的な URL 名は、各 API パスの最初のオペレーションにのみ設定されます。暗黙的な逆引き URL 名を生成したく*ない*場合は、メソッドデコレータに `url_name=""`（空文字列）を指定するだけです。

### URL 名の変更

デフォルトの URL 名を使用する代わりに、メソッドデコレータのプロパティとして明示的に指定できます。
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

これにより、この API パスの暗黙的な URL 名はオーバーライドされます。


#### デフォルトの URL 名をオーバーライドする

`get_operation_url_name` メソッドをオーバーライドすることで、暗黙的な URL 命名をオーバーライドすることもできます:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### カスタム名前空間

デフォルトの URL 名前空間は、スキーマのバージョンに `"api-"` という接頭辞を付けたものですが、NinjaAPI スキーマクラスの `urls_namespace` 属性をオーバーライドすることで、名前空間を明示的に指定できます。
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    次のセクション **[非同期サポート](async-support.md)** に進みましょう

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
