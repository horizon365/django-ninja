**Contribution Guide**
=========

  
Thank you for considering contributing to NinjaExtra! Your contributions help make the project better for everyone. Before getting started, please take a moment to review the following guidelines.

  
Setting Up the Development Environment
---------

1.    
    Fork the repository: Fork the NinjaExtra repository on GitHub and clone it locally.
    
2.    
    Virtual environment: Create and activate a virtual environment for the project.
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    Install `flit`: Ensure `flit` is installed globally.
    
        pip install flit
        
    
4.    
    Install dependencies: Install development libraries and pre-commit hooks.
    
        make install-full
        

### **Code Style and Formatting**

*     
    Formatting: To format code and ensure consistency, run:
    
        make fmt
        
    
*     
    Linting: NinjaExtra uses `mypy` and `ruff` for linting. Run the following command to check code syntax:
    
        make lint
        

### **Testing**

*     
    Unit tests: We use `pytest` for unit testing. Run the test suite:
    
        make test
        
    
*     
    Test coverage: To check test coverage:
    
        make test-cov
        

### **Submitting a Pull Request**

1.    
    Branch: Create a new branch for your feature or bug fix.
    
        git checkout -b feature-branch
        
    
2.    
    Commit messages: Follow the conventional commit specification for commit messages.
    
3.    
    Push changes: Push your branch to your forked repository.
    
        git push origin feature-branch
        
    
4.    
    Pull request: Open a pull request against the `master` branch of the NinjaExtra repository. Provide a clear title and description for your changes.
    

  
Thank you for contributing to NinjaExtra! 🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
