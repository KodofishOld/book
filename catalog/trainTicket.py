import numpy as np
inf = np.inf

class Route:
    seatNum = 0
    stationInfo = {}
    def __init__(self,stationList = ["1","2","3","4","5","6","7","8","9","10"]
                 ,seatNum = 5):
        self.seatNum = seatNum
        seatMap = []
        for x in range (seatNum):
            seatMap.append(1)
        for x in stationList:
            self.stationInfo.update({x:[list(seatMap),0]})

    def requestTicket(self,stationN):
        isAvailable = True
        isRemainSeat = True
        seatMap, totalPerson = self.stationInfo.get(stationN)
        if(totalPerson > 3*self.seatNum):
            isAvailable = False
        if(totalPerson >= self.seatNum):
            isRemainSeat = False

        return seatMap,isAvailable,isRemainSeat

    def getTicket(self,stationN,seatN):
        seatMap, totalPerson = self.stationInfo.get(stationN)
        if(seatN != -1):
            seatMap[seatN] = 0
        self.stationInfo.update({stationN:[seatMap,totalPerson+1]})

class Railway:
    route = {}
    graphDict = {}
    routeDict = {}
    stationDict = {}
    def __init__(self,routeDict = {'峽谷線':['底層','毒沼','主城','破戒僧','菜'],
                                   '一心線':['天守閣','待命室','主城','正門','古廟']}):
        self.routeDict = routeDict
        print(routeDict)
        
        for routeName in routeDict.keys():
            stationList = routeDict.get(routeName)
            self.route.update({routeName:Route(stationList)})

            for i in stationList:
                stationBelongs = self.stationDict.get(i)
                if(stationBelongs == None):
                    self.stationDict.update({i:[routeName]})
                else:
                    stationBelongs.append(routeName)
                    self.stationDict.update({i:stationBelongs})

            for i in range(0,len(stationList)-1):
                self.graphDict.setdefault(stationList[i],{}).update({stationList[i+1]:1})
                print(self.graphDict)
            for i in range(len(stationList)-1,0,-1):
                self.graphDict.setdefault(stationList[i],{}).update({stationList[i-1]:1})
            print(self.graphDict)
            print(self.stationDict)
    def booking(self,sN,dN):
        optMessage = ""
        try:
            bookRoute = self.getBookRoute(sN,dN)
            optMessage = optMessage + "乘坐" + bookRoute[0][0]
            isNotFirstLine = False
            for routeTable in bookRoute:
                if(isNotFirstLine):
                    print("換乘" + routeTable[0])
                    optMessage = optMessage + "\r\n" + "換乘" + routeTable[0]
                isNotFirstLine = True

                obj,bookTable = self.getBookTicket(routeTable)
                
                for station,seatNum in bookTable:
                    obj.getTicket(station,seatNum)
                    print(' ',station,seatNum)
                    optMessage = optMessage + " " + station +"站"
                    if(seatNum == -1):
                        optMessage = optMessage + " 無座"
                    else:
                        optMessage = optMessage + ' ' + str(seatNum) + '號座'
                optMessage = optMessage + '\n'
            print('optMessage',optMessage)
            return optMessage

            print("訂票成功")
        except Exception as e:
            
            print("抱歉 票已售完")
            #print(e)
            #return "抱歉 票已售完"

    def getBookTicket(self,routeTable):
        #routeTable = ['Line 1','A','B','C','F']
        print('routeTable',routeTable)
        lineName = routeTable[0]
        trueTable = []
        bookTable = []
        noSeatIndex = []
        requestTrueTable = []
        obj = self.route.get(lineName)
        for i in range(1,len(routeTable)-1):
            requestTrueTable.append(1)
            trueMap,isAvailable,isRemainSeat = obj.requestTicket(routeTable[i])
            if(not isAvailable):
                print("No ticket available")
                raise Exception("No ticket available")
                break
            if(not isRemainSeat):
                noSeatIndex.append(i)
            trueTable.append(trueMap)
        print('noSeatIndex',noSeatIndex)
        print('requestTrueTable',requestTrueTable)
        for i in noSeatIndex:
            print('i',i)
            requestTrueTable[i-1] = 0
        print('requestTrueTable',requestTrueTable)
        begin = True
        startIndex = None
        endIndex = None
        for i in range(0,len(requestTrueTable)):
            print("i,requestTrueTable[i],startIndex,endIndex",i,requestTrueTable[i],startIndex,endIndex)
            if(begin):
                if(requestTrueTable[i] == 1):
                    startIndex = i
                    endIndex = i
                    begin = False
            elif(requestTrueTable[i] == 1):
                endIndex = i
            if( (requestTrueTable[i] == 0 or i == len(requestTrueTable) - 1)
                                 and startIndex != None):
                print("trueTable_2",trueTable)
                print('startIndex endIndex',startIndex,endIndex)
                requestTicketRoute = self.calcLongest(trueTable,outputTable=[],
                                                                   beginIndex = startIndex,
                                                                   endIndex = endIndex)
                print('requestTicketRoute',requestTicketRoute)
                for seatKey,beginStation,endStation in requestTicketRoute:
                    for j in range(beginStation,endStation + 1):
                        bookTable.append([routeTable[j+1],seatKey])
                begin = True
                startIndex = None
                endIndex = None
            if(requestTrueTable[i] == 0 ):
                bookTable.append([routeTable[i+1],-1])

        print('bookTable',bookTable)
        return obj,bookTable

    def getBookRoute(self,sN,dN):
        trace = [sN]
        gottenRoute = self.dijkstra(sN,dN)
        lineTable = list(self.routeDict.keys())
        trueTable = []
        tmpTable = []
        #init trueTable
        for i in range (len(self.routeDict.keys()) ):
            tmpTable.append(0)
        for i in range (len(gottenRoute)):
            trueTable.append(list(tmpTable))
        #setValuesInTrueTable
        for stationIndex in range(len(gottenRoute)):
            for stationLine in self.stationDict.get(gottenRoute[stationIndex]):
                for lineIndex in range(len(lineTable)):
                    if(lineTable[lineIndex] == stationLine):
                        trueTable[stationIndex][lineIndex] = 1
        #end setTrueTable
        print("trueTable",trueTable)
        routeTable = self.calcLongest(trueTable,outputTable = [])
        print('routeTable',routeTable)
        bookRoute = []
        for key,beginIndex,endIndex in routeTable:
            route = [lineTable[key]]
            for i in range(beginIndex,endIndex+1):
                route.append(gottenRoute[i])
            bookRoute.append(route)
        print('bookRoute',bookRoute)
        return bookRoute
        
    def calcLongest(self,trueTable,outputTable = [],beginIndex = 0,endIndex = -1):
        # 0 = True,1 = False
        #trueTable = [[1,0],[1,1],[1,1],[0,1]] [[True,False], ...]
        #outputTable = [[0,0,2],[1,2,3]] [[indexOfKey,beginIndex,endIndex], ...]
        if(endIndex == -1):
            endIndex = len(trueTable) - 1
        firstPos = trueTable[beginIndex] #[1,0]..
        maxDeep = 0
        maxKey = None
        for i in range(0,len(firstPos)):
            if(trueTable[beginIndex][i] != 0):
                preDeep = 0
                for j in range(beginIndex,len(trueTable)):
                    if(trueTable[j][i] == 1):
                        preDeep = preDeep + 1
                    else:
                        break
                if(preDeep > maxDeep):
                    maxDeep = preDeep
                    maxKey = i
        nextIndex = beginIndex + maxDeep - 1
        print('[maxKey,beginIndex,nextIndex]',[maxKey,beginIndex,nextIndex])
        outputTable.append([maxKey,beginIndex,nextIndex])
        print('maxKey',maxKey)
        if(beginIndex + maxDeep - 1 < endIndex):
            self.calcLongest(trueTable,outputTable,nextIndex,endIndex)
        else:
            print('outputTable',outputTable)
            return outputTable
        return outputTable


    def getMinNode(self,costTable,foundTable):
        minNode = None
        minCost = inf
        for i in costTable:
            if not foundTable.get(i):
                if (costTable.get(i) < minCost):
                    minCost = costTable.get(i)
                    minNode = i
        return minNode

    def dijkstra(self,sN,dN):
        graphDict = self.graphDict
        nodeNum = len(graphDict)
        foundTable = {}
        costTable = {}
        routeTable = {}
        #init
        for i in graphDict.keys():
            costTable.update({i:inf})
            foundTable.update({i:False})
            routeTable.update({i:sN})
        foundTable.update({sN:True})
        
        for i in graphDict.get(sN):
            costTable.update({i:graphDict.get(sN).get(i)})
        #end init
        for _ in range (nodeNum):
            minCostNode = self.getMinNode(costTable,foundTable)
        
            foundTable.update({minCostNode:True})
            for i in costTable.keys():
                try:
                    newCost = costTable.get(minCostNode)+graphDict.get(minCostNode).get(i)
                except TypeError:
                    newCost = inf#costTable.get(minCostNode)
                except AttributeError:
                    newCost = inf
                if(costTable.get(i) > newCost):
                    costTable.update({i:newCost})
                    routeTable.update({i:minCostNode})
        routeRecord = [dN]
        minRoute = dN
        pN = dN
        while (routeTable.get(pN) != sN):
            pN = str(routeTable.get(pN))
            minRoute = pN + '->' + minRoute
            routeRecord.append(pN)
        minRoute = sN + '->' + minRoute
        routeRecord.append(sN)
        routeRecord.reverse()
        print(minRoute)
        print(routeRecord)
        return routeRecord

def inputByWebInit():
    a = Railway(routeDict = {'峽谷線':['底層','毒沼','主城','破戒僧','菜'],
                            '一心線':['天守閣','待命室','主城','正門','古廟']})
    return a

def inputByWeb(a, sN, dN):
    infoFromBooking = a.booking(sN,dN)
    return infoFromBooking

if __name__ == '__main__':
    a = Railway()
    for i in range(10):
        a.booking('A','H')
    for i in range(10):
        a.booking('A','J')
'''
    rail = Ticket()
    rail.getTicket(1,10)
    rail.getTicket(1,10)
    rail.getTicket(2,8)
    rail.getTicket(3,5)
    rail.getTicket(4,10)
    rail.getTicket(5,6)
    rail.getTicket(5,7)
    rail.getTicket(4,5)
    rail.getTicket(1,4)
'''
        