Een schemabestand exporteren met `export_openapi_schema` na het aanpassen van het API-pad op het hoogste niveau
==========================================================
De standaard top-level route in ninja is `'api'`. Stel dat je deze wijzigt in `'coast/api'` en vervolgens
`python manage.py export_openapi_schema` uitvoert, dan treedt er een fout op.

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
Dit gebeurt omdat de broncode standaard `api = resolve("/api/").func.keywords["api"]` gebruikt.
Als je top-level route niet `/api/` is, moet je deze opgeven via de `--api`-parameter. Deze parameter wordt geladen via `import_string(api_path)`, dus het moet het importpad van de `NinjaAPI`-instantie zijn.
In mijn project is dat bijvoorbeeld `'website.utils.tools.api.ninja_api'`. Als je het niet kunt vinden, kijk dan in `urls.py` naar de variabele vóór `add_router` of `urls` — dat is wat je nodig hebt.

Aanvullende kennis:

## Ik
In deze code: als de `--api`-parameter via de commandoregel wordt doorgegeven, wat moet dan het formaat zijn?



## AI-assistent
In deze code wordt de `--api`-parameter gebruikt om een API-instantiemodule op te geven. Volgens de opmerkingen en de docstring in de code moet het formaat van de `--api`-parameter een **modulepad** zijn — specifiek een Python-modulepad dat kan worden opgelost door de functie `import_string` van Django.

### Formaat
```shell script
--api <module_path>
```


### Voorbeeld
Stel dat je projectstructuur er als volgt uitziet:
```
project/
    urls.py
    api.py
```


Als de `NinjaAPI`-instantie is gedefinieerd in het bestand `project/api.py` en de instantie `api` heet, kun je de parameter als volgt doorgeven:
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### Opmerkingen
1. `<module_path>` is een Python-modulepad dat verwijst naar de module die de `NinjaAPI`-instantie bevat.
2. Het laatste deel van het pad is de variabelenaam van de `NinjaAPI`-instantie in de module (bijvoorbeeld `api`).
3. Als de `--api`-parameter niet wordt opgegeven, probeert de code de `NinjaAPI`-instantie dynamisch op te halen via `resolve("/api/")`. Als dat mislukt, treedt er een fout op die de gebruiker vraagt deze expliciet op te geven via de `--api`-parameter.

### Kanttekeningen
- Zorg ervoor dat het opgegeven modulepad geldig is en dat er daadwerkelijk een `NinjaAPI`-instantie in de module bestaat. Anders treedt er een `CommandError` op met de melding dat de module of het attribuut niet is gevonden.
- Als je het pad naar de `NinjaAPI`-instantie niet zeker weet, raadpleeg dan de `urls.py` van je project of andere gerelateerde bestanden om te vinden waar de `NinjaAPI` wordt geïnstantieerd.



#### Methode 1: Bekijk de URL-configuratie van het project
Doorgaans worden de URL-routes van een Django-project geconfigureerd in het bestand `urls.py`. Open de `urls.py` van het project en zoek het deel dat te maken heeft met `/api/`. Bijvoorbeeld:

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


In dit voorbeeld:
- `api` is een `NinjaAPI`-instantie.
- Deze is gedefinieerd in de module `project.api` (ervan uitgaande dat de projecthoofdmap `project` is).

Daarom moet de equivalente `--api`-parameter zijn:
```shell script
--api project.api.api
```


### Samenvatting
Om het gedrag van `resolve("/coast/api/")` na te bootsen, moet je het modulepad weten van de `NinjaAPI`-instantie waaraan het pad `/coast/api/` is gekoppeld, en dit doorgeven als waarde van de `--api`-parameter. Bijvoorbeeld:

```shell script
python manage.py export_openapi_schema --api project.api.api
```


Als je niet zeker weet waar de instantie zich bevindt, bekijk dan het bestand `urls.py` van het project of bevestig dit via debugging.
