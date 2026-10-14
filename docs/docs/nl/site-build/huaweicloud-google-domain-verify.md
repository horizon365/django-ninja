---
comments: true
---
# Het eigendom van een Google-domein verifiëren op Huawei Cloud

Als je Google Analytics wilt inschakelen, moet je eerst het eigendom van het domein verifiëren.

Er zijn twee methoden. Eén ervan gaat via de URL-prefix: als je bijvoorbeeld `https://pingti.ren/` invoert, kunnen alle URL's daaronder worden gemonitord, maar er is een nadeel. Subdomeinen kunnen niet worden gemonitord — bijvoorbeeld `https://docs.pingti.ren/` kan niet worden gemonitord.
Daarom kent Google het concept van domeinverificatie. Zolang het met `pingti.ren` te maken heeft, kan het allemaal worden gedekt.

Welke van de twee beter is, hangt af van individuele behoeften. Als je veel subdomeinen hebt, is het uiteraard beter om ze allemaal tegelijk via een domein te verifiëren.

Hier zal ik uitleggen hoe je het TXT-record op Huawei Cloud invult om de domeinverificatie van Google te doorstaan. Er is vrijwel geen informatie online beschikbaar; ik heb het zelf uitgevonden.

Het belangrijkste punt is om het type TXT te selecteren, het veld Name leeg te laten en het veld Value in te vullen met de code die Google je geeft, zoals "google-site-verification=xxxx-xxxxx". En het moet tussen aanhalingstekens staan. De volledige configuratie is te zien in de afbeelding:

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

Dit is de domeinverificatiemethode die Google aanbeveelt. Je kunt het ook via CNAME doen, maar dat vereist twee records.

Zodra de verificatie is geslaagd, wordt het toevoegen van een sitemap in de Google-console heel flexibel, zonder de beperking van de URL-prefix.

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

Zoals je ziet is het heel handig om allerlei subdomeinen toe te voegen.
