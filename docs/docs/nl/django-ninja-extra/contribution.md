**Bijdragegids**
=========

  
Bedankt dat je overweegt bij te dragen aan NinjaExtra! Jouw bijdragen helpen het project voor iedereen beter te maken. Voordat je begint, neem even de tijd om de volgende richtlijnen door te nemen.

  
De ontwikkelomgeving opzetten
---------

1.    
    Fork de repository: fork de NinjaExtra-repository op GitHub en kloon deze lokaal.
    
2.    
    Virtuele omgeving: maak en activeer een virtuele omgeving voor het project.
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    Installeer `flit`: zorg dat `flit` globaal is geïnstalleerd.
    
        pip install flit
        
    
4.    
    Installeer afhankelijkheden: installeer ontwikkelbibliotheken en pre-commit hooks.
    
        make install-full
        

### **Codestijl en opmaak**

*     
    Opmaak: voer het volgende uit om code op te maken en consistentie te waarborgen:
    
        make fmt
        
    
*     
    Linting: NinjaExtra gebruikt `mypy` en `ruff` voor linting. Voer het volgende commando uit om de codesyntaxis te controleren:
    
        make lint
        

### **Testen**

*     
    Unittests: we gebruiken `pytest` voor unit testing. Voer de testsuite uit:
    
        make test
        
    
*     
    Testdekking: om de testdekking te controleren:
    
        make test-cov
        

### **Een pull request indienen**

1.    
    Branch: maak een nieuwe branch aan voor je feature of bugfix.
    
        git checkout -b feature-branch
        
    
2.    
    Commitberichten: volg de conventional commit-specificatie voor commitberichten.
    
3.    
    Wijzigingen pushen: push je branch naar je geforkte repository.
    
        git push origin feature-branch
        
    
4.    
    Pull request: open een pull request tegen de `master`-branch van de NinjaExtra-repository. Geef een duidelijke titel en beschrijving voor je wijzigingen.
    

  
Bedankt voor je bijdrage aan NinjaExtra! 🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
