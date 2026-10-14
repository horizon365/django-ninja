So exportieren Sie eine Schema-Datei mit `export_openapi_schema`, nachdem Sie den API-Pfad auf oberster Ebene angepasst haben
==========================================================
Die Standard-Route auf oberster Ebene in ninja ist `'api'`. Angenommen, Sie ändern sie in `'coast/api'` und führen anschließend
`python manage.py export_openapi_schema` aus, dann wird ein Fehler ausgelöst.

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
Das passiert, weil der Quellcode standardmäßig `api = resolve("/api/").func.keywords["api"]` verwendet.
Wenn Ihre Route auf oberster Ebene nicht `/api/` ist, müssen Sie sie über den Parameter `--api` angeben. Dieser Parameter wird über `import_string(api_path)` geladen, daher muss er der Import-Pfad der `NinjaAPI`-Instanz sein.
Zum Beispiel ist es in meinem Projekt `'website.utils.tools.api.ninja_api'`. Wenn Sie ihn nicht finden können, schauen Sie in `urls.py` nach der Variablen vor `add_router` bzw. `urls` — genau diese ist gemeint.

Zusätzliches Wissen:

## Ich
In diesem Code: Wenn der Parameter `--api` über die Kommandozeile übergeben wird, welches Format sollte er dann haben?



## KI-Assistent
In diesem Code wird der Parameter `--api` verwendet, um ein API-Instanz-Modul anzugeben. Laut den Kommentaren und dem Docstring im Code sollte das Format des Parameters `--api` ein **Modulpfad** sein — genauer gesagt ein Python-Modulpfad, der von Djangos Funktion `import_string` aufgelöst werden kann.

### Format
```shell script
--api <module_path>
```


### Beispiel
Angenommen, Ihre Projektstruktur sieht wie folgt aus:
```
project/
    urls.py
    api.py
```


Wenn die `NinjaAPI`-Instanz in der Datei `project/api.py` definiert ist und die Instanz `api` heißt, können Sie den Parameter wie folgt übergeben:
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### Hinweise
1. `<module_path>` ist ein Python-Modulpfad, der auf das Modul zeigt, das die `NinjaAPI`-Instanz enthält.
2. Der letzte Teil des Pfads ist der Variablenname der `NinjaAPI`-Instanz in diesem Modul (zum Beispiel `api`).
3. Wenn der Parameter `--api` nicht angegeben wird, versucht der Code, die `NinjaAPI`-Instanz dynamisch über `resolve("/api/")` zu ermitteln. Schlägt dies fehl, wird ein Fehler ausgelöst, der den Benutzer auffordert, sie explizit über den Parameter `--api` anzugeben.

### Einschränkungen
- Stellen Sie sicher, dass der angegebene Modulpfad gültig ist und im Modul tatsächlich eine `NinjaAPI`-Instanz existiert. Andernfalls löst der Code einen `CommandError` aus, der angibt, dass das Modul oder Attribut nicht gefunden wurde.
- Wenn Sie den Pfad zur `NinjaAPI`-Instanz nicht kennen, sehen Sie sich die `urls.py` Ihres Projekts oder andere verwandte Dateien an, um herauszufinden, wo die `NinjaAPI` instanziiert wird.



#### Methode 1: URL-Konfiguration des Projekts prüfen
In der Regel werden die URL-Routen eines Django-Projekts in der Datei `urls.py` konfiguriert. Öffnen Sie die `urls.py` des Projekts und suchen Sie den Teil, der sich auf `/api/` bezieht. Zum Beispiel:

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


In diesem Beispiel:
- `api` ist eine `NinjaAPI`-Instanz.
- Sie ist im Modul `project.api` definiert (unter der Annahme, dass das Projektstammverzeichnis `project` ist).

Der äquivalente Parameter `--api` lautet daher:
```shell script
--api project.api.api
```


### Zusammenfassung
Um das Verhalten von `resolve("/coast/api/")` nachzubilden, müssen Sie den Modulpfad der `NinjaAPI`-Instanz kennen, auf die der Pfad `/coast/api/` abgebildet wird, und ihn als Wert des Parameters `--api` übergeben. Zum Beispiel:

```shell script
python manage.py export_openapi_schema --api project.api.api
```


Wenn Sie nicht sicher sind, wo sich die Instanz befindet, prüfen Sie die Datei `urls.py` des Projekts oder klären Sie es per Debugging.
