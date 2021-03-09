from GenerateAndTest import linear_congruence, test_all
from Player import Player
from Team import Team


class Play:
    team_1_history = []
    team_2_history = []

    def init_play(self, team_1, team_2):
        team_1.new_round()
        team_2.new_round()
        team_1.finish_game()
        team_2.finish_game()
        winner = {"player": self.create_player(0, 0, 0, 0), "team": ""}
        male = 0
        female = 0
        for round in range(1, 11):
            launch_1 = int(sum(player.endurance_round for player in team_1.players) / 5) + 5
            launch_2 = int(sum(player.endurance_round for player in team_2.players) / 5) + 5
            count = launch_1 + launch_2
            launch = linear_congruence(count)
            while not test_all(launch):
                launch = linear_congruence(count)
            self.play_round(team_1, launch[0:launch_1])
            self.play_round(team_2, launch[launch_1:launch_1 + launch_2])
            self.assign_luck(team_1)
            self.assign_luck(team_2)
            winner_1 = team_1.get_player_winner()
            winner_2 = team_2.get_player_winner()
            if winner_1.points == winner_2.points:
                self.solve_tie(team_1, team_2)
            if winner_1.points != winner_2.points:
                if winner_1.points > winner_2.points:
                    winner_round = team_1.get_player_winner_round()
                if winner_1.points < winner_2.points:
                    winner_round = team_2.get_player_winner_round()
            if winner_round.gender == "male":
                male += 1
            if winner_round.gender == "female":
                female += 1
            self.launch_lucky(team_1)
            self.launch_lucky(team_2)
        if team_1.get_player_win().win == team_2.get_player_win().win:
            self.solve_tie_finish(team_1, team_2)
        if team_1.get_player_win().win > team_2.get_player_win().win:
            winner = {"player": team_1.get_player_win(), "team": team_1.name}
        if team_1.get_player_win().win < team_2.get_player_win().win:
            winner = {"player": team_2.get_player_win(), "team": team_2.name}
        self.team_1_history.append(team_1)
        self.team_2_history.append(team_2)
        lucky = {"player": self.create_player(0, 0, 0, 0), "team": ""}
        if team_1.lucky_player_round().extra > team_2.lucky_player_round().extra:
            lucky = {"player": team_1.lucky_player_round(), "team": team_1.name}
        if team_1.lucky_player_round().extra < team_2.lucky_player_round().extra:
            lucky = {"player": team_2.lucky_player_round(), "team": team_2.name}
        return {"team_1": team_1,
                "team_2": team_2,
                "team_win": team_1 if team_1.points > team_2.points else team_2,
                "winner": winner,
                "lucky": lucky,
                "male": male,
                "female": female}

    def solve_tie_finish(self, team_1, team_2):
        while team_1.get_player_winner().win == team_2.get_player_winner().win:
            launch = linear_congruence(2)
            while not test_all(launch):
                launch = linear_congruence(2)
            point_1 = self.get_point(launch[0], team_1.get_player_winner())
            point_2 = self.get_point(launch[1], team_2.get_player_winner())
            if point_1 > point_2:
                team_1.get_player_winner().win += 1
            elif point_1 < point_2:
                team_2.get_player_winner().win += 1

    def solve_tie(self, team_1, team_2):
        while team_1.get_player_winner().points == team_2.get_player_winner().points:
            launch = linear_congruence(2)
            while not test_all(launch):
                launch = linear_congruence(2)
            point_1 = self.get_point(launch[0], team_1.get_player_winner())
            point_2 = self.get_point(launch[1], team_2.get_player_winner())
            team_1.get_player_winner().win_points(point_1)
            team_2.get_player_winner().win_points(point_2)

    def create_player(self, id, endurance, luck, gender):
        return Player(id, int(45 + (65 - 45) * endurance), 1 + (5 - 1) * luck, "female" if gender < 0.5 else "male")

    def create_teams(self, name, color):
        numbers = linear_congruence(55)
        while not test_all(numbers):
            numbers = linear_congruence(55)
        players = []
        for i in range(1, 16):
            players.append(self.create_player(i, numbers[i], numbers[i + 1], numbers[i + 2]))
        return Team(players=players, name=name, color=color)

    def get_point(self, launch, player):
        new_launch = int(99 * launch)
        if player.gender == "male":
            if new_launch < 20:
                return 10
            if 20 <= new_launch < 53:
                return 8
            if 53 <= new_launch < 93:
                return 6
            if 93 <= new_launch < 100:
                return 0
        if player.gender == "female":
            if new_launch < 30:
                return 10
            if 30 <= new_launch < 68:
                return 8
            if 68 <= new_launch < 95:
                return 6
            if 95 <= new_launch < 100:
                return 0

    def launch_for_player(self, launch, player):
        player.launch()
        player.win_points(self.get_point(launch, player))

    def play_round(self, team, launch):
        init = 0
        for player in team.players:
            count = init + int(player.endurance_round / 5) + 1
            for step in launch[init:count]:
                self.launch_for_player(step, player)
            team.get_global_score(player.points)
            init = count
        self.launch_lucky(team)
        team = self.assign_fatigue(team)
        return team

    def assign_fatigue(self, team):
        fatigues = self.get_fatigue_team()
        for i in range(0, 15):
            team.players[i].fatigue(fatigues[i])
        return team

    def assign_luck(self, team):
        lucky = linear_congruence(15)
        while not test_all(lucky):
            lucky = linear_congruence(15)
        for i, player in enumerate(team.players):
            player.assign_luck(lucky[i])

    def get_fatigue_team(self):
        fatigues_random = linear_congruence(15)
        while not test_all(fatigues_random):
            fatigues_random = linear_congruence(15)
        fatigues = []
        for fatigue in fatigues_random:
            if fatigue < 0.5:
                fatigues.append(1)
            fatigues.append(2)
        return fatigues

    def launch_lucky(self, team):
        lucky = linear_congruence(2)
        while not test_all(lucky):
            lucky = linear_congruence(2)
        team.get_global_score(self.get_point(lucky[0], team.lucky_player()))
        if team.lucky_player().extra == 0:
            team.lucky_player().extra = 1
        else:
            team.lucky_player().extra_launch()
        if team.lucky_player().extra >= 3:
            lucky = linear_congruence(2)
            while not test_all(lucky):
                lucky = linear_congruence(2)
            team.get_global_score(self.get_point(lucky[0], team.lucky_player()))

# play = Play()
# print(play.init_play(play.create_teams("efr", ""), play.create_teams("efr", "")))
