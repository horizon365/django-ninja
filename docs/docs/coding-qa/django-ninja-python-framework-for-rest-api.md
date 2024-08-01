---
created: 2024-07-25T13:23:12 (UTC +08:00)
tags: []
source: https://medium.com/@mrclemrkz/django-ninja-python-framework-for-rest-api-83808d1037d0
author: Clement Fernando

---


Django-Ninja：用于 REST API 的 Python 框架
===========================================================



> 我最近想在 REST API 中构建一个非常简单的 CRUD 服务。不得不四处寻找，我发现了一个具有两个流行框架最佳功能的简单框架。那就是 Django-ninja……

* * *



TL;DR
-----


我最近想在 REST API 中构建一个非常简单的 CRUD 服务。不得不四处寻找，我发现了一个具有两个流行框架最佳功能的简单框架。那就是 Django-ninja；我认为它是 Django 和 FastAPI 的组合。

---
让我解释一下为什么我认为这是一种有益的方法。


至于强调我的背景，我是一名 Python Django 开发者，并且在 Flask 中做过一些项目。


随着 FastAPI 的流行，我想先尝试一下。所以我在这里按照文档运行了它的示例，感觉，嗯，这很酷。然后 Pydantic 的使用激发了我的热情。最重要的是，它是基于异步构建的。在 Swagger UI 上完美且轻松地生成 OpenAPI 让它更甜了。


这让我大开眼界。于是，我开始深入挖掘更多。


在那里我发现由于 FastAPI 不像 Django 那样“自带”，它仍然需要配置一个 ORM（SQLAlchemy 或 SQLModel），更不用说还需要另一个第三方包用于数据库迁移工具如 Alembic 了。


所以，我心里想，是否存在更多且更好的解决方案，配置更少且更稳定。其中可能仍有待被突出。然后我开始寻找。


我列出了所有选项中的一些（截至 2023 年 9 月时的 github 星数）：


Flask：64K 颗星——首次发布：2010 年 4 月 1 日


FastAPI：61.8K 星——首次发布：2018 年 12 月 5 日


Django Rest Framework：26.2K 颗星——首次发布：2005 年 7 月 21 日


Sanic：17.3K 颗星——首次发布：2016 年 10 月 23 日


Django Ninja：4.8K 颗星——首次发布：2020 年 12 月 20 日


所以，很明显我对 Django Ninja 产生了兴趣，以下是我认为它好的原因。

**Popularity**
--------------


Django-Ninja 是基于最受欢迎且明显的 Web 框架 Django 构建的。Django-Ninja 于 2020 年底首次发布，在短短 3 年左右的时间里获得了很高的人气。

**常见项目结构**
-----------


与 Flask 和 FastAPI 不同，Django 在创建时强制实施一种结构。然而，它在你希望如何维护项目方面更具灵活性。这是我喜欢 Django 的一点，它显著提高了另一个 Django 开发人员对项目的遵循性。


是的，Django Rest Framework（DRF）也可以做到这一点。但我确实说过“快速开发”对吧？谁会不喜欢简单而有条理的代码呢？这就是使用 Django-Ninja 的美妙之处。

**强大的 ORM**
------------


再次，与强大的核心框架（Django）相关联为 Django-Ninja 带来了名声。


相比于用安全性较差的方式自己编写 SQL 查询，我们倾向于使用 ORM。它有助于编写简单且安全的数据库调用。


然而，当然 Django ORM 和 SQLAlchemy ORM 之间的概念是不同的。Django ORM 使用活动记录方法，而 SQLAlchemy 使用数据映射器方法，这些将在稍后的另一个博客中详细解释。

**  

易开式 API 文档
-----------------


是的，DRF（Django Rest Framework）有自己的 API 文档。但在我看来 OpenAPI Swagger UI 要好得多。所以当我需要带有 DRF 的 Swagger UI 时，我使用了一个名为 drf-yasg 的 swagger 生成器包，它做得相当不错。


但就像 FastAPI 一样，在 Django-Ninja 中除了 url 函数之外，不需要再编写其他代码就能获得交互式 OpenAPI Swagger UI。

**Performance**
---------------


就像 FastAPI 一样，内置了对 Pydantic 的类型强制支持和异步执行。


Django-ninja 的文档没有忘记通过与 Flask、DRF 和 Django-ninja 之间的基准数据比较来吹嘘这一点。

**Faster delivery**
-------------------


同样，就像 FastAPI 一样，它可以用非常少的代码基础启动一个 REST API 服务。同时，它有助于根据你认为合适的自己的哲学方法轻松开发。这就是特权的美妙之处。


最小化且简洁的代码基础可提高高可读性。从而为更快实现提升直觉。


对此，您有什么评论、想法和意见？请在下面的评论中告诉我。


