
要为 Ninja JWT 进行开发工作，在 Github 上创建自己的分支，
将其本地克隆，为其创建并激活一个虚拟环境，然后在项目目录内：

之后，安装 flit

```shell
$(venv) pip install flit
```

安装用于代码linting 和风格的开发库和预提交钩子

```shell
$(venv) make install
```

要运行测试：

```shell
$(venv) make test
```

要带着覆盖率运行测试：

```shell
$(venv) make test-cov
```

!!! 大功告成

    本教程到此结束！

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
