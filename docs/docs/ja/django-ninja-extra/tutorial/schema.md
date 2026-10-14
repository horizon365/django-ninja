---
comments: true
---
Django-Ninja と Pydantic の統合は、Django-Ninja の最も優れた機能のひとつです。
Pydantic を使えば、API に入出力されるデータをバリデーションでき、しかも非常に高速です。DRF シリアライザの機能の一部を置き換えることができます。

しかし、DRF シリアライザを完全に置き換えたいのであれば、必要なのは **Ninja-Schema** です。

## Ninja Schema

Ninja Schema は、Django ORM モデルを、より多くの Pydantic 機能をサポートする Pydantic スキーマに変換します。

**インスピレーション**: [django-ninja](https://django-ninja.cn/) と [djantic](https://jordaneremieff.github.io/djantic/)

**主な機能：**

- **カスタムフィールドのサポート**: Ninja Schema は Django モデルをネイティブな Pydantic 型に変換するため、高速なフィールドバリデーションを直接利用できます。たとえば、enum、メールアドレス、IP アドレス、URL、JSON などが含まれます。
- **フィールドバリデータ**: フィールドは、Pydantic の **[validator](https://pydantic.com.cn/usage/validators/)** や **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)** と同じように、**model_validator** を使ってバリデーションできます。

!!! info
    詳しくは [Ninja Schema](https://pypi.org/project/ninja-schema/) をご覧ください。

## スキーマ内でのリクエストオブジェクトへのアクセス
Django Ninja Extra は、リクエストのライフサイクル中に利用できる `RouteContext` オブジェクトを提供します。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
