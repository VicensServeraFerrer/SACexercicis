from threading import Event, Thread, Timer
from datetime import datetime, timedelta
import time
from nodeServer import NodeServer
from nodeSend import NodeSend
from message import Message
import config
import random
class Node():
    def __init__(self,id):
        Thread.__init__(self)
        self.id = id
        self.port = config.port+id
        self.daemon = True
        self.lamport_ts = 0

        self.server = NodeServer(self)
        self.server.start()

        if id % 2 == 0:
            self.collegues = list(range(0,config.numNodes,2))
        else:
            self.collegues = list(range(1,config.numNodes,2))

        self.client = NodeSend(self)    

    def do_connections(self):
        self.client.build_connection()

    def state(self):
        timer = Timer(1, self.state) #Each 1s the function call itself
        timer.start()
        self.curr_time = datetime.now()
        #wakeup
        self.wakeupcounter += 1
        #TODO shomething
        havetoentercs = random.randint(0, 10)
        if havetoentercs == 0:
            message = Message(msg_type="request",
                            src=self.id,
                            data="Node_%i|counter:%i"%(self.id,self.wakeupcounter))

            print(f'Node{self.id} {message.msg_type} to {message.src}')
            self.client.multicast(message, self.collegues)
        
    def send(self, msg, dest, Multicast=False):
        if not Multicast:
            self.client.send_message(msg, dest)
        else:
            self.client.multicast(msg, self.collegues)

    def run(self):
        print("Run Node%i with the follows %s"%(self.id,self.collegues))
        self.client.start()
        self.wakeupcounter = 0
        self.state()

