Как экспортировать файл схемы с помощью `export_openapi_schema` после изменения пути верхнего уровня API
==========================================================
Путь верхнего уровня в ninja по умолчанию — `'api'`. Предположим, вы изменили его на `'coast/api'` и затем запускаете
`python manage.py export_openapi_schema`, — будет вызвана ошибка.

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
Это происходит потому, что в исходном коде по умолчанию используется `api = resolve("/api/").func.keywords["api"]`.
Если ваш путь верхнего уровня — не `/api/`, вы должны указать его с помощью параметра `--api`. Этот параметр загружается через `import_string(api_path)`, поэтому он должен быть путём импорта экземпляра `NinjaAPI`.
Например, в моём проекте это `'website.utils.tools.api.ninja_api'`. Если вы не можете его найти, поищите в `urls.py` переменную перед `add_router` или `urls` — это именно то, что вам нужно.

Дополнительные знания:

## Я
В этом коде, если параметр `--api` передаётся через командную строку, каким должен быть его формат?



## AI-ассистент
В этом коде параметр `--api` используется для указания модуля экземпляра API. Согласно комментариям и docstring в коде, формат параметра `--api` должен быть **путём к модулю** — а именно путём к модулю Python, который может быть разрешён функцией `import_string` в Django.

### Формат
```shell script
--api <module_path>
```


### Пример
Предположим, структура вашего проекта выглядит следующим образом:
```
project/
    urls.py
    api.py
```


Если экземпляр `NinjaAPI` определён в файле `project/api.py` и экземпляр называется `api`, вы можете передать параметр так:
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### Примечания
1. `<module_path>` — это путь к модулю Python, указывающий на модуль, который содержит экземпляр `NinjaAPI`.
2. Последняя часть пути — это имя переменной экземпляра `NinjaAPI` в модуле (например, `api`).
3. Если параметр `--api` не указан, код пытается динамически получить экземпляр `NinjaAPI` через `resolve("/api/")`. Если это не удаётся, вызывается ошибка, предлагающая пользователю явно указать его с помощью параметра `--api`.

### Предостережения
- Убедитесь, что указанный путь к модулю действителен и что экземпляр `NinjaAPI` действительно существует в модуле. В противном случае код вызовет `CommandError`, указывающий, что модуль или атрибут не найдены.
- Если вы не уверены в пути к экземпляру `NinjaAPI`, обратитесь к файлу `urls.py` вашего проекта или другим связанным файлам, чтобы найти, где создаётся экземпляр `NinjaAPI`.



#### Способ 1: Проверьте конфигурацию URL проекта
Обычно маршруты URL проекта Django настраиваются в файле `urls.py`. Откройте `urls.py` проекта и найдите часть, относящуюся к `/api/`. Например:

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


В этом примере:
- `api` — это экземпляр `NinjaAPI`.
- Он определён в модуле `project.api` (предполагая, что корневой каталог проекта — `project`).

Следовательно, эквивалентный параметр `--api` должен быть таким:
```shell script
--api project.api.api
```


### Итог
Чтобы воспроизвести поведение `resolve("/coast/api/")`, вам нужно узнать путь к модулю экземпляра `NinjaAPI`, которому соответствует путь `/coast/api/`, и передать его в качестве значения параметра `--api`. Например:

```shell script
python manage.py export_openapi_schema --api project.api.api
```


Если вы не уверены, где находится экземпляр, проверьте файл `urls.py` проекта или уточните это с помощью отладки.
