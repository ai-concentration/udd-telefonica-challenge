# udd-telefonica-challenge
This python file uses a Google API to get information from the position of the antenna,
we give the longitud and latitud of each antena and the API helps us to know in which 
comuna they are. At the end, the script generates the "antennas_geolocation.csv"

This file contains:
- the id of the antena,
- the coordinates
- the name of the comuna where each antena. 

How to run comunas.py

- You need to install all the needed dependencies, you can do it by runing:
```sh
		!pip install -r"requirements.txt" #(dont forget to put requirements.txt file in the same folder)
		```
- You must have the "reverse-geocoding-responses" folder as a subfolder so the script can take the information
	of the antenna from it
- You must have the dataset with the whole data in the same folder
