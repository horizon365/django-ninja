How to Export a Schema File with `export_openapi_schema` After Customizing the Top-Level API Path
==========================================================
The default top-level route in ninja is `'api'`. Suppose you change it to `'coast/api'` and then run
`python manage.py export_openapi_schema`, it will raise an error.

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
This happens because the source code defaults to `api = resolve("/api/").func.keywords["api"]`.
If your top-level route is not `/api/`, you must specify it via the `--api` parameter. This parameter is loaded through `import_string(api_path)`, so it needs to be the import path of the `NinjaAPI` instance.
For example, in my project it is `'website.utils.tools.api.ninja_api'`. If you cannot find it, look in `urls.py` for the variable in front of `add_router` or `urls` — that is what you want.

Additional knowledge:

## Me
In this code, if the `--api` parameter is passed via the command line, what should its format be?



## AI Assistant
In this code, the `--api` parameter is used to specify an API instance module. According to the comments and docstring in the code, the format of the `--api` parameter should be a **module path** — specifically, a Python module path that can be resolved by Django's `import_string` function.

### Format
```shell script
--api <module_path>
```


### Example
Assume your project structure is as follows:
```
project/
    urls.py
    api.py
```


If the `NinjaAPI` instance is defined in the `project/api.py` file and the instance is named `api`, you can pass the parameter like this:
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### Notes
1. `<module_path>` is a Python module path pointing to the module that contains the `NinjaAPI` instance.
2. The last part of the path is the variable name of the `NinjaAPI` instance in the module (for example, `api`).
3. If the `--api` parameter is not provided, the code attempts to fetch the `NinjaAPI` instance dynamically via `resolve("/api/")`. If that fails, it raises an error prompting the user to specify it explicitly via the `--api` parameter.

### Caveats
- Make sure the provided module path is valid and that a `NinjaAPI` instance actually exists in the module. Otherwise, the code will raise a `CommandError` indicating that the module or attribute was not found.
- If you are unsure of the path to the `NinjaAPI` instance, refer to your project's `urls.py` or other related files to find where the `NinjaAPI` is instantiated.



#### Method 1: Inspect the project URL configuration
Typically, the URL routes for a Django project are configured in the `urls.py` file. Open the project's `urls.py` and find the part related to `/api/`. For example:

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


In this example:
- `api` is a `NinjaAPI` instance.
- It is defined in the module `project.api` (assuming the project root directory is `project`).

Therefore, the equivalent `--api` parameter should be:
```shell script
--api project.api.api
```


### Summary
To replicate the behavior of `resolve("/coast/api/")`, you need to know the module path of the `NinjaAPI` instance that the `/coast/api/` path maps to, and pass it as the value of the `--api` parameter. For example:

```shell script
python manage.py export_openapi_schema --api project.api.api
```


If you are not sure where the instance is located, inspect the project's `urls.py` file or confirm by debugging.
