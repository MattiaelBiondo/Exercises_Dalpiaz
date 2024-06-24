from pyqgis_scripting_ext.core import*
# import the http requests library to get stuff from the internet
import requests
# import the url parsing library to urlencode the query
import urllib.parse
# define the query to launch
endpointUrl = "https://query.wikidata.org/sparql?query=";
# define the query to launch
query = """
SELECT ?elevation ?unitLabel ?itemLabel ?itemDescription ?coord
WHERE
{
?psv_triples wikibase:quantityAmount ?elevation .
filter(?elevation > 8000)
?psv_triples wikibase:quantityUnit ?unit .
?p_triples psv:P2044 ?psv_triples .
?p_triples a wikibase:BestRank .
?item p:P2044 ?p_triples .
?item wdt:P625 ?coord .
SERVICE wikibase:label {
bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
}
}
ORDER BY DESC(?elevation)
"""

# URL encode the query string
encoded_query = urllib.parse.quote(query)
# prepare the final url
url = f"{endpointUrl}{encoded_query}&format=json"
# run the query online and get the produced result as a dictionary
r=requests.get(url)
result = r.json()
# print(result)


#Data paths:
folder = "C:/Users/matti/Documents/Magistrale/primo_anno_2023-2024/advanced geomatics/exam_exercise/"
geopackagePath = folder + "natural_earth_vector.gpkg"
countries = "ne_50m_admin_0_countries"

#Clean up, to avoid that everytime you run the code, it creates a new layer
HMap.remove_layers_by_name(["OpenStreetMap", "mountains", countries])

#Load openstreetmap layer and add it to the map:
osm = HMap.get_osm_layer()
HMap.add_layer(osm)
#Load the countries layer:
countriesLayer = HVectorLayer.open(geopackagePath, countries)


#Copy the "result" dictionary and paste in another dictionary called "data":
data = result
# Split the data dictionary to get the information neede to create the map
if data:
    #To select the value corresponding to the key called "head"
    featureHead = result['head']
    #To select the value corresponding to the key called "vars"
    featureHeadList = featureHead['vars']
    #The "featureHeadList" contains the name of the attributes we need
    
    #To select the value corresponding to the key called "results"
    featureResults = result['results']
    #To select the value corresponding to the key called "bindings"
    featureList = featureResults['bindings']
    #The "featureList" contains the value for each peak of the attributes we want to have
    #Print the results to check if the code works:
    # print(featureHeadList)
    # print(featureList)

#Create a schema for the attribute table of the layer: the fields are the item of the "featureHeadList"
fields = {
    "elevation": "float",
    "unitLabel": "String",
    "itemLabel": "String",
    "itemDescription": "String",
    "lon": "Double",
    "lat": "Double"
}

#Create the layer that represents the peaks:
mountainsLayer = HVectorLayer.new("mountains", "Point", "EPSG:4326", fields)

#Create an empty dictionary to fill in with names and elevations: it will be used to list the two highest peaks
highestPeakDict = {}

#Create a loop for each item of the list "featureList", to isolate the value of each attribute(elevation, coordinates,...)
for feature in featureList:
    unitLabelDict = feature['unitLabel']
    unitLabel = unitLabelDict['value']
    
    if 'itemDescription' in feature:
        itemDescriptionDict = feature.get('itemDescription', {})
        itemDescription = itemDescriptionDict['value']
    else:
        itemDescription = "No description"
    
    elevationDict = feature['elevation']
    if unitLabel == "metre":
        elevation = float(elevationDict['value'])
        unitLabel = "meter"
    elif unitLabel == "foot":
        elevation = float(elevationDict['value'])/3.28084
        unitLabel = "meter"
    
    itemLabelDict = feature['itemLabel']
    itemLabel = itemLabelDict['value']
    
    coordDict = feature['coord']
    coordList = coordDict['value']
    #if statement to filter whether the peaks are on the Earth or not:
    if coordList.startswith("<"):
        continue
    coordString = coordList.replace("(", " ")
    coordString1 = coordString.replace(")", "")
    coordSplit = coordString1.split(" ")
    lon = float(coordSplit[1])
    lat = float(coordSplit[2])
    point = HPoint(lon, lat)
    #Add the features to the layer, with an if statement that exclude peaks higher than Mt Everest(known to be the highest point on Earth)
    if elevation < 8850:
        mountainsLayer.add_feature(point, [elevation, unitLabel, itemLabel, itemDescription, lon, lat])
        #Add names and elevations to the dictionary
        highestPeakDict[itemLabel] = elevation
    else:
        continue
    

#Create a list sorted by elevation starting from the dictionary:
peaksSortedList = sorted(highestPeakDict.items(), key=lambda x:x[1], reverse=True)
#Print the two higest peaks:
print("The two highest mountains on Earth are:")
for peak in peaksSortedList[:2]:
    name, height = peak
    print(f"{name} with an elevation of {int(height)} m a.s.l.")

#Styling countriesLayer:
polygonStyle = HFill("Transparent") + HStroke("green", 0.5)
countriesLayer.set_style(polygonStyle)
HMap.add_layer(countriesLayer)

#Styling peaks layer:

ranges = [
    [0, 3000],
    [3001, 5000],
    [5001, 7000],
    [7001, 8000],
    [8001, float('inf')]
]
styles = [
    HMarker("triangle", 2) + HFill('yellow') + HStroke('yellow', 0.1),
    HMarker("triangle", 2) + HFill('orange') + HStroke('orange', 0.1),
    HMarker("triangle", 2) + HFill('red') + HStroke('red', 0.1),
    HMarker("triangle", 2) + HFill('blue') + HStroke('blue', 0.1),
    HMarker("triangle", 2) + HFill('purple') + HStroke('purple', 0.1)
]

labelStyle = HLabel('itemLabel', size=5, color='black') + HHalo() + HFill()
mountainsLayer.set_graduated_style("elevation", ranges, styles, labelStyle)

HMap.add_layer(mountainsLayer)

#Add the layer to the geopackage:
path = folder + "mountains.gpkg"
error = mountainsLayer.dump_to_gpkg(path, overwrite=True)
if error:
    print(error)
#Load the gpkg layer and add to the map, to check if it was created properly
# Earth_mountains = HVectorLayer.open(path, "mountains")
# HMap.add_layer(Earth_mountains)



#Create a PDF:
printer = HPrinter(iface)

mapProperties = {
    "x": 5,
    "y": 25,
    "width": 285,
    "height": 180,
    "extent": countriesLayer.bbox(),
    "frame": True
    }

printer.add_map(**mapProperties)

labelProperties = {
    "x": 110,
    "y": 5,
    "text": "Peaks on Earth",
    "font_size": 28,
    "bold": True,
    "italic": False
}

printer.add_label(**labelProperties)

labelProperties2 = {
    "x": 185,
    "y": 185,
    "text": "The two highest mountains on Earth are:\n 1. Mount Everest: 8848 m a.s.l \n 2. Himalayas: 8848 m a.s.l",
    "font_size": 15,
    "bold": False,
    "italic": False
}
printer.add_label(**labelProperties2)

legendProperties = {
    "x": 5,
    "y": 120,
    "width": 150,
    "height": 90,
    "max_symbol_size": 3
}

printer.add_legend(**legendProperties)

scalebarProperties = {
    "x": 10,
    "y": 190,
    "units": "km",
    "segments": 4,
    "unit_per_segment": 5000,
    "style": "Numeric", #We chose numeric one, because the bar didn't work properly
    "font_size": 15
    }

printer.add_scalebar(**scalebarProperties)

outputPdf = f"{folder}/mountains.pdf"
printer.dump_to_pdf(outputPdf)
    

