
Pour travailler sur le développement de Ninja JWT, créez votre propre fork sur Github,
clonez-le localement, créez et activez un environnement virtuel pour celui-ci, puis dans le répertoire du projet :

Ensuite, installez flit

```shell
$(venv) pip install flit
```

Installez les bibliothèques de développement et les hooks pre-commit utilisés pour le linting du code et le style

```shell
$(venv) make install
```

Pour exécuter les tests :

```shell
$(venv) make test
```

Pour exécuter les tests avec la couverture :

```shell
$(venv) make test-cov
```

!!! success

    Ceci conclut le tutoriel !

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
