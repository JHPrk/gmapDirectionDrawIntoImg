# coding: utf-8
import time
import json
import os
import ssl
import urllib.request
from PIL import Image
from path_parser import encParser, lonLatParser

def createParser(pathType):
    if pathType == "enc" : 
        return encParser()
    elif pathType == "lonlat" :
        return lonLatParser()
    else :
        raise Exception("pathType is not accurate! you must select {enc, lonlat}")

class GmapDirectionToMap:
    def __init__(self, key_file_name, pathType="enc"):
        self.client = None
        self.parser = createParser(pathType)
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
        return self.parser.jsonPathParsing(jsonPath)

    def drawImageWithJsonPath(self, pathLists, center, zoom = 13, maptype = "roadmap", size = "600x300", color = "0x0000ff", weight = 3):
        
        key = self.client["key"]

        url = "https://maps.googleapis.com/maps/api/staticmap?center=" + center \
                + "&zoom=" + str(zoom) \
                + "&size=" + size \
                + "&maptype=" + maptype \
                + "&path=color:" + color \
                + "|weight:" + str(weight) \
                + "|" + self.__parseStrFittedIntoQuery(pathLists) \
                + "&key=" + key

        #request         = urllib.request.Request(url)
        #context         = ssl._create_unverified_context()
        img = Image.open(urllib.request.urlopen(url))
        return img


    def __parseStrFittedIntoQuery(self, paths):
        return self.parser.parseStrFittedIntoQuery(paths)
if (__name__ == "__main__") :

    key_file_name = "./google_key.json"
    # 37.561902588364596, 126.99876128465598 공차 동국대점
    # 37.558635453265275, 126.9979472126123 남산학사
    # 37.55419153372528, 126.96900733060052 서울역
    gmapManager = GmapDirectionToMap(key_file_name, pathType="lonlat") # "enc"
    gongchaLoc = "37.561902588364596,126.99876128465598"
    namsanDormLoc = "37.558635453265275,126.9979472126123"
    seoulStationLoc = "37.55419153372528,126.96900733060052"
    jsonResponse = gmapManager.findDirectionOfNowToDestination(origin=gongchaLoc, dest = seoulStationLoc)
    steps = gmapManager.jsonPathParsing(jsonResponse)
    img = gmapManager.drawImageWithJsonPath(steps, gongchaLoc)
    img.save('path.png')
    img.show()


    with open("./Agent_Transit_Directions2.json","w") as rltStream :
        json.dump(jsonResponse,rltStream)

 