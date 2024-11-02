import paho.mqtt.client as mqtt
import random
import time

# Configuración del broker
broker = "localhost"
port = 1883
topic_getName = "game/connect"
topic_getGame = "game/getGame"
name = str(random.randint(0, 10000000))
inaroom = False
room_topic = None
win = False


# Callback para recibir mensajes
def on_message(client, userdata, message):
    global room_topic, win, inaroom, name, topic_getGame, topic_getName
    topic_recived = message.topic
    if topic_recived==topic_getGame:
        decoded_message = message.payload.decode()
        player_name, new_name, r_topic = decoded_message.split(':')
        if player_name==name and not inaroom:
             inaroom = True
             name = new_name
             room_topic = r_topic
             client.subscribe(r_topic)
    elif topic_recived==room_topic:
        decoded_message = message.payload.decode()
        pre, msg, tablero = decoded_message.split(':')
        if pre=='win':
            if msg==name:
                print("I win")
            elif msg=='draw':
                print("DRAW")
            else:
                print('I lose')
            win = True
            print(tablero)
        elif pre==name:
            if msg=='Is not your turn!':
                return
            elif msg=='Your turn!':
                print('My turn!')
                if not win:
                    move = makeMove()
                    print(f'My move: {name}:{move[0]},{move[1]},{name}')
                    time.sleep(1)
                    client.publish(room_topic, f'{name}:{move[0]},{move[1]},{name}:0')
                


# Configuración del cliente Subscriber
client = mqtt.Client(name)
client.on_message = on_message
client.connect(broker, port, keepalive=60)
time.sleep(1)
client.subscribe(topic_getGame)

def makeMove():
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    return [x, y]


client.publish(topic_getName, f'{name}:getName')
print('getName')

client.loop_forever()

