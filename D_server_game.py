
import socketserver
import threading
import random 
import time

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

    def process_commands(self):
        while True:
            command = self.rfile.readline()
            print(command)
            if not command:
                break
            command = command.decode('utf-8')
            if command.startswith('QUIT'):
                return
            if self.mark != '1':
                time.sleep(random.randint(100, 500))
            else:
                if self.timeout <= 0:
                    self.send('help')
                    self.timeout = 1000
            self.process_move_command(command)

    def process_move_command(self, command):
        try:
            if self.mark != '1':
                if command.startswith('help'):
                    if random.randint(1, 10) <= 3:
                        self.send("support")
            else:
                if command.startswith('support'):
                    self.beenHelped += 1
                    if self.beenHelped >= 2:
                        self.beenHelped = 0
                        self.send('Thanks for helping')
                        self.game.rechoose()

                      
        except Exception as e:
            self.send('MESSAGE ' + str(e))

class Game():
    size = 10
    next_game = None
    game_selection_lock = threading.Lock()
    players = []

    def __init__(self):
        self.thevalue = random.randint(0,self.size)
        print("the value is: %i"%self.thevalue)
        self.current_player = None
        self.lock = threading.Lock()

    
    def rechoose(self):
        for player in self.players:
            player.mark = '0'
        rand = random.randint(0, len(self.players))
        self.players[rand].mark = '1'
        self.players[rand].timeout = 1000
        self.players[rand].beenHeped = 0

    def choice(self, value, player):
        with self.lock:
            if player.master == ture:
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
                player.beenHelped = 0
                player.timeout = 1000
            else:
                player.mark = '0'
                player.game = cls.next_game
            cls.players.append(player)

server = ThreadedTCPServer(('', 9999), PlayerHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()





# IDEAS A DESARROLLAR
#
# Lista de usuarios que se han conectado
# Al primero se le asigna el master
# Hasta que el master no ha sido ayudado no se cambia la jerarquia
# Conexión udp
# Slave: sleep(random), leer ayuda (si existe => ayudar( si o no ? = random 30% accuracy), caso contrario se vuelve a dormir)
# Master: help (mirar como hacer exporation time), esperar si le responden 2 (en caso de si => reorganizar jerarquia, en caso contrario dormir i volver a preguntar)
#
#
# Deduccions
# Classe Player handler, maneja las peticiones de los threads que se conectan
# Game maneja la logica del juego
# 
# 
# 
# 
# 
# 
# 
# 
# 