# RETO: TELEFONICA CHALLENGUE

----------------------------------------------------------------------------------------------------------------------------------------------------

## Team members

	- Gerardo Peña Pérez A01701474
	- Kevin Joan Delgado Pérez A01706328
	- Wenguang hu A01706648
----------------------------------------------------------------------------------------------------------------------------------------------------
CRISP-DM phases:
https://github.com/ai-concentration/udd-telefonica-challenge/blob/GerardoA01701474_possibles_branch/CRISPDM.png

- At the beginning, we wanted to generate clusters in order to classify between types of trips (type of transportation, reason of the trip, etc.)
but we decided not to train a k-means model due to scatter plots indicating the presence of messy and dense single chunks instead of the expected and desired  clusters
- Then we realised that the information we were using was not enough so added some new data and start a new iteration in the crisp DM process
 

-----------------------------------------------------------------------------------------------------------------------------------------------------
## Feedback: Reto Documentation
https://drive.google.com/drive/folders/12ECv0qVQ6qV_3E2VJsSBZK5w1__2-KaN?usp=share_link 
Inside the folder called CRISP-DM in Reto2 you will find new folders:
- Business Understanding:
	- Contains the business objectives and data mining objectives. There is described the success criteria of the project
- Data Understanding:
	- Contains all the details of the data used to make new information or inferences of the study cases.
	- This folder just contains the document with the sections of data understanding and the adjusts with CRISP-DM.
- Data preparation:
	- Contains all the process that the team do to get the matrix of origin destiny for count the tracks of the phone_id. And a description of the privacy of the
	 data in the project
	- This folder just contains the document with the sections of data preparation and the adjusts with CRISP-DM.
- Modeling:
	- Contains information that is relevant for choosing a model to get the objetives of data mining.
	- This folder just contains the document with the sections of data modeling and the adjusts with CRISP-DM.
- Evaluation:
	- Contains the review of the process CRISP_DM, and a list of metrics to detemine if the model is correct
- Deployment:
	- Contains the Final Report, the Delivery Plan and the Experience Documentation
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
## Models2.ipynb
In this document is a deeper explanation for the models and the decisions taken: 
https://docs.google.com/document/d/1JN3yrL40wKIZF2NxIs0wxvXpS2e1mmdnepEdiSKPhIA/edit?usp=share_link 

This NoteBook has the 4 models generated for the solution for the Reto:
- 1st Benchmark Model:
	- It is a logistic Regression. We took this baseline model to have a start point and try to improve the performance of the simpliest solution
- 2nd Benchmark Model:
	- It is a Neural Network. We tried to use deeplearning architecture but we came to conclusion that this kind of models are not strong enough to solve
	our problem
	
- 3th Model:
	- It is a random forest. We went for a different approach and used a machine learning architecture, it gave us better results, but still not good enough
- 4th Model:
	- It is a decision tree with XGBoost. With this model we got the higher accuracy score, and after several metrics we decided that this is a good solution
	for the problem we want to solve
- Last and selected Model:
	- It is a similar architecture than the previous model, but with some tuning in the hyperparameters and using a dataset with more information 
	(amount of recreation centers and population of each comuna)

----------------------------------------------------------------------------------------------------------------------------------------------------

## Matrix.py 

This python file takes the dataset 'routes_ready.csv' and adds the name of the comuna where each connection took place.
Generates a dataset with origin, destination and categorical variable for the dwell time and the speed.
Then we use that dataset to generate the matrix with the number of the trips between comunas. Then we display a heatmap for a better visualization 

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
