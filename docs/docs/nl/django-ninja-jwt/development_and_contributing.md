
Om ontwikkelwerk aan Ninja JWT te doen, maak je je eigen fork op Github,
kloon je deze lokaal, maak en activeer je een virtuele omgeving ervoor, en voer je vervolgens in de projectmap het volgende uit:

Daarna installeer je flit

```shell
$(venv) pip install flit
```

Installeer de ontwikkelbibliotheken en pre-commit hooks die worden gebruikt voor code-linting en stijl

```shell
$(venv) make install
```

Om de tests uit te voeren:

```shell
$(venv) make test
```

Om de tests uit te voeren met coverage:

```shell
$(venv) make test-cov
```

!!! success

    Hiermee eindigt de tutorial!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
