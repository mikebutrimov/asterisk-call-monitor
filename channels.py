__author__ = 'unhack'
import re
import ariclient
import devices

client = ariclient.getClient()
deviceContainer = devices.getDeviceContainer()

class Channel(object):
    def __init__(self, chan_id, from_number, from_name, connected_number, connected_name, state, body, endpoint):
        self.id = chan_id
        self.fromNumber = from_number
        self.fromName = from_name
        self.connectedNumber = connected_number
        self.connectedName = connected_name
        self.bridgeId = self.getBridgeId()
        self.state = state
        self.body = body
        self.bridgedChannel = None
        self.endpoint = endpoint

    def getBridgeId(self):
        bridges = client.bridges.list()
        if bridges is not None:
            for bridge in bridges:
                if self.id in bridge.json["channels"]:
                    return bridge.id
        else:
            print "crash on l:84 with 0 bridges"
        return None

    def update(self ,chan_id=None, from_number=None, from_name=None, connected_number=None, connected_name=None,
               state=None):
        if chan_id is not None: self.id = chan_id
        if from_number is not None: self.fromNumber = from_number
        if from_name is not None: self.fromName = from_name
        if connected_number is not None: self.connectedNumber = connected_number
        if connected_name is not None: self.connectedName = connected_name
        if state is not None: self.state = state
        self.bridgeId =  self.getBridgeId()

    def getBridge(self):
        return self.bridgeId

    def getChannel(self):
        return [self.id, self.fromNumber, self.fromName, self.connectedNumber, self.connectedName, self.bridgeId,
                self.state]

    def getId(self):
        return self.id

    def getAllFields(self):
        return [self.id, self.fromNumber, self.fromName, self.connectedNumber, self.connectedName, self.bridgeId,
                self.state, self.endpoint]

    def getEndpoint(self):
        return self.endpoint

    def getFromNumber(self):
        return self.fromNumber

    def getState(self):
        return self.state

    def getConnectedNumber(self):
        return self.connectedNumber



class ChannelContainer(object):
    def __init__(self):
        self.container = {}
        #self.bridges = {}

    def parseChannel(self,channel_obj):
        if channel_obj is not None:
            _channelId = channel_obj.json["id"]
            _channelState = channel_obj.json["state"]
            _fromNumber = channel_obj.json["caller"]["number"]
            _fromName = channel_obj.json["caller"]["name"]
            _connectedName = channel_obj.json["connected"]["name"]
            _connectedNumber = channel_obj.json["connected"]["number"]
            _channelBody = channel_obj.json
            ###############
            endps = self.getEndpointByChannelId(_channelId)
            if (endps != []):
                if endps[0]["resource"] is not None:
                    _endpoint = endps[0]["resource"]
            else:
                _endpoint = None
            #################
            channel = Channel(_channelId,_fromNumber,_fromName,_connectedNumber,_connectedName,_channelState,_channelBody,_endpoint)
            return channel
        else:
            print "crash on l:127 zero channel input"
            return None

    def clear(self):
        self.container = {}

    def processChannel(self,channel_obj=None):
        self.clear() 
        for i in client.channels.list():
            self.processChannel2(i)
        self.genDevices()
        #self.processCalls()
        
    
    def processChannel2(self, channel_obj):
        if channel_obj is not None:
            channel = self.parseChannel(channel_obj)
            self.container[channel.getId()] = channel
            #self.getChannels()
        else:
            print "crash on l:145 zero channel to parse"
    
    
    def genDevices(self):
        #clear killed channels
        def parseEndpoint(endpoint):
            if endpoint is not None:
                if "dev" in endpoint:
                    if re.search('[0-9]*',endpoint) is not None:
                        return re.search('[0-9]*',endpoint).group(0)
            return None
        
        active_nums = [channel.fromNumber for channel in self.container.values()]
        active_endpoints = [parseEndpoint(channel.endpoint) for channel in self.container.values()] 
        active_nums.extend(active_endpoints)

        for dev in deviceContainer.getContainer().keys():
            if dev not in active_nums:
                deviceContainer.delDevice(dev)


        for channel in self.container.values():
            direction=None
            
            def parse(fromNumber,endpoint,callState,connectedNumber,direction,channelid,secondchannelid):
                number,state,connected = (None,None,None)
                number = parseEndpoint(endpoint)
                if number is None and fromNumber is not None:
                    number = fromNumber
                
                connected = connectedNumber
                state = callState
                    
                if connected == "":
                    for device in deviceContainer.container.values():
                        if number == device.getConnected():
                            connected = device.getNumber()
                
                if number and state and connected:
                    if number in deviceContainer.container:
                        direction = deviceContainer.container[number].getDirection()
                    buf_device = devices.Device(number,state,connected,direction,channelid,secondchannelid)
                    buf_device.setPrimary(connected)
                    deviceContainer.putDevice(buf_device)
                                        
            
            #determine direction
            if channel.getState() == unicode('Ring'):
                direction = '>'
            elif channel.getState() == unicode('Down'):
                direction = '<'
            elif channel.getState() == unicode('Ringing'):
                direction = '<'
            elif channel.getState() == unicode('Up'):
                direction = '<>'
            else:
                pass

            #find for second channel
            if channel.getConnectedNumber() in deviceContainer.container:
                secondchannelid = deviceContainer.container[channel.getConnectedNumber()].getChanId()
            else:
                secondchannelid = ''
            
            parse(channel.getFromNumber(),channel.getEndpoint(),channel.getState(),channel.getConnectedNumber(),direction,channel.getId(),secondchannelid)
    
    def getChannels(self):
        return self.container

    def delChannel(self,channel_obj):
        self.processChannel()
        
    def getChannelByBridge(self,bridgeId):
        result = []
        for k,v in self.container.items():
            if v.getBridgeId() == bridgeId:
                result.append(v)
        return result

    def getBridgedChannels(self):
        result = []
        bridges = []
        for channel in self.container.values():
            bridges.append(channel.getBridgeId())
        bridges = set(bridges)
        for i in bridges:
            channels = self.getChannelByBridge(i)
            result.append(channels)
        return result

    def processCalls(self):
        bridgedChannels = channelContainer.getBridgedChannels()
        callContainer.clearStorage()
        for i in bridgedChannels:
            self.constructCall(i)

    def getEndpointByChannelId(self,channelId):
        endpoints = client.endpoints.list()
        return [i.json for i in endpoints if channelId in i.json["channel_ids"]]


channelContainer = ChannelContainer()
def getChannelContainer():
    return channelContainer
