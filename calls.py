__author__ = 'unhack'

class Call(object):
    def __init__(self):
        self.endpoint = ''
        self.fromNumber = ''
        self.connectedNumber = ''
        self.state = ''
        self.pairedChannels = ''
        self.fromName = ''
        self.connectedName = ''
        self.secondEndpoint = ''

    def setFields(self, endpoint, fromNumber, connectedNumber, state,fromName,connectedName, secondEndpoint, pairedChannels=None):
        self.endpoint = endpoint
        self.fromNumber = fromNumber
        self.connectedNumber = connectedNumber
        self.state = state
        self.fromName = fromName
        self.connectedName = connectedName
        self.secondEndpoint = secondEndpoint
        if pairedChannels is '':
            self.pairedChannels = ''
        else:
            self.pairedChannels = pairedChannels

    def getFromNumber(self):
        return self.fromNumber

    def getConnectedNumber(self):
        return self.connectedNumber
    
    def getFromName(self):
        return self.fromName

    def getConnectedName(self):
        return self.connectedName

    def getState(self):
        return self.state

    def getPairedChannels(self):
        return self.pairedChannels

    def getEndpoint(self):
        return self.endpoint

    def getSecondEndpoint(self):
        return self.secondEndpoint

    
    def getAllFields(self):
        return [self.endpoint, self.fromNumber, self.fromName, self.connectedName,  self.connectedNumber, self.state, self.secondEndpoint, [i.getAllFields() for i in  self.pairedChannels]]

    def getPairedChannelsIds(self):
        result = []
        for channel in self.pairedChannels:
            result.append(channel.getChannelId())
        return result

    def getCall(self):
        if self.endpoint:
            _endpoint = self.endpoint
        else:
            _endpoint = ""
        _connectedNumber = self.connectedNumber
        _state = self.state
        _fromNumber = self.fromNumber
        _fromName = self.fromName
        _connectedName = self.connectedName
        _secondEndpoint = self.secondEndpoint
        return [_endpoint,_fromNumber,_connectedNumber,_state,_fromName,_connectedName,_secondEndpoint]


class CallContainer(object):
    def __init__(self):
        self.container = {}

    def putCall(self,call):
        fromNumber = call.fromNumber
        connectedNumber = call.connectedNumber
        call_key = (fromNumber,connectedNumber)
        self.container[call_key] = call


    def killDup(self):
        #let's start with outputing some debug to console
        #predicted complexity is O(n). maybe 
        def merge (call1,call2):
            #five fields to rule them all
            cmp = lambda x,y: x if len(x)>len(y) else y
            call1.fromNumber = cmp(call1.fromNumber,call2.connectedNumber)
            call1.connectedNumber = cmp(call1.connectedNumber,call2.fromNumber)
        
        for key,call in self.container.items():
            fromNumber = call.fromNumber
            connectedNumber = call.connectedNumber  
            alt_key = (connectedNumber,fromNumber)
            #spam console if there is a copy
            if alt_key in self.container and key in self.container:
                #existential crysis:
                #not exactly what i've planned, but everything is fine with keys
                #let's go ahead
                merge(self.container[key],self.container[alt_key])
                del self.container[alt_key]
                
        
    def getAllCalls(self):
        return self.container.values()

    def delCallByChannelId(self,channelId):
        for key,call in self.container.items():
            if channelId in call.getPairedChannelsIds():
                self.container.pop(key)

    def clearStorage(self):
        self.container = {}

    def outputCalls(self):
        result = []
        for call in self.container.values():
            result.append(call.getCall())
        return result

callContainer = CallContainer()
def getCallContainer():
    return callContainer
