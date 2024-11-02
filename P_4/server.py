import paho.mqtt.client as mqtt

# Configuración del broker
broker = "localhost"
port = 1883
topic_getName = "game/connect"
topic_getGame = "game/getGame"
topic_create_sala = "create/sala"

room_id = 0
rooms = {}

player_names = []
picked = []

for i in range(0, 50):
    player_names.append(f"Player{i}")
    picked.append(False)

def getName():
    for i in range(0, len(player_names)):
        if not picked[i]:
            picked[i] = True
            return player_names[i]
    return 0

# Callback para recibir mensajes
def on_message(client, userdata, message):
    global room_id, rooms, topic_getGame, topic_getName, topic_create_sala
    decoded_message = message.payload.decode()
    if ':' in decoded_message:
        client_name, func = decoded_message.split(':')
        print(f"Client {client_name} wants to play.")
        if room_id in rooms and rooms[room_id]["num_players"] < 2:
            rooms[room_id]["num_players"] += 1  
        elif room_id in rooms and rooms[room_id]["num_players"] == 2: 
            room_id += 1
            rooms[room_id] = {"room_topic": create_room_topic(), 
                             "num_players": 1}
        elif not room_id in rooms:
            rooms[room_id] = {"room_topic": create_room_topic(), 
                             "num_players": 1}
        new_name = getName()
        new_message = f'{client_name}:{new_name}:{rooms[room_id]["room_topic"]}'
        client.publish(topic_getGame, new_message)
        message_create = f'{new_name}:{rooms[room_id]["room_topic"]}'
        client.publish(topic_create_sala, message_create)


# Configuración del cliente Subscriber
client = mqtt.Client("Server")
client.on_message = on_message
client.connect(broker, port, keepalive=60)
client.subscribe(topic_getName)

def create_room_topic():
    global room_id
    return f'game/room{room_id}'

client.loop_forever()

