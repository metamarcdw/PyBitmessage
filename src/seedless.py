#!/usr/bin/env python

from urllib2 import *
from base64 import b64encode, urlsafe_b64decode

knownSeedlessServers = [
    "rx6qfevnrak7fljbotcw2xibpqfzsnwsbf5ouk6f7shwdepmlp5a.b32.i2p",
    "vnmf4apo3mpxitki2nzqjx24cq4ykuiptpdmihgyecomcql5ttaa.b32.i2p",
    "zy37tq6ynucp3ufoyeegswqjaeofmj57cpm5ecd7nbanh2h6f2ja.b32.i2p"]

def pad_b64(b64, size=3):
    mod = len(b64) % size
    if mod != 0:
        eq = "=" * (size - mod)
        b64 += eq
    return b64

def call_seedless(url, cmd, query):
    b64_query = b64encode(query)
    req = Request( url, headers={"X-Seedless": "%s %s" % (cmd, b64_query)} )
    res = urlopen(req, timeout=100)

    list = []
    for b64 in res:
        b64 = pad_b64( b64.strip() )
        list.append( urlsafe_b64decode(b64) )
    return ( res.info().headers, list )

def call_seedless_server(b32, cmd, query):
    proxy = ProxyHandler({'http': 'localhost:4444'})
    opener = build_opener(proxy)
    install_opener(opener)
    
    url = "http://%s/Seedless/seedless" % b32
    return call_seedless(url, cmd, query)

def call_seedless_plugin(cmd, query):
    url = "http://localhost:7657/SeedlessConsole/Service"
    return call_seedless(url, cmd, query)

if __name__ == "__main__":
    default_b32 = knownSeedlessServers[0]
    default_cmd = "locate"
    
    b32 = raw_input("B32: ")
    cmd = raw_input("COMMAND: ")
    query = raw_input("QUERY: ")
    
    if not b32:
        b32 = default_b32
    if not cmd:
        cmd = default_cmd
    
    if b32 == "local":
        result = call_seedless_plugin(cmd, query)
    else:
        result = call_seedless_server(b32, cmd, query)
    print result
