---
comments: true
---
The integration of Django-Ninja with Pydantic is one of the best features of Django-Ninja.
With Pydantic, you can validate the data flowing in and out of your API, and it is very fast. It can partially replace DRF serializers.

But if you want to completely replace DRF serializers, then what you need is **Ninja-Schema**.

## Ninja Schema

Ninja Schema converts your Django ORM models into Pydantic schemas that support more Pydantic features.

**Inspiration**: [django-ninja](https://django-ninja.cn/) and [djantic](https://jordaneremieff.github.io/djantic/)

**Key Features:**

- **Custom Field Support**: Ninja Schema converts Django models to native Pydantic types, which allows you to get fast field validation directly. Examples include enums, emails, IP addresses, URLs, JSON, etc.
- **Field Validators**: Fields can be validated using **model_validator** just like Pydantic's **[validator](https://pydantic.com.cn/usage/validators/)** or **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)**.

!!! info
    Visit [Ninja Schema](https://pypi.org/project/ninja-schema/) for more information

## Accessing the Request Object in Schemas
Django Ninja Extra provides a `RouteContext` object that is available during the request lifecycle.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
