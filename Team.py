from operator import attrgetter


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.points = 0

    def win_round(self):
        self.points += 1

    def sort_by_luck(self):
        self.players.sort(key=lambda player: player.luck, reverse=True)

    def sort_by_points(self):
        self.players.sort(key=lambda player: player.points, reverse=True)

    def get_global_score(self, individual):
        self.points += individual

    def lucky_player(self):
        return max(self.players, key=attrgetter('luck'))

    def finish_game(self):
        for player in self.players:
            player.restart_endurance()

    def get_player_winner_round(self):
        winner = max(self.players, key=attrgetter('points'))
        print(winner)
        winner.win_round()
        return winner

    def get_player_winner(self):
        return max(self.players, key=attrgetter('points'))

    def new_round(self):
        for player in self.players:
            player.finish_round()

    def get_player_win(self):
        return max(self.players, key=attrgetter('win'))