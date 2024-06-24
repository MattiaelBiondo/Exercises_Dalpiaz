from pyqgis_scripting_ext.core import*

#Necessary functions:
def fromLatString(latString):
    sign = latString[0]
    latDegrees = float(latString[1:3])
    latMinutes = float(latString[4:6])
    latSeconds = float(latString[7:9])
    lat = latDegrees + latMinutes/60 + latSeconds/3600 #lat is a variable inside a function; it won't overwrite the two variable of the center point
    if sign == '-':
        lat = lat * -1
    return lat
    
def fromLonString(lonString):
    sign = lonString[0]
    lonDegrees = float(lonString[1:4])
    lonMinutes = float(lonString[5:7])
    lonSeconds = float(lonString[8:10])
    lon = lonDegrees + lonMinutes/60 + lonSeconds/3600
    if sign == '-':
        lon = lon * -1
    return lon

# Here the code starts:

lon = 11.34999
lat = 46.49809
radiusKm = 20.0

stationFile = r"C:\Users\matti\Documents\Magistrale\primo_anno_2023-2024\advanced geomatics\refreshing_ex\stations.txt"
centerPoint = HPoint(lon, lat)
with open(stationFile, 'r') as file:
    lines = file.readlines()

crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(32632)

centerPoint32632 = crsHelper.transform(centerPoint)


buffer = centerPoint32632.buffer(radiusKm * 1000)

for line in lines[1:]:
    line = line.strip()
    lineSplit = line.split(",")
    name = lineSplit[1].strip()
    latString = lineSplit[3]
    lonString = lineSplit[4]
    
    latDec = fromLatString(latString)
    lonDec = fromLonString(lonString)
    
    point = HPoint(lonDec, latDec)
    point32632 = crsHelper.transform(point)
    
    if buffer.intersects(point32632):
        distance = point32632.distance(centerPoint32632)
        print(name, distance/1000, point)