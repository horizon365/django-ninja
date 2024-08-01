---
comments: true
---
Django-Ninja　与 Pydantic 的集成是 Django-Ninja　的最佳特性这一。
借助 Pydantic你可以验证来自你 API 的数据流入和流出，而且速度非常快。可以部分替代 DRF 序列化器。

但如果你想要完全替代 DRF 序列化器，那么你需要的是 **Ninja-Schema** 。

## Ninja Schema

Ninja Schema 将你的 Django ORM 模型转换为支持更多 Pydantic 特性的　Pydantic　schemas 。

**灵感来源**: [django-ninja](https://django-ninja.cn/) and [djantic](https://jordaneremieff.github.io/djantic/)

**主要特性：**

- **自定义字段支持**: Ninja 模式将 Django 模型转换为原生的 Pydantic 类型，这使你可以直接获得快速的字段验证。例如枚举、电子邮件、IP 地址、URL、JSON 等。
- **字段验证器**: 字段可以像 Pydantic 的**[validator](https://pydantic-docs.helpmanual.io/usage/validators/)** 或 **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)**　一样使用 **model_validator** 进行验证。

!!! info
    访问 [Ninja Schema](https://pypi.org/project/ninja-schema/) 获取更多信息

## 在模式中访问请求对象
Django Ninja Extra 提供了 `RouteContext` 对象，该对象在请求生命周期内可用。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
