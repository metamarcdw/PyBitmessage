#!/usr/bin/env python

import seedless
from random import choice
from urllib2 import HTTPError
from socket import timeout

def result_to_list(result, index):
    list = []
    for entry in result[1]:
        item = entry.split(" ")[index]
        list.append(item)
    return list

service = ""

def scrapePeers(dest):
    # LOCATE
    tryPlugin = True
    while True:     # Try plugin first, then keep trying random servers
        cmd = "locate"
        query = "seedless %s" % service
        try:
            if tryPlugin:
                tryPlugin = False
                res = seedless.call_seedless_plugin(cmd, query)
            else:
                randomServer = choice(seedless.knownSeedlessServers)
                res = seedless.call_seedless_server(randomServer, cmd, query)
        except ( HTTPError, timeout ) as e:
            if e.code != 404:
                print "Seedless:locate", e
            continue
            
        currentServerList = result_to_list(res, 0)
        if len(currentServerList) > 0:
            print "servers: ", len(currentServerList)
            break
            
    maxServers = len(currentServerList)
    if maxServers > 3:
        maxServers = 3
    elif maxServers <= 0:
        raise Exception("No %s compatible seedless servers were found." % service)
    
    # ANNOUNCE
    for server in currentServerList:
        while True:
            try:
                ann_res = seedless.call_seedless_server( \
                        server, "announce", "%s %s" % (service, dest) )
            except ( HTTPError, timeout ) as e:
                print "Seedless:announce", e
                continue
            if ann_res:
                break
    
    # SCRAPE
    peerDestinations = set()
    serversScraped = 0
    while True:
        currentServer = choice(currentServerList)
        try:
            res = seedless.call_seedless_server( \
                        currentServer, "locate", "%s  " % service)
        except ( HTTPError, timeout ) as e:
            print "Seedless:scrape", e
            continue
        
        peers = result_to_list(res, 2)
        if len(peers) > 0:
            currentServerList.remove(currentServer)
            peerDestinations.update(peers)
            serversScraped += 1
        
        if serversScraped >= maxServers:
            break
        
    return list( peerDestinations )

if __name__ == "__main__":
    service = "pybitmsg-i2p"
    mydest = "fmzq6Y8MLj2IPwmym2d1xuM5oSRT2-Db0Zv4yAPS3deGZNDPTZu4ZguWXQrqcZ6~lptHql4~h4y6ttjzg3NA2cGF44x5JvGTkOwmcopLLx5WsD-LzXwDqU1ncO6K7nmRQovgwZCWgqOrjs9TugN9ci3c2QzUIqN4TgUVMMJHm4yMScAsR4tFBlJpSXe9RnWyXskgf3IvcDWNmCuiNryXNMlb~hyy1lnC29rNIgjYh1nHL9RQ0RUyPuUiyid~GkBCNeSfwzCYi5W8pMErEYmKSwLBcR1MSaRcXD~Tkr3K4KNSPQNCxaCnsuOZoDVMw64NECqAkVVHMnZKU1R0exHiDEds4gJelP-5qSdlYXR6azVde4rrC559Mh9XM1Dlw6kAS1Gv3B7ZyGt6HPhn2uN8rwLvpk60N03J0vi8oubBqkmAhHI2w~FL4apkORdjquz~m~r5bW3CPxH7P1LadnrsNE-m5gO6Sts~9UwVRG-Wmz-L2Za~cDXTP~HXG61IE9IKAAAA"
    print scrapePeers(mydest)

