import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

#df: the data frame of the tele data
#gdf: the geo data frame
def get_comunas_bts_dict(df, gdf):
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
                #df_bts_comuna['comuna'][count] = comuna
                df_bts_comuna.iloc[count, df_bts_comuna.columns.get_loc('comuna')] = comuna

    #output the comunas csv
    df_bts_comuna.to_csv('bts_comuna.csv')

    #add lat and lon to coord column
    df_bts_comuna['coord'] = list(zip(df_bts_comuna['lat'], df_bts_comuna['lon']))            

    print('Finish locate conmas')

    list_coord = df_bts_comuna['coord'].unique().tolist()
    dict_coord_bts = {}

    for coord in list_coord:
        dict_coord_bts[coord] = df_bts_comuna[df_bts_comuna['coord'] == coord]['bts_id'].tolist()

    import pickle
    with open("dict_coord_bts.pickle", "wb") as outfile:
        # "wb" argument opens the file in binary mode
        pickle.dump(dict_coord_bts, outfile)

    print('finish dict_coord_bts.pickle')    

if __name__ == '__main__':
    print('start to load csv')
    #load tele data
    teledata_location = '~/H/OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey/MachineLearning_Extern/ClassContent/Reto/Matrices de Viaje para Santiago Chile/DataSet/'
    df = pd.read_csv(teledata_location + '20210101_RM.csv')  
    print('finish loading tele data')


    #load map data
    map_loc = '~/H/OneDrive - Instituto Tecnologico y de Estudios Superiores de Monterrey/MachineLearning_Extern/ClassContent/Reto/Actividades/R13/'
    gdf = gpd.read_file(map_loc + "COMUNA_C17.shp")
    print('finish loading map data')

    #generate comunas and bts dict
    get_comunas_bts_dict(df, gdf)