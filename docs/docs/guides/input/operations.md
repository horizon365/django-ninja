# HTTP 方法

## 定义操作

一个 `操作` 可以是 [HTTP 方法](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)之一:

- GET（获取）
- POST（提交）
- PUT（更新）
- DELETE（删除）
- PATCH（补丁）

**Django Ninja** 为每个操作都有一个装饰器：

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

有关可以传递给这些装饰器中的任何一个的信息，请参阅 [操作参数](../../reference/operations-parameters.md) 参考文档。

## 处理多种方法

如果你需要用一个函数处理给定路径的多种方法，你可以使用 `api_operation` 装饰器：

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

这个功能也可以用于实现其他没有相应 **Django Ninja** 方法的 HTTP 方法, 例如 `HEAD（头部）` 或 `OPTIONS（选项）`。

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```
