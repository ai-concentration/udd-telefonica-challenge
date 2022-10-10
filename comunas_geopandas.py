import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

from pathlib import Path

#load tele data
DATA_DIR = Path("data")
df = pd.read_csv(DATA_DIR / 'data.csv')  
print('finish loading tele data')

#load map data
MAP_LOC = DATA_DIR / Path("santiago-chile-shape-files")
gdf = gpd.read_file(MAP_LOC / "COMUNA_C17.shp")
print('finish loading map data')

#get the list of bts_id and phone_id
list_bts_id = df['bts_id'].unique()
list_phone_id = df['PHONE_ID'].unique()

#group the data by bts_id lat and lon
df_groupby_bts = df.groupby(['bts_id', 'lat', 'lon']).size().reset_index(name='counts_per_bts')
print('finish group data by bts')

#create the list of lat and lon for each bts
bts_lat_list = []
bts_lon_list = []
for bts in list_bts_id:
    lat = df_groupby_bts[df_groupby_bts['bts_id'] == bts]['lat'].values[0]
    lon = df_groupby_bts[df_groupby_bts['bts_id'] == bts]['lon'].values[0]
    bts_lat_list.append(lat)
    bts_lon_list.append(lon)

print('finish get lat and lon for bts')

#create the dataframe for the bts to lat and lon
dict_bts = {'bts_id':list_bts_id.tolist(), 'lat':bts_lat_list ,'lon':bts_lon_list}
df_bts = pd.DataFrame(dict_bts)

#check if the location of the bts fall into the specific comunas
df_bts_comuna = df_bts.copy()
df_bts_comuna['comuna'] = pd.NA

for count_comuna in range(gdf['NOM_COMUNA'].count()):
    comuna = gdf['NOM_COMUNA'][count_comuna]
    for count in range(df_bts_comuna['bts_id'].count()):
        lon = df_bts_comuna['lon'][count]
        lat = df_bts_comuna['lat'][count]

        bts_loc = Point(lon, lat)
        geo = gdf['geometry'][count_comuna]
        if(geo.contains(bts_loc)):
            df_bts_comuna['comuna'][count] = comuna

print('Finish locate conmas')

df_bts_comuna.to_csv(DATA_DIR / 'bts_comuna.csv')