
Ninja JWT의 개발 작업을 하려면 Github에서 자신의 포크를 만들고,
로컬로 클론한 뒤, 가상 환경을 생성하고 활성화한 다음, 프로젝트 디렉터리 안에서 작업합니다:

그다음 flit을 설치합니다

```shell
$(venv) pip install flit
```

코드 린팅과 스타일 검사에 사용되는 개발 라이브러리와 pre-commit 훅을 설치합니다

```shell
$(venv) make install
```

테스트를 실행하려면:

```shell
$(venv) make test
```

커버리지와 함께 테스트를 실행하려면:

```shell
$(venv) make test-cov
```

!!! success

    이것으로 튜토리얼을 마칩니다!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
