import xml.etree.ElementTree as ET
from random import random
import math
import easygui

inputPath = easygui.fileopenbox(filetypes="*.gpx")
outputPath = inputPath[:-4]+" OUTPUT.gpx"


def truncate(n):
    return int(n * 100_000) / 100_000


def dist(a, b, c, d):
    return math.sqrt((a-c)*(a-c)+(b-d)*(b-d))


def getTracks(parent):
    foundTracks = []
    print(parent.tag)

    if parent.tag.find("trkpt") != -1:
        return [parent, ]

    for child in parent:

        foundTracks.extend(getTracks(child))

    return foundTracks


ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
tree = ET.parse(inputPath)
root = tree.getroot()

tracks = getTracks(root)
print(len(tracks)+" track poinst found")
unaccuracy = 6  # metre
difference = unaccuracy/70_000  # degree
direction = 0
dirDif = math.pi*0.7
prevLat = 0
prevLon = 0
for point in tracks:
    
    lat = float(point.attrib["lat"])
    lon = float(point.attrib["lon"])
    direction += dirDif*(2*random()-1)*(dist(prevLat, prevLon, lat, lon)/2000)

    point.attrib["lat"] = str(truncate(lat+(math.sin(direction)*difference)))
    point.attrib["lon"] = str(truncate(lon+(math.cos(direction)*difference)))

tree.write(outputPath)

# Adding the xml header
with open(outputPath, "r+") as file:
    string = file.read()
    string = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n"+string
    file.seek(0)
    file.write(string)
print("The track was succesfully randomized")