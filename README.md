# udd-telefonica-challenge
-----------------------------------------------------------------------------------------------------------------------------------------------
## Momento de Retroalimentación: Reto Metodología 
Dentro del folder llamado Reto2 se encuentra:
- To do list:
	- Contiene la lista de las tareas realizadaas y por realizar para el proyecto. Nos da información como la cantidad de horas que tomó hacer la tarea,
		fecha planeada, fecha en la que se completó, entre otra información útil. Tambien incluye dos graficas(en hojas diferentes) en las que podemos
		comparar el costo planeado de la actividad contra el costo real en horas (TablaDinámica2) y comparar el avance de poryecto que se tiene planeado
		contra el avance real hasta el momento(TablaDinámica1)
- Business Understanding:
	- Contiene información que resulta relevante dentro del reto,como datos sobre el socio formador, los recursos con los que el equipo cuenta, 
		software que se estará usando para la solución del reto. 
- Este folder también contiene algunos archivos auxiliares generado para el manejo de datos
	
-----------------------------------------------------------------------------------------------------------------------------------------------------

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

Contiene 2 funciones que esperamos resulten útiles para generar la matriz origen destino
- Función que ayuda a conocer la distancia en Kilometros entre 2 puntos dados en coordenadas. 
- Función que recibe una coordenada "coor" y una distancia "d" y devuelve 3 puntos que se encuentran a "d" kilometros del punto "coor"
Contiene alguna visualizaciones básicas para poder comenzar a comprender los datos
- Comportamiento sobre el tiempo de las 3 antenas más concurridas
- Se revisa que no hayan outliers, checando que no los datos de coordenadas fuera del rango esperado.
