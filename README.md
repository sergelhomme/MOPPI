# MOPPI
<p align="justify"> Plugin QGIS cherchant à minimiser les problèmes de mobilité du personnel d'une entreprise, ou plus généralement d'une organisation, en période d'inondation, MOPPI est l'acronyme de MObilité du Personnel en Période d'Inondation. </p>

<p align="justify"> A partir de simples fichiers comportant des adresses (un fichier "employés" et un fichier "établissements" par exemple), l'outil permet premièrement de géolocaliser les employés et les établissements, puis de calculer les temps de parcours des employés vers tous les établissements en se fondant sur différents scénarios de pertubations du réseau routier et/ou du réseau de transport en commun. Le distancier ainsi produit pourra alors être utilisé pour résoudre un problème d'optimisation (de manière exacte ou approchée), cherchant à minimiser le temps total parcouru par l'ensemble des employés vers les établissements. Lorsque qu'il n'est pas possible que tous les employés puissent se rendre sur un lieu de travail accessible à cause de l'inondation, l'outil cherchera à minimiser le nombre d'employés ne pouvant pas se rendre sur un lieu de travail. Parfois, afin réduire les temps de calcul, il peut se révéler nécessaire de regrouper les individus en se fondant sur des critères de proximité de leur lieu d'habitation, c'est pourquoi l'outil permet aussi d'effectuer du clustering (des regroupements).</p>

## Optimisation

<p align="justify"> Objectif final de l'outil, le modèle d'optimisation développé propose de réaffecter (redistribuer) le personnel au sein des différents lieux de travail d’une organisation, en tenant compte des probables perturbations de l’offre de transport générées par une inondation. Cette réaffectation doit permettre de minimiser l'impact d'une crue à cinétique lente pour une entreprise ou une oraginisation en permettant au plus grand nombre d'employés de venir travailler alors que les système de transport sont perturbés. </p>

![Une illustration de l'optimisation](https://github.com/sergelhomme/MOPPI/blob/master/images/MOPPI3.png)

<p align="center"> Les 5 pentagones en orange représentent les établissements pouvant accueillir les employés. Chaque établissement peut acceullir dans cet exemple 100 personnes. Les 500 employés à réaffecter sont repésentés par des points. L'outil détermine ici que les employés représentés par la même couleur sont affectés au même établissement afin d'obtenir la meilleure solution. Ici, tous les employés peuvent se rendre sur un lieu de travail. </p>

## Géocodage et Distancier

<p align="justify"> Pour résoudre le modèle d'optimisation, il est nécessaire : 1) de disposer de données géocodées concernant les établissements et les employés ; 2) de disposer d'un distancier. C'est pourquoi, MOPPI propose de géocoder des données et de calculer ce distancier, c'est à dire de calculer toutes les distances entre les employés et les établissements. Pour calculer, ce distancier deux solutions sont proposées, utiliser des API (par exemple durant la crise) ou utiliser des shapefiles (voire données plus bas). </p>

![Une illustration du distancier](https://github.com/sergelhomme/MOPPI/blob/master/images/MOPPI4.png)

<p align="center"> Les 5 pentagones en orange représentent les établissements pouvant accueillir les employés. Les dix points bleus représentent les employés. Les lignes rouges correspondent au distancier calculé par MOPPI. Ce distancier se fonde sur les lignes et les noeuds du réseau représentés en gris. La table du distancier permet de voir le temps nécessaire à un employé pour se rendre à un établissement donné. </p>

## Clustering

xxxx

![Une illustration du clustering](https://github.com/sergelhomme/MOPPI/blob/master/images/MOPPI5.png)

<p align="center"> xxx </p>

## RGC4

<p align="justify"> L'outil MOPPI a été développé dans le cadre d'un projet ANR (CNRS) nommé RGC4. Ce projet regroupe des chercheurs du Lab'Urba (UPEC, EIVP), du LITIS (INSA Rouen), de GéoRessources (Mines de Nancy) et du Cemotev (UVSQ). </p>
 
https://rgc4.wordpress.com/

## Données

<p align="justify"> MOPPI nécessite de disposer de données concernant les réseaux de transport. Pour tester l'outil, des données sont disponibles ici. Pour des applications plus précises, veuillez écrire à l'adresse mail suivante : serge.lhomme[at]u-pec.fr </p>

<p align="justify"> Produites dans le cadre du projet RGC4, des données concernant l'Ile-de-France pourront être mises à votre disposition rapidement. </p>
