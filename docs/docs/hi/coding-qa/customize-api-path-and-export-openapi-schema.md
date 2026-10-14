टॉप-लेवल API path को कस्टमाइज़ करने के बाद `export_openapi_schema` से Schema फ़ाइल को एक्सपोर्ट कैसे करें
==========================================================
ninja में डिफ़ॉल्ट टॉप-लेवल route `'api'` होता है। मान लीजिए आप इसे `'coast/api'` में बदलते हैं और फिर
`python manage.py export_openapi_schema` चलाते हैं, तो यह एक error raise करेगा।

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
ऐसा इसलिए होता है क्योंकि सोर्स कोड में डिफ़ॉल्ट रूप से `api = resolve("/api/").func.keywords["api"]` होता है।
यदि आपका टॉप-लेवल route `/api/` नहीं है, तो आपको इसे `--api` parameter के माध्यम से निर्दिष्ट करना होगा। यह parameter `import_string(api_path)` के माध्यम से लोड किया जाता है, इसलिए यह `NinjaAPI` instance का import path होना चाहिए।
उदाहरण के लिए, मेरे project में यह `'website.utils.tools.api.ninja_api'` है। यदि आपको यह नहीं मिल रहा है, तो `urls.py` में `add_router` या `urls` के सामने वाले variable को देखें — वही आपके लिए चाही गई चीज़ है।

अतिरिक्त जानकारी:

## मैं
इस कोड में, यदि `--api` parameter command line के माध्यम से पास किया जाए, तो उसका format क्या होना चाहिए?



## AI Assistant
इस कोड में, `--api` parameter का उपयोग एक API instance module निर्दिष्ट करने के लिए किया जाता है। कोड की comments और docstring के अनुसार, `--api` parameter का format एक **module path** होना चाहिए — विशेष रूप से, एक Python module path जिसे Django के `import_string` function द्वारा resolve किया जा सके।

### Format
```shell script
--api <module_path>
```


### उदाहरण
मान लीजिए आपकी project structure इस प्रकार है:
```
project/
    urls.py
    api.py
```


यदि `NinjaAPI` instance को `project/api.py` फ़ाइल में define किया गया है और instance का नाम `api` है, तो आप parameter इस प्रकार पास कर सकते हैं:
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### ध्यान दें
1. `<module_path>` एक Python module path है जो उस module की ओर इशारा करता है जिसमें `NinjaAPI` instance स्थित है।
2. path का अंतिम भाग module में `NinjaAPI` instance के variable का नाम है (उदाहरण के लिए, `api`)।
3. यदि `--api` parameter प्रदान नहीं किया गया है, तो कोड `resolve("/api/")` के माध्यम से `NinjaAPI` instance को dynamically प्राप्त करने का प्रयास करता है। यदि वह विफल हो जाता है, तो यह एक error raise करता है जो user को `--api` parameter के माध्यम से इसे स्पष्ट रूप से निर्दिष्ट करने का संकेत देता है।

### सावधानियाँ
- सुनिश्चित करें कि प्रदान किया गया module path मान्य है और module में वास्तव में एक `NinjaAPI` instance मौजूद है। अन्यथा, कोड एक `CommandError` raise करेगा जो बताएगा कि module या attribute नहीं मिला।
- यदि आप `NinjaAPI` instance का path नहीं जानते हैं, तो अपनी project की `urls.py` या अन्य संबंधित फ़ाइलों को देखें ताकि पता चल सके कि `NinjaAPI` कहाँ instantiate किया गया है।



#### विधि 1: project की URL configuration की जाँच करें
आम तौर पर, किसी Django project के URL routes `urls.py` फ़ाइल में configure किए जाते हैं। project की `urls.py` खोलें और `/api/` से संबंधित भाग खोजें। उदाहरण के लिए:

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


इस उदाहरण में:
- `api` एक `NinjaAPI` instance है।
- इसे module `project.api` में define किया गया है (मान लें कि project की root directory `project` है)।

इसलिए, समतुल्य `--api` parameter होना चाहिए:
```shell script
--api project.api.api
```


### सारांश
`resolve("/coast/api/")` के व्यवहार को replicate करने के लिए, आपको उस `NinjaAPI` instance का module path जानना होगा जिस पर `/coast/api/` path map होता है, और उसे `--api` parameter के मान के रूप में पास करना होगा। उदाहरण के लिए:

```shell script
python manage.py export_openapi_schema --api project.api.api
```


यदि आप निश्चित नहीं हैं कि instance कहाँ स्थित है, तो project की `urls.py` फ़ाइल की जाँच करें या debugging द्वारा पुष्टि करें।
