Een eigenaardig probleem op de django ninja docs-pagina: twee verschillende endpoints gaan tegelijk open
==========================================================

Onlangs meldde een communitylid een probleem: op de docs-pagina gaan, wanneer je op een van twee endpoints klikt, beide tegelijk open. Andere API's gedragen zich niet zo.

![django-ninja-docs-wrong](/img/docs-wrong.png)


De oorzaak werd uiteindelijk gevonden: de functienamen of paden waren gedupliceerd. Met andere woorden: bij het schrijven van de view was een functie gekopieerd en was men vergeten de naam te wijzigen.
