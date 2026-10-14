---
comments: true
---
De integratie van Django-Ninja met Pydantic is een van de beste functies van Django-Ninja.
Met Pydantic kun je de gegevens die in en uit je API stromen valideren, en het is erg snel. Het kan DRF-serializers gedeeltelijk vervangen.

Maar als je DRF-serializers volledig wilt vervangen, dan heb je **Ninja-Schema** nodig.

## Ninja Schema

Ninja Schema converteert je Django ORM-modellen naar Pydantic-schema's die meer Pydantic-functies ondersteunen.

**Inspiratie**: [django-ninja](https://django-ninja.cn/) en [djantic](https://jordaneremieff.github.io/djantic/)

**Belangrijkste functies:**

- **Ondersteuning voor aangepaste velden**: Ninja Schema converteert Django-modellen naar native Pydantic-types, waardoor je direct snelle veldvalidatie krijgt. Voorbeelden zijn enums, e-mails, IP-adressen, URL's, JSON, enz.
- **Veldvalidatoren**: Velden kunnen worden gevalideerd met **model_validator**, net zoals Pydantic's **[validator](https://pydantic.com.cn/usage/validators/)** of **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)**.

!!! info
    Bezoek [Ninja Schema](https://pypi.org/project/ninja-schema/) voor meer informatie

## Toegang tot het Request-object in Schema's
Django Ninja Extra biedt een object `RouteContext` dat beschikbaar is tijdens de levenscyclus van het request.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
