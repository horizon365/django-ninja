## मैं
इस कोड में, यदि `--api` parameter command line के माध्यम से पास किया जाए, तो उसका format क्या होना चाहिए?
```python
import pdb
import json
from pathlib import Path
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.urls.base import resolve
from django.utils.module_loading import import_string
from ninja.main import NinjaAPI
from ninja.management.utils import command_docstring
from ninja.responses import NinjaJSONEncoder

class Command(BaseCommand):
    """
    Example:
        ```terminal
        python manage.py export_openapi_schema
        ```
        ```terminal
        python manage.py export_openapi_schema --api project.urls.api
        ```
    """
    help = "Exports Open API schema"
    def _get_api_instance(self, api_path: Optional[str] = None) -> NinjaAPI:
        if not api_path:
            try:
                pdb.set_trace()
                return resolve("/coast/api/").func.keywords["api"]  # type: ignore
            except AttributeError:
                raise CommandError(
                    "No NinjaAPI instance found; please specify one with --api"
                ) from None
        try:
            api = import_string(api_path)
        except ImportError:
            raise CommandError(
                f"Module or attribute for {api_path} not found!"
            ) from None
        if not isinstance(api, NinjaAPI):
            raise CommandError(f"{api_path} is not instance of NinjaAPI!")
        return api
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--api",
            dest="api",
            default=None,
            type=str,
            help="Specify api instance module",
        )
        parser.add_argument(
            "--output",
            dest="output",
            default=None,
            type=str,
            help="Output schema to a file (outputs to stdout if omitted).",
        )
        parser.add_argument(
            "--indent", dest="indent", default=None, type=int, help="JSON indent"
        )
        parser.add_argument(
            "--sorted",
            dest="sort_keys",
            default=False,
            action="store_true",
            help="Sort Json keys",
        )
    def handle(self, *args: Any, **options: Any) -> None:
        api = self._get_api_instance(options["api"])
        schema = api.get_openapi_schema()
        result = json.dumps(
            schema,
            cls=NinjaJSONEncoder,
            indent=options["indent"],
            sort_keys=options["sort_keys"],
        )
        if options["output"]:
            with Path(options["output"]).open("wb") as f:
                f.write(result.encode())
        else:
            self.stdout.write(result)

__doc__ = command_docstring(Command)
```
```
`


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
3. यदि `--api` parameter प्रदान नहीं किया गया है, तो कोड `resolve("/coast/api/")` के माध्यम से `NinjaAPI` instance को dynamically प्राप्त करने का प्रयास करता है। यदि वह विफल हो जाता है, तो यह एक error raise करता है जो user को `--api` parameter के माध्यम से इसे स्पष्ट रूप से निर्दिष्ट करने का संकेत देता है।

### सावधानियाँ
- सुनिश्चित करें कि प्रदान किया गया module path मान्य है और module में वास्तव में एक `NinjaAPI` instance मौजूद है। अन्यथा, कोड एक `CommandError` raise करेगा जो बताएगा कि module या attribute नहीं मिला।
- यदि आप `NinjaAPI` instance का path नहीं जानते हैं, तो अपनी project की `urls.py` या अन्य संबंधित फ़ाइलों को देखें ताकि पता चल सके कि `NinjaAPI` कहाँ instantiate किया गया है।

आशा है कि यह आपको `--api` parameter का उपयोग करने के तरीके को समझने में मदद करेगा!

## मैं
`api` parameter को कैसे भरूँ ताकि यह `resolve("/coast/api/")` के समतुल्य हो?


## AI Assistant
`--api` parameter को `resolve("/coast/api/")` के व्यवहार के समतुल्य बनाने के लिए, निम्नलिखित बिंदुओं को स्पष्ट करने की आवश्यकता है:

1. **`resolve("/coast/api/")` क्या करता है**  
   कोड की logic के अनुसार:
```python
resolve("/coast/api/").func.keywords["api"]
```

इस line का उद्देश्य Django के URL routing resolution का उपयोग करके path `/coast/api/` से जुड़े view function को खोजना और उस function के keyword arguments से `"api"` नाम का मान निकालना है। यह मान एक `NinjaAPI` instance होना चाहिए।

2. **समतुल्यता की शर्त**  
   यदि आप `--api` parameter के माध्यम से वही प्रभाव प्राप्त करना चाहते हैं, तो आपको यह जानना होगा कि `/coast/api/` के अनुरूप `NinjaAPI` instance किस module में define किया गया है, और उसका path `--api` parameter को पास करना होगा।

---

### समतुल्य `--api` parameter कैसे निर्धारित करें?

#### विधि 1: project की URL configuration की जाँच करें
आम तौर पर, किसी Django project के URL routes `urls.py` फ़ाइल में configure किए जाते हैं। project की `urls.py` खोलें और `/coast/api/` से संबंधित भाग खोजें। उदाहरण के लिए:

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


---

#### विधि 2: dynamic debugging द्वारा पुष्टि करें
यदि आप `urls.py` फ़ाइल से सीधे `NinjaAPI` instance का स्थान नहीं खोज पा रहे हैं, तो आप debugging के माध्यम से इसकी पुष्टि कर सकते हैं। कोड में पहले से ही `pdb.set_trace()` मौजूद है, जो आपको runtime पर program को रोकने और `resolve("/coast/api/")` के परिणाम की जाँच करने की अनुमति देता है:

1. `--api` parameter के बिना command चलाएँ:
```shell script
python manage.py export_openapi_schema
```


2. Program `pdb.set_trace()` पर रुक जाएगा। इस बिंदु पर, `resolve("/coast/api/")` के परिणाम की जाँच करने के लिए निम्नलिखित command दर्ज करें:
```python
resolve("/coast/api/").func.keywords["api"]
```


3. Return किए गए object और उसके module path की पुष्टि करें। उदाहरण के लिए, यदि return किया गया object `<NinjaAPI: api>` है और इसे module `project.api` में define किया गया है, तो समतुल्य `--api` parameter है:
```shell script
--api project.api.api
```


django-ninja में OpenAPI schema को चीनी (Chinese) में एक्सपोर्ट करें
---

## मैं
`json.dumps` में, `ensure_ascii` parameter का उद्देश्य क्या है?

## AI Assistant
Python की `json.dumps` method में, `ensure_ascii` parameter नियंत्रित करता है कि generated JSON string में केवल ASCII characters हों या नहीं।

### डिफ़ॉल्ट व्यवहार
- **डिफ़ॉल्ट मान**: `ensure_ascii=True`
- जब इसे `True` सेट किया जाता है, तो non-ASCII characters (जैसे चीनी, जापानी, special symbols, आदि) को `\uXXXX` format के Unicode sequences में escape कर दिया जाएगा।  
  उदाहरण के लिए:
```python
import json

  data = {"name": "张三", "age": 30}
  result = json.dumps(data, ensure_ascii=True)
  print(result)
```

आउटपुट:
```json
{"name": "\u5f20\u4e09", "age": 30}
```


---

### `False` सेट करें
- जब इसे `False` सेट किया जाता है, तो non-ASCII characters को बिना escape किए उनके मूल characters के रूप में सीधे आउटपुट किया जाता है।
  उदाहरण के लिए:
```python
import json

  data = {"name": "张三", "age": 30}
  result = json.dumps(data, ensure_ascii=False)
  print(result)
```

आउटपुट:
```json
{"name": "张三", "age": 30}
```


---

### उपयोग के मामले
1. **`ensure_ascii=True`**:
    - जब generated JSON data को केवल ASCII characters को support करने वाले systems या protocols (उदाहरण के लिए, कुछ पुराने HTTP clients) के साथ compatible होने की आवश्यकता होती है, तब इस विकल्प का उपयोग करें।
    - उदाहरण: data को केवल ASCII को support करने वाले database field में संग्रहीत करना।

2. **`ensure_ascii=False`**:
    - जब आपको अधिक पठनीय (readable) JSON data generate करने की आवश्यकता होती है (विशेष रूप से जब इसमें multilingual text हो), तो इस parameter को `False` सेट करने की सलाह दी जाती है।
    - उदाहरण: JSON data को सीधे frontend को return करना, non-ASCII characters को पठनीय रखते हुए।

---

### सारांश
- `ensure_ascii=True`: Non-ASCII characters को `\uXXXX` format में escape किया जाता है।
- `ensure_ascii=False`: Non-ASCII characters को उनके मूल characters के रूप में सीधे आउटपुट किया जाता है।

विशेष रूप से django-ninja में, यदि आपको चीनी characters एक्सपोर्ट करने की आवश्यकता है, तो आप `export_openapi_schema.py` फ़ाइल में `json.dumps` function के parameters को समायोजित कर सकते हैं।
