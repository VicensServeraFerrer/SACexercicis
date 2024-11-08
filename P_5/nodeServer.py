import select
from threading import Thread
import utils
from message import Message
import json
import time

class NodeServer(Thread):
    def __init__(self, node):
        Thread.__init__(self)
        self.node = node
        self.granted = None
        self.requests = []
        self.failed = None
        self.yieldes = None
        self.grants = []

    def run(self):
        self.update()

    def update(self):
        self.connection_list = []
        self.server_socket = utils.create_server_socket(self.node.port)
        self.connection_list.append(self.server_socket)

        while self.node.daemon:
            (read_sockets, write_sockets, error_sockets) = select.select(
                self.connection_list, [], [], 5)
            if not (read_sockets or write_sockets or error_sockets):
                print('NS%i - Timed out'%self.node.id) #force to assert the while condition 
            else:
                for read_socket in read_sockets:
                    if read_socket == self.server_socket:
                        (conn, addr) = read_socket.accept()
                        self.connection_list.append(conn)
                    else:
                        try:
                            msg_stream = read_socket.recvfrom(4096)
                            for msg in msg_stream:
                                try:
                                    ms = json.loads(str(msg,"utf-8"))
                                    self.process_message(ms)
                                except:
                                    None
                        except:
                            read_socket.close()
                            self.connection_list.remove(read_socket)
                            continue
        
        self.server_socket.close()

    def process_message(self, msg):
        # Do shomething
        if msg['msg_type']=="request":
            print(f'Node {self.node.id} revieved {msg}')
            if not self.granted:
                id_requesting = msg['data'].split('|')[0].split('_')[1]
                ts = msg['data'].split('|')[1].split(':')[1]

                message = Message(msg_type="grant",
                            src=self.node.id,
                            data="Node_%i"%(self.node.id))
                
                print(f'Node{self.node.id} {message.msg_type} to {id_requesting}')
                self.node.send(message, id_requesting, False)
                self.granted = {"id": id_requesting, "ts": ts}
            else:
                id_requesting = msg['data'].split('|')[0].split('_')[1]
                ts = msg['data'].split('|')[1].split(':')[1]
                if ts > self.granted["ts"]:
                    message = Message(msg_type="failed",
                            src=self.node.id,
                            data="Node_%i"%(self.node.id))  
                    
                    print(f'Node{self.node.id} {message.msg_type} to {message.src}')
                    self.node.send(message, id_requesting, False)
                    self.requests.append({"id": id_requesting})
                else:
                    message = Message(msg_type="inquire",
                            src=self.node.id,
                            data="Node_%i"%(self.node.id))  
                    
                    self.node.client.send_message(message, self.granted["id"])        
        if msg['msg_type']=="inquire":
            id_reciving = msg['data'].split('_')[1]
            if self.failed or (self.yieldes and self.yieldes["dst"]!=id_reciving):
                message = Message(msg_type="yield",
                            src=self.node.id,
                            data="Node_%i"%(self.node.id))  
                    
            print(f'Node{self.node.id} {message.msg_type} to {message.src}')
            self.node.send(message, id_reciving, False)
        if msg['msg_type']=="yield":
            id_reciving = msg['data'].split('_')[1]

            message = Message(msg_type="grant",
                            src=self.node.id,
                            data="Node_%i"%(self.node.id)) 
            print(f'Node{self.node.id} {message.msg_type} to {message.src}')
            self.node.send(message, self.requests[0]["id"])
            self.requests[0] = {"id": self.granted["id"]}
            self.requests.append({"id":id_reciving})
        if msg['msg_type']=="release":
            id_reciving = msg['data'].split('_')[1]
            self.requests.remove({"id": id_reciving})

            if self.requests != []:
                message = Message(msg_type="grant",
                                src=self.node.id,
                                data="Node_%i"%(self.node.id))  
                print(f'Node{self.node.id} {message.msg_type} to {message.src}')
                self.node.send(message, self.requests[0]["id"], False)
        if msg['msg_type']=="grant":
            id_recived = msg['data'].split('_')[1]
            if int(id_recived) not in self.grants:
                self.grants.append(int(id_recived))
            
            if sorted(self.grants)==sorted(self.node.collegues):
                print(f'Node{self.node.id} in CS')
                time.sleep(5)
                print(f'Node{self.node.id} out of CS')
                
                message = Message(msg_type="release",
                                src=self.node.id,
                                data="Node_%i"%(self.node.id))  
                print(f'Node{self.node.id} {message.msg_type} to {message.src}')
                self.failed = False
                self.node.send(message, self.node.collegues, False)
        if msg['msg_type']=="failed":
            self.failed = True




        


 