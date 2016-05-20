__author__ = 'unhack'
import ari
def getClient():
    client = ari.connect('server:port', 'login', 'password')
    return client
