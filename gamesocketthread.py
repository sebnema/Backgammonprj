import threading
import hashlib
import socket
import time
import re
import commands as Commands
import user

import sys

class GameSocketThread(threading.Thread):
    lastsentservercomand = ""

    def __init__(self, channel, details, manager):
        self.channel = channel
        self.details = details
        self.manager = manager
        threading.Thread.__init__ ( self )

    def run ( self ):
        print ("BG> Received connection ", self.details [ 0 ])
        #self.handshake(self.channel)
        while True:
            try:
                self.interact(self.channel)
            except Exception, err:
                sys.stderr.write('ERROR: %s\n' % str(err))
              #  self.channel.close()
               # break

    def send_data(self, client, str):
        try:
            return client.send(str)
        except IOError as e:
            #if e.errno == 32:
                #user = self.manager.findUserBySocket(client)
            print ("BG> pipe error")

    def recv_data(self, client, count):
        data = client.recv(count)
        return data

    def interact(self, client):
        #this_user = self.manager.findUserBySocket(client)
        data = self.recv_data(client, 2048)
        print "Got data: ", data
        response, users= Commands.processcommand(client, self.manager, data) #this_user.socket
        self.lastsentservercomand = response.split("||")[0]
        #if (len(users)>0):
        #    for u in users:
        #        if isinstance(u,user.User):
        #            self.send_data(u.socket, response)
        #else:
        #    self.send_data(client, response)
        self.send_data(client, response)












