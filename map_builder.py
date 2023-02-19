'''Module to create a map'''
import argparse
from math import radians, sin, cos, sqrt, asin
import folium
from folium import plugins
from geopy.geocoders import Nominatim

def read_file(way: str, date: int):
    """Function to read locations of mivies of certain year

    Args:
        way (str): pth to file
        date (int): year of films to look for

    Returns:
        list: list of locations
    """
    with open(way, 'rb') as file:
        date = f'({date})'
        res = []
        for line in file:
            try:
                line = line.decode().strip()
                if date in line:
                    res.append(line)
            except UnicodeDecodeError:
                continue

        res = [elem.split('\t') for elem in res[14:-2]]
        res = {line[-2] if '(' in line[-1] else line[-1] for line in res}

        return res


def find_coords(points: str) -> list:
    """
    Function to find coordinates based on addresses

    Args:
        points (str): list of addresses

    Returns:
        list(tuple): list of coordinates
    """
    geolocator = Nominatim(user_agent="http")
    places = []

    for point in points:
        try:
            location = geolocator.geocode(point)
            if location:
                places.append((location.latitude, location.longitude))
        except:
            print('error')
            continue
    return places


def calc_distance(lat1: int, lon1: int, lat2: int, lon2: int) -> list:
    """Function to calculate distance from our location to location of movie

    Args:
        lat1 (int): our latitude
        lon1 (int): our longtitude
        lat2 (int): movie's latitude
        lon2 (int): movie's longtitude

    Returns:
        list: list of distances
    """
    radius = 6372.8

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dist = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    res = 2 * asin(sqrt(dist))

    return radius * res


def build_map(my_loc: tuple, addresses: list):
    """_summary_

    Args:
        my_loc (tuple): _description_
        addresses (list): _description_
    """  
    lat = [address[0][0] for address in addresses]
    lon = [address[0][1] for address in addresses]
    dists = [address[1] for address in addresses]
    maps = folium.Map(location=my_loc, zoom_start=10)
    html = """<h4>Info:</h4>
        Distance to me: {}
        """
    maps.add_child(folium.Marker(location=my_loc,
                   popup='Me',
                   icon=folium.Icon(color="blue")))

    fg = folium.FeatureGroup(name='Popups')

    for lt, ln, dist in zip(lat, lon, dists):
        iframe = folium.IFrame(html=html.format(f'{round(dist, 1)} km'),
                          width=300,
                          height=100)

        fg.add_child(folium.Marker(location=[lt, ln],
                    popup=folium.Popup(iframe),
                    icon=folium.Icon(color = "red")))

    fg2 = folium.FeatureGroup(name='Circles')

    for lt, ln, _ in zip(lat, lon, dists):
        fg2.add_child(folium.CircleMarker(location=[lt, ln],radius=20, fill_color='blue'))

    maps.add_child(fg)
    maps.add_child(fg2)

    minimap = plugins.MiniMap(toggle_display=True)
    maps.add_child(minimap)
    maps.add_child(folium.LayerControl())
    maps.save('Map_New.html')

def main():
    """
    The main budy of function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='enter year of movie')
    parser.add_argument('lat', type=float, help='enter latitude')
    parser.add_argument('lon', type=float, help='enter longtitude')
    parser.add_argument('path', type=str, help='enter path to dataset')

    args = parser.parse_args()

    year = args.year
    lat = args.lat
    lon = args.lon
    path = args.path
    my_loc = [lat, lon]

    locations = find_coords(read_file(path, year))
    points = [[elem, calc_distance(lat, lon, elem[0], elem[1])] for elem in locations]
    points.sort(key = lambda x: x[1])
    points = points[:10]
    build_map(my_loc, points)

if __name__ == '__main__':
    main()
