Ein kurioses Problem auf der django-ninja-Dokumentationsseite: Zwei verschiedene Endpunkte öffnen sich gleichzeitig
==========================================================

Kürzlich meldete ein Community-Mitglied ein Problem: Auf der Dokumentationsseite öffnet sich beim Klicken auf einen von zwei Endpunkten immer gleichzeitig auch der andere. Andere APIs verhalten sich nicht so.

![django-ninja-docs-wrong](/img/docs-wrong.png)


Die Ursache wurde schließlich gefunden: Die Funktionsnamen oder Pfade waren doppelt vorhanden. Das heißt, beim Schreiben des View wurde eine Funktion kopiert und vergessen, deren Namen zu ändern.
