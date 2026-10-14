---
comments: true
---
## Introductie
Ik had al lang van JWT gehoord, maar had het nooit daadwerkelijk gebruikt. Onlangs, tijdens het onderzoeken van het tus-protocol voor hervatbare uploads, kwam ik uit bij het niveau van hooks-http, met als doel authenticatie tijdens bestandsuploads. Natuurlijk dacht ik aan het pakket `django-ninja-jwt`. Ik dacht dat het simpel zou zijn, maar na het lezen van de [Chinese documentatie](https://django-ninja.cn/django-ninja-jwt/) ontdekte ik dat het niet alleen simpel was — het was tot verbluffende mate kaal.

## Aan de slag

Volgens de gids hoef je alleen `dango-ninja-jwt` en `django-ninja-extra` te installeren, vervolgens `NinjaAPI` te vervangen door `njaExtraAPI`, en dat kost slechts één regel.

```python
api.register_controllers(NinjaJWTDefaultController)
```

Eerlijk gezegd verbijsterend.

Even wachten — laten we eerst naar de docs kijken. Er verschijnen drie nieuwe endpoints: `pair`, `refresh` en `verify`.
![JWT swagger UI token](../img/jwt-token.png)
Let op het slotpictogram in de rechterbovenhoek — dat komt later nog van pas. Het verschijnt alleen wanneer je de functie `JWTAuth` gebruikt.

### pair
De eerste is het `pair`-endpoint. Dit betekent dat het, nadat je een gebruikersnaam en wachtwoord hebt opgegeven, authenticatietokens en refreshtokens teruggeeft.
Het formaat van de request body is als volgt:
```json
{
  "password": "string",
  "username": "string"
}
```
Let op: hier staat `username` onderaan, wat iets anders is dan je misschien zou verwachten.
Na het klikken op Execute krijg je zoiets als dit:
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
Het `access`-token hierboven kan worden gebruikt voor authenticatie, maar heeft standaard een beperkte levensduur. Het `refresh`-token heeft een langere levensduur dan `access` en wordt gebruikt om een nieuw `access`-token te verkrijgen nadat het vorige is verlopen.
Na het verversen wordt het vorige `access`-token ongeldig gemaakt.

Op dit punt kun je `access` kopiëren naar het slotpictogram in de rechterbovenhoek. Zo kan elk endpoint op de huidige pagina het gebruiken, wat handig is voor het debuggen.
### verify
Je kunt naar het derde endpoint, `verify`, gaan om te controleren of het `access`-token geldig is.

Al met al bouwt `django-ninja-jwt` gewoon drie endpoints voor je, wat het handig maakt om tokens te verkrijgen, te verversen en te testen.

## Aanpassing
Alleen deze drie endpoints zijn niet genoeg — we moeten in elk geval authenticatie toevoegen aan onze eigen specifieke endpoints.
Wat je hier nodig hebt is `JWTAuth`; pas nadat je het gebruikt, verschijnt het slotpictogram.
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
En op het `some`-endpoint staat ook een los slotpictogram.
![JWT swagger UI token custom](../img/jwt-token-custom.png)
Voor het bovenstaande `some`-endpoint geldt: als authenticatie slaagt, reageert het met de gebruikersnaam van de momenteel ingelogde gebruiker. Als het mislukt, geeft het een 401-response terug.
Backend-ontwikkelaars moeten het frontendteam vertellen deze waarde mee te sturen — laat hen naar de sectie [pair](#pair) gaan om deze te verkrijgen en periodiek naar [refresh](#refresh) gaan om hem te verversen.

### De tokenlevensduur configureren

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### Verdere aanpassing
Als het gebruik van `@route.get('/some', auth=JWTAuth())` in je ninja-route niet aan je behoeften voldoet, kun je `authenticate` binnen de functie aanroepen.

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # If it fails, a 401 is raised internally
    if auth.authenticate(request, token):
        return request.auth.username

```
Het `token` hierboven moet je zelf uit het `request`-object halen.
