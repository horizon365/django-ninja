Comment exporter un fichier de schéma avec `export_openapi_schema` après avoir personnalisé le chemin d'API de premier niveau
==========================================================
La route de premier niveau par défaut dans ninja est `'api'`. Supposons que vous la changiez en `'coast/api'` puis que vous exécutiez
`python manage.py export_openapi_schema`, une erreur sera levée.

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
Cela se produit parce que le code source suppose par défaut `api = resolve("/api/").func.keywords["api"]`.
Si votre route de premier niveau n'est pas `/api/`, vous devez la spécifier via le paramètre `--api`. Ce paramètre est chargé via `import_string(api_path)`, il doit donc s'agir du chemin d'import de l'instance `NinjaAPI`.
Par exemple, dans mon projet, il s'agit de `'website.utils.tools.api.ninja_api'`. Si vous ne le trouvez pas, cherchez dans `urls.py` la variable devant `add_router` ou `urls` — c'est ce que vous cherchez.

Connaissances supplémentaires :

## Moi
Dans ce code, si le paramètre `--api` est passé en ligne de commande, quel doit être son format ?



## Assistant IA
Dans ce code, le paramètre `--api` est utilisé pour spécifier un module d'instance d'API. Selon les commentaires et la docstring du code, le format du paramètre `--api` doit être un **chemin de module** — plus précisément, un chemin de module Python qui peut être résolu par la fonction `import_string` de Django.

### Format
```shell script
--api <module_path>
```


### Exemple
Supposons que la structure de votre projet est la suivante :
```
project/
    urls.py
    api.py
```


Si l'instance `NinjaAPI` est définie dans le fichier `project/api.py` et que l'instance s'appelle `api`, vous pouvez passer le paramètre ainsi :
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### Remarques
1. `<module_path>` est un chemin de module Python pointant vers le module qui contient l'instance `NinjaAPI`.
2. La dernière partie du chemin est le nom de la variable de l'instance `NinjaAPI` dans le module (par exemple, `api`).
3. Si le paramètre `--api` n'est pas fourni, le code tente de récupérer dynamiquement l'instance `NinjaAPI` via `resolve("/api/")`. Si cela échoue, une erreur est levée, invitant l'utilisateur à la spécifier explicitement via le paramètre `--api`.

### Avertissements
- Assurez-vous que le chemin de module fourni est valide et qu'une instance `NinjaAPI` existe réellement dans le module. Sinon, le code lèvera une `CommandError` indiquant que le module ou l'attribut n'a pas été trouvé.
- Si vous n'êtes pas sûr du chemin de l'instance `NinjaAPI`, reportez-vous au fichier `urls.py` de votre projet ou à d'autres fichiers associés pour trouver où l'instance `NinjaAPI` est instanciée.



#### Méthode 1 : Examiner la configuration des URL du projet
En général, les routes URL d'un projet Django sont configurées dans le fichier `urls.py`. Ouvrez le fichier `urls.py` du projet et trouvez la partie liée à `/api/`. Par exemple :

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


Dans cet exemple :
- `api` est une instance de `NinjaAPI`.
- Elle est définie dans le module `project.api` (en supposant que le répertoire racine du projet est `project`).

Par conséquent, le paramètre `--api` équivalent devrait être :
```shell script
--api project.api.api
```


### Résumé
Pour reproduire le comportement de `resolve("/coast/api/")`, vous devez connaître le chemin du module de l'instance `NinjaAPI` vers laquelle le chemin `/coast/api/` pointe, et le passer comme valeur du paramètre `--api`. Par exemple :

```shell script
python manage.py export_openapi_schema --api project.api.api
```


Si vous n'êtes pas sûr de l'emplacement de l'instance, examinez le fichier `urls.py` du projet ou confirmez-le par le débogage.
