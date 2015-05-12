import threading
import shared
from i2p import socket
from class_sendDataThread import *
from class_receiveDataThread import *
import helper_bootstrap
import errno
import re

# Only one singleListener thread will ever exist. It creates the
# receiveDataThread and sendDataThread for each incoming connection. Note
# that it cannot set the stream number because it is not known yet- the
# other node will have to tell us its stream number in a version message.
# If we don't care about their stream, we will close the connection
# (within the recversion function of the recieveData thread)


class singleListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def setup(self, selfInitiatedConnections):
        self.selfInitiatedConnections = selfInitiatedConnections

    def _createListenSocket(self, session=shared.i2psession):
        sock = socket.socket(session, socket.SOCK_STREAM)
        # This option apparently avoids the TIME_WAIT state so that we can
        # rebind faster
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.bind((HOST, PORT))
        sock.listen(2)
        return sock

    def run(self):
        # If there is a trusted peer then we don't want to accept
        # incoming connections so we'll just abandon the thread
        if shared.trustedPeer:
            return

        while shared.safeConfigGetBoolean('bitmessagesettings', 'dontconnect'):
            time.sleep(1)

        # First try listening on an IPv6 socket. This should also be
        # able to accept connections on IPv4. If that's not available
        # we'll fall back to IPv4-only.
        try:
            sock = self._createListenSocket()
        except socket.Error, e:
            if (isinstance(e.args, tuple) and
                e.args[0] in (errno.EAFNOSUPPORT,
                              errno.EPFNOSUPPORT,
                              errno.ENOPROTOOPT)):
                sock = self._createListenSocket()
            else:
                raise

        with shared.printLock:
            print 'Listening for incoming connections.'
            print 'Listening on:', sock.dest

        while True:
            while len(shared.connectedHostsList) > 220:
                with shared.printLock:
                    print 'We are connected to too many people. Not accepting further incoming connections for ten seconds.'

                time.sleep(10)

            while True:
                socketObject, sockdest = sock.accept()

                # The following code will, unfortunately, block an
                # incoming connection if someone else on the same LAN
                # is already connected because the two computers will
                # share the same external IP. This is here to prevent
                # connection flooding.
                if sockdest in shared.connectedHostsList:
                    socketObject.close()
                    with shared.printLock:
                        print 'We are already connected to', sockdest + '. Ignoring connection.'
                else:
                    break

            someObjectsOfWhichThisRemoteNodeIsAlreadyAware = {} # This is not necessairly a complete list; we clear it from time to time to save memory.
            sendDataThreadQueue = Queue.Queue() # Used to submit information to the send data thread for this connection.
            socketObject.settimeout(120)

            sd = sendDataThread(sendDataThreadQueue)
            sd.setup(
                socketObject, sockdest, -1, someObjectsOfWhichThisRemoteNodeIsAlreadyAware)
            sd.start()

            rd = receiveDataThread()
            rd.daemon = True  # close the main program even if there are threads left
            rd.setup(
                socketObject, sockdest, -1, someObjectsOfWhichThisRemoteNodeIsAlreadyAware, self.selfInitiatedConnections, sendDataThreadQueue)
            rd.start()

            with shared.printLock:
                print self, 'connected to', sockdest, 'during INCOMING request.'

