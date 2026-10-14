
Ninja JWT पर development work करने के लिए, Github पर अपना स्वयं का fork बनाएं,
इसे locally clone करें, इसके लिए एक virtual environment बनाएं और activate करें, फिर project directory के भीतर:

उसके बाद, flit install करें

```shell
$(venv) pip install flit
```

Code linting और style के लिए उपयोग की जाने वाली development libraries और pre-commit hooks install करें

```shell
$(venv) make install
```

Tests चलाने के लिए:

```shell
$(venv) make test
```

Coverage के साथ tests चलाने के लिए:

```shell
$(venv) make test-cov
```

!!! success

    यह tutorial यहीं समाप्त होता है!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
