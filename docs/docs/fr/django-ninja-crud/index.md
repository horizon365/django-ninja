Documentation de Django Ninja CRUD
=======================

![Django Ninja CRUD](../img/django-ninja-crud-cover.JPG)


Django Ninja CRUD est un framework puissant, déclaratif, mais légèrement opinionné, qui simplifie le développement d'endpoints CRUD (Create, Read, Update, Delete) avec Django Ninja, et fournit également une approche déclarative et basée sur des scénarios pour tester ces endpoints à l'aide de Django REST Testing (le petit frère de ce paquet)🐣. Il vous permet de définir des endpoints courants sous forme de vues basées sur des classes et de les personnaliser facilement selon les conventions de votre projet, ainsi que de créer facilement vos propres vues personnalisées et de les déclarer aux côtés des vues CRUD fournies, favorisant ainsi la modularité et l'extensibilité. Ce paquet encourage à se concentrer sur ce qui compte le plus : résoudre des problèmes concrets, plutôt que de réinventer la roue tout au long de votre projet.


Initialement inspiré du ModelViewSet de DRF, Django Ninja CRUD a évolué pour remédier à ses limites, adoptant une approche de composition plutôt qu'héritage pour atteindre une véritable modularité — une étape fondamentale vers une interface déclarative plus large de création d'endpoints.


Principaux défis des viewsets basés sur l'héritage :

*     Unicité des endpoints CRUD par modèle : Django Ninja CRUD vous permet de définir plusieurs endpoints pour le même modèle, permettant le versionnage ou des représentations alternatives.
*     Flexibilité de personnalisation : au lieu de surcharger des méthodes sur une classe monolithique, des vues individuelles sont personnalisées par composition et configuration.
*     Relations implicites dans les hiérarchies d'héritage : la composition découple les vues, réduisant les dépendances et améliorant la réutilisabilité.
*     Manque de modularité pour les nouveaux endpoints : l'ajout d'endpoints personnalisés ne nécessite plus de créer une sous-classe de l'ensemble du viewset, ce qui facilite l'introduction incrémentale de nouvelles fonctionnalités.

✨ Fonctionnalités clés
-------

*     Purement déclaratif : définissez des vues et des tests en déclarant ce que vous voulez, plutôt que comment le faire.
*     Modularité inégalée : personnalisez les viewsets avec les vues CRUD souhaitées, en personnalisant le comportement de chaque vue.
*     Facile à étendre : créez vos propres vues personnalisées et utilisez-les comme composants réutilisables aux côtés des vues CRUD fournies.
*     Framework de test basé sur des scénarios : exploitez le framework de test basé sur des scénarios pour définir divers cas de test de manière déclarative et concise.
*     Concentrez-vous sur l'essentiel : passez plus de temps à résoudre des problèmes concrets et moins sur les tâches courantes et répétitives.

> **
> Django Ninja CRUD est plus qu'un outil ; c'est un changement de paradigme dans le développement et le test d'applications web Django.**

🫶 Soutien
----------


Tout d'abord, remerciements sincères aux 400+ stargazers pour leur soutien à ce projet. Votre reconnaissance et votre confiance dans son potentiel me motivent à continuer de maintenir et d'améliorer ce travail, le rendant plus visible pour les nouveaux utilisateurs et contributeurs potentiels.

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


Si vous avez bénéficié de ce projet ou que vous appréciez le dévouement qui le sous-tend, envisagez d'offrir un soutien supplémentaire. Qu'il s'agisse du prix d'un café, d'un mot d'encouragement ou d'un parrainage, chaque geste alimente le feu de l'open source et le fait briller davantage.✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


Votre gentillesse et votre soutien comptent beaucoup. Merci !🙏
