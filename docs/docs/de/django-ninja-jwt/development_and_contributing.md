
Um an Ninja JWT zu entwickeln, erstellen Sie Ihren eigenen Fork auf Github,
klonen Sie ihn lokal, erstellen und aktivieren Sie eine virtuelle Umgebung dafür, und führen Sie dann im Projektverzeichnis Folgendes aus:

Installieren Sie danach flit

```shell
$(venv) pip install flit
```

Installieren Sie die Entwicklungs-Bibliotheken und Pre-Commit-Hooks, die für Code-Linting und Stil verwendet werden

```shell
$(venv) make install
```

Um die Tests auszuführen:

```shell
$(venv) make test
```

Um die Tests mit Coverage auszuführen:

```shell
$(venv) make test-cov
```

!!! success

    Damit ist das Tutorial abgeschlossen!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
