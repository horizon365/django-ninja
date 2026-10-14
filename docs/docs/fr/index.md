---
title: Django Ninja - Framework REST rapide pour Django
template: home.html
comments: true
---

Django Ninja est un framework web pour construire des API avec Django et les annotations de types de Python 3.6+.

Caractéristiques principales :

 - **Facile à comprendre** : conçu pour être facile à utiliser et intuitif.
 - **Exécution rapide** : grâce à **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** et à la **<a href="guides/async-support/">prise en charge de l'asynchrone</a>**, il offre de très hautes performances.
 - **Code rapide à écrire** : Django Ninja est un framework web pour construire des API avec Django et les annotations de types de Python 3.6+.
 - **Basé sur les standards** : fondé sur les standards : **OpenAPI** (anciennement Swagger) et **JSON Schema**.
 - **Compatible avec Django** : (évidemment) s'intègre bien au cœur de Django et à l'ORM.
 - **Prêt pour la production** : utilisé par de nombreuses entreprises dans de vrais projets (si vous utilisez Django Ninja et souhaitez publier votre retour d'expérience, veuillez écrire à ppr.vitaly@gmail.com).

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">Benchmarks</a> :

![Django Ninja REST Framework](img/benchmark.png)

## Installation

```
pip install django-ninja
```

## Exemple rapide

Démarrez un nouveau projet Django (ou utilisez-en un existant)
```
django-admin startproject apidemo
```

Dans `urls.py`

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

Maintenant, exécutez-le comme d'habitude :
```
./manage.py runserver
```

Remarque : vous n'avez pas besoin d'ajouter Django Ninja à vos applications installées pour qu'il fonctionne.

## Vérifiez-le

Ouvrez votre navigateur à l'adresse <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

Vous verrez la réponse JSON suivante :
```JSON
{"result": 3}
```
Vous venez de créer une API qui :

 - Reçoit une requête HTTP GET sur `/api/add`
 - Reçoit, valide et convertit les types des paramètres GET `a` et `b`
 - Encode le résultat en JSON
 - Génère un schéma OpenAPI pour l'opération définie

## Documentation interactive de l'API

Rendez-vous maintenant à l'adresse <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Vous verrez la documentation interactive de l'API générée automatiquement (fournie par <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> ou <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>) :

![Swagger UI](img/index-swagger-ui.png)


## Résumé

En résumé, vous ne déclarez les types des paramètres, des corps de requête, etc. qu'**une seule fois**, comme arguments de fonction.

Vous le faites avec des types Python standard et modernes.

Vous n'avez pas à apprendre une nouvelle syntaxe, les méthodes ou classes d'une bibliothèque spécifique, etc.

Juste du **Python 3.6+** standard.

Par exemple, pour un `int` :

```python
a: int
```

Ou, pour un modèle `Item` plus complexe :

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...avec cette seule déclaration, vous obtenez :

* La prise en charge par l'éditeur, notamment :
    * L'autocomplétion
    * La vérification des types
* La validation des données :
    * Des erreurs automatiques et claires lorsque les données sont invalides
    * La validation même pour des objets JSON profondément imbriqués
* La <abbr title="Also known as: serialization, parsing, marshalling">sérialisation</abbr> des données d'entrée réseau et leur conversion en données Python, ainsi que la lecture depuis :
    * JSON
    * Les paramètres de chemin (path)
    * Les paramètres de requête (query)
    * Les cookies
    * Les en-têtes (headers)
    * Les formulaires
    * Les fichiers
* Une documentation interactive de l'API générée automatiquement

Ce projet a été fortement inspiré par <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>.

!!! note

    Consultez le **[Tutoriel](tutorial/index.md)** pour démarrer rapidement.

    L'écosystème autour de Django Ninja :

    1. [django-ninja](index.md) : un framework basé sur Django qui prend le meilleur de Django et l'associe à la puissance de Pydantic — le choix optimal à l'intersection de la sécurité et de la commodité.

    2. [django-ninja-crud](django-ninja-crud/index.md) : un framework construit sur django-ninja pour simplifier le développement d'interfaces CRUD, offrant des model viewsets déclaratifs et des méthodes de test par scénarios.

    3. [django-ninja-extra](django-ninja-extra/index.md) : un outil qui permet aux développeurs de s'affranchir de la documentation Django verbeuse et de construire rapidement des applications web puissantes et des interfaces API modernes avec un minimum de code.

    4. [django-ninja-jwt](django-ninja-jwt/index.md) : un plugin JSON Web Token pour django-ninja qui implémente l'authentification et les fonctionnalités associées, forké d'un plugin populaire de Django Rest Framework.
