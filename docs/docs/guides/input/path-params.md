---
comments: true
---
# 路径参数
您可以使用与 Python 格式化字符串相同的语法 (幸运的是，这也与 <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">OpenAPI 路径参数</a>匹配)来声明路径“参数”：

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

路径参数 `item_id` 的值将作为参数 `item_id` 传递给您的函数。

因此，如果您运行此示例并转到 <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a>, 您将看到此响应：

```JSON
{"item_id":"foo"}
```


### 带类型的路径参数
您可以在函数中使用标准 Python 类型注解来声明路径参数的类型：

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

在这种情况下，`item_id` 被声明为一个 **`int`**。这将为您提供编辑器和代码检查器对错误检查、代码补全等的支持。

如果您在浏览器中使用 <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a>运行此代码，您将看到此响应：
```JSON
{"item_id":3}
```

!!! 提示
    请注意，您的函数接收（并返回）的值是 **3**, 作为 Python 的 `int` - 而不是字符串 `"3"`.
    因此，仅通过该类型声明，**Django Ninja** 就为您提供了自动请求“解析”和验证。



### 数据验证
另一方面，如果您在浏览器中访问 <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"` 不是int)*</small>，您将看到如下 HTTP 错误：

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Django 路径转换器

您可以使用 [Django 路径转换器](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters)
来帮助解析路径：

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

在这种情况下，`item_id` 将被解析为一个 **`int`**。如果 `item_id` 不是有效的 `int`则该 URL 将不匹配。
（例如，如果没有其他路径匹配，则会返回一个404 未找到）

!!! 提示
    请注意，由于 **Django Ninja** 对未注释的参数使用默认的 `str` 类型, 上述函数接收（和返回）的值是 `"3"`, 
    作为一个 Python `str` - 而不是整数 **3**。 要接收一个 `int`，只需像平常一样在函数定义中简单地将 `item_id` 
    声明为 `int` 类型注释：

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```
 
#### 带斜线的路径参数

Django 的 `path` 转换器允许你处理类似路径的参数：

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
你可以用 `/dir/some/path/with-slashes` 来查询此操作，并且你的 `value` 将等于 `some/path/with-slashes`

### 多个参数

你可以向  `path` 传递任意多的变量只要记住要有唯一的名称，并且不要忘记在函数参数中使用相同的名称。

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### 使用 Schema 模式

你也可以使用 Schema 模式来封装相互依赖的路径参数（并作为一个组进行验证）：


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! 注意
    请注意，这里我们使用了一个  `Path` 源提示，让 **Django Ninja** 知道这个模式将应用于路径参数。

### 文档
现在，当你在浏览器中打开 <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> 时，你将看到自动的、交互式的 API 文档。
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! 大功告成

    继续下一章节！ **[查询参数](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
