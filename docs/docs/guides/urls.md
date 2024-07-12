---
comments: true
---
# URL 的反向解析

在 Django Ninja 模式 (or `Router`) 中的每个方法都会生成一个反向 URL 名称。

## URL 如何生成

这些 URL 都包含在一个命名空间中，默认是 `"api-1.0.0"`并且每个 URL 名称与它所装饰的函数相匹配。

例如:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

这种隐式的 URL 名称只会为每个 API 路径的第一个操作设置。如果你 *不* 希望生成任何隐式的反向 URL 名称，只需在方法装饰器上明确指定 `url_name=""` (一个空字符串)。

### 更改 URL 名称

你可以不使用默认的 URL 名称，而是明确地将其作为方法装饰器上的属性指定。
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

这将覆盖此 API 路径的任何隐式 URL 名称。


#### 覆盖默认 URL 名称

你也可以通过覆盖 `get_operation_url_name` 方法来覆盖隐式的 URL 命名：

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### 自定义命名空间

默认的 URL 命名空间是通过在模式的版本前加上 `"api-"` 构建的，然而你可以通过覆盖 NinjaAPI 模式类的 `urls_namespace` 属性来明确指定命名空间。
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
