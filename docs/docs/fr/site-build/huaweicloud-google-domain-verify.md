---
comments: true
---
# Vérifier la propriété d'un domaine Google sur Huawei Cloud

Si vous souhaitez activer Google Analytics, vous devez d'abord vérifier la propriété du domaine.

Il existe deux méthodes. L'une passe par le préfixe d'URL : par exemple, si vous saisissez `https://pingti.ren/`, alors toutes les URLs situées sous celle-ci pourront être surveillées, mais il y a un inconvénient. Les sous-domaines ne peuvent pas être surveillés — par exemple, `https://docs.pingti.ren/` ne peut pas être surveillé.
Google a donc le concept de vérification de domaine. Tant que c'est lié à `pingti.ren`, tout peut être couvert.

Quant à savoir laquelle est la meilleure, cela dépend des besoins de chacun. Si vous avez beaucoup de sous-domaines, il est évidemment préférable de tout vérifier d'un coup via un domaine.

Ici, je vais expliquer comment renseigner l'enregistrement TXT sur Huawei Cloud pour passer la vérification de domaine de Google. Il n'y a pratiquement aucune information disponible en ligne ; je l'ai découvert par moi-même.

Le point essentiel est de sélectionner le type TXT, de laisser le champ Name vide, et de renseigner le champ Value avec le code que Google vous donne, par exemple « google-site-verification=xxxx-xxxxx ». Et il doit impérativement être entouré de guillemets. La configuration complète est montrée dans la figure :

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

C'est la méthode de vérification de domaine recommandée par Google. Vous pouvez aussi le faire via CNAME, mais cela nécessite deux enregistrements.

Une fois la vérification passée, l'ajout d'un sitemap dans la console Google devient très flexible, sans la restriction du préfixe d'URL.

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

Comme vous pouvez le voir, il est très pratique d'ajouter divers sous-domaines.
