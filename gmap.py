# coding: utf-8
import time
import json
import os
import ssl
import urllib.request
from PIL import Image

class GmapDirectionToMap:
    def __init__(self, key_file_name):
        self.client = None
        with open(key_file_name,"r") as clientJson :
            self.client = json.load(clientJson)
        
    def findDirectionOfNowToDestination(self, origin, dest, mode = "transit", departure_time = "now"):
        
        key = self.client["key"]

        url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ origin \
                + "&destination=" + dest \
                + "&mode=" + mode \
                + "&departure_time=" + departure_time\
                + "&language=ko" \
                + "&key=" + key

        request         = urllib.request.Request(url)
        context         = ssl._create_unverified_context()
        response        = urllib.request.urlopen(request, context=context)
        responseText    = response.read().decode('utf-8')
        responseJson    = json.loads(responseText)

        return responseJson

    def jsonPathParsing(self, jsonPath):

        path = jsonPath["routes"][0]["legs"][0]
        stepList = path["steps"]

        return stepList

    def drawImageWithJsonPath(self, stepList, center, zoom = 15, maptype = "roadmap", size = "600x300", color = "0x0000ff", weight = 3):
        
        key = self.client["key"]

        pointLongsLats = []
        for path in stepList :
            startLoc = path["start_location"]
            endLoc = path["end_location"]
            pointLongsLats.append((startLoc, endLoc))

        url = "https://maps.googleapis.com/maps/api/staticmap?center=" + center \
                + "&zoom=" + str(zoom) \
                + "&size=" + size \
                + "&maptype=" + maptype \
                + "&path=color:" + color \
                + "|weight:" + str(weight) \
                + "|" + self.__parseStrFittedIntoQuery(pointLongsLats) \
                + "&key=" + key

        #request         = urllib.request.Request(url)
        #context         = ssl._create_unverified_context()
        img = Image.open(urllib.request.urlopen(url))
        img.save('path.png')
        img.show()


    def __parseStrFittedIntoQuery(self, paths):
        parsedStr = str(paths[0][0]["lat"]) + "," + str(paths[0][0]["lng"])
        for start, end in paths:
            parsedStr += "|" + str(end["lat"]) + "," + str(end["lng"])
        return parsedStr

if (__name__ == "__main__") :

    key_file_name = "./google_key.json"
    # 37.561902588364596, 126.99876128465598 공차 동국대점
    # 37.558635453265275, 126.9979472126123 남산학사
    gmapManager = GmapDirectionToMap(key_file_name)
    gongchaLoc = "37.561902588364596,126.99876128465598"
    namsanDormLoc = "37.558635453265275,126.9979472126123"
    jsonResponse = gmapManager.findDirectionOfNowToDestination(origin=gongchaLoc, dest = namsanDormLoc)
    steps = gmapManager.jsonPathParsing(jsonResponse)
    gmapManager.drawImageWithJsonPath(steps, gongchaLoc)


    with open("./Agent_Transit_Directions2.json","w") as rltStream :
        json.dump(jsonResponse,rltStream)

 