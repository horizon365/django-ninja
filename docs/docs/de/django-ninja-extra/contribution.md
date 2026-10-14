**Leitfaden für Mitwirkende**
=========

  
Vielen Dank, dass Sie erwägen, zu NinjaExtra beizutragen! Ihre Beiträge helfen, das Projekt für alle besser zu machen. Bevor Sie loslegen, nehmen Sie sich bitte einen Moment Zeit, um die folgenden Richtlinien zu prüfen.

  
Einrichtung der Entwicklungsumgebung
---------

1.    
    Repository forken: Forken Sie das NinjaExtra-Repository auf GitHub und klonen Sie es lokal.
    
2.    
    Virtuelle Umgebung: Erstellen und aktivieren Sie eine virtuelle Umgebung für das Projekt.
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    `flit` installieren: Stellen Sie sicher, dass `flit` global installiert ist.
    
        pip install flit
        
    
4.    
    Abhängigkeiten installieren: Installieren Sie Entwicklungsbibliotheken und Pre-Commit-Hooks.
    
        make install-full
        

### **Code-Stil und Formatierung**

*     
    Formatierung: Um Code zu formatieren und Konsistenz sicherzustellen, führen Sie aus:
    
        make fmt
        
    
*     
    Linting: NinjaExtra verwendet `mypy` und `ruff` für das Linting. Führen Sie den folgenden Befehl aus, um die Codesyntax zu prüfen:
    
        make lint
        

### **Testen**

*     
    Unit-Tests: Wir verwenden `pytest` für Unit-Tests. Führen Sie die Testsuite aus:
    
        make test
        
    
*     
    Testabdeckung: Um die Testabdeckung zu prüfen:
    
        make test-cov
        

### **Pull Request einreichen**

1.    
    Branch: Erstellen Sie einen neuen Branch für Ihre Funktion oder Ihren Bugfix.
    
        git checkout -b feature-branch
        
    
2.    
    Commit-Nachrichten: Folgen Sie bei Commit-Nachrichten der konventionellen Commit-Spezifikation.
    
3.    
    Änderungen pushen: Pushen Sie Ihren Branch in Ihr geforktes Repository.
    
        git push origin feature-branch
        
    
4.    
    Pull Request: Öffnen Sie einen Pull Request gegen den `master`-Branch des NinjaExtra-Repositorys. Geben Sie einen klaren Titel und eine klare Beschreibung für Ihre Änderungen an.

  
Vielen Dank für Ihren Beitrag zu NinjaExtra! 🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
