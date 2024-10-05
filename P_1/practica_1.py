
import socketserver
import threading
import random 
import time
import socket

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
        self.request.setblocking(False)

    def process_commands(self):
        while True:
            if self.mark == '1':
                self.game.askHelp()
            else:
                if not self.game.havetobeawake(self):
                    self.send("I go to sleep")
                    time.sleep(random.randint(1, 3))
                else:
                    if self.game.helpAsked:
                        self.game.help(self)

class Game():
    next_game = None
    game_selection_lock = threading.Lock()
    players = []
    current_master = None
    helpAsked = False
    timeout = 10000000

    def __init__(self):
        self.current_player = None
        self.lock = threading.Lock()

    def havetobeawake(self, player):
        if player.timeWakenUp > 0:
            player.timeWakenUp -= 1
            return True
        else:
            player.timeWakenUp = 2000000
            return False

    def askHelp(self):
        if self.helpAsked:
            self.timeout -= 1
            if self.timeout <= 0:
                self.timeout = 10000000
                self.helpAsked = False
                self.current_master.numberHelps = 0
                for player in self.players:
                    player.isupported = False
        else:
            self.current_master.send("help")
            self.helpAsked = True

    def help(self, player):
        if not player.isupported:
            if self.haveToSupport():
                player.send("support")
                self.current_master.numberHelps += 1
            player.isupported = True
            self.current_master.send(self.current_master.numberHelps)
        if self.current_master.numberHelps >=2:
            self.helpAsked = False
            self.timeout = 10000000
            self.rechoose()

    def haveToSupport(self):
        if random.randint(1, 10) <= 3:
            return True
        return False

    def rechoose(self):
        for player in self.players:
            player.mark = '0'
            player.timeout = 10000000
            player.numberHelps = 0
            player.isupported = False
            player.timeWakenUp = 2000000
        rand = random.randint(0, len(self.players)-1)
        self.players[rand].mark = '1'
        self.current_master = self.players[rand]    

    @classmethod
    def join(cls, player):
        with cls.game_selection_lock:
            if cls.next_game is None:
                cls.next_game = Game()
                player.game = cls.next_game
                player.mark = '1'
                player.numberHelps = 0
                player.timeWakenUp = 2000000
                player.isupported = False
                cls.current_master = player
            else:
                player.mark = '0'
                player.game = cls.next_game
                player.numberHelps = 0
                player.timeWakenUp = 2000000
                player.isupported = False
            cls.players.append(player)

server = ThreadedTCPServer(('', 9999), PlayerHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()







