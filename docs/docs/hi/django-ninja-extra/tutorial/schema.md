---
comments: true
---
Pydantic के साथ Django-Ninja का एकीकरण Django-Ninja की सर्वोत्तम features में से एक है।
Pydantic के साथ, आप अपने API में आने और बाहर जाने वाले data को validate कर सकते हैं, और यह बहुत तेज़ है। यह आंशिक रूप से DRF serializers को replace कर सकता है।

लेकिन यदि आप DRF serializers को पूरी तरह से replace करना चाहते हैं, तो आपको **Ninja-Schema** की आवश्यकता है।

## Ninja Schema

Ninja Schema आपके Django ORM models को उन Pydantic schemas में बदलता है जो अधिक Pydantic features का समर्थन करते हैं।

**प्रेरणा**: [django-ninja](https://django-ninja.cn/) और [djantic](https://jordaneremieff.github.io/djantic/)

**मुख्य Features:**

- **Custom Field समर्थन**: Ninja Schema Django models को native Pydantic types में बदलता है, जिससे आप सीधे तेज़ field validation प्राप्त कर सकते हैं। उदाहरणों में enums, emails, IP addresses, URLs, JSON आदि शामिल हैं।
- **Field Validators**: Fields को **model_validator** का उपयोग करके validate किया जा सकता है, बिल्कुल Pydantic के **[validator](https://pydantic.com.cn/usage/validators/)** या **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)** की तरह।

!!! info
    अधिक जानकारी के लिए [Ninja Schema](https://pypi.org/project/ninja-schema/) देखें

## Schemas में Request Object तक पहुँच
Django Ninja Extra एक `RouteContext` object प्रदान करता है जो request lifecycle के दौरान उपलब्ध होता है।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
