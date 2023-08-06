# Add a "+" to the modifier of an Ability score
def addplus(integer):
    if integer > -1:
        return f"+{integer}"
    else:
        return str(integer)
# A simple class to calculate ability scores and modifiers
class Ability:
    scoretable = {
    1: -5,
    2: -4, 3: -4,
    4: -3, 5: -3,
    6: -2, 7: -2,
    8: -1, 9: -1,
    10: 0, 11: 0,
    12: 1, 13: 1,
    14: 2, 15: 2,
    16: 3, 17: 3,
    18: 4, 19: 4,
    20: 5, 21: 5,
    22: 6, 23: 6,
    24: 7, 25: 7,
    26: 8, 27: 8,
    28: 9, 29: 9,
    30: 10
    }
    def __init__(self, score):
        self.score = score;
        self.modifier = Ability.scoretable[score];
        self.strmod = addplus(self.modifier)
    # A function to add the scare modifier:
    def mod(self, modvalue):
        self.score = self.score + modvalue;
        self.modifier = Ability.scoretable[self.score];
        self.strmod = addplus(self.modifier)
    def __str__(self):
        return f"Ability: {self.score} +{slf.modifier}"
