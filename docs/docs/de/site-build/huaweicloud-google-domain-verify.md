---
comments: true
---
# Google-Domain-Verifizierung auf Huawei Cloud

Wenn Sie Google Analytics aktivieren möchten, müssen Sie zuerst das Eigentum an der Domain verifizieren.

Es gibt zwei Methoden. Eine davon über das URL-Präfix: Wenn Sie z. B. `https://pingti.ren/` eingeben, können alle URLs darunter überwacht werden, aber es gibt einen Nachteil: Subdomains können nicht überwacht werden — z. B. kann `https://docs.pingti.ren/` nicht überwacht werden.
Daher hat Google das Konzept der Domain-Verifizierung. Alles, was mit `pingti.ren` zu tun hat, kann damit abgedeckt werden.

Welche Methode besser ist, hängt von den individuellen Anforderungen ab. Wenn Sie viele Subdomains haben, ist es natürlich besser, sie alle auf einmal über eine Domain zu verifizieren.

Hier erkläre ich, wie man den TXT-Eintrag auf Huawei Cloud ausfüllt, um die Google-Domain-Verifizierung zu bestehen. Dazu gibt es im Internet praktisch keine Informationen; ich habe es selbst herausgefunden.

Der entscheidende Punkt ist: Wählen Sie den Typ TXT, lassen Sie Name leer und tragen Sie bei Value den Code ein, den Google Ihnen gibt, z. B. „google-site-verification=xxxx-xxxxx". Er muss in Anführungszeichen gesetzt werden. Die vollständige Konfiguration ist in der Abbildung zu sehen:

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

Dies ist die von Google empfohlene Methode zur Domain-Verifizierung. Sie können dies auch über CNAME tun, dafür sind jedoch zwei Einträge erforderlich.

Sobald die Verifizierung bestanden ist, wird das Hinzufügen einer Sitemap in der Google-Konsole sehr flexibel, ohne die Einschränkung durch das URL-Präfix.

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

Wie Sie sehen, ist es sehr bequem, verschiedene Subdomains hinzuzufügen.
