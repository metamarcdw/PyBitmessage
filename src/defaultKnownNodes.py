import pickle
from i2p import socket
from struct import *
import time
import random
import sys
from time import strftime, localtime
import shared

def getBootstrapListFromEepsite():
    try:
        dest = shared.config.get('bitmessagesettings', 'bootstrapeepsite')
    except:
        return []
    
    if not dest or dest == '':
        return []

    while True:
        print 'Getting some defaultKnownNodes from eepsite', dest    
        try:
            S = socket.socket('', socket.SOCK_STREAM)  
            S.connect(dest)
            S.send('GET /bootstrap.json HTTP/1.0\r\n\r\n')          # Send request
            break
        except socket.NetworkError as ne:
            print "I2P Network Error:", ne
            continue
        
    f = S.makefile()                          # File object
    
    while True:                               # Read header
        line = f.readline().strip()           # Read a line
        if line == '': break                  # Content begins
    
    str = f.read()                            # Read file object
    f.close()                                 # Close file, connection
    S.close()

    import json
    return json.loads(str)                    # Load list from JSON and return

def createDefaultKnownNodes(appdata):
    ############## Stream 1 ################
    stream1 = {}
    #stream1[shared.Peer('VXVZRtml-XDgkwFcehckXBQ1qOx8whwjYlPZnKyIp3L5OFhwF6moUjkAoN~4J5TmdBLP5jxoOEwe5pC6TcgkKAvEXLqGvb607LPr9XhhWdgfHFyfcEG1zGhMziisOSHwmnUAjlvd5FT9H7ouv2on5JvLAHRiqe-vO0Ifz~dnkQyhd-IouWArdTlXQqhm7ArMS1-vHQKaslktY9BrFS8ZxKojbAMxcrBrt-9IND1f9-KpRBwtKp0Hup6jzIk3cNGbP4eadZ3F-Zic6oy-ktsH0iz5FBKmpMdc36SQDG8rReMjngKZntl4OhxjAZ7eYLllA6T3X5wdICkoqNJEobByGx9TEYXq6bVlyp7aoxGuB8~piqJWoCqbgfcIDUznP050YoCKp3Uk6u9DmROP4pckzg910FdKSF3TRlebKRRzB7KHWXV~CY3xZEp8CKblBljJEw3FNv0IZ5Guq0tNi9bjs6uXtY1IPviEN9cVfmT3EZ5WK8b~3JdvZrDGKoWAJkRAAAAA')] = int(time.time())
    
    eepsite_list = getBootstrapListFromEepsite()
    for dest in eepsite_list:
        stream1[shared.Peer( str(dest) )] = int(time.time())
        
    ############# Stream 2 #################
    stream2 = {}
    # None yet

    ############# Stream 3 #################
    stream3 = {}
    # None yet

    allKnownNodes = {}
    allKnownNodes[1] = stream1
    allKnownNodes[2] = stream2
    allKnownNodes[3] = stream3

    #print stream1
    #print allKnownNodes

    with open(appdata + 'knownnodes.dat', 'wb') as output:
        # Pickle dictionary using protocol 0.
        pickle.dump(allKnownNodes, output)

    return allKnownNodes

def readDefaultKnownNodes(appdata):
    pickleFile = open(appdata + 'knownnodes.dat', 'rb')
    knownNodes = pickle.load(pickleFile)
    pickleFile.close()
    for stream, storedValue in knownNodes.items():
        for dest,value in storedValue.items():
            # New knownNodes format.
            storedtime = value
            print dest, '\t', unicode(strftime('%a, %d %b %Y  %I:%M %p',localtime(storedtime)),'utf-8')

if __name__ == "__main__":

    APPNAME = "config/PyBitmessage"
    from os import path, environ
    if sys.platform == 'darwin':
        from AppKit import NSSearchPathForDirectoriesInDomains  # @UnresolvedImport
        # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
        # NSApplicationSupportDirectory = 14
        # NSUserDomainMask = 1
        # True for expanding the tilde into a fully qualified path
        appdata = path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], APPNAME) + '/'
    elif 'win' in sys.platform:
        appdata = path.join(environ['APPDATA'], APPNAME) + '\\'
    else:
        appdata = path.expanduser(path.join("~", "." + APPNAME + "/"))


    print 'New list of all known nodes:', createDefaultKnownNodes(appdata)
    readDefaultKnownNodes(appdata)


