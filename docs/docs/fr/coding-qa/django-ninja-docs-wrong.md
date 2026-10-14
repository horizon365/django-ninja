Un problème curieux sur la page de documentation de django ninja : deux endpoints différents s'ouvrent en même temps
==========================================================

Récemment, un membre de la communauté a signalé un problème : sur la page de documentation, cliquer sur l'un des deux endpoints ouvre les deux simultanément. Les autres API ne se comportent pas de cette façon.

![django-ninja-docs-wrong](/img/docs-wrong.png)


La cause profonde a finalement été localisée : les noms de fonctions ou les chemins étaient dupliqués. Autrement dit, en écrivant la vue, une fonction a été copiée et son nom a été oublié lors du changement.
