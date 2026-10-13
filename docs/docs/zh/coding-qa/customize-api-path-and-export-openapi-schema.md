自定义api一级路径后，如何使用export_openapi_schema导出schema文件
==========================================================
ninja的默认一级路由是 'api'，假设你调整它为 ‘coast/api’ 后，运行
python manage.py export_openapi_schema 则会报错

```python
python manage.py export_openapi_schema 
System check identified some issues:

WARNINGS:
?: (ckeditor.W001) django-ckeditor bundles CKEditor 4.22.1 which isn't supported anmyore and which does have unfixed security issues, see for example https://ckeditor.com/cke4/release/CKEditor-4.24.0-LTS . You should consider strongly switching to a different editor (maybe CKEditor 5 respectively django-ckeditor-5 after checking whether the CKEditor 5 license terms work for you) or switch to the non-free CKEditor 4 LTS package. See https://ckeditor.com/ckeditor-4-support/ for more on this. (Note! This notice has been added by the django-ckeditor developers and we are not affiliated with CKSource and were not involved in the licensing change, so please refrain from complaining to us. Thanks.)
Traceback (most recent call last):
  File "/Users/baoge/WebstormProjects/coast_be/manage.py", line 27, in <module>
    main()
  File "/Users/baoge/WebstormProjects/coast_be/manage.py", line 23, in main
    execute_from_command_line(sys.argv)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/__init__.py", line 419, in execute_from_command_line
    utility.execute()
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/__init__.py", line 413, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/base.py", line 354, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/base.py", line 398, in execute
    output = self.handle(*args, **options)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/ninja/management/commands/export_openapi_schema.py", line 79, in handle
    api = self._get_api_instance(options["api"])
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/ninja/management/commands/export_openapi_schema.py", line 34, in _get_api_instance
    return resolve("/api/").func.keywords["api"]  # type: ignore
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/urls/base.py", line 24, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/urls/resolvers.py", line 589, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.urls.exceptions.Resolver404: {'tried': [[<URLResolver <URLResolver list> (None:None) 'coast/'>]], 'path': 'api/'}
```
这是因为源码中默认取的是 api = resolve("/api/").func.keywords["api"]，
如果你的一级路由不是/api/，则要通过  --api参数指定，这是一个 import_string(api_path) 导入的参数，需要传递的是 NinjaAPI实例的导入路径。
例如我的项目为 'website.utils.tools.api.ninja_api'，如果你找不到，可以去 urls.py中查找 add_router 或者  urls 前面的那个变量，则是你想要的。

额外知识：

## 我
这段代码中，如果通过命令行传递了 --api参数，它的格式应该是什么样的



## AI Assistant
在这段代码中，`--api` 参数用于指定一个 API 实例模块。根据代码中的注释和文档字符串，`--api` 参数的格式应该是 **模块路径**，具体来说，是一个可以被 Django 的 `import_string` 函数解析的 Python 模块路径。

### 格式
```shell script
--api <module_path>
```


### 示例
假设你的项目结构如下：
```
project/
    urls.py
    api.py
```


如果 `NinjaAPI` 实例定义在 `project/api.py` 文件中，并且实例名为 `api`，那么你可以这样传递参数：
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### 说明
1. `<module_path>` 是一个 Python 模块路径，指向包含 `NinjaAPI` 实例的模块。
2. 路径的最后一部分是模块中 `NinjaAPI` 实例的变量名（例如 `api`）。
3. 如果未提供 `--api` 参数，代码会尝试通过 `resolve("/api/")` 动态获取 `NinjaAPI` 实例。如果失败，则会抛出错误，提示用户必须通过 `--api` 参数显式指定。

### 注意事项
- 确保提供的模块路径是有效的，并且模块中确实存在一个 `NinjaAPI` 实例。否则，代码会抛出 `CommandError`，提示模块或属性未找到。
- 如果你不确定 `NinjaAPI` 实例的路径，可以参考项目的 `urls.py` 或其他相关文件，找到实例化 `NinjaAPI` 的位置。



#### 方法 1：检查项目的 URL 配置
通常，Django 项目的 URL 路由会在 `urls.py` 文件中配置。打开项目的 `urls.py` 文件，找到与 `/api/` 相关的部分。例如：

```python
# project/urls.py
from django.urls import path
from .api import api  # 假设 NinjaAPI 实例名为 `api`

urlpatterns = [
    path("coast/api/", api.urls),  # 将 `api` 的路由挂载到 `/coast/api/`
]
```


在这个例子中：
- `api` 是一个 `NinjaAPI` 实例。
- 它定义在模块 `project.api` 中（假设项目根目录为 `project`）。

因此，等价的 `--api` 参数应该是：
```shell script
--api project.api.api
```


### 总结
为了等价于 `resolve("/coast/api/")` 的行为，你需要明确 `/coast/api/` 路径对应的 `NinjaAPI` 实例的模块路径，并将其作为 `--api` 参数的值。例如：

```shell script
python manage.py export_openapi_schema --api project.api.api
```


如果你不确定实例的具体位置，可以检查项目的 `urls.py` 文件或通过调试确认。
