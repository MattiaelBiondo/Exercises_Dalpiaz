from pyqgis_scripting_ext.core import*

#Function to convert coordinates:
def fromLatString(latString):
    sign = latString[0]
    latDegrees = float(latString[1:3])
    latMinutes = float(latString[4:6])
    latSeconds = float(latString[7:9])
    lat = latDegrees + latMinutes/60 + latSeconds/3600
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


folder = "C:/Users/matti/Documents/Magistrale/primo_anno_2023-2024/advanced geomatics/packages/"
stationFile = "C:/Users/matti/Documents/Magistrale/primo_anno_2023-2024/advanced geomatics/refreshing_ex/stations.txt"
geopackagePath = folder + "natural_earth_vector.gpkg"

with open(stationFile, 'r') as file:
    lines = file.readlines()

HMap.remove_layers_by_name(["OpenStreetMap", "stations"])

osm = HMap.get_osm_layer()
HMap.add_layer(osm)




lineSplit = lines[0].strip()[1:].split(",")
print(lineSplit)
fields = {i.strip(): "String" for i in lineSplit}
# print(fields)
stationLayer = HVectorLayer.new("stations", "Point", "EPSG:4326", fields)



for line in lines[1:]:
    lineSplit2 = line.strip().split(",")
    # print(lineSplit2)
    latString = lineSplit2[3]
    lonString = lineSplit2[4]
    
    latDec = fromLatString(latString)
    lonDec = fromLonString(lonString)
    
    point = HPoint(lonDec, latDec)
    stationLayer.add_feature(point, lineSplit2)

# HMap.add_layer(stationLayer)
path = folder + "stations.gpkg"
error = stationLayer.dump_to_gpkg(path, overwrite=True)
if error:
    print(error)
allStations = HVectorLayer.open(path, "stations")

HMap.add_layer(allStations)