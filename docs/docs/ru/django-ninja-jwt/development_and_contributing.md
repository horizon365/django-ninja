
Чтобы заниматься разработкой Ninja JWT, создайте собственный форк на Github,
клонируйте его локально, создайте и активируйте для него виртуальное окружение, затем внутри каталога проекта:

После этого установите flit

```shell
$(venv) pip install flit
```

Установите библиотеки для разработки и pre-commit хуки, используемые для линтинга кода и проверки стиля

```shell
$(venv) make install
```

Чтобы запустить тесты:

```shell
$(venv) make test
```

Чтобы запустить тесты с покрытием:

```shell
$(venv) make test-cov
```

!!! success

    На этом руководство завершается!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
