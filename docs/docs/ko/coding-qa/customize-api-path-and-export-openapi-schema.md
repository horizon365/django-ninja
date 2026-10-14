최상위 API 경로를 커스터마이즈한 후 `export_openapi_schema`로 스키마 파일을 내보내는 방법
==========================================================
ninja의 기본 최상위 라우트는 `'api'`입니다. 이를 `'coast/api'`로 변경한 후
`python manage.py export_openapi_schema`를 실행하면 오류가 발생합니다.

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
이는 소스 코드가 기본적으로 `api = resolve("/api/").func.keywords["api"]`로 되어 있기 때문에 발생합니다.
최상위 라우트가 `/api/`가 아닌 경우 `--api` 파라미터로 지정해야 합니다. 이 파라미터는 `import_string(api_path)`를 통해 로드되므로 `NinjaAPI` 인스턴스의 import 경로여야 합니다.
예를 들어 제 프로젝트에서는 `'website.utils.tools.api.ninja_api'`입니다. 찾을 수 없다면 `urls.py`에서 `add_router`나 `urls` 앞에 있는 변수를 확인하세요 — 그것이 바로 원하는 것입니다.

추가 지식:

## 나
이 코드에서 `--api` 파라미터를 명령줄을 통해 전달하는 경우, 어떤 형식이어야 하나요?



## AI 어시스턴트
이 코드에서 `--api` 파라미터는 API 인스턴스 모듈을 지정하는 데 사용됩니다. 코드의 주석과 docstring에 따르면 `--api` 파라미터의 형식은 **모듈 경로**여야 합니다 — 구체적으로는 Django의 `import_string` 함수로 해석할 수 있는 Python 모듈 경로입니다.

### 형식
```shell script
--api <module_path>
```


### 예시
프로젝트 구조가 다음과 같다고 가정합니다:
```
project/
    urls.py
    api.py
```


`NinjaAPI` 인스턴스가 `project/api.py` 파일에 정의되어 있고 인스턴스 이름이 `api`라면 다음과 같이 파라미터를 전달할 수 있습니다:
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### 참고 사항
1. `<module_path>`는 `NinjaAPI` 인스턴스를 포함하는 모듈을 가리키는 Python 모듈 경로입니다.
2. 경로의 마지막 부분은 모듈 내 `NinjaAPI` 인스턴스의 변수 이름입니다(예: `api`).
3. `--api` 파라미터가 제공되지 않으면 코드는 `resolve("/api/")`를 통해 `NinjaAPI` 인스턴스를 동적으로 가져오려고 시도합니다. 실패하면 사용자에게 `--api` 파라미터로 명시적으로 지정하라는 오류를 발생시킵니다.

### 주의 사항
- 제공된 모듈 경로가 유효하고 해당 모듈에 실제로 `NinjaAPI` 인스턴스가 존재하는지 확인하세요. 그렇지 않으면 모듈 또는 속성을 찾을 수 없다는 `CommandError`가 발생합니다.
- `NinjaAPI` 인스턴스의 경로를 잘 모르겠다면 프로젝트의 `urls.py` 또는 기타 관련 파일에서 `NinjaAPI`가 인스턴스화되는 위치를 참조하세요.



#### 방법 1: 프로젝트 URL 설정 확인
일반적으로 Django 프로젝트의 URL 라우트는 `urls.py` 파일에 설정되어 있습니다. 프로젝트의 `urls.py`를 열고 `/api/`와 관련된 부분을 찾으세요. 예를 들어:

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


이 예시에서:
- `api`는 `NinjaAPI` 인스턴스입니다.
- 모듈 `project.api`에 정의되어 있습니다(프로젝트 루트 디렉터리가 `project`라고 가정).

따라서 이에 해당하는 `--api` 파라미터는 다음과 같아야 합니다:
```shell script
--api project.api.api
```


### 요약
`resolve("/coast/api/")`의 동작을 재현하려면 `/coast/api/` 경로가 매핑되는 `NinjaAPI` 인스턴스의 모듈 경로를 알아야 하며, 이를 `--api` 파라미터의 값으로 전달해야 합니다. 예를 들어:

```shell script
python manage.py export_openapi_schema --api project.api.api
```


인스턴스가 어디에 있는지 확실하지 않다면 프로젝트의 `urls.py` 파일을 확인하거나 디버깅을 통해 확인하세요.
