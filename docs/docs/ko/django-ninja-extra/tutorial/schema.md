---
comments: true
---
Django-Ninja와 Pydantic의 통합은 Django-Ninja의 가장 훌륭한 기능 중 하나입니다.
Pydantic을 사용하면 API로 들어오고 나가는 데이터를 검증할 수 있으며, 매우 빠릅니다. DRF 시리얼라이저를 일부 대체할 수 있습니다.

하지만 DRF 시리얼라이저를 완전히 대체하고 싶다면, 필요한 것은 **Ninja-Schema**입니다.

## Ninja Schema

Ninja Schema는 Django ORM 모델을 더 많은 Pydantic 기능을 지원하는 Pydantic 스키마로 변환합니다.

**영감**: [django-ninja](https://django-ninja.cn/) 및 [djantic](https://jordaneremieff.github.io/djantic/)

**주요 기능:**

- **커스텀 필드 지원**: Ninja Schema는 Django 모델을 네이티브 Pydantic 타입으로 변환하므로, 빠른 필드 검증을 바로 얻을 수 있습니다. 예를 들어 enum, 이메일, IP 주소, URL, JSON 등이 있습니다.
- **필드 검증기**: Pydantic의 **[validator](https://pydantic.com.cn/usage/validators/)** 또는 **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)**처럼 **model_validator**를 사용하여 필드를 검증할 수 있습니다.

!!! info
    자세한 내용은 [Ninja Schema](https://pypi.org/project/ninja-schema/)를 참고하세요

## 스키마에서 요청 객체 접근하기
Django Ninja Extra는 요청 라이프사이클 동안 사용할 수 있는 `RouteContext` 객체를 제공합니다.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
