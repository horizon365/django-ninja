
To do development work on Ninja JWT, create your own fork on Github,
clone it locally, create and activate a virtual environment for it, then inside the project directory:

After that, install flit

```shell
$(venv) pip install flit
```

Install the development libraries and pre-commit hooks used for code linting and style

```shell
$(venv) make install
```

To run the tests:

```shell
$(venv) make test
```

To run the tests with coverage:

```shell
$(venv) make test-cov
```

!!! success

    This concludes the tutorial!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
