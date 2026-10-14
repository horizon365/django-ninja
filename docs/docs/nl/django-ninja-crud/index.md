Django Ninja CRUD-documentatie
=======================

![Django Ninja CRUD](../img/django-ninja-crud-cover.JPG)


Django Ninja CRUD is een krachtig, declaratief en lichtelijk opiniegedreven framework dat de ontwikkeling van CRUD-endpoints (Create, Read, Update, Delete) met Django Ninja vereenvoudigt, en ook een declaratieve, op scenario's gebaseerde aanpak biedt voor het testen van deze endpoints met Django REST Testing (het kleine broertje van dit pakket)🐣. Het stelt je in staat om veelvoorkomende endpoints te definiëren als class-based views en ze eenvoudig aan te passen aan de conventies van je project, en om eenvoudig je eigen aangepaste views te maken en deze naast de meegeleverde CRUD-views te declareren, wat modulariteit en uitbreidbaarheid bevordert. Dit pakket moedigt aan om je te richten op wat het belangrijkst is: echte problemen oplossen, in plaats van het wiel opnieuw uit te vinden in je project.


Oorspronkelijk geïnspireerd door DRF's ModelViewSet, evolueerde Django Ninja CRUD om de beperkingen ervan aan te pakken, met een aanpak van compositie boven overerving om echte modulariteit te bereiken — een fundamentele stap richting een bredere declaratieve interface voor het creëren van endpoints.


Belangrijkste uitdagingen bij op overerving gebaseerde viewsets:

*     Uniekheid van CRUD-endpoints per model: Django Ninja CRUD stelt je in staat om meerdere endpoints voor hetzelfde model te definiëren, wat versionering of alternatieve representaties mogelijk maakt.
*     Aanpassingsflexibiliteit: in plaats van methoden te overschrijven op een monolithische klasse, worden individuele views aangepast via compositie en configuratie.
*     Impliciete relaties binnen overervingshiërarchieën: compositie ontkoppelt views, vermindert afhankelijkheden en verbetert hergebruik.
*     Gebrek aan modulariteit voor nieuwe endpoints: het toevoegen van aangepaste endpoints vereist niet langer het subclassen van de gehele viewset, waardoor het gemakkelijker wordt om stap voor stap nieuwe functies te introduceren.

✨ Belangrijkste functies
-------

*     Puur declaratief: definieer views en tests door te declareren wat je wilt, in plaats van hoe het moet.
*     Ongeëvenaarde modulariteit: stel viewsets samen met de gewenste CRUD-views en pas het gedrag van elke view aan.
*     Gemakkelijk uit te breiden: maak je eigen aangepaste views en gebruik ze als herbruikbare componenten naast de meegeleverde CRUD-views.
*     Op scenario's gebaseerd testframework: gebruik het op scenario's gebaseerde testframework om uiteenlopende testcases op een declaratieve en beknopte manier te definiëren.
*     Focus op wat er toe doet: besteed meer tijd aan het oplossen van echte problemen en minder aan veelvoorkomende, repetitieve taken.

> **
> Django Ninja CRUD is meer dan een tool; het is een paradigmaverschuiving in de ontwikkeling en het testen van Django-webapplicaties.**

🫶 Ondersteuning
----------


Allereerst een hartelijk dank aan de 400+ sterrengevers voor hun steun aan dit project. Jullie erkenning van en vertrouwen in het potentieel ervan motiveren me om dit werk te blijven onderhouden en verbeteren, en het zichtbaarder te maken voor nieuwe potentiële gebruikers en bijdragers.

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


Als je baat hebt gehad bij dit project of de inzet erachter waardeert, overweeg dan om verdere steun te bieden. Of het nu de prijs van een koffie is, een woord van aanmoediging of een sponsorcontract: elk gebaar voegt brandstof toe aan het open source-vuur en laat het feller schijnen.✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


Je vriendelijkheid en steun betekenen veel. Bedankt!🙏
