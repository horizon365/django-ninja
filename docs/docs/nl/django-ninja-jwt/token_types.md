
Ninja JWT biedt twee verschillende token types die gebruikt kunnen worden om authenticatie aan te tonen.
In de payload van een token kan het type worden geïdentificeerd aan de hand van de waarde van de token type claim, die standaard `token_type` is.
Deze kan echter de waarde `access`, `sliding` of `refresh` hebben,
maar momenteel worden refresh tokens niet beschouwd als geldige authenticatie tokens. De naam van de claim die wordt gebruikt om het type op te slaan, kan worden aangepast via de instelling `TOKEN_TYPE_CLAIM`.

Standaard verwacht Ninja JWT een `access` token om authenticatie aan te tonen.
De toegestane authenticatie token types worden bepaald door de waarde van de instelling `AUTH_TOKEN_CLASSES`.
Deze instelling bevat een lijst met dotted paths die verwijzen naar token classes. Standaard bevat deze het dotted path `'ninja_jwt.tokens.AccessToken'`,
maar kan ook het dotted path `'ninja_jwt.tokens.SlidingToken'` bevatten.
Een of beide van deze dotted paths kunnen voorkomen in de lijst met authenticatie token classes.
Als beide aanwezig zijn, dan kunnen beide token types worden gebruikt om authenticatie aan te tonen.

Sliding Tokens
==============

Sliding tokens bieden een handigere ervaring voor token gebruikers, maar dit gaat ten koste van minder beveiliging en, wanneer de blacklist app wordt gebruikt, lagere prestaties.
Een sliding token is een token dat zowel een expiratie claim als een refresh expiratie claim bevat. Zolang de timestamp in de expiratie claim van het sliding token nog niet is verstreken,
kan het worden gebruikt om authenticatie aan te tonen. Daarnaast, zolang de timestamp in de refresh expiratie claim nog niet is verstreken,
kan het ook worden ingediend bij de refresh view om een kopie van zichzelf te verkrijgen met een bijgewerkte expiratie claim.

Als je sliding tokens wilt gebruiken, wijzig dan de instelling `AUTH_TOKEN_CLASSES` naar `('ninja_jwt.tokens.SlidingToken',)`.
(Als alternatief, als je beide token types wilt toestaan voor authenticatie, kan de instelling `AUTH_TOKEN_CLASSES` dotted paths bevatten die verwijzen naar de token classes `AccessToken` en `SlidingToken`
in de module `ninja_jwt.tokens`)

Registreer daarnaast `NinjaJWTSlidingController` bij de `api`:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

Let op: als je de blacklist app gebruikt, zal Ninja JWT bij elk geauthenticeerd verzoek alle sliding tokens valideren tegen de blacklist.
Dit zal de prestaties van geauthenticeerde API views verslechteren.

!!! success

    Ga verder naar het volgende hoofdstuk **[Blacklist App](blacklist_app.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
