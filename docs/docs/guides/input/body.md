---
comments: true
---
# 请求体

请求体通常与“创建”和“更新”操作（POST、PUT、PATCH）一起使用。
例如，使用 POST 或 PUT 创建资源时，请求体通常包含要创建的资源的表示形式。

要声明一个请求体 **request body**, 你需要使用 **Django Ninja 的 `Schema`**.

!!! 注意
    在底层实现上，**Django Ninja** 使用了 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> Model 的所有能力和特性。
    选择 `Schema` 作为别名是为了在使用 Django 模型时避免代码混淆，因为 Pydantic 的模型类默认情况下被称为 Model，这与 Django 的Model类冲突。
    

## 导入 Schema

首先，你需要从 `ninja` 中导入`Schema`:

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## 创建你的数据模型

然后将你的数据模型声明为一个继承自 `Schema` 的类。

为所有属性使用标准的 Python 类型：

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

注意: 如果你将一个属性的默认值设置为 **`None`** ，它将在请求体中成为可选的。例如，上面的模型声明了一个 JSON "`object`" (或 Python `dict`) ，如下所示:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...由于 `description` 是可选的(默认值为 `None`), 因此这个 JSON "`object`" 也将是有效的:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## 将其声明为参数

要将其添加到你的 *路径操作* 中，以与声明路径和查询参数相同的方式进行声明：


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

... 并将其类型声明为你创建的 `Item` 模型。

## 结果

仅使用该 Python 类型声明, **Django Ninja** 将:

* 将请求体读取为 JSON。
* 转换相应的类型（如果需要）。
* 验证数据。
    * 如果数据无效，它将返回一个友好且有意义的错误，准确指出错误数据的位置和内容。
* 在参数`item`中为你提供接收到的数据.
    * 由于你在函数中声明它的类型为Item，你还将获得所有属性及其类型的编辑器支持
（自动完成等）。
* 为你的模型生成 <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> 定义，你也可以在项目中需要的任何地方使用它们。
* 这些模式将成为生成的 OpenAPI 模式的一部分，并由自动文档 <abbr title="User Interfaces">UI</abbr> 使用。

## 自动文档

你的模型的 JSON Schemas 将成为你生成的 OpenAPI 模式的一部分，并将在交互式 API 文档中显示：

![Openapi schema](../../img/body-schema-doc.png)

...并且它们也将在每个需要它们的 *路径操作* 的 API 文档中使用：

![Openapi schema](../../img/body-schema-doc2.png)

## 编辑器支持

在你的编辑器中，在你的函数内部，你将获得无处不在的类型提示和完成功能（如果使用`dict`而不是Schema对象，则不会发生这种情况）：

![Type hints](../../img/body-editor.gif)


前面的截图中使用的是<a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>。

你将在<a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 和大多数其它Python 编辑器获得相同的编辑器支持。

## 请求体 + 路径参数

你可以同时声明路径参数**和**请求体。


**Django Ninja** 将识别出与路径参数匹配的函数参数应 **从路径中** 获取，而使用 `Schema` 声明的函数参数应 **从请求体中** 获取。

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## 请求体 + 路径 + 查询参数

你也可以同时声明 **请求体 **、 **路径 **和 **查询 **参数。

 **Django Ninja** 将识别出每个参数，并从正确的位置获取数据。

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

函数参数将被识别为：

* 如果参数也在 **路径** 中声明，它将被用作路径参数。

 
* 如果参数是一个**单一类型** (如 `int`, `float`, `str`, `bool`等)，它将被解释为 **查询**参数。
* 如果参数被声明为**Schema** (or Pydantic `BaseModel`)的类型，它将被解释为 **请求体**。

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
