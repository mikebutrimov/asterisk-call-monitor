__author__ = 'unhack'

import logging
import threading
import websocket
import time
import socket
import ariclient
import mysockets
import channels
import threading
import sched
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory


megastorage = mysockets.getMegaStorage()
channelContainer = channels.getChannelContainer()
client = ariclient.getClient()

class myAriThread(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                print "Ari thread instance was created"
                client.on_channel_event('ChannelStateChange', onChannelStateChanged)
                client.on_channel_event('ChannelDestroyed', onChannelDestroyed)
                client.on_channel_event('ChannelCreated', onChannelStateChanged)
                client.on_channel_event('ChannelVarset', onChannelStateChanged)

        def run(self):
            print "run was executed"
            try:
                print "starting ari thread"
                client.run(apps='channel-dump')
            except:
                print "Ooooooops Asterisk has gone"
                client.close()
                print "Close something"
                print "try to sleep for 10 seconds, than restart"
                time.sleep(10)
                print "Starting something...."
                initApp()
                self.run()



class myWsThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print "WS thread instance was created"
        factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
        factory.protocol = mysockets.AriServerProtocol
        reactor.listenTCP(9000, factory)
    def run(self):
        reactor.run()

def onChannelStateChanged(channel_obj,ev):
    channelContainer.processChannel(channel_obj)
    megastorage.pushData()

def onChannelDestroyed(channel_obj,ev):
    channelContainer.delChannel(channel_obj)
    megastorage.pushData()

def fireUp():
    for i in client.channels.list():
        channelContainer.processChannel(i)
        megastorage.pushData()


def initApp():
    ws = websocket.WebSocket()
    print ("Opening socket")
    ws.connect("ws://server:port/ari/events?api_key=login:password&app=channel-dump",sockopts = socket.SO_KEEPALIVE)
    print ("Sleep for a couple of seconds, because my name is Rajesh Rukozhopalli and i'm not able to check socket state")
    time.sleep(1)

    postRequest=client.applications.subscribe(applicationName=["channel-dump"], eventSource="endpoint:PJSIP")
    print ("If there was no error, then lucky me. If not - shame on me, sorry and goodbye")

def foo():

    initApp()
    fireUp()
    logging.basicConfig()


    ariThread  = myAriThread()
    ariThread.daemon = True
    ariThread.start()

    wsThread = myWsThread()
    wsThread.daemon = True
    wsThread.start()
    
    
    while True:
        
        pass
if __name__ == '__main__':
    foo()
