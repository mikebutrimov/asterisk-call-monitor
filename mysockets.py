__author__ = 'unhack'
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import calls
import json
import devices
import channels
import sys
deviceContainer = devices.getDeviceContainer()
#callContainer = calls.getCallContainer()
channelContainer = channels.getChannelContainer()

with open('ariserver.log', 'w') as logFile:
    logFile.write('________________________________________')


class instanceStorage(object):
    def __init__(self):
        self.storage = []

    def getStorage(self):
        return self.storage

    def putInstance(self,instance):
        self.storage.append(instance)

    def delInstance(self,instance):
        if instance in self.storage:
            self.storage.remove(instance)
            return 1
        return -1

    def getSocketCount(self):
        return len(self.storage)

    
    
    def pushData(self):
        newPayload = deviceContainer.getDevices()
        for i in self.storage:
            result = i.newFilter(newPayload)
            if result != i.getPayload():
                i.sendMessage(json.dumps(result),False)
                i.setPayload(result)
        
            
    def comfortNoise(self):
        for i in self.storage:
            i.sendMessage('[]',False)

class AriServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        megastorage.putInstance(self)
        self.payload = ''
        self.callFilter = None
        print ("New protocol instance was created.\r\nNumber of instances: %s"%megastorage.getSocketCount())

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        megastorage.pushData()

    def onClose(self, wasClean, code, reason):
        if (megastorage.delInstance(self) == 1 ):
            print "Da Instanz was deleted"
        else:
            print "Something fucky"
        print("WebSocket connection closed: {0}".format(reason))
        print("Protocol instance deleted.\r\nNumber of instances: %s"%megastorage.getSocketCount())

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        
        payload = json.loads(payload)
        #parse incoming payload
        print payload
        if payload[0] ==unicode('lesCommand'):
            fromNumber = payload[1]
            toNumber = payload[2]
            channelContainer.redirectCall(fromNumber,1126)    
            
        else:
            self.callFilter = payload
            print "call filter was set\n"
        megastorage.pushData()


    
    def newFilter(self,payload):
        result = {}
        buf = {}
        logs = []
        if self.callFilter is not None:
            for k in self.callFilter:
                k = unicode(k)
                if k in payload:
                    result[k] = payload[k]
        else:
            result = payload
        
        for k,v in result.items():
            buf[k] = [v.getState(),v.getConnected(),v.getDirection(),v.getChanId(),v.getSecChanId()]
        return  buf
        
    
    def setPayload(self,payload):
        self.payload = payload

    def getPayload(self):
        return self.payload

megastorage = instanceStorage()
def getMegaStorage():
    return megastorage
