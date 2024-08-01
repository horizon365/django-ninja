**贡献指南**
=========

  
感谢您考虑为 NinjaExtra 做出贡献！您的贡献使每个人都能让项目变得更好。在开始之前，请花一点时间回顾以下指南。

  
设置开发环境
---------

1.    
    分叉仓库：在 GitHub 上分叉 NinjaExtra 仓库，并在本地克隆它。
    
2.    
    虚拟环境：为项目创建并激活一个虚拟环境。
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    安装 `flit` ：确保全局安装了 `flit` 。
    
        pip install flit
        
    
4.    
    安装依赖项：安装开发库和预提交挂钩。
    
        make install-full
        
    

### **  
代码风格和格式**

*     
    格式化：要格式化代码并确保一致性，请运行：
    
        make fmt
        
    
*     
    语法检查：NinjaExtra 使用 `mypy` 和 `ruff` 进行语法检查。运行以下命令检查代码语法：
    
        make lint
        
    

### **Testing**

*     
    单元测试：我们使用 `pytest` 进行单元测试。运行测试套件：
    
        make test
        
    
*     
    测试覆盖：为了检查测试覆盖：
    
        make test-cov
        
    

### **  
提交拉取请求**

1.    
    分支：为你的功能或错误修复创建一个新分支。
    
        git checkout -b feature-branch
        
    
2.    
    提交消息：遵循提交消息的常规提交规范。
    
3.    
    推送更改：将你的分支推送到你分叉的存储库。
    
        git push origin feature-branch
        
    
4.    
    拉取请求：针对 NinjaExtra 存储库的 `master` 分支打开一个拉取请求。为你的更改提供清晰明了的标题和描述。
    

  
感谢你为 NinjaExtra 做出贡献！🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
