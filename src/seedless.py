from urllib2 import *
from base64 import b64encode, urlsafe_b64decode

knownSeedlessServers = [
"4kecr3jdeiuihtuib7dgtsq4sd2jicxyiaclrn26xhvhqw7ocrma.b32.i2p",
"msxukjtkaoscqarobbfijwhxvkzrxddvk2ddx5mdxmu7iytk6c4q.b32.i2p",
"uksrtndz3zedszjofm624zqyuzft3qimdmxs4xlte6547fbk37aa.b32.i2p",
"4vqibd62riv4z2jhs2jq2z6nkwvk5ywog7cf4qcrygij2ulrbqiq.b32.i2p",
"o5hu7phy7udffuhts6w5wn5mw3sepwe3hyvw6kthti33wa2xn5tq.b32.i2p",
"7znvtn7seqgk72kfcmvyqlsdae3uvicffjncqzmqn3jmruusekba.b32.i2p",
"vnmf4apo3mpxitki2nzqjx24cq4ykuiptpdmihgyecomcql5ttaa.b32.i2p",
"wrrwzdgsppwl2g2bdohhajz3dh45ui6u3y7yuop5ivvfzxtwnipa.b32.i2p"]

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
