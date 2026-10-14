**기여 가이드**
=========

  
NinjaExtra에 기여하는 것을 고려해 주셔서 감사합니다! 여러분의 기여는 모든 사람을 위해 프로젝트를 더 좋게 만드는 데 도움이 됩니다. 시작하기 전에 다음 지침을 검토해 주세요.

  
개발 환경 설정
---------

1.    
    저장소 포크: GitHub에서 NinjaExtra 저장소를 포크하고 로컬에 클론합니다.
    
2.    
    가상 환경: 프로젝트용 가상 환경을 생성하고 활성화합니다.
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    `flit` 설치: `flit`이 전역으로 설치되어 있는지 확인합니다.
    
        pip install flit
        
    
4.    
    종속성 설치: 개발 라이브러리와 pre-commit hook을 설치합니다.
    
        make install-full
        

### **코드 스타일 및 포맷팅**

*     
    포맷팅: 코드를 포맷하고 일관성을 보장하려면 다음을 실행합니다:
    
        make fmt
        
    
*     
    린팅: NinjaExtra는 린팅을 위해 `mypy`와 `ruff`를 사용합니다. 다음 명령을 실행하여 코드 구문을 검사합니다:
    
        make lint
        

### **테스팅**

*     
    단위 테스트: 단위 테스트에는 `pytest`를 사용합니다. 테스트 스위트를 실행합니다:
    
        make test
        
    
*     
    테스트 커버리지: 테스트 커버리지를 확인하려면:
    
        make test-cov
        

### **Pull Request 제출**

1.    
    브랜치: 기능 또는 버그 수정을 위한 새 브랜치를 생성합니다.
    
        git checkout -b feature-branch
        
    
2.    
    커밋 메시지: 커밋 메시지는 conventional commit 명세를 따릅니다.
    
3.    
    변경 사항 푸시: 브랜치를 포크한 저장소에 푸시합니다.
    
        git push origin feature-branch
        
    
4.    
    Pull request: NinjaExtra 저장소의 `master` 브랜치에 대해 pull request를 엽니다. 변경 사항에 대한 명확한 제목과 설명을 제공합니다.
    

  
NinjaExtra에 기여해 주셔서 감사합니다! 🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
