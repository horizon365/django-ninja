Django Ninja CRUD 문서
=======================

![Django Ninja CRUD](../img/django-ninja-crud-cover.JPG)


Django Ninja CRUD는 Django Ninja로 CRUD(Create, Read, Update, Delete) 엔드포인트 개발을 단순화하는 강력하고 선언적이면서도 다소 독선적인 프레임워크이며, Django REST Testing(이 패키지의 작은 동생)🐣을 사용하여 이러한 엔드포인트를 테스트하기 위한 선언적이고 시나리오 기반 접근 방식도 제공합니다. 이를 통해 일반적인 엔드포인트를 클래스 기반 뷰로 정의하고 프로젝트의 관례에 맞게 쉽게 커스터마이즈할 수 있으며, 자체 커스텀 뷰를 쉽게 만들어 제공된 CRUD 뷰와 함께 선언함으로써 모듈성과 확장성을 촉진할 수 있습니다. 이 패키지는 가장 중요한 것, 즉 프로젝트 전반에 걸쳐 바퀴를 재발명하는 대신 **실제 문제를 해결하는 데** 집중하도록 권장합니다.


원래 DRF의 ModelViewSet에서 영감을 받은 Django Ninja CRUD는 그 한계를 해결하기 위해 발전하여, 상속보다는 합성을 통한 접근 방식을 채택하여 진정한 모듈성을 달성했습니다 — 이는 엔드포인트 생성을 위한 더 넓은 선언적 인터페이스를 향한 기초적인 단계입니다.


상속 기반 뷰셋의 주요 과제:

*     모델당 CRUD 엔드포인트의 고유성: Django Ninja CRUD를 사용하면 동일한 모델에 대해 여러 엔드포인트를 정의하여 버전 관리 또는 대체 표현을 가능하게 합니다.
*     커스터마이징 유연성: 모놀리식 클래스의 메서드를 오버라이드하는 대신 개별 뷰가 합성과 구성을 통해 커스터마이즈됩니다.
*     상속 계층 내의 암시적 관계: 합성은 뷰를 분리하여 종속성을 줄이고 재사용성을 향상시킵니다.
*     새 엔드포인트에 대한 모듈성 부족: 커스텀 엔드포인트를 추가하는 데 더 이상 전체 뷰셋을 서브클래싱할 필요가 없어 새로운 기능을 점진적으로 도입하기 쉬워집니다.

✨ 주요 기능
-------

*     순수하게 선언적: 수행 방법이 아닌 원하는 것을 선언하여 뷰와 테스트를 정의합니다.
*     비교할 수 없는 모듈성: 원하는 CRUD 뷰로 뷰셋을 커스터마이즈하고 각 뷰의 동작을 커스터마이즈합니다.
*     확장 용이성: 자체 커스텀 뷰를 만들고 제공된 CRUD 뷰와 함께 재사용 가능한 컴포넌트로 사용합니다.
*     시나리오 기반 테스트 프레임워크: 시나리오 기반 테스트 프레임워크를 활용하여 다양한 테스트 케이스를 선언적이고 간결하게 정의합니다.
*     중요한 것에 집중: 일반적이고 반복적인 작업에 더 적은 시간을, 실제 문제 해결에 더 많은 시간을 사용합니다.

> **
> Django Ninja CRUD는 단순한 도구 그 이상입니다; 이는 Django 웹 애플리케이션 개발 및 테스트의 패러다임 전환입니다.**

🫶 지원
----------


무엇보다도 이 프로젝트를 지원해 주신 400명 이상의 stargazer에게 진심으로 감사드립니다. 프로젝트의 잠재력에 대한 여러분의 인정과 신뢰는 이 작업을 계속 유지하고 개선하여 새로운 잠재 사용자와 기여자에게 더 잘 보이도록 하는 동기가 됩니다.

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


이 프로젝트에서 혜택을 받았거나 그 뒤의 헌신을 높이 평가한다면 추가 지원을 고려해 보세요. 커피 한 잔 값이든 격려의 말이든 후원이든, 모든 제스처가 오픈 소스의 불꽃에 연료를 더하고 더 밝게 빛나게 합니다.✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


여러분의 친절과 지원은 큰 의미가 있습니다. 감사합니다!🙏
