---
comments: true
---
# URLs reversen

Jede Methode in einem Django-Ninja-Schema (oder `Router`) erzeugt einen Namen für die Reverse-URL.

## Wie URLs generiert werden

Diese URLs sind alle in einem Namespace enthalten, der standardmäßig `"api-1.0.0"` lautet, und jeder URL-Name entspricht der Funktion, die er dekoriert.

Zum Beispiel:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

Dieser implizite URL-Name wird nur für die erste Operation auf jedem API-Pfad gesetzt. Wenn Sie *keinen* impliziten Reverse-URL-Namen erzeugen möchten, geben Sie im Methoden-Dekorator einfach `url_name=""` (einen leeren String) an.

### Den URL-Namen ändern

Statt des Standard-URL-Namens können Sie ihn auch explizit als Property am Methoden-Dekorator angeben.
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

Dies überschreibt jeden impliziten URL-Namen für diesen API-Pfad.


#### Den Standard-URL-Namen überschreiben

Sie können die implizite URL-Benennung auch überschreiben, indem Sie die Methode `get_operation_url_name` überschreiben:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### Benutzerdefinierter Namespace

Der Standard-URL-Namespace wird gebildet, indem `"api-"` der Version des Schemas vorangestellt wird; Sie können den Namespace jedoch auch explizit angeben, indem Sie das Attribut `urls_namespace` der NinjaAPI-Schema-Klasse überschreiben.
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    Fahren Sie mit dem nächsten Abschnitt fort: **[Asynchrone Unterstützung](async-support.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
