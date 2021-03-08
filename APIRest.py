from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from Play import Play

app = Flask(__name__)
CORS(app, support_credentials=True)
play = Play()


# Petición para comprobar la conexión del servidor
@app.route('/ping', methods=['GET'])
@cross_origin(supports_credentials=True)
def ping():
    return jsonify({'response': 'pong!'})


@app.route('/create_team', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_team():
    name = request.json["name"]
    team = play.create_teams(name=name)
    players = []
    for player in team.players:
        players.append({'id': player.id, 'endurance': player.endurance, 'luck': player.luck, 'gender': player.gender})
    res = {'name': team.name, 'players': players}
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
