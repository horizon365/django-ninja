`ninja_schema`와 `ninja` 내부의 schema는 느낌이 확연히 다르다 — ninja 것은 잘 동작하지만 `ninja_schema`의 것은 오류를 발생시킨다
==========================================================

A: `ninja_schema`가 별도의 패키지인가요?
B: 네, pip으로 설치해야 합니다. 소스 코드를 살펴봤는데 pydantic에서 뭔가 가져온 것 같았습니다. 하지만 pydantic을 잘 모르기 때문에 새로 추가된 것들이 정확히 어떤 기능을 구현하는지는 모르겠습니다.

A: ninja의 schema만으로도 충분하다고 생각합니다.
B: 외래 키 출력을 평탄화하는 경우, 문서에서는 이렇게 사용합니다: `owner_first_name: str = Field(None, alias="owner.first_name")`
B: `ninja_schema`의 것을 사용하면 입력이 `str`이어야 하는데 객체가 주어졌다는 오류가 계속 발생합니다.
B: 이 `Schema`가 `ninja_schema`에서 온 것이 원인일 줄은 꿈에도 몰랐습니다.
