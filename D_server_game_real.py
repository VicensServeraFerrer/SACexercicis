
import socketserver
import threading
import random 

# The server based on threads for each connection
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # DOC: ThreadingMixIn define un atributo daemon_threads, que indica si el servidor debe esperar o no la terminación del hilo

    daemon_threads = True
    allow_reuse_address = True

# Session of the game
class PlayerHandler(socketserver.StreamRequestHandler):
    def handle(self): # A new message come
        self.opponent = None
        print("Connected: %s on %s"%(self.client_address,threading.currentThread().getName()))
        try:
            self.initialize()
            self.process_commands()
        except Exception as e:
            print(e)
        finally:
            try:
                self.opponent.send('OTHER_PLAYER_LEFT')
            except:
                # Hack for when the game ends, not happy about this
                pass
        print("Closed: client %s on %s"%(self.client_address,threading.currentThread().getName()))

    def send(self, message):
        self.wfile.write(("%s\n"%message).encode('utf-8'))

    def initialize(self):
        Game.join(self)
        self.send('WELCOME ' + self.mark)
        if self.mark == '1':
            self.game.current_player = self
            self.send('MESSAGE Waiting for opponent to connect')
        else:
            self.opponent = self.game.current_player
            self.opponent.opponent = self
            self.opponent.send('MESSAGE Your move')

    def process_commands(self):
        while True:
            command = self.rfile.readline()
            print(command)
            if not command:
                break
            command = command.decode('utf-8')
            if command.startswith('QUIT'):
                return
            self.process_move_command(command)

    def process_move_command(self, command):
        try:
            value = int(command)
            res = self.game.choice(value, self)
            if res == "WIN":
                self.send('Your win!')
                self.opponent.send('DEFEAT')

            else:
                self.send('No. It is %s'%res)
                self.opponent.send("your turn:")

                      
        except Exception as e:
            self.send('MESSAGE ' + str(e))

class Game():
    size = 10
    next_game = None
    game_selection_lock = threading.Lock()

    def __init__(self):
        self.thevalue = random.randint(0,self.size)
        print("the value is: %i"%self.thevalue)
        self.current_player = None
        self.lock = threading.Lock()

    
    def choice(self, value, player):
        with self.lock:
            if player != self.current_player:
                raise ValueError('Not your turn')
            elif player.opponent is None:
                raise ValueError('You don’t have an opponent yet')

            if self.thevalue == value:
                return "WIN"
            elif self.thevalue > value:
                self.current_player = self.current_player.opponent
                return ">"
            else:
                self.current_player = self.current_player.opponent
                return "<"
            

    @classmethod
    def join(cls, player):
        with cls.game_selection_lock:
            if cls.next_game is None:
                cls.next_game = Game()
                player.game = cls.next_game
                player.mark = '1'
            else:
                player.mark = '2'
                player.game = cls.next_game
                cls.next_game = None

server = ThreadedTCPServer(('', 9999), PlayerHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()