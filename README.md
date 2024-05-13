NIPS Papers
==============================

## 🖊️ Rappel du problème

Nous souhaitons explorer la base de données des articles de la conférence NeurIPS de 1987 à 2016.
Télécharger le jeu de données se trouvant ici : https://www.kaggle.com/datasets/benhamner/nips-papers

    1. Dans un premier temps, nous n'allons pas nous intéresser au contenu des articles, mais juste aux relations entre auteurs.
    On considère que deux auteurs sont en lien s’ils sont co-auteurs d’un papier, ce qui permet de définir un graphe dont les nœuds sont les auteurs.
    En Python, explorer le graphe obtenu en faisant une détection et une visualisation des communautés présentes.
    Mettre en évidence des auteurs remarquables par la méthode de votre choix.
    Privilégier la clarté et la lisibilité du code plutôt que la complexité des traitements.

    2. Question bonus : sans nécessairement les implémenter, réfléchir à d’autres méthodes d’exploration et/ou visualisation de ce jeu de données, idéalement en prenant en compte les titres / abstracts / contenus des articles. Nous aborderons ces autres pistes d’exploration le jour de l’entretien.

## 🎁 Livrable du Projet

Le notebook sous `notebooks/NIPS_Paper.ipynb` répond aux questions posées ci-dessus.
De plus, un streamlit d'exploration est lançable via la commande #TODO

## 📦 Installation du projet

_Prérequis_

* Environnement linux (ou WSL2)
* Installation de _poetry_ : https://python-poetry.org/docs/#installing-with-pipx

▶️ Installer les dépendances: `poetry install`


## 💻 Fonctionnalités CLI du projet
* `poetry ...` pour exécuter les commandes de poetry pour gérer votre environnement et votre projet python
* `make format` Pour lancer le formattage du code avec Ruff
* `make lint` Pour lancer le linting du code avec Ruff
* `make full_check` Pour lancer le formattage et le linting du code avec Ruff, et l'analyse statique avec mypy

## Ressources
* https://sites.google.com/site/findcommunities/
* https://python-louvain.readthedocs.io/en/latest/index.html
* https://www.kaggle.com/code/kevinvdsk/community-detection
