import argparse
import folium
from geopy.geocoders import Nominatim

def read_file(path: str, year: int):
    with open(path, 'rb') as file:
        year = f'({year})'
        res = []
        counter = 0
        for line in file:
            try:
                line = line.decode().strip()
                if line.startswith('"') and counter < 10 and year in line:
                    res.append(line)
                    counter += 1
            except UnicodeDecodeError:
                continue
        
        res = [[val for val in elem if val != ''] for elem in [elem.split('\t') for elem in res]]
        res = [[' '.join(elem[1:])] for elem in res]

        return res
print(read_file('/Users/julia/Desktop/OP/week_1/locations.list', 1982))

def find_cord(place):
    pass

def build_map(my_loc, addresses):
    pass

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('year', type=str, help='enter year of movie')
#     parser.add_argument('lat', type=str, help='enter latitude')
#     parser.add_argument('lon', type=str, help='enter longtitude')
#     parser.add_argument('path', type=str, help='enter path to dataset')

#     args = parser.parse_args()

#     year = args.year
#     lat = args.lat
#     lon = args.lon
#     path = args.path
#     my_loc = [lat, lon]
