---
comments: true
---
# Filtering

If you want to allow users to filter your querysets by multiple different attributes, it makes sense to encapsulate your filters into a `FilterSchema` class.
`FilterSchema` is a regular `Schema`, so it uses all the necessary features of Pydantic, but it also adds some conveniences
to easily convert user-facing filtering parameters into database queries.

First, define a subclass of `FilterSchema`:

```python hl_lines="6 7 8"
from ninja import FilterSchema, Field
from typing import Optional


class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
    author: Optional[str] = None
    created_after: Optional[datetime] = None
```


Next, use this schema together with `Query` in your API handler:
```python hl_lines="2"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Just like described in [Using a Schema to Define Query Parameters](./query-params.md#using-schema), Django Ninja turns the fields defined in `BookFilterSchema` into query parameters.
You can use the shorthand one-liner `.filter()` to apply these filters to your queryset:
```python hl_lines="4"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.all()
    books = filters.filter(books)
    return books
```

Under the hood, `FilterSchema` converts its fields into [Q expressions](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects), then combines them and uses them to filter your queryset.


Alternatively, instead of using the `.filter` method, you can get the prepared `Q` expression and perform the filtering yourself.
This can be useful when you have some additional queryset filtering on top of what you expose to users via the API:
```python hl_lines="5 8"
@api.get("/books")
def list_books(request, filters: BookFilterSchema = Query(...)):

    # Never serve books from inactive publishers and authors
    q = Q(author__is_active=True) | Q(publisher__is_active=True)
    
    # But allow filtering the rest of the books
    q &= filters.get_filter_expression()
    return Book.objects.filter(q)
```

By default, the filters will behave as follows:

* `None` values will be ignored and no filtering will be applied;
* Each non-`None` field will be converted into a `Q` expression according to each field's `Field` definition;
* All `Q` expressions will be combined into one using the `AND` logical operator;
* The resulting `Q` expression is used to filter the queryset, and a queryset with the `.filter` clause applied is returned to you.

## Custom Fields
By default, `FilterSet` uses the field name to generate the Q expression:
```python
class BookFilterSchema(FilterSchema):
    name: Optional[str] = None
```
The `name` field will be converted into a `Q(name=...)` expression.

When your database lookup is more complex than this, you can explicitly specify them using the `"q"` keyword argument in the field definition:
```python hl_lines="2"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains') 
```
You can even specify multiple lookup keyword argument names as a list:
```python hl_lines="2 3 4"
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains',
                                     'author__name__icontains',
                                     'publisher__name__icontains']) 
```
By default, field-level expressions are combined using the `"OR"` connector, so with the above setup, a query parameter `?search=foobar` will search for books that contain "foobar" in either their name, author, or publisher.


## Combining Expressions
By default,

* field-level expressions are combined using the `OR` operator.
* the fields themselves are combined using the `AND` operator.

So, for the following `FilterSchema`...
```python
class BookFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'author__name__icontains'])
    popular: Optional[bool] = None
```
...and the following query parameters from a user
```
http://localhost:8000/api/books?search=harry&popular=true
```
The `FilterSchema` instance will look for popular books that contain `harry` in either the book's _or_ the author's name.


You can customize this behavior using the `expression_connector` parameter in both field-level and class-level definitions:
```python hl_lines="3 7"
class BookFilterSchema(FilterSchema):
    active: Optional[bool] = Field(None, q=['is_active', 'publisher__is_active'],
                                   expression_connector='AND')
    name: Optional[str] = Field(None, q='name__icontains')
    
    class Config:
        expression_connector = 'OR'
```

The expression connector can take the values `"OR"`, `"AND"`, and `"XOR"`, but the latter is only [supported](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor) in Django 4.1.

Now, a request with these query parameters
```
http://localhost:8000/api/books?name=harry&active=true
```
...will look for books that have `harry` in their name _or_ are themselves active and published by an active publisher.


## Filtering by Nones
You can make `FilterSchema` treat `None` as a valid value for which filtering should be performed.

This can be done at the field level via the `ignore_none` keyword argument:
```python hl_lines="3"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
```

This way, when the user does not provide another value for `"tag"`, the filter will always include the `tag=None` condition.

You can also specify this for all fields at once in the configuration:
```python hl_lines="6"
class BookFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')
    tag: Optional[str] = Field(None, q='tag', ignore_none=False)
    
    class Config:
        ignore_none = False
```


## Custom Expressions
Sometimes you may have complex filtering scenarios that cannot be handled by a single field annotation.
For such cases, you can implement your field filtering logic as a custom method. Just define a method named `filter_<fieldname>` that accepts a filtering value and returns a Q expression:

```python hl_lines="5"
class BookFilterSchema(FilterSchema):
    tag: Optional[str] = None
    popular: Optional[bool] = None
    
    def filter_popular(self, value: bool) -> Q:
        return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()
```
Such field methods take precedence over what is specified in the corresponding field's `Field()` definition.
If that is not enough, you can implement your own custom filtering logic for the entire `FilterSet` class in the `custom_expression` method:

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
The `custom_expression` method takes precedence over any other definition described above, including the `filter_<fieldname>` methods.

!!! done

    The input parameter series is complete! Continue to the next section **[Handling Responses](../response/index.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
