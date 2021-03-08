class Player:
    def __init__(self, id, endurance, luck, gender):
        self.id = id
        self.endurance = endurance
        self.gender = gender
        self.experience = 10
        self.luck = luck
        self.endurance_round = endurance
        self.endurance_previous_round = endurance
        self.points = 0
        self.extra = 0
        self.win = 0

    def launch(self):
        self.endurance_round -= 5

    def win_points(self, point_launch):
        self.points += point_launch

    def finish_round(self):
        self.points = 0

    def win_round(self):
        self.win += 1
        self.experience += 3

    def assign_luck(self, luck):
        self.luck = luck

    def fatigue(self, fatigue):
        self.endurance_round = self.endurance_previous_round - fatigue
        self.endurance_previous_round = self.endurance_round

    def restart_endurance(self):
        self.endurance_round = self.endurance

    def extra_launch(self):
        if self.extra != 0:
            self.extra += 1
        else:
            self.extra = 0
