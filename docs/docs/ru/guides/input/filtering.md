---
comments: true
---
# Фильтрация

Если вы хотите позволить пользователям фильтровать ваши queryset'ы по нескольким различным атрибутам, имеет смысл инкапсулировать фильтры в класс `FilterSchema`.
`FilterSchema` — это обычная `Schema`, поэтому она использует все необходимые возможности Pydantic, но при этом добавляет некоторые удобства
для простого преобразования пользовательских параметров фильтрации в запросы к базе данных.

Сначала определите подкласс `FilterSchema`:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


Затем используйте эту схему вместе с `Query` в вашем API-обработчике:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Как описано в разделе [Использование схемы для определения параметров запроса](./query-params.md#using-schema), Django Ninja превращает поля, определённые в `BookFilterSchema`, в параметры запроса.
Вы можете использовать краткую однострочную запись `.filter()`, чтобы применить эти фильтры к вашему queryset:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

«Под капотом» `FilterSchema` преобразует свои поля в [Q-выражения](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects), затем объединяет их и использует для фильтрации вашего queryset.


В качестве альтернативы, вместо метода `.filter`, вы можете получить подготовленное `Q`-выражение и выполнить фильтрацию самостоятельно.
Это может быть полезно, когда у вас есть дополнительная фильтрация queryset поверх той, что вы предоставляете пользователям через API:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

По умолчанию фильтры ведут себя следующим образом:

* значения `None` игнорируются, и фильтрация не применяется;
* каждое поле со значением не `None` преобразуется в `Q`-выражение в соответствии с определением `Field` этого поля;
* все `Q`-выражения объединяются в одно с помощью логического оператора `AND`;
* результирующее `Q`-выражение используется для фильтрации queryset, и вам возвращается queryset с применённым условием `.filter`.

## Пользовательские поля
По умолчанию `FilterSet` использует имя поля для генерации Q-выражения:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
Поле `name` будет преобразовано в выражение `Q(name=...)`.

Когда ваш запрос к базе данных сложнее, вы можете явно указать его с помощью ключевого аргумента `"q"` в определении поля:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
Вы даже можете указать несколько имён ключевых аргументов поиска в виде списка:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
По умолчанию выражения на уровне поля объединяются с помощью соединителя `"OR"`, поэтому при такой настройке параметр запроса `?search=foobar` будет искать книги, содержащие «foobar» в названии, имени автора или издателя.


## Объединение выражений
По умолчанию

* выражения на уровне поля объединяются оператором `OR`.
* сами поля объединяются оператором `AND`.

Итак, для следующего `FilterSchema`...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...и следующих параметров запроса от пользователя
```
http://localhost:8000/api/books?search=harry&popular=true
```
Экземпляр `FilterSchema` будет искать популярные книги, содержащие `harry` в названии книги _или_ в имени автора.


Вы можете настроить это поведение с помощью параметра `expression_connector` как в определениях на уровне поля, так и на уровне класса:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

Соединитель выражений может принимать значения `"OR"`, `"AND"` и `"XOR"`, но последний [поддерживается](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) только в Django 4.1.

Теперь запрос с такими параметрами
```
http://localhost:8000/api/books?name=harry&active=true
```
...будет искать книги, которые содержат `harry` в названии _или_ сами являются активными и опубликованы активным издателем.


## Фильтрация по значениям None
Вы можете заставить `FilterSchema` рассматривать `None` как допустимое значение, по которому следует выполнять фильтрацию.

Это можно сделать на уровне поля с помощью ключевого аргумента `ignore_none`:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

Таким образом, когда пользователь не указывает другое значение для `"tag"`, фильтр всегда будет включать условие `tag=None`.

Вы также можете задать это сразу для всех полей в конфигурации:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## Пользовательские выражения
Иногда у вас могут быть сложные сценарии фильтрации, которые невозможно обработать с помощью одной аннотации поля.
Для таких случаев вы можете реализовать логику фильтрации поля в виде пользовательского метода. Просто определите метод с именем `filter_<fieldname>`, который принимает значение фильтрации и возвращает Q-выражение:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
Такие методы полей имеют приоритет над тем, что указано в определении `Field()` соответствующего поля.
Если этого недостаточно, вы можете реализовать свою собственную логику фильтрации для всего класса `FilterSet` в методе `custom_expression`:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    popular: Optional[bool] = None

    def custom_expression(self) -> Q:
        q = Q()
        if self.name:
            q &= Q(name__icontains=self.name)
        if self.popular:
            q &= (
                Q(view_count__gt=1000) |
                Q(downloads__gt=100) |
                Q(tag='popular')
            )
        return q
```
Метод `custom_expression` имеет приоритет над любым другим определением, описанным выше, включая методы `filter_<fieldname>`.

!!! done

    Серия про входные параметры завершена! Переходите к следующему разделу **[Обработка ответов](../response/index.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
