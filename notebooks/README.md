# Bonnes pratiques

### Nom du notebook

Suivre la convention de nommage `votreTrigramme.NuméroExecution.titreDescriptif`. Par exemple:
> vha.0.data_preprocessing.ipynb
> lvi.1.great_expectations_profiling.ipynb

L'extension peut aussi être en `*.py` grâce à Databricks ou VScode

### Structure du notebook

1. User et abuser du Markdown pour mettre des titres et explications clairs à chaque section
2. Ajouter un petit préambule au début du notebook qui explique ce que ce dernier contient
3. Utilisez l'extension [TOC](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/toc2/README.html)
4. Vos cellules doivent bien être ordonnées pour que le notebook puisse être rejoué sans erreur si vous le pushez sur le repo.
5. Idéallement, vous regroupez tous vos imports dans une cellule unique en début de notebook
6. N'hésitez pas à utiliser le snippet suivant pour recharger les modules importés s'ils changent

```
%load_ext autoreload
%autoreload 2
```

### Productivité et qualité du code

1. Autocomplétion du code: [Hinterland](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/hinterland/README.html)
2. [Auto PEP-8](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/code_prettify/README_autopep8.html)
3. Code répétitif (imports, ...) ? [Créez vos snippets prêt à l'emploi](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/snippets/README.html?highlight=Snippets)


### Code stable et important: à sortir du notebook

Une fois que certaines de vos fonctions deviennent fixes et ont une qualité d'édition suffisante, sortez-les du notebook
et importez les depuis le module dans lequel vous les avez rangé.

```python
df = pd.read_csv(filename)
df.drop( ...
df.query( ...
df.groupby( ...
```

deviendra

```python
def load_and_preprocess_data(filename: str) -> pd.DataFrame:
   """DOCSTRING"""
   # do stuff
   # ...
   return df
```

puis:

```python
import dataprep
...
df = dataprep.load_and_preprocess_data(filename=filename)
```
