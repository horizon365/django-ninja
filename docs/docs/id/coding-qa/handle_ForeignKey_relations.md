---
comments: true
---
# Cara Menangani Field ForeignKey

## Masalah: CreateView menyertakan sebuah ForeignKey, dan Anda ingin mengirimkan foreign key seperti `author_id`, tetapi muncul error

## Reproduksi Kode
models.py
```python
from django.contrib.auth.models import User
from django.db import models
class Article(models.Model):
    title = models.CharField(verbose_name="Title", max_length=100)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name

```
schema.py
```python
from ninja import ModelSchema
class ArticleIn(ModelSchema):
    class Meta:
        model = Article
        fields = ['title', 'author_id']


class ArticleOut(ModelSchema):
    class Meta:
        model = Article
        fields = '__all__'
```
views.py
```python
from ninja_crud import views, viewsets
from ninja import Router
from .schema import ArticleIn, ArticleOut

route = Router()

class ArticleViewSet(viewsets.APIViewSet):
    router = route
    model = Article
    default_request_body = ArticleIn
    default_response_body = ArticleOut
    create_view = views.CreateView()
    read_view = views.ReadView()
    update_view = views.UpdateView()
    delete_view = views.DeleteView()
```

## Melakukan Network Request

Request body
```json
{
  "title": "string",
  "author_id": 12
}
```

Respons
```text
Traceback (most recent call last):
  File "/Users/yiqun/Venv/repgpt_be/lib/python3.10/site-packages/ninja/operation.py", line 107, in run
    result = self.view_func(request, **values)
  File "/Users/yiqun/Venv/repgpt_be/lib/python3.10/site-packages/ninja_crud/views/api_view.py", line 284, in wrapped_view_function
    return self.view_function(
  File "/Users/yiqun/Venv/repgpt_be/lib/python3.10/site-packages/ninja_crud/views/create_view.py", line 198, in default_view_function
    setattr(instance, field, value)
  File "/Users/yiqun/Venv/repgpt_be/lib/python3.10/site-packages/django/db/models/fields/related_descriptors.py", line 215, in __set__
    raise ValueError(
ValueError: Cannot assign "12": "Article.author" must be a "User" instance.

```
## Analisis Masalah
Dari analisis model, "Article.author" harus berupa instance "User", tetapi frontend hanya mengirimkan nilai int.
Selain itu, frontend hampir tidak mungkin mengirimkan nilai ini secara langsung kepada Anda, jadi kita perlu mengkustomisasi `request_body` milik `CreateView` agar dapat menerima integer.

schema.py
```python
class NewArticleIn(Schema):
    author_id: int
    title: str
```


```python hl_lines="10"
from ninja_crud import views, viewsets
from ninja import Router
from .schema import ArticleIn, ArticleOut

route = Router()

class ArticleViewSet(viewsets.APIViewSet):
    router = route
    model = Article
    default_request_body = ArticleIn
    default_response_body = ArticleOut
    create_view = views.CreateView(request_body=NewArticleIn)
    read_view = views.ReadView()
    update_view = views.UpdateView()
    delete_view = views.DeleteView()
```
Sumber masalah: Pertanyaan dari anggota komunitas

[Link issue terkait](https://github.com/hbakri/django-ninja-crud/issues/240)

Akhir dari issue ini.

Jika Anda memiliki pertanyaan, silakan tinggalkan komentar, atau bergabung ke grup diskusi melalui link di pojok kanan atas halaman.

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" alt="relax for django-ninja" src="https://picsum.photos/825/47.jpg">
