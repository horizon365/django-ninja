---
comments: true
---
# 表单数据 Form data

**Django Ninja** 还允许你解析和验证 `request.POST` 数据
(也就是 `application/x-www-form-urlencoded` 或 `multipart/form-data`).

## 作为参数的表单数据

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

请注意以下几点:

1) 你需要从 `ninja` 导入 `Form` 类
```python
from ninja import Form
```

2) 使用 `Form` 作为参数的默认值：
```python
username: Form[str]
```

## 使用模式

与 [请求体 Body](body.md#declare-it-as-a-parameter)类似, 你可以使用模式来组织你的参数。

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## 请求表单 + 路径 + 查询参数

与 [请求体 Body](body.md#request-body-path-query-parameters)类似, 你可以结合其他参数来源使用表单数据。

你可以 **同时** 声明查询参数 **和**  路径 **和** 表单字段, **等等** ... 参数。

**Django Ninja** 将识别出与路径参数匹配的函数参数应 **从路径中获取**，
而声明为`Form(...)` 的函数参数应 **从请求表单字段中获取** 等等。

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## 将空表单字段映射到默认值

可选的表单字段经常以空值发送。这个值被解释为空字符串，因此对于诸如 `int` 或 `bool` 等字段可能无法通过验证。

如 Pydantic 文档所述，可以通过使用[作为类型的泛型类](https://pydantic-docs.helpmanual.io/usage/types/#generic-classes-as-types) 来解决这个问题。

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
