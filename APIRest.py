from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from Play import Play
from Player import Player
from Team import Team

app = Flask(__name__)
CORS(app, support_credentials=True)
play = Play()
team_1_history = []
team_2_history = []
male_total = 0
female_total = 0


# Petición para comprobar la conexión del servidor
@app.route('/ping', methods=['GET'])
@cross_origin(supports_credentials=True)
def ping():
    return jsonify({'response': 'pong!'})


@app.route('/create_team', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_team():
    name = request.json["name"]
    color = request.json["color"]
    team = play.create_teams(name=name, color=color)
    players = []
    for player in team.players:
        players.append({'id': player.id, 'endurance': player.endurance, 'luck': player.luck, 'gender': player.gender,
                        'experience': player.experience})
    res = {'name': team.name, 'players': players, 'color': color}
    return jsonify(res)


@app.route('/play_game', methods=['POST'])
@cross_origin(supports_credentials=True)
def play_round():
    team_1 = get_team(request.json["team1"])
    team_2 = get_team(request.json["team2"])
    iteration = request.json["i"]
    if iteration == 1:
        play.restart_historial()
    results = play.init_play(team_1, team_2)
    res = {"team_1": send_team(results["team_1"]),
           "team_2": send_team(results["team_2"]),
           "team_win": send_team(results["team_win"]),
           "winner": {'id': results["winner"]["player"].id, 'endurance': results["winner"]["player"].endurance,
                      'luck': results["winner"]["player"].luck,
                      'gender': results["winner"]["player"].gender, 'points': results["winner"]["player"].points,
                      "team": results["winner"]["team"]},
           "lucky": {'id': results["lucky"]["player"].id, 'endurance': results["lucky"]["player"].endurance,
                     'luck': results["lucky"]["player"].luck,
                     'gender': results["lucky"]["player"].gender, 'points': results["lucky"]["player"].points,
                     "team": results["lucky"]["team"]},
           "female": results["female"],
           "male": results["male"]
           }
    return jsonify(res)


@app.route('/statistics', methods=['GET'])
@cross_origin(supports_credentials=True)
def total():
    res = play.get_total_points()
    return jsonify(
        {"male": res["male"], "female": res["female"], "team_1": res["team_1"], "total_points_1": res["total_points_1"],
         "team_2": res["team_2"], "total_points_2": res["total_points_2"]})


def get_team(team):
    players = team["players"]
    players_arr = []
    for player in players:
        new = Player(player["id"], player["endurance"], player["luck"], player["gender"])
        new.experience = player["experience"]
        players_arr.append(new)
    return Team(name=team["name"], players=players_arr, color=team["color"])


def send_team(team):
    players = []
    for player in team.players:
        players.append({'id': player.id, 'endurance': player.endurance, 'luck': player.luck, 'gender': player.gender,
                        'points': player.points, 'experience': player.experience})
    return {'name': team.name, 'players': players, 'color': team.color, "points": team.points}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
