---
comments: true
---
# Huawei Cloud에서 Google 도메인 소유권 확인하기

Google Analytics를 사용하려면 먼저 도메인 소유권을 확인해야 합니다.

두 가지 방법이 있습니다. 하나는 URL prefix를 사용하는 방식입니다: 예를 들어 `https://pingti.ren/`을 입력하면 그 아래의 모든 URL을 모니터링할 수 있지만, 단점이 있습니다. 서브도메인은 모니터링할 수 없습니다 — 예를 들어 `https://docs.pingti.ren/`은 모니터링할 수 없습니다.
그래서 Google에는 도메인 확인(domain verification)이라는 개념이 있습니다. `pingti.ren`과 관련된 것이라면 모두 커버할 수 있습니다.

어느 쪽이 더 좋은지는 개인의 필요에 따라 다릅니다. 서브도메인이 많다면 당연히 도메인을 통해 한 번에 모두 확인하는 것이 더 좋습니다.

여기서는 Huawei Cloud에서 Google의 도메인 확인을 통과하기 위해 TXT 레코드를 입력하는 방법을 설명하겠습니다. 온라인에서 찾을 수 있는 정보가 거의 없어서 제가 직접 알아냈습니다.

핵심은 TXT 타입을 선택하고, Name은 비워 두고, Value에 Google이 제공하는 코드(예: "google-site-verification=xxxx-xxxxx")를 입력하는 것입니다. 그리고 반드시 따옴표로 감싸야 합니다. 전체 설정은 아래 그림과 같습니다:

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

이것이 Google이 권장하는 도메인 확인 방식입니다. CNAME으로도 할 수 있지만, 두 개의 레코드가 필요합니다.

확인이 통과되면 Google 콘솔에서 sitemap을 추가하는 것이 매우 유연해지며, URL prefix 제한이 없어집니다.

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

보시다시피 다양한 서브도메인을 추가하기가 매우 편리합니다.
