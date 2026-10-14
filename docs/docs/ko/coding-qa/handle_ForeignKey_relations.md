---
comments: true
---
# ForeignKey 필드를 처리하는 방법

## 문제: CreateView에 ForeignKey가 포함되어 있고 `author_id`와 같은 외래 키를 전달하고 싶지만 오류가 발생합니다

## 코드 재현
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

## 네트워크 요청 만들기

요청 본문
```json
{
  "title": "string",
  "author_id": 12
}
```

응답
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
## 문제 분석
모델 분석에 따르면 "Article.author"는 "User" 인스턴스여야 하지만 프론트엔드는 int 값만 전달했습니다.
게다가 프론트엔드가 이 값을 직접 전달할 가능성은 낮으므로, 정수가 전달될 수 있도록 `CreateView`의 `request_body`를 커스터마이즈해야 합니다.

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
이슈 출처: 커뮤니티 회원 질문

[관련 이슈 링크](https://github.com/hbakri/django-ninja-crud/issues/240)

이슈 끝.

질문이 있으시면 댓글을 남기거나 페이지 오른쪽 상단의 링크를 통해 토론 그룹에 참여하세요.

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" alt="relax for django-ninja" src="https://picsum.photos/825/47.jpg">
