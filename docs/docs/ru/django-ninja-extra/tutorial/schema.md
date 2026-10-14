---
comments: true
---
Интеграция Django-Ninja с Pydantic — одна из лучших возможностей Django-Ninja.
С помощью Pydantic вы можете валидировать данные, поступающие в API и выходящие из него, причём это происходит очень быстро. Он может частично заменить сериализаторы DRF.

Но если вы хотите полностью заменить сериализаторы DRF, то то, что вам нужно, — это **Ninja-Schema**.

## Ninja Schema

Ninja Schema преобразует ваши модели Django ORM в Pydantic-схемы, поддерживающие больше возможностей Pydantic.

**Вдохновение**: [django-ninja](https://django-ninja.cn/) и [djantic](https://jordaneremieff.github.io/djantic/)

**Ключевые возможности:**

- **Поддержка пользовательских полей**: Ninja Schema преобразует модели Django в нативные типы Pydantic, что позволяет сразу получать быструю валидацию полей. Примеры включают перечисления (enum), адреса электронной почты, IP-адреса, URL, JSON и т.д.
- **Валидаторы полей**: Поля могут валидироваться с помощью **model_validator**, подобно **[validator](https://pydantic.com.cn/usage/validators/)** или **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)** в Pydantic.

!!! info
    Посетите [Ninja Schema](https://pypi.org/project/ninja-schema/) для получения дополнительной информации

## Доступ к объекту запроса в схемах
Django Ninja Extra предоставляет объект `RouteContext`, который доступен на протяжении жизненного цикла запроса.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
