---
comments: true
---
# 查询参数

当你声明其他不属于路径参数的函数参数时，它们会自动被解释为 “查询” 参数。
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

要查询此操作，你可以使用这样的 URL：

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
默认情况下，所有 GET 参数都是字符串，当你用类型标注你的函数参数时，它们会被转换为该类型并根据该类型进行验证。

适用于路径参数的相同好处也适用于查询参数：

- 编辑器支持（显然）
- 数据 “解析”
- 数据验证
- 自动文档


!!! 注意
    如果你不标注你的参数，它们将被视为 `str` 类型

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### 默认值

由于查询参数不是路径的固定部分，它们是可选的并且可以有默认值：

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

在上面的例子中，我们设置了 `offset=0` 和 `limit=10`的默认值。

所以，访问 URL：
```
http://localhost:8000/api/weapons
```
将与访问以下是一样的：
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
如果你访问，例如：
```
http://localhost:8000/api/weapons?offset=20
```

你函数中的参数值将是：

 - `offset=20` （因为你在 URL 中设置了它）
 - `limit=10` （因为那是默认值）


### 必需和可选参数

你可以以声明 Python 函数参数的相同方式声明必需或可选的 GET 参数：

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

在这种情况下，**Django Ninja** 将始终验证你在 GET 中传递的 `q` 参数， 而 `offset` 参数是可选整数。

### GET 参数类型转换

让我们声明多个类型参数：
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
`str` 类型按原样传递。

对于 `bool` 类型，所有以下情况：
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
或任何其他大小写变化（大写，首字母大写等），你的函数将看到
参数 `b` 具有 `True` 的 `bool`值 , 否则为 `False`。

日期可以是日期字符串和整数（Unix 时间戳）：

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # 等同于 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### 使用模式

你也可以使用模式来封装 GET 参数：

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

对于更复杂的筛选场景，请参考 [过滤](./filtering.md).
