---
created: 2024-07-25T13:23:12 (UTC +08:00)
tags: []
source: https://medium.com/@mrclemrkz/django-ninja-python-framework-for-rest-api-83808d1037d0
author: Clement Fernando

---


Django-Ninja: A Python Framework for REST APIs
===========================================================



> I recently wanted to build a very simple CRUD service in a REST API. After searching around, I found a simple framework that combines the best features of two popular frameworks. That is Django-ninja...

* * *


TL;DR
-----


I recently wanted to build a very simple CRUD service in a REST API. After searching around, I found a simple framework that combines the best features of two popular frameworks. That is Django-ninja; I consider it a combination of Django and FastAPI.

---
Let me explain why I think this is a beneficial approach.


To emphasize my background, I am a Python Django developer and have done some projects in Flask.


With the popularity of FastAPI, I wanted to try it first. So I ran its examples following the documentation, and the feeling was, well, this is cool. Then the use of Pydantic excited me. Most importantly, it is built on async. The perfect and effortless generation of OpenAPI on the Swagger UI made it even sweeter.


This was an eye-opener for me. So, I started digging deeper.


There I found that since FastAPI is not "batteries-included" like Django, it still requires configuring an ORM (SQLAlchemy or SQLModel), not to mention needing another third-party package for database migration tools such as Alembic.


So, I thought to myself, is there a better solution out there, with less configuration and more stable. There might be something that has yet to be highlighted. Then I started searching.


I listed some of all the options (GitHub stars as of September 2023):


Flask: 64K stars — first release: April 1, 2010


FastAPI: 61.8K stars — first release: December 5, 2018


Django Rest Framework: 26.2K stars — first release: July 21, 2005


Sanic: 17.3K stars — first release: October 23, 2016


Django Ninja: 4.8K stars — first release: December 20, 2020


So, clearly I became interested in Django Ninja, and here is why I think it is good.

**Popularity**
--------------


Django-Ninja is built on top of Django, the most popular and obvious web framework. Django-Ninja was first released in late 2020, and in just around 3 years it has gained significant popularity.

**Common Project Structure**
-----------


Unlike Flask and FastAPI, Django enforces a structure when you create a project. However, it is more flexible in terms of how you wish to maintain the project. This is something I like about Django, as it significantly improves how easily another Django developer can follow the project.


Yes, Django Rest Framework (DRF) can do this too. But I did say "rapid development," right? Who wouldn't love simple and organized code? That's the beauty of using Django-Ninja.

**Powerful ORM**
------------


Again, being associated with the powerful core framework (Django) brings reputation to Django-Ninja.


Rather than writing SQL queries ourselves in a less secure manner, we tend to use ORMs. It helps write simple and secure database calls.


However, of course, the concepts between the Django ORM and the SQLAlchemy ORM are different. Django ORM uses the Active Record pattern, while SQLAlchemy uses the Data Mapper pattern, which will be explained in detail in another blog later.

**  
Easy-to-use API Documentation
-----------------


Yes, DRF (Django Rest Framework) has its own API documentation. But in my opinion, the OpenAPI Swagger UI is much better. So when I needed Swagger UI with DRF, I used a swagger generator package called drf-yasg, which did a fairly good job.


But like FastAPI, in Django-Ninja, you can get an interactive OpenAPI Swagger UI without writing any additional code besides the url function.

**Performance**
---------------


Just like FastAPI, it has built-in type enforcement support via Pydantic and asynchronous execution.


The Django-ninja documentation did not forget to brag about this by comparing benchmark data among Flask, DRF, and Django-ninja.

**Faster delivery**
-------------------


Again, just like FastAPI, it can spin up a REST API service with very little code base. At the same time, it helps you develop easily according to whatever philosophical approach you deem fit. That's the beauty of privilege.


A minimal and concise code base leads to high readability. This in turn fuels intuition for faster implementation.


What are your comments, thoughts, and opinions on this? Let me know in the comments below.
