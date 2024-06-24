from pyqgis_scripting_ext.core import*

#Exercise 1
path = r"C:\Users\matti\Documents\Magistrale\primo_anno_2023-2024\advanced geomatics\class4\02_exe0_geometries.csv"

with open(path, 'r') as file:
    readLines = file.readlines()


points = []
lines = []
polygons = []
for line in readLines:
    line = line.strip()
    lineSplit = line.split(";")
    print(lineSplit)
    gtype = lineSplit[0]
    coords = lineSplit[1]
    num = lineSplit[2]
    
    if gtype == "point":
        cSplit = coords.split(",")
        lon = float(cSplit[0])
        lat = float(cSplit[1])
        point = HPoint(lon, lat)
        points.append(point)
        
    elif gtype == "line":
        cSplit = coords.split(" ")
        pointList = []
        for cStr in cSplit:
            split = cStr.split(",")
            lon = float(split[0])
            lat = float (split[1])
            pointList.append([lon, lat])
        line = HLineString.fromCoords(pointList)
        lines.append(line)
    
    elif gtype == "polygon":
        cSplit = coords.split(" ")
        pointList = []
        for i in cSplit:
            split = i.split(",")
            lon = float(split[0])
            lat = float(split[1])
            pointList.append([lon, lat])
        polygon = HPolygon.fromCoords(pointList)
        polygons.append(polygon)
        
canvas = HMapCanvas()

for arancia in points:
    canvas.add_geometry(arancia, "magenta", 50)

for kiwi in lines:
    canvas.add_geometry(line, "blue", 3)
    
for polygon in polygons:
    canvas.add_geometry(polygon, "red", 1)

bounds = [0, 0, 50, 50]
canvas.set_extent(bounds)
canvas.show()
        