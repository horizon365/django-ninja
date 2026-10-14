---
comments: true
---
# HTTP メソッド

## オペレーションの定義

`operation`（オペレーション）は、[HTTP メソッド](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)のいずれかです:

- GET（取得）
- POST（送信）
- PUT（更新）
- DELETE（削除）
- PATCH（部分更新）

**Django Ninja** には各オペレーションに対応するデコレータが用意されています:

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

これらのデコレータに何を渡せるかについては、[オペレーションパラメータ](../../reference/operations-parameters.md)のリファレンスドキュメントを参照してください。

## 複数メソッドの処理

1 つの関数で特定のパスに対する複数のメソッドを処理する必要がある場合は、`api_operation` デコレータを使用できます:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

この機能は、**Django Ninja** の対応するメソッドが存在しない他の HTTP メソッド（`HEAD` や `OPTIONS` など）を実装するためにも使用できます。

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    次の章に進みましょう！ **[パスパラメータ](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
