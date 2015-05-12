from struct import unpack, pack
from addresses import decodeVarint
import time

# We have received a version message
def recversion(data):
    remoteProtocolVersion, = unpack('>L', data[:4])
    print 'remoteProtocolVersion:', remoteProtocolVersion
    if remoteProtocolVersion < 3:
        print 'Closing connection to old protocol version',  remoteProtocolVersion, 'node: ', 'peer'
        return
    timestamp, = unpack('>Q', data[12:20])
    print 'timestamp:', timestamp
    timeOffset = timestamp - int(time.time())
    myExternalDest = data[28:544]
    print 'myExternalDest:', myExternalDest
    
    useragentLength, lengthOfUseragentVarint = decodeVarint(data[1076:1080])
    readPosition = 1076 + lengthOfUseragentVarint
    useragent = data[readPosition:readPosition + useragentLength]
    readPosition += useragentLength
    numberOfStreamsInVersionMessage, lengthOfNumberOfStreamsInVersionMessage = decodeVarint(
        data[readPosition:])
    readPosition += lengthOfNumberOfStreamsInVersionMessage
    streamNumber, lengthOfRemoteStreamNumber = decodeVarint(
        data[readPosition:])
    print 'Remote node useragent:', useragent, '\nstream number:', streamNumber, '\ntime offset:', timeOffset, 'seconds.'
    
    if streamNumber != 1:
        print 'Closed connection to', 'peer', 'because they are interested in stream', streamNumber, '.'
        return
    if data[1068:1076] == 'Z\xef\x86\x05\x1f\x06\xb0\x9e':
        print 'Closing connection to myself: ', 'peer'
        return

packet = "\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00UO\x9f\x05\x00\x00\x00\x00\x00\x00\x00\x01Gl~Nx-u7ItPZM3vCF63xYamL4FYaGWI6HPDGbWzfTFuXhIBMH8W2PrFEny6FPSxNXmDHT8aQvyysuBms9F3xSFhIV5HEQy2evlx~kfLz2RvW91xnvi6YBGpXAOTZEqLD~g20UhnBdASKnN7UkimJ6jjW4rXb180BY-TM1-~mOn4zh4Rz-9zj-VOVw49~lJVKtwfzfZbKGzNOfFR59f82QMIrATS5d1TPN2Jnme~WN8oXnNBsK-gaohJKnJtUCIokhK8FsxGJ2sHHk~kZ9g73Fzpxf1mw6DYBialGkCQy0HqovF6tybudL4KVpbjAcAJdqK~P9C2SMRTaQazZ6mNL4S0UnCSZRZ4PciUF15QqmuwLXNgPRLBgBxXBkOKXvwjs9uUncitiUOkUy4y5DPcl1gmlaKw2K7HkapKujc0xsPCnNCIyVCtLuZjz5k3UN8b7XMufHAEdq-y2CAYXIH8gogrus-bVu7BR0SX2x3H0omA2UKmo-yORzKMSJXVoOQ5rAAAA\x00\x00\x00\x00\x00\x00\x00\x01VXVZRtml-XDgkwFcehckXBQ1qOx8whwjYlPZnKyIp3L5OFhwF6moUjkAoN~4J5TmdBLP5jxoOEwe5pC6TcgkKAvEXLqGvb607LPr9XhhWdgfHFyfcEG1zGhMziisOSHwmnUAjlvd5FT9H7ouv2on5JvLAHRiqe-vO0Ifz~dnkQyhd-IouWArdTlXQqhm7ArMS1-vHQKaslktY9BrFS8ZxKojbAMxcrBrt-9IND1f9-KpRBwtKp0Hup6jzIk3cNGbP4eadZ3F-Zic6oy-ktsH0iz5FBKmpMdc36SQDG8rReMjngKZntl4OhxjAZ7eYLllA6T3X5wdICkoqNJEobByGx9TEYXq6bVlyp7aoxGuB8~piqJWoCqbgfcIDUznP050YoCKp3Uk6u9DmROP4pckzg910FdKSF3TRlebKRRzB7KHWXV~CY3xZEp8CKblBljJEw3FNv0IZ5Guq0tNi9bjs6uXtY1IPviEN9cVfmT3EZ5WK8b~3JdvZrDGKoWAJkRAAAAAZ\xef\x86\x05\x1f\x06\xb0\x9e\x14/PyBitmessage:0.4.4/\x01\x01"
recversion(packet)


