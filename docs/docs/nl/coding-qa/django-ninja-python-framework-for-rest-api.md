---
created: 2024-07-25T13:23:12 (UTC +08:00)
tags: []
source: https://medium.com/@mrclemrkz/django-ninja-python-framework-for-rest-api-83808d1037d0
author: Clement Fernando

---


Django-Ninja: een Python-framework voor REST API's
===========================================================



> Ik wilde onlangs een heel eenvoudige CRUD-service bouwen in een REST API. Na wat zoeken vond ik een eenvoudig framework dat de beste eigenschappen van twee populaire frameworks combineert. Dat is Django-ninja...

* * *


TL;DR
-----


Ik wilde onlangs een heel eenvoudige CRUD-service bouwen in een REST API. Na wat zoeken vond ik een eenvoudig framework dat de beste eigenschappen van twee populaire frameworks combineert. Dat is Django-ninja; ik beschouw het als een combinatie van Django en FastAPI.

---
Laat me uitleggen waarom ik dit een gunstige aanpak vind.


Om mijn achtergrond te benadrukken: ik ben een Python Django-ontwikkelaar en heb enkele projecten in Flask gedaan.


Met de populariteit van FastAPI wilde ik het eerst uitproberen. Dus draaide ik de voorbeelden volgens de documentatie, en het gevoel was nou ja, dit is cool. Toen maakte het gebruik van Pydantic mij enthousiast. Het allerbelangrijkste: het is gebouwd op async. De perfecte en moeiteloze generatie van OpenAPI in de Swagger UI maakte het nog zoeter.


Dit was een eyeopener voor me. Dus begon ik dieper te graven.


Daar ontdekte ik dat FastAPI, omdat het niet "batteries-included" is zoals Django, nog steeds een ORM vereist (SQLAlchemy of SQLModel), om nog maar te zwijgen van het nodig hebben van een ander pakket van derden voor databasemigratietools zoals Alembic.


Dus dacht ik bij mezelf: is er niet een betere oplossing, met minder configuratie en stabieler. Misschien is er iets dat nog niet in de spotlights staat. Toen begon ik te zoeken.


Ik zette een deel van alle opties op een rij (GitHub-sterren per september 2023):


Flask: 64K sterren — eerste release: 1 april 2010


FastAPI: 61.8K sterren — eerste release: 5 december 2018


Django Rest Framework: 26.2K sterren — eerste release: 21 juli 2005


Sanic: 17.3K sterren — eerste release: 23 oktober 2016


Django Ninja: 4.8K sterren — eerste release: 20 december 2020


Dus uiteraard raakte ik geïnteresseerd in Django Ninja, en dit is waarom ik het goed vind.

**Populariteit**
--------------


Django-Ninja is gebouwd bovenop Django, het populairste en meest voor de hand liggende webframework. Django-Ninja kwam eind 2020 voor het eerst uit en heeft in slechts ongeveer 3 jaar aanzienlijke populariteit gekregen.

**Gangbare projectstructuur**
-----------


Anders dan Flask en FastAPI legt Django een structuur op wanneer je een project aanmaakt. Het is echter flexibeler wat betreft hoe je het project wilt onderhouden. Dit is iets dat ik aan Django waardeer, omdat het aanzienlijk verbetert hoe gemakkelijk een andere Django-ontwikkelaar het project kan volgen.


Ja, Django Rest Framework (DRF) kan dit ook. Maar ik zei toch "snelle ontwikkeling"? Wie houdt er nu niet van eenvoudige en georganiseerde code? Dat is de schoonheid van Django-Ninja.

**Krachtige ORM**
------------


Opnieuw geldt: verbonden zijn met het krachtige kernframework (Django) geeft Django-Ninja reputatie.


In plaats van zelf SQL-query's te schrijven op een minder veilige manier, gebruiken we liever ORM's. Het helpt om eenvoudige en veilige databaseaanroepen te schrijven.


Natuurlijk verschillen de concepten tussen de Django ORM en de SQLAlchemy ORM. De Django ORM gebruikt het Active Record-patroon, terwijl SQLAlchemy het Data Mapper-patroon gebruikt, wat later in een andere blog in detail zal worden uitgelegd.

**  
Gebruiksvriendelijke API-documentatie
-----------------


Ja, DRF (Django Rest Framework) heeft zijn eigen API-documentatie. Maar naar mijn mening is de OpenAPI Swagger UI veel beter. Dus toen ik Swagger UI met DRF nodig had, gebruikte ik een swagger-generatorpakket genaamd drf-yasg, dat behoorlijk goed werk leverde.


Maar zoals FastAPI, kun je in Django-Ninja een interactieve OpenAPI Swagger UI krijgen zonder extra code te schrijven, afgezien van de url-functie.

**Prestaties**
---------------


Net als FastAPI heeft het ingebouwde ondersteuning voor typehandhaving via Pydantic en asynchrone uitvoering.


De Django-ninja-documentatie vergat niet hiermee te pochen door benchmarkgegevens te vergelijken tussen Flask, DRF en Django-ninja.

**Snellere oplevering**
-------------------


Opnieuw, net als FastAPI, kan het een REST API-service opzetten met een zeer kleine codebasis. Tegelijkertijd helpt het je gemakkelijk te ontwikkelen volgens welke filosofische aanpak jij passend vindt. Dat is de schoonheid van het voorrecht.


Een minimale en beknopte codebasis leidt tot hoge leesbaarheid. Dit stimuleert op zijn beurt de intuïtie voor snellere implementatie.


Wat zijn je opmerkingen, gedachten en meningen hierover? Laat het me weten in de reacties hieronder.
