import numpy as np

def distance_km(origin, destination):
    """
    Computes the distance between two lat-lon coordinates

    @params
        tuple(int, int)
        origin: lat-lon pair in radians
        
        tuple(int, int)
        destination: lat-lon pair in radians

    @returns
        Distance between origin and destination in km
    """
    EARTH_RADIUS = 6371

    lat = destination[0] - origin[0]
    lon = destination[1] - origin[1]

    arc = np.sin(lat / 2) ** 2 + np.cos(origin[0]) \
        * np.sin(lon / 2) ** 2 * np.cos(destination[0])
    c = 2 * np.arctan2(np.sqrt(arc), np.sqrt(1 - arc))

    return c * EARTH_RADIUS