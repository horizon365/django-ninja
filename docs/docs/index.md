# Django Ninja - 快速的 Django REST 框架


![Django Ninja](img/hero.png)

Django Ninja 是一个使用 Django 和 Python 3.6+ 类型提示构建 API 的网络框架。

主要特点:

 - **简单易懂**: 设计为易于使用和符合直觉。
 - **快速执行**: 多亏了 **<a href="https://pydantic-docs.helpmanual.io" target="_blank">Pydantic</a>** 和 **<a href="guides/async-support/">异步支持</a>**，具有非常高的性能。
 - **快速编程**: Django Ninja 是一个用于使用 Django 和 Python 3.6+ 类型提示构建 API 的网络框架。
 - **基于标准**: 基于标准: **OpenAPI** (以前称为 Swagger) 和 **JSON 模式**。
 - **对 Django 友好**: （显然）与 Django 核心和对象关系映射有良好的集成。
 - **可用于生产**: 被多家公司用于实际项目（如果你使用 Django Ninja 并想发布你的反馈，请发邮件至 ppr.vitaly@gmail.com）。

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">基准测试</a>:

![Django Ninja REST Framework](img/benchmark.png)

## 安装

```
pip install django-ninja
```

## 快速示例

开始一个新的 Django 项目（或使用现有的一个）
```
django-admin startproject apidemo
```

在 `urls.py` 中

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

现在，像平常一样运行它:
```
./manage.py runserver
```

注意：你不必将 Django Ninja 添加到你的已安装应用中，它就可以工作。     

## 检查它

打开你的浏览器，在 <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

你将看到 JSON 响应为：
```JSON
{"result": 3}
```
现在，你刚刚创建了一个 API，该 API：

 - 在 `/api/add` 接收一个 HTTP GET 请求
 - 接收、验证并类型转换 GET 参数 `a` 和 `b`
 - 将结果解码为 JSON
 - 为定义的操作生成一个 OpenAPI 模式

## 交互式 API 文档

现在前往 <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

你将看到自动的、交互式 API 文档 (由 <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> 或 <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a> 提供) :

![Swagger UI](img/index-swagger-ui.png)


## 总结

总之，你只需 **一次** 声明参数、请求体等的类型， 作为函数参数。 

你使用标准的现代 Python 类型来做到这一点。

你不必学习新的语法、特定库的方法或类等。

只需标准的 **Python 3.6+**.

例如, 对于一个 `int`:

```python
a: int
```

或者, 对于一个更复杂的 `Item` 模型:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...仅通过这一个声明，你就可以得到 :

* 编辑器支持，包括:
    * 自动完成
    * 类型检查
* 数据验证:
    * 当数据无效时自动且清晰的错误
    * 甚至对深度嵌套的 JSON 对象进行验证
* <abbr title="也称为: serialization, parsing, marshalling">序列化</abbr> 网络输入的数据并转换成 Python 数据输出, 并从以下读取:
    * JSON
    * Path parameters 路径参数
    * Query parameters 查询参数
    * Cookies
    * Headers 请求头
    * Forms 表单
    * Files 文件
* 自动的、交互式 API 文档

这个项目很大程度上受到了 <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (由 <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>开发)的启发。

