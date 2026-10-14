---
created: 2024-07-25T13:23:12 (UTC +08:00)
tags: []
source: https://medium.com/@mrclemrkz/django-ninja-python-framework-for-rest-api-83808d1037d0
author: Clement Fernando

---


Django-Ninja: Ein Python-Framework für REST-APIs
===========================================================



> Ich wollte kürzlich einen sehr einfachen CRUD-Dienst in einer REST-API aufbauen. Nach einigem Suchen fand ich ein schlankes Framework, das die besten Eigenschaften zweier populärer Frameworks vereint. Das ist Django-ninja...

* * *


TL;DR
-----


Ich wollte kürzlich einen sehr einfachen CRUD-Dienst in einer REST-API aufbauen. Nach einigem Suchen fand ich ein schlankes Framework, das die besten Eigenschaften zweier populärer Frameworks vereint. Das ist Django-ninja; ich betrachte es als eine Kombination aus Django und FastAPI.

---
Lassen Sie mich erklären, warum ich das für einen sinnvollen Ansatz halte.


Um meinen Hintergrund zu betonen: Ich bin ein Python-Django-Entwickler und habe einige Projekte in Flask umgesetzt.


Mit dem Aufstieg von FastAPI wollte ich es zuerst ausprobieren. Also habe ich seine Beispiele gemäß der Dokumentation ausgeführt, und mein Eindruck war: na ja, das ist cool. Dann hat mich die Verwendung von Pydantic begeistert. Vor allem aber baut es auf async auf. Die perfekte und mühelose Generierung von OpenAPI in der Swagger UI hat das Ganze noch süßer gemacht.


Das hat mich den Blick geöffnet. Also fing ich an, tiefer zu graben.


Dort stellte ich fest: Da FastAPI nicht wie Django „batteries-included" ist, muss man weiterhin ein ORM konfigurieren (SQLAlchemy oder SQLModel), ganz zu schweigen davon, dass man für Datenbank-Migrationstools wie Alembic ein weiteres Paket von Drittanbietern braucht.


Da habe ich mich gefragt: Gibt es da draußen eine bessere Lösung — mit weniger Konfiguration und stabiler? Vielleicht gibt es etwas, das bislang noch nicht genügend Beachtung gefunden hat. Dann habe ich angefangen zu suchen.


Ich habe einige der Optionen aufgelistet (GitHub-Stars Stand September 2023):


Flask: 64K Sterne — erste Veröffentlichung: 1. April 2010


FastAPI: 61,8K Sterne — erste Veröffentlichung: 5. Dezember 2018


Django Rest Framework: 26,2K Sterne — erste Veröffentlichung: 21. Juli 2005


Sanic: 17,3K Sterne — erste Veröffentlichung: 23. Oktober 2016


Django Ninja: 4,8K Sterne — erste Veröffentlichung: 20. Dezember 2020


So wurde ich klar auf Django Ninja aufmerksam, und hier ist, warum ich es für gut halte.

**Popularität**
--------------


Django-Ninja baut auf Django auf, dem beliebtesten und naheliegendsten Web-Framework. Django-Ninja wurde Ende 2020 erstmals veröffentlicht und hat in nur rund 3 Jahren erheblich an Popularität gewonnen.

**Gemeinsame Projektstruktur**
-----------


Anders als Flask und FastAPI erzwingt Django eine Struktur, sobald man ein Projekt anlegt. Allerdings ist es flexibler, was die Frage betrifft, wie Sie das Projekt pflegen möchten. Das ist etwas, das ich an Django mag, denn es verbessert erheblich, wie leicht ein anderer Django-Entwickler dem Projekt folgen kann.


Ja, Django Rest Framework (DRF) kann das auch. Aber ich hatte doch von „schneller Entwicklung" gesprochen, oder? Wer liebt nicht einfachen und gut organisierten Code? Das ist die Schönheit von Django-Ninja.

**Leistungsfähiges ORM**
------------


Auch hier verleiht die Nähe zum leistungsfähigen Kern-Framework (Django) Django-Ninja einen guten Ruf.


Statt selbst SQL-Abfragen auf weniger sichere Weise zu schreiben, greifen wir in der Regel auf ORMs zurück. Es hilft dabei, einfache und sichere Datenbankzugriffe zu schreiben.


Allerdings sind natürlich die Konzepte zwischen dem Django ORM und dem SQLAlchemy ORM unterschiedlich. Das Django ORM folgt dem Active-Record-Muster, während SQLAlchemy dem Data-Mapper-Muster folgt; das wird in einem späteren Blog-Beitrag noch ausführlich erklärt.

**  
Einfach zu bedienende API-Dokumentation
-----------------


Ja, DRF (Django Rest Framework) hat eine eigene API-Dokumentation. Aber meiner Meinung nach ist die OpenAPI-Swagger-UI deutlich besser. Als ich also Swagger UI mit DRF brauchte, verwendete ich ein Swagger-Generator-Paket namens drf-yasg, das ziemlich gute Arbeit leistete.


Aber wie bei FastAPI erhalten Sie auch in Django-Ninja eine interaktive OpenAPI-Swagger-UI, ohne zusätzlichen Code zu schreiben, abgesehen von der url-Funktion.

**Performance**
---------------


Genau wie FastAPI bietet es integrierte Unterstützung für Typerzwingung durch Pydantic und für asynchrone Ausführung.


Die Django-ninja-Dokumentation hat es sich nicht nehmen lassen, damit zu prahlen, indem sie Benchmark-Daten zwischen Flask, DRF und Django-ninja vergleicht.

**Schnellere Auslieferung**
-------------------


Wiederum genau wie FastAPI lässt sich damit ein REST-API-Dienst mit sehr wenig Code aufbauen. Gleichzeitig hilft es Ihnen, sich entsprechend Ihrem bevorzugten philosophischen Ansatz mühelos zu entwickeln. Das ist die Schönheit dieses Privilegs.


Ein minimaler und prägnanter Codebestand führt zu hoher Lesbarkeit. Das wiederum nährt die Intuition für eine schnellere Umsetzung.


Was sind Ihre Kommentare, Gedanken und Meinungen dazu? Lassen Sie es mich in den Kommentaren unten wissen.
