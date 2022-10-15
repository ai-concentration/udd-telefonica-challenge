# udd-telefonica-challenge
-----------------------------------------------------------------------------------------------------------------------------------------------
## Feedback: Reto Metodology 
https://drive.google.com/drive/folders/1p9R4YdBi9gdW8mukZyk7JRWFNDUAqrAt?usp=sharing
Inside the folder called Reto2 you will find:
- To do list:
	- Contains the list of tasks performed and to be performed for the project. It gives us information such as the number of hours it took to do the task,
	planned date, date completed, among other useful information. It also includes two graphs (on different sheets) in which we can
	compare the planned cost of the activity against the actual cost in hours (PivotTable2) and compare the progress of the project that is planned
	against actual progress so far(PivotTable1)
-Business Understanding:
	- Contains information that is relevant to the challenge, such as data on the training partner, the resources that the team has,
	software that will be used to solve the challenge.
	- This folder also contains some auxiliary files generated for data management
	
-----------------------------------------------------------------------------------------------------------------------------------------------------
## Feedback: Reto Data
https://docs.google.com/document/d/1OKse4OCg9Cg-0ZdUdqQauTMbn7EcfO73dvcSvLNCciY/edit?usp=sharing
The Data preparation section includes:
	- The tools and tecniques
	- Cleaning data
	- Scripts configuration
	- Are we will using split data?
	- Does the project use Big data?

----------------------------------------------------------------------------------------------------------------------------------------------------
## comunas.py

This python file uses a Google API to get information from the position of the antenna,
we give the longitud and latitud of each antena and the API helps us to know in which 
comuna they are. At the end, the script generates the "antennas_geolocation.csv"

This file contains:
- the id of the antena,
- the coordinates
- the name of the comuna where each antena. 

How to run comunas.py

- You need to install all the needed dependencies, you can do it by runing:
```
!pip install -r"requirements.txt" #(dont forget to put requirements.txt file in the same folder)
```
- You must have the "reverse-geocoding-responses" folder as a subfolder so the script can take the information
	of the antenna from it
- You must have the dataset with the whole data in the same folder

-------------------------------------------------------------------------------------------------------------------------------------------------------
## Functions_and_visualization.ipynb

- Contiene 2 funciones que esperamos resulten útiles para generar la matriz origen destino
	- Función que ayuda a conocer la distancia en Kilometros entre 2 puntos dados en coordenadas. 
	- Función que recibe una coordenada "coor" y una distancia "d" y devuelve 3 puntos que se encuentran a "d" kilometros del punto "coor"
- Contiene alguna visualizaciones básicas para poder comenzar a comprender los datos
	- Comportamiento sobre el tiempo de las 3 antenas más concurridas
	- Se revisa que no hayan outliers, checando que no los datos de coordenadas fuera del rango esperado.

# Expected directory tree
For the programs of the project to run without any issues, the 
following directory tree must be in place:
```
.
├── json
│   ├── routes
│   └── reverse-geocoding-responses
├── data
│   ├── data.csv
│   └── santiago-chile-shape-files
├── README.md
├── environment.yml
└── phones_dataset.names
```

# Conda setup
1. Install a distribution of Anaconda or Miniconda
2. Create conda environment from `environment.yml`:
	```sh
	conda env create -f environment.yml
	```
3. Activate environment:
	```sh
	conda activate udd-telefonica-challenge
	```
