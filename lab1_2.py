import argparse
from math import radians, sin, cos, sqrt, asin
import folium
from folium import plugins
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def read_file(path: str, year: int):
    with open(path, 'rb') as file:
        year = f'({year})'
        res = []
        for line in file:
            try:
                line = line.decode().strip()
                if year in line:
                    res.append(line)
            except UnicodeDecodeError:
                continue
        
        res = [elem.split('\t') for elem in res[14:-2]]
        res = {line[-2] if '(' in line[-1] else line[-1] for line in res}

        return res
# print(read_file('/Users/julia/Desktop/OP/week_1/locations.list', 2015))
def find_coords(points):
    geolocator = Nominatim(user_agent="http")
    places = []
    
    j = 0
    print(points)
    for point in points:
        print(j)
        j+=1

        try:
            location = geolocator.geocode(point)
            if location:
                places.append((location.latitude, location.longitude))
        except:
            continue
    return places


def calc_distance(lat1, lon1, lat2, lon2) -> list:
    radius = 6372.8

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dist = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    res = 2 * asin(sqrt(dist))

    return radius * res


def build_map(my_loc, addresses):
    lat = [address[0][0] for address in addresses]
    lon = [address[0][1] for address in addresses]
    names = [address[1] for address in addresses]
    maps = folium.Map(location=my_loc, zoom_start=10)
    html = """<h4>Info:</h4>
        Distance to me: {}
        """
    maps.add_child(folium.Marker(location=my_loc,
                   popup='Me',
                   icon=folium.Icon(color="blue")))

    fg = folium.FeatureGroup(name='Popups')
    
    for lt, ln, name in zip(lat, lon, names):
        iframe = folium.IFrame(html=html.format(name),
                          width=300,
                          height=100)
        
        fg.add_child(folium.Marker(location=[lt, ln],
                    popup=folium.Popup(iframe),
                    icon=folium.Icon(color = "red")))
    
    fg2 = folium.FeatureGroup(name='Circles')
    
    for lt, ln, _ in zip(lat, lon, names):
        fg2.add_child(folium.CircleMarker(location=[lt, ln],radius=20, fill_color='blue'))

    maps.add_child(fg)
    maps.add_child(fg2)
   
    minimap = plugins.MiniMap(toggle_display=True)
    maps.add_child(minimap)
    maps.add_child(folium.LayerControl())
    maps.save('Map_New.html')

# print(build_map([49.83826, 24.02324], [(49.841952, 24.0315921, "Львів"), (48.287312, 25.1738, "Старі Кути"), (49.993694, 24.898352, "Кути"), (48.296581, 24.87579, "Брустурів")]))

if __name__ == '__main__':
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
    print(points)
    points = points[:5]
    build_map(my_loc, points)

