---
comments: true
---
# How to Handle ForeignKey Fields

## Problem: The CreateView includes a ForeignKey, and you want to pass a foreign key such as `author_id`, but it raises an error

## Code Reproduction
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

## Make a Network Request

Request body
```json
{
  "title": "string",
  "author_id": 12
}
```

Responses
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
## Problem Analysis
From the model analysis, "Article.author" must be a "User" instance, but the frontend only passed an int value.
Moreover, the frontend is unlikely to directly pass this value to you, so we need to customize the `request_body` of `CreateView` to allow an integer to be passed in.

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
Source of the issue: Community member question

[Related issue link](https://github.com/hbakri/django-ninja-crud/issues/240)

End of issue.

If you have any questions, please leave a comment, or join the discussion group via the link in the upper right corner of the page.

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" alt="relax for django-ninja" src="https://picsum.photos/825/47.jpg">
