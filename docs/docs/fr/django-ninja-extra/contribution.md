**Guide de contribution**
=========

  
Merci d'envisager de contribuer à NinjaExtra ! Vos contributions contribuent à rendre le projet meilleur pour tout le monde. Avant de commencer, veuillez prendre un moment pour consulter les directives suivantes.

  
Configuration de l'environnement de développement
---------

1.    
    Forkez le dépôt : Forkez le dépôt NinjaExtra sur GitHub et clonez-le localement.
    
2.    
    Environnement virtuel : Créez et activez un environnement virtuel pour le projet.
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    Installez `flit` : Assurez-vous que `flit` est installé globalement.
    
        pip install flit
        
    
4.    
    Installez les dépendances : Installez les bibliothèques de développement et les hooks pre-commit.
    
        make install-full
        

### **Style de code et formatage**

*     
    Formatage : Pour formater le code et garantir la cohérence, exécutez :
    
        make fmt
        
    
*     
    Linting : NinjaExtra utilise `mypy` et `ruff` pour le linting. Exécutez la commande suivante pour vérifier la syntaxe du code :
    
        make lint
        

### **Tests**

*     
    Tests unitaires : Nous utilisons `pytest` pour les tests unitaires. Exécutez la suite de tests :
    
        make test
        
    
*     
    Couverture des tests : Pour vérifier la couverture des tests :
    
        make test-cov
        

### **Soumission d'une pull request**

1.    
    Branche : Créez une nouvelle branche pour votre fonctionnalité ou votre correction de bug.
    
        git checkout -b feature-branch
        
    
2.    
    Messages de commit : Suivez la spécification des commits conventionnels pour les messages de commit.
    
3.    
    Poussez les modifications : Poussez votre branche vers votre dépôt forké.
    
        git push origin feature-branch
        
    
4.    
    Pull request : Ouvrez une pull request contre la branche `master` du dépôt NinjaExtra. Fournissez un titre et une description clairs pour vos modifications.
    

  
Merci de contribuer à NinjaExtra ! 🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
