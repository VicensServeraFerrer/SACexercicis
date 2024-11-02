import paho.mqtt.client as mqtt


topic_create = "create/sala"
client = None
tablero = [[1,1,1], [1,1,1], [1,1,1]]
broker = "localhost"
port = 1883
players = []
turn = None
salas = {}

def getTablero():
    return [[1,1,1], [1,1,1], [1,1,1]]

def on_message(client, userdata, message):
    decoded_message = message.payload.decode()
    if message.topic==topic_create:
        player_name, room_topic = decoded_message.split(':')
        if room_topic in salas:
            salas[room_topic]["players"].append(player_name)
            client.publish(room_topic, f'{salas[room_topic]["turn"]}:Your turn!:0')
        else:
            salas[room_topic] = {"players": [player_name],
                                 "turn": player_name,
                                 "tablero": getTablero()}
            client.subscribe(room_topic)
    else:
        topic_room = message.topic
        player, move, null = decoded_message.split(":")
        if ',' in move:
            itsTurn = makeMove(player, move, topic_room)
            if itsTurn:
                print(f"Player '{player}' makes move")
                win = check_victory(topic_room)
                if win==1:
                    client.publish(topic_room, f'win:{decoded_message.split(":")[0]}:{salas[topic_room]["tablero"]}')
                elif win==2:
                    client.publish(topic_room, f'draw:{decoded_message.split(":")[0]}:{salas[topic_room]["tablero"]}')
                else:
                    for p in salas[topic_room]["players"]:
                        if p!=salas[topic_room]["turn"]:
                            salas[topic_room]["turn"]=p
                            client.publish(topic_room, f'{p}:Your turn!:{salas[topic_room]["tablero"]}')
                            return



def makeMove(player, move, room_topic):
    global salas
    if salas[room_topic]["turn"] == player:
        x, y, symbol = move.split(',')
        if salas[room_topic]["tablero"][int(x)][int(y)] == 1:
            salas[room_topic]["tablero"][int(x)][int(y)] = symbol
        return True
    else:
        return False      

def check_victory(room_topic):
    global salas
    for row in salas[room_topic]["tablero"]:
        if row[0] == row[1] == row[2] and row[0] != 1:
            return 1

    for col in range(3):
        if salas[room_topic]["tablero"][0][col] == salas[room_topic]["tablero"][1][col] == salas[room_topic]["tablero"][2][col] and salas[room_topic]["tablero"][0][col] != 1:
            return 1
    if salas[room_topic]["tablero"][0][0] == salas[room_topic]["tablero"][1][1] == salas[room_topic]["tablero"][2][2] and salas[room_topic]["tablero"][0][0] != 1:
        return 1

    if salas[room_topic]["tablero"][0][2] == salas[room_topic]["tablero"][1][1] == salas[room_topic]["tablero"][2][0] and salas[room_topic]["tablero"][0][2] != 1:
        return 1

    for row in salas[room_topic]["tablero"]:
        if 1 in row:
            return 0
        

    return 2



client = mqtt.Client("Sala")
client.on_message = on_message
client.connect(broker, port, keepalive=60)
client.subscribe(topic_create)
client.loop_forever()




