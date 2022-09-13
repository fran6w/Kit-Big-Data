# Kit Big Data - Session 2
**Plan de la session**

- Correction projet maison n° 1
- Introduction à **NumPy**
- Introduction à **pandas**
- Series et DataFrame

**Projet maison n° 1**

- Compléter le chargement des données en ajoutant au dataframe `GEO`
    - les colonnes "lat" et "lon" avec la latitude et la longitude des communes
    - une colonne "cp_ville" avec le Code Postal + un espace + et le nom de la Commune
- Ecrire une fonction `search_city(lat, lon)` qui retourne le "cp_ville" de la commune la plus proche d'un point à partir de sa latitude et sa longitude.
- Ecrire une fonction `dms2dec(deg, min, sec)` qui convertit les degrés, minutes, secondes en valeur numérique pour pouvoir utiliser la fonction précédente avec un GPS.

**Projet maison n° 2**

La colonne "geo_shape" comporte des chaines de catactères au format JSON. Elles représentent les formes géométriques des communes qui sont soit des polygones soit composées de plusieurs polygones.\n",

- Utiliser la librairie Python **json** pour parser les valeurs de la colonne "geo_shape" et mettre le résultat (`Series`) dans la variable `GEO_SHAPE`.
- Ecrire une fonction `get_types()` qui retourne le décompte (`value_counts()`) des valeurs accédées avec la clé "type".
- Ecrire une fonction `get_coordinates_len()` qui retourne le décompte (`value_counts()`) des longueurs des listes accédées avec la clé "coordinates".
- Ecrire une fonction `get_most_complex_city()` qui retourne la commune est constituée du plus grand nombre de polygones ?
- Ecrire une fonction `get_nb_cities_2_polygons()` qui retourne  le nombre de villes qui sont de type "Polygon" mais dont la longueur des listes accédées avec la clé "coordinates" vaut 2 ?
- **Facultatif :**
- Pour ces villes vérifier que le premier polygone contient bien le second (enclave). NB : on pourra installer la librairie **shapely**, utiliser la classe Polygon de **shapely.geometry**  et la méthode `contains()`. Sur Windows **shapely** peut nécessiter d'installer manuellement la dll "geos_c.dll" dans le répertoire "Library/bin" de votre environnement Python.

**Utilisation d'environnements virtuels** :

Pour isoler les librairies utilisées dans un projet, se créer un environnement Python par projet, par exemple :

<code>conda create --name myenv</code> ou <code>conda create --name myenv Python=3.9</code> pour préciser une version de Python

Ensuite activer l'environnement à utiliser dans un terminal au niveau de votre notebook :

<code>conda activate myenv</code> (linux) ou <code>activate myenv</code> (Windows)

Puis lancer jupyter :

<code>jupyter notebook</code>

Votre notebook sera dans l'envrionnement sélectionné.

Voir la doc complète sur le sujet : https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html 

**Utilisation de git**

- Se créer un compte sur github et le mettre dans l'organisation du Master
- Rappatrier le cours une première fois avec : <code>git clone https://github.com/fran6w/Kit-Big-Data</code>
- Puis le mettre à jour à chaque fois avec : <code>git pull</code>
- Copier ce repository local dans un répertoire de travail pour suivre le cours ou faire les projets.
- Copier ensuite vos travaux dans le repository local de <u>votre compte github</u> et les exporter avec la séquence  :
  - <code>git add .</code>
  - <code>git commit -m "message"</code>
  - <code>git push</code>
