---
comments: true
---
# Foutafhandeling

**Django Ninja** stelt je in staat om aangepaste exception handlers te installeren om te bepalen hoe responses worden teruggegeven wanneer er fouten of afgehandelde exceptions optreden.

## Aangepaste exception handlers

Stel dat je een API bouwt die afhankelijk is van een externe service die op bepaalde momenten onbeschikbaar is. Je kunt die fout afhandelen en een vriendelijke response teruggeven aan de client (waarin je zegt dat ze later terug kunnen komen) in plaats van de standaard 500-fout te gooien wanneer de exception optreedt.
Om dit te bereiken, moet je:

 - 1) Een exception maken (of een bestaande gebruiken)
 - 2) De decorator api.exception_handler gebruiken


Voorbeeld:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

De exception handler functie ontvangt 2 argumenten:

 - **request** - het HTTP verzoek van Django
 - **exc** - de daadwerkelijke exception

De functie moet een HTTP response teruggeven

## Standaard exception handlers overriden

Standaard initialiseert **Django Ninja** de volgende exception handlers:


#### `ninja.errors.AuthenticationError`

Gegooid wanneer de authenticatiedata ongeldig is

#### `ninja.errors.ValidationError`

Gegooid wanneer de request data de validatie niet doorstaat

#### `ninja.errors.HttpError`

Wordt gebruikt om vanaf elke plek in de code een HTTP fout met een statuscode te gooien
#### `django.http.Http404`

De standaard 404 exception van Django (kan bijvoorbeeld worden teruggegeven met get_object_or_404)
#### `Exception`
 
Elke andere exception die niet door de applicatie wordt afgehandeld.
Standaardgedrag
 
  - **Als `settings.DEBUG` op `True` staat** - geeft een traceback in platte tekst terug (handig bij het debuggen in de console of Swagger UI)
  - **anders** - gebruikt het standaard mechanisme voor exception handling van Django (fouten loggen, e-mails sturen naar ADMINS)


### Standaard handlers overriden

Als je de standaarduitvoer van validatiefouten wilt wijzigen - override de ValidationError exception handler:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## HTTP responses gooien via exceptions

Als alternatief voor het maken van een aangepaste exception en het schrijven van een handler daarvoor - kun je ook een HTTP exception gooien, wat ertoe leidt dat er een HTTP response met de gewenste code wordt teruggegeven

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    Ga verder naar de volgende sectie **[URLs reverse-resolven](urls.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
