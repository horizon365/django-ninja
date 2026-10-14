
Ninja JWT wordt geleverd met een applicatie die token-blacklist-functionaliteit biedt.
Om deze applicatie te gebruiken, neem je deze op in de lijst met geïnstalleerde applicaties in `settings.py`:

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

Zorg er ook voor dat je `python manage.py migrate` uitvoert om de migraties van de applicatie uit te voeren.

Als de blacklist-applicatie wordt gedetecteerd in `INSTALLED_APPS`, voegt Ninja JWT alle gegenereerde refresh tokens of sliding tokens toe aan de lijst met outstanding tokens.
Het controleert ook, voordat een refresh token of sliding token als geldig wordt beschouwd, of het token niet voorkomt in de token-blacklist.

De blacklist-applicatie van Ninja JWT gebruikt twee modellen: `OutstandingToken` en `BlacklistedToken` om de lijsten met outstanding tokens en blacklisted tokens te implementeren.
Voor beide modellen zijn model-admins gedefinieerd. Om een token aan de blacklist toe te voegen, zoek je het bijbehorende `OutstandingToken`-record in de admin,
en maak je vervolgens via de admin een `BlacklistedToken`-record aan dat naar het `OutstandingToken`-record verwijst.

Als alternatief kun je een token blacklisten door een instantie van een subklasse van `BlacklistMixin` aan te maken en de methode `blacklist` op die instantie aan te roepen:

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

Dit creëert een uniek outstanding token- en blacklistrecord voor de `jti`-claim van het token, of voor welke claim dan ook die is gespecificeerd door de instelling `JTI_CLAIM`.

De blacklist-applicatie biedt ook een managementcommando `flushexpiredtokens`, dat verlopen tokens uit zowel de outstanding-lijst als de blacklist verwijdert.
Je moet een cronjob instellen op je server of hostingplatform dat dit commando dagelijks uitvoert.

!!! success

    Ga verder naar het volgende hoofdstuk **[Ontwikkeling en Bijdragen](development_and_contributing.md)**.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
