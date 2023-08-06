import random
from dndchar.scores import Ability

# A class that contains all the random functions
class Roller:
    # Get a ability score:
    def score(self):
        rolls = []
        for i in range(4):
            rolls.append(random.randint(1,6))
        rolls.remove(min(rolls))
        return sum(rolls)
    # Returns a dictionary of "Ability"s. pass in modifiers as kwyword args.
    def getscores(self, goodabilities, *, str=0, dex=0, con=0, int=0, wis=0, cha=0):
        scoresleft = ["str", "dex", "con", "int", "wis", "cha"]
        self.shuffle(scoresleft)
        x = {"str":str,"dex":dex,"con":con,"int":int,"wis":wis,"cha":cha}
        scores = [self.score() for i in range(6)]
        scores.sort()
        scores.reverse()
        x[goodabilities[0]] = Ability(scores[0] + x[goodabilities[0]])
        scores.pop(0)
        scoresleft.remove(goodabilities[0])
        x[goodabilities[1]] = Ability(scores[1] + x[goodabilities[1]])
        scores.pop(0)
        scoresleft.remove(goodabilities[1])
        for i in range(4):
            x[scoresleft[0]] = Ability(scores[0] + x[scoresleft[0]])
            scoresleft.pop(0)
            scores.pop(0)
        return x

        return scores
    # choice
    def choice(self, iterable):
        return random.choice(iterable)
    # shuffle
    def shuffle(self, iterable):
        return random.shuffle(iterable)
    # sample
    def sample(self, iterable, num_items):
        return random.sample(iterable, num_items)
