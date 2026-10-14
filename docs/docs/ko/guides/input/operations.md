---
comments: true
---
# HTTP 메서드

## Operation 정의

`operation`은 [HTTP 메서드](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) 중 하나입니다:

- GET (조회)
- POST (제출)
- PUT (수정)
- DELETE (삭제)
- PATCH (부분 수정)

**Django Ninja**에는 각 operation에 대한 데코레이터가 있습니다:

```python hl_lines="1 5 9 13 17"
@api.get("/path")
def get_operation(request):
    ...

@api.post("/path")
def post_operation(request):
    ...

@api.put("/path")
def put_operation(request):
    ...

@api.delete("/path")
def delete_operation(request):
    ...

@api.patch("/path")
def patch_operation(request):
    ...
```

이 데코레이터들에 전달할 수 있는 내용에 대한 정보는 [Operation 파라미터](../../reference/operations-parameters.md) 레퍼런스 문서를 참조하세요.

## 여러 메서드 처리

하나의 함수로 주어진 path에 대해 여러 메서드를 처리해야 하는 경우 `api_operation` 데코레이터를 사용할 수 있습니다:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

이 기능은 `HEAD`나 `OPTIONS`처럼 대응하는 **Django Ninja** 메서드가 없는 다른 HTTP 메서드를 구현하는 데에도 사용할 수 있습니다.

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    다음 챕터로 계속 진행하세요! **[Path 파라미터](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
