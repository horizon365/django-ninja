**Contribution Guide**
=========

  
NinjaExtra में contribute करने पर विचार करने के लिए धन्यवाद! आपके योगदान सभी के लिए project को बेहतर बनाने में मदद करते हैं। शुरू करने से पहले, कृपया निम्नलिखित guidelines की समीक्षा करने के लिए एक क्षण का समय लें।

  
Development Environment सेट अप करना
---------

1.    
    Repository को fork करें: GitHub पर NinjaExtra repository को fork करें और इसे स्थानीय रूप से clone करें।
    
2.    
    Virtual environment: project के लिए एक virtual environment बनाएं और सक्रिय करें।
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    `flit` install करें: सुनिश्चित करें कि `flit` globally installed है।
    
        pip install flit
        
    
4.    
    Dependencies install करें: development libraries और pre-commit hooks install करें।
    
        make install-full
        

### **Code Style और Formatting**

*     
    Formatting: code को format करने और consistency सुनिश्चित करने के लिए, चलाएँ:
    
        make fmt
        
    
*     
    Linting: NinjaExtra linting के लिए `mypy` और `ruff` का उपयोग करता है। Code syntax की जाँच करने के लिए निम्नलिखित command चलाएँ:
    
        make lint
        

### **Testing**

*     
    Unit tests: हम unit testing के लिए `pytest` का उपयोग करते हैं। Test suite चलाएँ:
    
        make test
        
    
*     
    Test coverage: test coverage की जाँच करने के लिए:
    
        make test-cov
        

### **Pull Request सबमिट करना**

1.    
    Branch: अपनी feature या bug fix के लिए एक नई branch बनाएं।
    
        git checkout -b feature-branch
        
    
2.    
    Commit messages: commit messages के लिए conventional commit specification का पालन करें।
    
3.    
    Changes push करें: अपनी branch को अपने forked repository में push करें।
    
        git push origin feature-branch
        
    
4.    
    Pull request: NinjaExtra repository की `master` branch के खिलाफ एक pull request खोलें। अपने changes के लिए एक स्पष्ट title और description प्रदान करें।
    

  
NinjaExtra में योगदान देने के लिए धन्यवाद! 🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
