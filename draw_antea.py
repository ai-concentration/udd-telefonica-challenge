import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from collections import defaultdict
import pickle
import matplotlib.pyplot as plt

def draw_antena(gdf, geodata):
    fig, ax = plt.subplots(figsize=(15,15))
    gdf.plot("NOM_COMUNA", legend = True, legend_kwds={'loc':'lower right', 'bbox_to_anchor':(-0.125,0), 'ncols':2}, ax=ax)
    geodata.plot(ax=ax, color='red', markersize=1)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    use_crs = False

    gdf = gpd.read_file("./data/santiago-chile-shape-files/COMUNA_C17.shp")
    
    with open("./data/dict_coord_bts.pickle", "rb") as infile:
        dict_coord_bts = pickle.load(infile)

    list_bts_coord = list(dict_coord_bts.keys())

    bts_geo = []
    for coord in list_bts_coord:
        bts_geo.append(Point(coord[1], coord[0]))

    if(use_crs):
        crs={'init':'epsg:4326'}
        geodata=gpd.GeoDataFrame(crs=crs, geometry=bts_geo)
    else:
        geodata=gpd.GeoDataFrame(geometry=bts_geo)

    draw_antena(gdf, geodata)