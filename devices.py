import copy
import log

class Device(object):
    def __init__(self,number,state,connected,direction,channelid,secondchannelid):
        self.deviceId = id(self)
        self.number = number
        self.state = state
        self.connected = connected
        self.channelid = channelid
        self.secondchannelid = secondchannelid
        if direction is not None:
            self.direction = direction
        else:
            self.direction = ""
        self.primaryIsSet = False
        self.primary = ''
    
    def setNumber(self,number):
        self.number = number
    
    def setState(self,state):
        self.state = state
    
    def setConnected(self,connected):
        self.setConnected = connected

    def setPrimary(self,primary):
        if not self.primaryIsSet:
            self.primary = primary
            self.primaryIsSet = True
    
    def getId(self):
        return self.deviceId
    
    def getNumber(self):
        return self.number

    def getState(self):
        return self.state
    
    def getConnected(self):
        return self.connected

    def setDirection(self,direction):
        self.direction = direction
    
    def getDirection(self):
        return self.direction

    def getChanId(self):
        return self.channelid

    def getSecChanId(self):
        return self.secondchannelid
    
    def getPrimary(self):
        return self.primary

class DeviceContainer(object):
    def __init__(self):
        self.container = {}
 
    
    def putDevice(self,device):
        if device.getNumber() in self.container:
            device.primary = self.container[device.getNumber()].primary
        self.container[device.getNumber()] = device

    
    def delDevice(self,key):
        logrecord = (key,self.container[key].getDirection(),
                     self.container[key].getPrimary(),
                     self.container[key].getConnected())
        log.putRecord(logrecord)
        self.container.pop(key) 
     
    def getDevice(self,number):
        return self.container[number]

    def getDevices(self):
        buf =  copy.copy(self.container)
        return buf
    
    def getContainer(self):
        return self.container

    def clearDevices(self):
        self.container = {}



deviceContainer = DeviceContainer()
def getDeviceContainer():
    return deviceContainer
    
            
