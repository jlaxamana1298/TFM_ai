import random


class RandomBot:
    def __init__(self):
        pass

    def ban_choice(self, char_pool, b_team, r_team, turn):
        choice = random.choice(char_pool)
        return choice

    def pick_choice(self, char_pool, b_team, r_team, turn):
        choice = random.choice(char_pool)
        return choice