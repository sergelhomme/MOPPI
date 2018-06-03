# MOPPI
<p align="justify"> Plugin QGIS cherchant à minimiser les problèmes de mobilité du personnel d'une entreprise, ou plus généralement d'une organisation, en période d'inondation, MOPPI est l'acronyme de MObilité du Personnel en Période d'Inondation. </p>

<p align="justify"> A partir de simples fichiers comportant des adresses (un fichier "employés" et un fichier "établissements" par exemple), l'outil permet premièrement de géolocaliser les employés et les établissements, puis de calculer les temps de parcours des employés vers tous les établissements en se fondant sur des scénarios de perturbations du réseau routier et/ou du réseau de transport en commun. Le distancier ainsi produit pourra alors être utilisé pour résoudre un problème d'optimisation (de manière exacte ou approchée), cherchant à minimiser le temps total parcouru par l'ensemble des employés pour se rendre à un établissement tout en respectant les capacités d’accueil des établissements. Lorsqu'il n'est pas possible que tous les employés puissent se rendre sur un lieu de travail à cause de l'inondation, l'outil cherchera à maximiser le nombre d'employés pouvant se rendre sur un lieu de travail. Parfois, afin de réduire les temps de calcul, il peut se révéler nécessaire de regrouper les employés en se fondant sur des critères de proximité spatiale (de leur lieu d'habitation), c'est pourquoi l'outil permet aussi d'effectuer du clustering (des regroupements).</p>

## Optimisation

<p align="justify"> Objectif final de l'outil, le modèle d'optimisation développé propose de réaffecter (redistribuer) le personnel au sein des différents lieux de travail d’une organisation, en tenant compte des probables perturbations de l’offre de transport générées par une inondation. Cette réaffectation doit permettre de minimiser l'impact d'une crue à cinétique lente pour une entreprise, ou une organisation, en permettant au plus grand nombre d'employés de venir travailler alors même que les systèmes de transport sont fortement perturbés. </p>

![Une illustration de l'optimisation](https://github.com/sergelhomme/MOPPI/blob/master/images/MOPPI3.png)

<p align="center"> Dans l’image ci-dessus, les 5 pentagones orange représentent des établissements pouvant accueillir des employés. Dans cet exemple, chaque établissement peut accueillir 100 employés. Les 500 employés à réaffecter dans ces établissements sont représentés par des points. MOPPI permet alors de déterminer où doivent être affectés ces employés afin de minimiser les problématiques de mobilité causées par une inondation. Ainsi, les employés représentés par la même couleur sont affectés à un même établissement. Ici, tous les employés peuvent se rendre sur un lieu de travail. </p>

## Géocodage et Distancier

<p align="justify"> Pour résoudre le problème d'optimisation, il est nécessaire : 1) de disposer de données géocodées concernant les établissements et les employés ; 2) de disposer d'un distancier. C'est pourquoi, MOPPI propose des outils pour géocoder des données (par exemple des fichiers textes d’adresses) et pour calculer des distanciers. Dans ces distanciers, tous les plus courts chemins (en termes de temps de parcours) entre les employés et les établissements sont calculés. Pour calculer ce distancier, deux solutions sont proposées : 1) utiliser des API (par exemple durant la crise) ; 2) utiliser des shapefiles (pour préparer la continuité d’activité en se fondant sur des scénarios de perturbation des réseaux de transport) (voir la partie « Données » plus bas). </p>

![Une illustration du distancier](https://github.com/sergelhomme/MOPPI/blob/master/images/MOPPI4.png)

<p align="center"> Les 5 pentagones en orange représentent les établissements pouvant accueillir les employés. Les dix points bleus représentent les employés. Les lignes rouges correspondent au distancier calculé par MOPPI. Ce distancier se fonde sur les lignes et les noeuds du réseau représentés en gris. La table du distancier permet de voir le temps nécessaire à un employé pour se rendre à un établissement donné. </p>

## Clustering

Afin d'être efficace, il peut être pertinent de regrouper les employés et de ne plus les considérer individuellement. En effet, résoudre le modèle d'optimisation ou calculer le distancier entre tous les employés et tous les établissements peut être très long. 

![Une illustration du clustering](https://github.com/sergelhomme/MOPPI/blob/master/images/MOPPI5.png)

<p align="center"> Les carrés correpsondent à des groupes d'individus regroupés selon des critères spatiaux. Les points sont les individus. Les points possédant une même couleur sont regroupés par MOPPI au sein du carré de la même couleur. Ici les individus regourpés ne peuvent pas habiter à plus de 50 km et doivent appartenir à une même zones (découpage en orange). La taille des carrés est proportionnel au nombre d'individus regroupés. </p>

## RGC4

<p align="justify"> L'outil MOPPI a été développé dans le cadre d'un projet ANR (CNRS) nommé RGC4. Ce projet regroupe des chercheurs du Lab'Urba (UPEC, EIVP), du LITIS (INSA Rouen), de GéoRessources (Mines de Nancy) et du Cemotev (UVSQ). </p>
 
https://rgc4.wordpress.com/

## Données

<p align="justify"> MOPPI nécessite de disposer de données concernant les réseaux de transport. Pour tester l'outil, des données sont disponibles ici. Pour des applications plus précises, veuillez écrire à l'adresse mail suivante : serge.lhomme[at]u-pec.fr </p>

<p align="justify"> Produites dans le cadre du projet RGC4, des données concernant l'Ile-de-France pourront être mises à votre disposition rapidement. </p>
