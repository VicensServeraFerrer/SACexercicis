from flask import Flask, jsonify
import random

servei = Flask(__name__)

quantitat_numeros_generats = [0,0,0]
numeros_generats = [11,12,13]

@servei.route('/agent/<int:agent_id>/generar', methods=['GET'])
def generar_numero(agent_id):
    global numeros_generats, quantitat_numeros_generats

    numeros_generats[agent_id] = random.randint(1, 9)

    quantitat_numeros_generats[agent_id] += 1

    return jsonify({
        'number_generated': numeros_generats[agent_id],
        'tries': quantitat_numeros_generats[agent_id]
    })

@servei.route('/consens', methods=['GET'])
def existeix_consens():
    global numeros_generats

    if numeros_generats.count(numeros_generats[0]) >= 2 or numeros_generats.count(numeros_generats[1]) >= 2:
        return jsonify({
        'message': "Hi ha consens!",
        'consens': True
        })
    else: 
        return jsonify({
        'message': "No hi ha consens",
        'consens': False
        })

# if __name__ == '__main__':
#     servei.run(debug=True)