---
comments: true
---
L'intégration de Django-Ninja avec Pydantic est l'une des meilleures fonctionnalités de Django-Ninja.
Avec Pydantic, vous pouvez valider les données entrant et sortant de votre API, et c'est très rapide. Il peut remplacer partiellement les serializers de DRF.

Mais si vous souhaitez remplacer complètement les serializers de DRF, alors ce qu'il vous faut est **Ninja-Schema**.

## Ninja Schema

Ninja Schema convertit vos modèles Django ORM en schémas Pydantic qui prennent en charge davantage de fonctionnalités Pydantic.

**Inspirations** : [django-ninja](https://django-ninja.cn/) et [djantic](https://jordaneremieff.github.io/djantic/)

**Fonctionnalités clés :**

- **Prise en charge des champs personnalisés** : Ninja Schema convertit les modèles Django en types Pydantic natifs, ce qui vous permet d'obtenir une validation de champs rapide et directe. Exemples : enums, e-mails, adresses IP, URLs, JSON, etc.
- **Validateurs de champs** : les champs peuvent être validés à l'aide de **model_validator**, tout comme le **[validator](https://pydantic.com.cn/usage/validators/)** ou le **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)** de Pydantic.

!!! info
    Consultez [Ninja Schema](https://pypi.org/project/ninja-schema/) pour plus d'informations

## Accès à l'objet Request dans les schémas
Django Ninja Extra fournit un objet `RouteContext` disponible durant le cycle de vie de la requête.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
