# RETO: TELEFONICA CHALLENGUE

----------------------------------------------------------------------------------------------------------------------------------------------------

## Team members

	- Gerardo Peña Pérez A01701474
	- Carlos Alberto Hurtado Sanchez A01700885
	- Kevin Joan Delgado Pérez A01706328
	- Wenguang hu A01706648

-----------------------------------------------------------------------------------------------------------------------------------------------------
## Feedback: Reto Documentation
https://drive.google.com/drive/folders/1p9R4YdBi9gdW8mukZyk7JRWFNDUAqrAt?usp=share_link
Inside the folder called CRISP-DM in Reto2 you will find new folders:

- Data Understanding:
	- Contains all the details of the data used to make new information or inferences of the study cases.
	- This folder just contains the document with the sections of data understanding and the adjusts with CRISP-DM.
- Data preparation:
	- Contains all the process that the team do to get the matrix of origin destiny for count the tracks of the phone_id.
	- This folder just contains the document with the sections of data preparation and the adjusts with CRISP-DM.
- Modeling:
	- Contains information that is relevant for choosing a model to get the objetives of data mining.
	- This folder just contains the document with the sections of data modeling and the adjusts with CRISP-DM.
-----------------------------------------------------------------------------------------------------------------------------------------------------
## Feedback: Reto Security
https://docs.google.com/document/d/19bzXYv0qmKwh5fwQ419PEu9nYqN7SvClEHKyyjYAtAc/edit?usp=sharing
Inside the Data preparation in Google drive, you will find:

- Privacity and Security of data:
	- Contains information that is relevant the process of security that the team and the socio formador do in terms of propposal to the Reto.
	- This folder only contains a document with all the points to answer.
-----------------------------------------------------------------------------------------------------------------------------------------------------
## Feedback: Reto Data
https://docs.google.com/document/d/1OKse4OCg9Cg-0ZdUdqQauTMbn7EcfO73dvcSvLNCciY/edit?usp=sharing
The Data preparation section includes:

	- The tools and tecniques
	- Cleaning data
	- Scripts configuration
	- Are we will using split data?
	- Does the project use Big data?
	
-----------------------------------------------------------------------------------------------------------------------------------------------
## Feedback: Reto Metodology 
https://drive.google.com/drive/folders/1p9R4YdBi9gdW8mukZyk7JRWFNDUAqrAt?usp=sharing
Inside the folder called CRISP-DM in Reto2 you will find:

- To do list:
	- Contains the list of tasks performed and to be performed for the project. It gives us information such as the number of hours it took to do the task,
	planned date, date completed, among other useful information. It also includes two graphs (on different sheets) in which we can
	compare the planned cost of the activity against the actual cost in hours (PivotTable2) and compare the progress of the project that is planned
	against actual progress so far(PivotTable1)
-Business Understanding:
	- Contains information that is relevant to the challenge, such as data on the training partner, the resources that the team has,
	software that will be used to solve the challenge.
	- This folder also contains some auxiliary files generated for data management
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
	- Función que ayuda a conocer la distancia en Kilometros entre 2 puntos dados en coordenadas, esta función se llama "distance_km". 
	- Función que recibe una coordenada "coor" y una distancia "d" y devuelve 3 puntos que se encuentran a "d" kilometros del punto "coor"
- Contiene alguna visualizaciones básicas para poder comenzar a comprender los datos
	- Comportamiento sobre el tiempo de las 3 antenas más concurridas
	- Se revisa que no hayan outliers, checando que no los datos de coordenadas fuera del rango esperado.
---------------------------------------------------------------------------------------------------------------------------------------------------------
## Close_far.py

- This script was used to know the closest and the farthest antena from each antena, we used this information to know if the change between two antenna 
was to one that was close enough to be considered as a real "trace" or if it was just a misconnection of the antenna. In other words, we want to
discard the trips wich speed does not make sense.
- We used the function "distance_km" described above
- Used a dataset with the antenna labeled with the name of the comuna where each antena is

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
