from random import choice


class Character:

    def __init__(self):
        self.strength = self.calculate_points()
        self.dexterity = self.calculate_points()
        self.constitution = self.calculate_points()
        self.intelligence = self.calculate_points()
        self.wisdom = self.calculate_points()
        self.charisma = self.calculate_points()
        self.hitpoints = 10 + modifier(self.constitution)

    def ability(self):
        score = choice([item for item in vars(self).values()])
        return score

    def dice_roll(self):
        return choice(range(1, 7))

    def calculate_points(self):
        rolls = sorted([self.dice_roll() for number in range(4)], reverse=True)
        return sum(rolls[:2])


def modifier(constitution):
    return (constitution - 10) // 2
