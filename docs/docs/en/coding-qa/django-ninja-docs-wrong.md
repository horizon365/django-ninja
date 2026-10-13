A Quirky Issue on the django ninja docs Page: Two Different Endpoints Open at the Same Time
==========================================================

Recently, a community member reported an issue: on the docs page, clicking either of two endpoints opens both of them simultaneously. Other APIs do not behave this way.

![django-ninja-docs-wrong](/img/docs-wrong.png)


The root cause was eventually located: the function names or paths were duplicated. In other words, while writing the view, a function was copied and the name was forgotten to be changed.
