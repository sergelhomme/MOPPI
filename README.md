# MOPPI
<p align="justify"> Plugin QGIS cherchant à minimiser les problèmes de mobilité du personnel d'une entreprise ou d'une organisation en période d'inondation. MOPPI est l'acronyme de MObilité du Personnel en Période d'Inondation. </p>

<p align="justify"> A partir de simples fichiers comportant des adresses (un fichier "employés" et un fichier "établissements" par exemple), l'outil permet premièrement de géolocaliser les employés et les établissements, puis de calculer les temps de parcours des employés vers tous les établissements en se fondant sur différents scénarios de pertubations du réseau routier et/ou du réseau de transport en commun. Le distancier ainsi produit pourra alors être utilisé pour résourdre un problème d'optimisation (de manière exacte ou approchée), cherchant à minimiser le temps total parcouru par l'ensemble des employés vers les établissements. Lorsque qu'il n'est pas possible que tous les employés puissent se rendre sur un lieu de travail accessible malgré l'inondation, l'outil cherchera à minimiser le nombre d'employés ne pouvant pas se rendre sur un lieu de travail. Parfois, afin réduire les temps de calcul, il peut se révéler nécessaire de regrouper les individus en se fondant sur des critères de proximité de leur lieu d'habitation, c'est pourquoi l'outil permet aussi d'effectuer du clustering (des regroupements).</p>

## Optimisation

Objectif final de l'outil, l'optimisation permet d'affecter au mieux le personnel à un lieu de travail afin de minimiser l'impact d'une crue à cinétique lente pour une entreprise ou une oraginisation.

![Une illustration de l'optimisation](https://github.com/sergelhomme/MOPPI/blob/master/images/MOPPI3.png)

<p align="center"> Les pentagones en orange représentent les établissements pouvant accueillir les employés. </p>

## Géocodage et Distancier

xxxx

## Clustering

xxxx

## RGC4

L'outil MOPPI a été développé dans le cadre d'un projet ANR (CNRS) nommé RGC4. Ce projet regroupe des chercheurs du Lab'Urba (UPEC, EIVP), du LITIS (INSA Rouen), de GéoRessources (Mines de Nancy) et du Cemotev (UVSQ). https://rgc4.wordpress.com/

## Données

MOPPI nécessite de disposer de données concernant les réseaux de transport. Pour tester l'outil, des données sont disponibles ici. Pour des applications plus précises, veuillez écrire à l'adresse mail suivante : serge.lhomme[at]u-pec.fr

Produites dans le cadre du projet RGC4, des données concernant l'Ile-de-France pourront être mises à votre disposition rapidement.
