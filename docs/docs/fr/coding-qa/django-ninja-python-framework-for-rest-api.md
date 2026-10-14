---
created: 2024-07-25T13:23:12 (UTC +08:00)
tags: []
source: https://medium.com/@mrclemrkz/django-ninja-python-framework-for-rest-api-83808d1037d0
author: Clement Fernando

---


Django-Ninja : un framework Python pour les API REST
===========================================================



> Je voulais récemment construire un service CRUD très simple dans une API REST. Après quelques recherches, j'ai trouvé un framework simple qui combine les meilleures caractéristiques de deux frameworks populaires. Il s'agit de Django-ninja...

* * *


TL;DR
-----


Je voulais récemment construire un service CRUD très simple dans une API REST. Après quelques recherches, j'ai trouvé un framework simple qui combine les meilleures caractéristiques de deux frameworks populaires. Il s'agit de Django-ninja ; je le considère comme une combinaison de Django et de FastAPI.

---
Laissez-moi expliquer pourquoi je pense que c'est une approche bénéfique.


Pour souligner mon parcours, je suis un développeur Python Django et j'ai réalisé quelques projets en Flask.


Avec la popularité de FastAPI, je voulais d'abord l'essayer. J'ai donc exécuté ses exemples en suivant la documentation, et le sentiment fut : eh bien, c'est cool. Puis l'utilisation de Pydantic m'a enthousiasmé. Plus important encore, il est construit sur l'async. La génération parfaite et sans effort d'OpenAPI dans la Swagger UI l'a rendu encore plus agréable.


Cela m'a ouvert les yeux. J'ai donc commencé à creuser davantage.


Là, j'ai découvert que, comme FastAPI n'est pas « batteries-included » comme Django, il nécessite encore de configurer un ORM (SQLAlchemy ou SQLModel), sans parler du besoin d'un autre paquet tiers pour les outils de migration de base de données tels qu'Alembic.


Alors, je me suis demandé s'il existait une meilleure solution, avec moins de configuration et plus de stabilité. Il y avait peut-être quelque chose qui n'avait pas encore été mis en avant. J'ai donc commencé à chercher.


J'ai listé quelques-unes de toutes les options (étoiles GitHub à compter de septembre 2023) :


Flask : 64K étoiles — première version : 1er avril 2010


FastAPI : 61.8K étoiles — première version : 5 décembre 2018


Django Rest Framework : 26.2K étoiles — première version : 21 juillet 2005


Sanic : 17.3K étoiles — première version : 23 octobre 2016


Django Ninja : 4.8K étoiles — première version : 20 décembre 2020


Ainsi, clairement, je me suis intéressé à Django Ninja, et voici pourquoi je le trouve bon.

**Popularité**
--------------


Django-Ninja est construit sur Django, le framework web le plus populaire et le plus évident. Django-Ninja a été publié pour la première fois fin 2020 et, en environ 3 ans à peine, il a acquis une popularité significative.

**Structure de projet commune**
-----------


Contrairement à Flask et FastAPI, Django impose une structure lorsque vous créez un projet. Cependant, il est plus flexible quant à la manière dont vous souhaitez maintenir le projet. C'est quelque chose que j'aime chez Django, car cela améliore considérablement la facilité avec laquelle un autre développeur Django peut suivre le projet.


Oui, Django Rest Framework (DRF) peut aussi le faire. Mais j'ai bien dit « développement rapide », n'est-ce pas ? Qui n'aimerait pas un code simple et organisé ? C'est la beauté d'utiliser Django-Ninja.

**ORM puissant**
------------


Encore une fois, être associé au framework cœur puissant (Django) apporte de la réputation à Django-Ninja.


Plutôt que d'écrire nous-mêmes des requêtes SQL de manière moins sécurisée, nous avons tendance à utiliser des ORM. Cela aide à écrire des appels à la base de données simples et sécurisés.


Cependant, bien sûr, les concepts entre l'ORM Django et l'ORM SQLAlchemy sont différents. L'ORM Django utilise le pattern Active Record, tandis que SQLAlchemy utilise le pattern Data Mapper, ce qui sera expliqué en détail dans un autre blog plus tard.

**  
Documentation API facile à utiliser
-----------------


Oui, DRF (Django Rest Framework) a sa propre documentation API. Mais à mon avis, la Swagger UI d'OpenAPI est bien meilleure. Donc, quand j'avais besoin de Swagger UI avec DRF, j'utilisais un paquet générateur de swagger appelé drf-yasg, qui faisait un travail assez correct.


Mais comme FastAPI, dans Django-Ninja, vous pouvez obtenir une Swagger UI OpenAPI interactive sans écrire de code supplémentaire en dehors de la fonction url.

**Performance**
---------------


Tout comme FastAPI, il dispose d'un support intégré de typage strict via Pydantic et d'une exécution asynchrone.


La documentation de Django-ninja n'a pas oublié de s'en vanter en comparant les données de benchmark entre Flask, DRF et Django-ninja.

**Livraison plus rapide**
-------------------


Encore une fois, tout comme FastAPI, il peut mettre en place un service d'API REST avec très peu de code. En même temps, il vous aide à développer facilement selon l'approche philosophique que vous jugez appropriée. C'est la beauté du privilège.


Une base de code minimale et concise conduit à une haute lisibilité. Cela alimente à son tour l'intuition pour une implémentation plus rapide.


Quels sont vos commentaires, réflexions et opinions à ce sujet ? Faites-le-moi savoir dans les commentaires ci-dessous.
