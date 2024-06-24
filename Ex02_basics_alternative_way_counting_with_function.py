from pyqgis_scripting_ext.core import*

folder = "C:/Users/matti/Documents/Magistrale/primo anno 2023-2024/advanced geomatics/exercises_class4/"

filePath = f"{folder}/stations.txt"
with open(filePath, 'r') as file:
    lines = file.readlines()

points = []
for line in lines[1:]:
    line = line.strip()
    lineSplit = line.split(",")
    
    lat = lineSplit[3]
    latSplit = lat.split(":")
    lat1 = float(latSplit[0])
    lat2 = float(latSplit[1])/60
    lat3 = float(latSplit[2])/3600
    latVal = lat1 + lat2 + lat3
    
    lon = lineSplit[4]
    lonSplit = lon.split(":")
    lon1 = float(lonSplit[0])
    lon2 = float(lonSplit[1])/60
    lon3 = float(lonSplit[2])/3600
    lonVal = lon1 + lon2 + lon3
    
    point = HPoint(lonVal, latVal)
    points.append(point)


canvas = HMapCanvas()

for point in points:
    canvas.add_geometry(point, "purple", 1)

bounds = [-50, 0, 80, 80]
canvas.set_extent(bounds)
canvas.show()
    

from collections import Counter

stationPos = []
for line in lines[1:]:
    line = line.strip()
    lineSplit2 = line.split(",")
    # print(lineSplit2)
    pos = lineSplit2[2]
    stationPos.append(pos)


def stationCount(stationPos):
    stationNum = Counter(stationPos)
    return stationNum

numbers = stationCount(stationPos)
for country, num in numbers.items():
    print(f"{country}: {num}")
    