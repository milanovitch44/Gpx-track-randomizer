import xml.etree.ElementTree as ET
from random import random
import math
import easygui


# ET.register_namespace('', "http://www.topografix.com/GPX/1/0")
# ET.register_namespace("", "http://www.book.org/Book-19200/biblography")
inputPath = easygui.fileopenbox(filetypes="*.gpx")
outputPath = inputPath[:-4]+" OUTPUT.gpx"
def truncate(n):
    return int(n * 100_000) / 100_000
def dist(a,b,c,d):
    return math.sqrt((a-c)*(a-c)+(b-d)*(b-d))
def getTracks(parent):
    print(parent)
    foundTracks = []
    print(parent.tag)


    if parent.tag.find("trkpt")!=-1:
        print("Track point returned")
        return [parent,]
    
    for child in parent:
        
        foundTracks.extend(getTracks(child))
    print("Return")
    return foundTracks


            


ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
tree = ET.parse(inputPath)
root = tree.getroot()
print(root[1].getchildren())

tracks = getTracks(root)
print(len(tracks))
imprecision = 6
difference = imprecision/70_000 #degree
direction = 0
dirDif = math.pi*0.7
prevLat = 0
prevLon = 0
for point in tracks:
    print(point.attrib, end="->")
    lat = float(point.attrib["lat"])
    lon = float(point.attrib["lon"])
    direction += dirDif*(2*random()-1)*(dist(prevLat,prevLon,lat,lon)/2000)
    
    point.attrib["lat"] = str(truncate(lat+(math.sin(direction)*difference)))
    point.attrib["lon"] = str(truncate(lon+(math.cos(direction)*difference)))
    print(point.attrib)

tree.write(outputPath)


with open(outputPath,"r+") as file:
    string = file.read()
    string = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n"+string
    file.seek(0)
    file.write(string)
    

    
