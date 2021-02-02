class lonLatParser:
    def jsonPathParsing(self, jsonPath):
        paths = jsonPath["routes"][0]["legs"][0]
        stepList = paths["steps"]

        pointLongsLats = []
        for path in stepList :
            startLoc = path["start_location"]
            endLoc = path["end_location"]
            pointLongsLats.append((startLoc, endLoc))

        return pointLongsLats

    def parseStrFittedIntoQuery(self, paths):
        
        parsedStr = str(paths[0][0]["lat"]) + "," + str(paths[0][0]["lng"])
        print(len(paths))
        for start, end in paths:
            parsedStr += "|" + str(end["lat"]) + "," + str(end["lng"])
        return parsedStr

class encParser:
    def jsonPathParsing(self, jsonPath):
        paths = jsonPath["routes"][0]["overview_polyline"]["points"]
        return paths

    def parseStrFittedIntoQuery(self, paths):
        return "enc%3A" + paths
