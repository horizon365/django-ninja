---
comments: true
---
# Inversion des URL

Chaque méthode dans un schéma Django Ninja (ou un `Router`) génère un nom d'URL inversée (reverse URL).

## Comment les URL sont générées

Ces URL sont toutes contenues dans un espace de noms (namespace), qui par défaut est `"api-1.0.0"`, et chaque nom d'URL correspond à la fonction qu'il décore.

Par exemple :

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

Ce nom d'URL implicite n'est défini que pour la première opération de chaque chemin d'API. Si vous ne voulez *pas* qu'un nom d'URL inversée implicite soit généré, spécifiez simplement `url_name=""` (une chaîne vide) sur le décorateur de méthode.

### Modifier le nom de l'URL

Au lieu d'utiliser le nom d'URL par défaut, vous pouvez le spécifier explicitement comme propriété sur le décorateur de méthode.
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

Cela remplacera tout nom d'URL implicite pour ce chemin d'API.


#### Redéfinir le nom d'URL par défaut

Vous pouvez également redéfinir la dénomination d'URL implicite en surchargeant la méthode `get_operation_url_name` :

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### Espace de noms personnalisé

L'espace de noms d'URL par défaut est construit en préfixant `"api-"` à la version du schéma, cependant vous pouvez spécifier explicitement l'espace de noms en surchargeant l'attribut `urls_namespace` de la classe de schéma NinjaAPI.
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    Poursuivez avec la section suivante **[Prise en charge asynchrone](async-support.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
