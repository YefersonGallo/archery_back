from GenerateAndTest import linear_congruence, test_all
from Player import Player
from Team import Team


class Play:

    def init_play(self):
        team_1 = self.create_teams("team1")
        team_2 = self.create_teams("team2")
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
            print("Points win team 1:{}".format(winner_1.points))
            print("Points win team 2:{}".format(winner_2.points))
            if winner_1.points == winner_2.points:
                print("Tie")
                self.solve_tie(team_1, team_2, launch)
            if winner_1.points != winner_2.points:
                if winner_1.points > winner_2.points:
                    team_1.get_player_winner_round()
                    print("Win Team 1!!!")
                if winner_1.points < winner_2.points:
                    team_2.get_player_winner_round()
                    print("Win Team 2!!!")
            team_1.new_round()
            team_2.new_round()
            print("------------ROUND {}--------------".format(round))
        print("||||||||||||||||||||||||||||||||||")
        print("Winner play team 1:{}".format(team_1.get_player_win().id))
        print("Winner play team 2:{}".format(team_2.get_player_win().id))
        print("___________________________")
        print("Team 1 points:{}".format(team_1.points))
        print("Team 2 points:{}".format(team_2.points))
        print("___________________________")
        team_1.get_global_score(self.launch_lucky(team_1.lucky_player()))
        team_2.get_global_score(self.launch_lucky(team_2.lucky_player()))
        team_1.finish_game()
        team_2.finish_game()
        print("___________________________")
        print("Team 1 points:{}".format(team_1.points))
        print("Team 2 points:{}".format(team_2.points))
        print(">>>>>>>>>>>>>>>>WIN TEAM {}<<<<<<<<<<<<<<<<<<<<".format(1 if team_1.points > team_2.points else 2))
        print("___________________________")
        for player in team_1.players:
            print("Id:{}, Experience:{}, Win:{}".format(player.id, player.experience, player.win))
        print("----------------------------////////////////////////")
        for player in team_2.players:
            print("Id:{}, Experience:{}, Win:{}".format(player.id, player.experience, player.win))
        print("READY FOR NEXT GAME!!!!!")

    def solve_tie(self, team_1, team_2, launch):
        print("Init")
        while team_1.get_player_winner().points == team_2.get_player_winner().points:
            launch = linear_congruence(2)
            while not test_all(launch):
                launch = linear_congruence(2)
            point_1 = self.get_point(launch[0], team_1.get_player_winner())
            point_2 = self.get_point(launch[1], team_2.get_player_winner())
            print(point_1, point_2)
            team_1.get_player_winner().win_points(point_1)
            team_2.get_player_winner().win_points(point_2)

    def create_player(self, id, endurance, luck, gender):
        return Player(id, int(45 + (65 - 45) * endurance), 1 + (5 - 1) * luck, "female" if gender < 0.5 else "male")

    def create_teams(self, name):
        numbers = linear_congruence(55)
        while not test_all(numbers):
            numbers = linear_congruence(55)
        players = []
        for i in range(1, 16):
            players.append(self.create_player(i, numbers[i], numbers[i + 1], numbers[i + 2]))
        return Team(players=players, name=name)

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

    def launch_lucky(self, player):
        lucky = linear_congruence(2)
        while not test_all(lucky):
            lucky = linear_congruence(2)
        return self.get_point(lucky[0], player)
