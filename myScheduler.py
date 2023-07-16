import os
from ScheduleItem import ScheduleItem
import datetime

class myScheduler:
    def __init__(self, savePath):
        self.items = []
        self.path = savePath
    
    def addScheduleItem(self, item):
        item.addId(len(self.items))
        self.items.append(item)
        self.saveSchedule()
    
    def saveSchedule(self):
        for item in self.items:
            fileName = os.path.join(self.path, "ScheduleItem" + str(item.id) +".txt")
            f = open(fileName, "w")
            f.write(str(item.channel)+"\n")
            f.write(str(item.message)+"\n")
            f.write(str(item.time)+"\n")
            f.write(str(item.delay)+"\n")
            f.write(str(item.id))
            f.close()

    def loadSchedule(self):
        loadeditems = []
        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)):
                f = open(os.path.join(self.path, file), "r")
                chan = int(f.readline())
                mes = f.readline()[:-1]
                time = datetime.datetime.strptime((str(f.readline())[:-1]), '%Y-%m-%d %H:%M:%S')
                delay = int(f.readline())
                id = int(f.readline())
                f.close()
                schedItem = ScheduleItem(chan, mes, time, delay)
                schedItem.addId(id)
                loadeditems.append(schedItem)
        self.items = loadeditems
    
    def removeItem(self, id):
        deleted = False
        modifiedList = []
        for item in self.items:
            if int(item.id) != int(id):
                modifiedList.append(item)
            if int(item.id) == int(id):
                deleted = True
        self.items = modifiedList
        self.updateIds()
        return deleted

    def updateIds(self):
        for idx, item in enumerate(self.items):
            if idx != item.id:
                item.id = idx
        self.cleanUpSaves()
        self.saveSchedule()

    def cleanUpSaves(self):
        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)):
                os.remove(os.path.join(self.path, file))