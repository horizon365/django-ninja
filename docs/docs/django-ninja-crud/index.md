Django Ninja CRUD 文档
=======================

![Django Ninja CRUD](https://raw.githubusercontent.com/hbakri/django-ninja-crud/main/docs/assets/images/django-ninja-crud-cover.png)


Django Ninja CRUD 是一个强大的、声明式的、但又有点固执己见的框架，它简化了使用 Django Ninja 开发 CRUD（创建、读取、更新、删除）端点的过程，并且还提供了一种声明式的基于场景的方法，用于使用 Django REST Testing（这个包的小弟）测试这些端点🐣。它允许您将常见的端点定义为基于类的视图，并轻松地根据项目的约定对其进行自定义，还可以轻松创建自己的自定义视图，并与提供的 CRUD 视图一起声明，从而促进了模块化和可扩展性。这个包提倡专注于最重要的事情：解决实际问题，而不是在整个项目中重新发明轮子。


最初受到 DRF 的 ModelViewSet 的启发，Django Ninja CRUD 为了解决其局限性而发展，采用了组合优于继承的方法来实现真正的模块化——这是为端点创建更广泛的声明式接口迈出的基础一步。


基于继承的视图集的主要挑战：

*     每个模型的 CRUD 端点的唯一性：Django Ninja CRUD 允许您为同一个模型定义多个端点，从而实现版本控制或其他表示方式。
*     定制灵活性：不是通过覆盖单体类上的方法，而是通过组合和配置来定制各个视图。
*     继承层次结构中的隐式关系：组合分离视图，减少依赖关系并提高可重用性。
*     新端点缺乏模块化：添加自定义端点不再需要继承整个视图集，从而更容易逐步引入新功能。

 ✨ 主要特点
-------

*     纯粹声明式：通过声明你想要的内容来定义视图和测试，而不是如何去做。
*     不匹配的模块性：使用所需的增删改查视图定制视图集，自定义每个视图的行为。
*     易于扩展：创建自己的自定义视图，并与提供的 CRUD 视图一起作为可重用组件使用。
*     基于场景的测试框架：利用基于场景的测试框架以声明式和简洁的方式定义多样化的测试用例。
*     聚焦重要事项：将更多时间用于解决实际问题，减少常见且重复的任务所花费的时间。

> **  
> Django Ninja CRUD 不仅仅是一个工具；它是 Django 网络应用程序开发和测试中的范式转变。**

🫶 Support
----------


首先，衷心感谢 400+ 的星空观测者对这个项目的支持。你们对其潜力的认可和信任激发了我继续维护和改进这个工作的动力，使其对新的潜在用户和贡献者更加可见。

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


如果你从这个项目中受益或赞赏其背后的奉献精神，考虑给予进一步的支持。无论是一杯咖啡的价格、一句鼓励的话，还是一份赞助，每一个举动都为开源之火增添燃料，使其更加闪耀。✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


您的善意和支持意义重大。谢谢！🙏
