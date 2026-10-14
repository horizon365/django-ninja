Django Ninja CRUD Docs
=======================

![Django Ninja CRUD](../img/django-ninja-crud-cover.JPG)


Django Ninja CRUD ist ein leistungsfähiges, deklaratives, dabei leicht meinungsstarkes Framework, das die Entwicklung von CRUD-Endpunkten (Create, Read, Update, Delete) mit Django Ninja vereinfacht, und zusätzlich einen deklarativen, szenariobasierten Ansatz zum Testen dieser Endpunkte mit Django REST Testing (das kleine Geschwisterchen dieses Pakets)🐣 bereitstellt. Es erlaubt Ihnen, häufige Endpunkte als klassenbasierte Views zu definieren und sie leicht an die Konventionen Ihres Projekts anzupassen, sowie einfach eigene benutzerdefinierte Views zu erstellen und sie neben den bereitgestellten CRUD-Views zu deklarieren, wodurch Modularität und Erweiterbarkeit gefördert werden. Dieses Paket ermutigt dazu, sich auf das Wesentlichste zu konzentrieren: echte Probleme zu lösen, statt im gesamten Projekt das Rad neu zu erfinden.


Ursprünglich inspiriert von DRFs ModelViewSet, wurde Django Ninja CRUD weiterentwickelt, um dessen Limitierungen zu beheben, und verfolgt einen Composition-over-Inheritance-Ansatz, um echte Modularität zu erreichen — ein grundlegender Schritt hin zu einer breiteren deklarativen Schnittstelle zur Erstellung von Endpunkten.


Wesentliche Herausforderungen bei auf Vererbung basierenden ViewSets:

*     Eindeutigkeit der CRUD-Endpunkte pro Modell: Django Ninja CRUD erlaubt es, mehrere Endpunkte für dasselbe Modell zu definieren, was Versionierung oder alternative Darstellungen ermöglicht.
*     Anpassungsflexibilität: statt Methoden auf einer monolithischen Klasse zu überschreiben, werden einzelne Views durch Komposition und Konfiguration angepasst.
*     Implizite Beziehungen innerhalb von Vererbungshierarchien: Komposition entkoppelt Views, reduziert Abhängigkeiten und verbessert die Wiederverwendbarkeit.
*     Mangelnde Modularität für neue Endpunkte: das Hinzufügen benutzerdefinierter Endpunkte erfordert keine Unterklasse des gesamten ViewSets mehr, was es erleichtert, neue Funktionen schrittweise einzuführen.

✨ Hauptmerkmale
-------

*     Rein deklarativ: definieren Sie Views und Tests, indem Sie deklarieren, was Sie wollen, nicht wie es zu tun ist.
*     Unschlagbare Modularität: passen Sie ViewSets mit den gewünschten CRUD-Views an und konfigurieren Sie das Verhalten jedes einzelnen Views.
*     Leicht erweiterbar: erstellen Sie Ihre eigenen benutzerdefinierten Views und verwenden Sie sie als wiederverwendbare Komponenten neben den bereitgestellten CRUD-Views.
*     Szenariobasiertes Testframework: nutzen Sie das szenariobasierte Testframework, um vielfältige Testfälle deklarativ und prägnant zu definieren.
*     Fokus auf das Wesentliche: verbringen Sie mehr Zeit mit der Lösung echter Probleme und weniger mit häufigen, sich wiederholenden Aufgaben.

> **
> Django Ninja CRUD ist mehr als ein Werkzeug; es ist ein Paradigmenwechsel in der Entwicklung und dem Testen von Django-Webanwendungen.**

🫶 Unterstützung
----------


Zunächst einmal ein herzliches Dankeschön an die über 400 Stargazer für ihre Unterstützung dieses Projekts. Ihre Anerkennung seines Potenzials und Ihr Vertrauen in dasselbe motivieren mich, diese Arbeit weiter zu pflegen und zu verbessern, sie für neue potenzielle Benutzer und Mitwirkende sichtbarer zu machen.

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


Wenn Sie von diesem Projekt profitiert haben oder den dahintersteckenden Einsatz schätzen, ziehen Sie bitte eine weitergehende Unterstützung in Betracht. Ob der Preis für einen Kaffee, ein aufmunterndes Wort oder eine Sponsorenschaft — jede Geste fügt dem Open-Source-Feuer Kraftstoff hinzu und lässt es heller leuchten.✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


Ihre Freundlichkeit und Unterstützung bedeuten mir sehr viel. Vielen Dank!🙏
