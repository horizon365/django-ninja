---
comments: true
---
# URL 역방향 조회

Django Ninja 스키마(또는 `Router`)의 각 메서드는 역방향 URL 이름을 생성합니다.

## URL이 생성되는 방식

이 URL들은 모두 하나의 네임스페이스에 포함되며, 네임스페이스의 기본값은 `"api-1.0.0"`이고 각 URL 이름은 데코레이션하는 함수와 일치합니다.

예를 들어:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

이 암시적 URL 이름은 각 API path의 첫 번째 operation에 대해서만 설정됩니다. 암시적 역방향 URL 이름이 생성되지 *않게* 하려면, 메서드 데코레이터에 `url_name=""`(빈 문자열)을 지정하기만 하면 됩니다.

### URL 이름 변경

기본 URL 이름을 사용하는 대신, 메서드 데코레이터의 속성으로 명시적으로 지정할 수 있습니다.
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

이렇게 하면 이 API path에 대한 암시적 URL 이름이 오버라이드됩니다.


#### 기본 URL 이름 오버라이드

`get_operation_url_name` 메서드를 오버라이드하여 암시적 URL 네이밍을 오버라이드할 수도 있습니다:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### 커스텀 네임스페이스

기본 URL 네임스페이스는 스키마의 버전에 `"api-"` 접두사를 붙여 구성되지만, NinjaAPI 스키마 클래스의 `urls_namespace` 속성을 오버라이드하여 네임스페이스를 명시적으로 지정할 수 있습니다.
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    다음 섹션 **[비동기 지원](async-support.md)**으로 계속 진행하세요.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
