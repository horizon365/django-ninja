---
comments: true
---
Die Integration von Django-Ninja mit Pydantic ist eine der besten Funktionen von Django-Ninja.
Mit Pydantic können Sie die Daten validieren, die in Ihre API hinein- und aus ihr herausfließen, und es ist sehr schnell. Es kann DRF-Serialisierer teilweise ersetzen.

Wenn Sie DRF-Serialisierer jedoch vollständig ersetzen möchten, dann brauchen Sie **Ninja-Schema**.

## Ninja Schema

Ninja Schema wandelt Ihre Django-ORM-Modelle in Pydantic-Schemas um, die weitere Pydantic-Funktionen unterstützen.

**Inspiration**: [django-ninja](https://django-ninja.cn/) und [djantic](https://jordaneremieff.github.io/djantic/)

**Hauptfunktionen:**

- **Unterstützung benutzerdefinierter Felder**: Ninja Schema wandelt Django-Modelle in native Pydantic-Typen um, was Ihnen eine schnelle Feldvalidierung direkt ermöglicht. Beispiele hierfür sind Enums, E-Mails, IP-Adressen, URLs, JSON usw.
- **Feld-Validatoren**: Felder können mit **model_validator** validiert werden, ganz wie Pydantics **[validator](https://pydantic.com.cn/usage/validators/)** oder **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)**.

!!! info
    Weitere Informationen finden Sie unter [Ninja Schema](https://pypi.org/project/ninja-schema/)

## Zugriff auf das Request-Objekt in Schemas
Django Ninja Extra stellt ein `RouteContext`-Objekt bereit, das während des Request-Lebenszyklus verfügbar ist.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
