---
comments: true
---
# URLs reverse-resolven

Elke methode in een Django Ninja schema (of `Router`) genereert een reverse URL naam.

## Hoe URLs worden gegenereerd

Deze URLs bevinden zich allemaal in een namespace, die standaard `"api-1.0.0"` is, en elke URL naam komt overeen met de functie die hij decoreert.

Bijvoorbeeld:

```python
api = NinjaAPI()

@api.get("/")
def index(request):
    ...

index_url = reverse_lazy("api-1.0.0:index")
```

Deze impliciete URL naam wordt alleen ingesteld voor de eerste operatie op elk API path. Als je *geen* impliciete reverse URL naam wilt laten genereren, geef dan simpelweg `url_name=""` (een lege string) op bij de methode decorator.

### De URL naam wijzigen

In plaats van de standaard URL naam te gebruiken, kun je deze expliciet opgeven als property op de methode decorator.
```python
@api.get("/users", url_name="user_list")
def users(request):
    ...

users_url = reverse_lazy("api-1.0.0:user_list")
```

Dit overschrijft elke impliciete URL naam voor dit API path.


#### De standaard URL naam overriden

Je kunt de impliciete URL naamgeving ook overriden door de methode `get_operation_url_name` te overriden:

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + '_my_extra_suffix'

api = MyAPI()
```

### Aangepaste namespace

De standaard URL namespace wordt gebouwd door `"api-"` toe te voegen als voorvoegsel aan de versie van het schema, maar je kunt de namespace expliciet opgeven door het attribuut `urls_namespace` van de NinjaAPI schema class te overriden.
```python

api = NinjaAPI(auth=token_auth, version='2')
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')

api_users_url = reverse_lazy("api-2:users")
private_api_admins_url = reverse_lazy("private_api:admins")
```

!!! success

    Ga verder naar de volgende sectie **[Async ondersteuning](async-support.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
