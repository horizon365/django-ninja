トップレベルの API パスをカスタマイズした後に `export_openapi_schema` で Schema ファイルをエクスポートする方法
==========================================================
ninja のデフォルトのトップレベルルートは `'api'` です。これを `'coast/api'` に変更してから
`python manage.py export_openapi_schema` を実行すると、エラーが発生します。

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
これは、ソースコードがデフォルトで `api = resolve("/api/").func.keywords["api"]` を使用しているために起こります。
トップレベルのルートが `/api/` でない場合は、`--api` パラメータで指定する必要があります。このパラメータは `import_string(api_path)` を通じて読み込まれるため、`NinjaAPI` インスタンスの import パスである必要があります。
たとえば、私のプロジェクトでは `'website.utils.tools.api.ninja_api'` です。見つからない場合は、`urls.py` 内で `add_router` または `urls` の前にある変数を探してください。それがまさに目的のものです。

補足知識：

## 私
このコードで、コマンドラインから `--api` パラメータを渡す場合、その形式はどのようなものでしょうか？



## AI アシスタント
このコードにおいて、`--api` パラメータは API インスタンスのモジュールを指定するために使用されます。コード内のコメントや docstring によると、`--api` パラメータの形式は **モジュールパス** である必要があります。具体的には、Django の `import_string` 関数で解決できる Python モジュールパスです。

### 形式
```shell script
--api <module_path>
```


### 例
プロジェクト構造が次のようになっていると仮定します：
```
project/
    urls.py
    api.py
```


`NinjaAPI` インスタンスが `project/api.py` ファイル内で定義されており、そのインスタンス名が `api` である場合は、次のようにパラメータを渡すことができます：
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### 注意点
1. `<module_path>` は、`NinjaAPI` インスタンスを含むモジュールを指す Python モジュールパスです。
2. パスの最後の部分は、モジュール内における `NinjaAPI` インスタンスの変数名です（例： `api`）。
3. `--api` パラメータが指定されていない場合、コードは `resolve("/api/")` を通じて `NinjaAPI` インスタンスを動的に取得しようとします。それが失敗すると、`--api` パラメータで明示的に指定するよう促すエラーが発生します。

### 注意事項
- 指定するモジュールパスが有効であり、そのモジュール内に実際に `NinjaAPI` インスタンスが存在することを確認してください。そうでない場合、コードはモジュールまたは属性が見つからなかったことを示す `CommandError` を発生させます。
- `NinjaAPI` インスタンスのパスがわからない場合は、プロジェクトの `urls.py` やその他の関連ファイルを参照して、`NinjaAPI` がインスタンス化されている場所を見つけてください。



#### 方法 1：プロジェクトの URL 設定を確認する
通常、Django プロジェクトの URL ルーティングは `urls.py` ファイルで設定されます。プロジェクトの `urls.py` を開き、`/api/` に関連する部分を見つけてください。例：

```python
# project/urls.py
from django.urls import path
from .api import api  # NinjaAPI インスタンスの名前が `api` であると仮定

urlpatterns = [
    path("coast/api/", api.urls),  # `api` のルートを `/coast/api/` の下にマウント
]
```


この例では：
- `api` は `NinjaAPI` インスタンスです。
- これは `project.api` モジュール内で定義されています（プロジェクトのルートディレクトリが `project` であると仮定）。

したがって、同等の `--api` パラメータは次のようになります：
```shell script
--api project.api.api
```


### まとめ
`resolve("/coast/api/")` の挙動を再現するには、`/coast/api/` パスがマッピングされている `NinjaAPI` インスタンスのモジュールパスを知り、それを `--api` パラメータの値として渡す必要があります。例：

```shell script
python manage.py export_openapi_schema --api project.api.api
```


インスタンスの場所がわからない場合は、プロジェクトの `urls.py` ファイルを確認するか、デバッグによって確認してください。
