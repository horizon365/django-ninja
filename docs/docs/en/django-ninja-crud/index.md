Django Ninja CRUD Docs
=======================

![Django Ninja CRUD](../img/django-ninja-crud-cover.JPG)


Django Ninja CRUD is a powerful, declarative, yet slightly opinionated framework that simplifies the development of CRUD (Create, Read, Update, Delete) endpoints with Django Ninja, and also provides a declarative, scenario-based approach for testing these endpoints using Django REST Testing (this package's little sibling)🐣. It allows you to define common endpoints as class-based views and easily customize them according to your project's conventions, and to easily create your own custom views and declare them alongside the provided CRUD views, thereby promoting modularity and extensibility. This package encourages focusing on what matters most: solving real-world problems, rather than reinventing the wheel throughout your project.


Originally inspired by DRF's ModelViewSet, Django Ninja CRUD evolved to address its limitations, adopting a composition-over-inheritance approach to achieve true modularity — a foundational step toward a broader declarative interface for creating endpoints.


Main challenges with inheritance-based viewsets:

*     Uniqueness of CRUD endpoints per model: Django Ninja CRUD allows you to define multiple endpoints for the same model, enabling versioning or alternative representations.
*     Customization flexibility: instead of overriding methods on a monolithic class, individual views are customized through composition and configuration.
*     Implicit relationships within inheritance hierarchies: composition decouples views, reducing dependencies and improving reusability.
*     Lack of modularity for new endpoints: adding custom endpoints no longer requires subclassing the entire viewset, making it easier to introduce new features incrementally.

✨ Key Features
-------

*     Purely declarative: define views and tests by declaring what you want, rather than how to do it.
*     Unmatched modularity: customize viewsets with the desired CRUD views, customizing the behavior of each view.
*     Easy to extend: create your own custom views and use them as reusable components alongside the provided CRUD views.
*     Scenario-based testing framework: leverage the scenario-based testing framework to define diverse test cases in a declarative and concise manner.
*     Focus on what matters: spend more time solving real-world problems and less on common, repetitive tasks.

> **
> Django Ninja CRUD is more than a tool; it is a paradigm shift in Django web application development and testing.**

🫶 Support
----------


First of all, heartfelt thanks to the 400+ stargazers for supporting this project. Your recognition of and trust in its potential motivates me to continue maintaining and improving this work, making it more visible to new potential users and contributors.

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


If you have benefited from this project or appreciate the dedication behind it, consider offering further support. Whether it's the price of a coffee, a word of encouragement, or a sponsorship, every gesture adds fuel to the open source fire and makes it shine brighter.✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


Your kindness and support mean a lot. Thank you!🙏
