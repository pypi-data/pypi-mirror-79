from dndchar.backgrounds import backgrounds
from dndchar.classes import classes
from dndchar.races import races
from dndchar.scores import Ability
from dndchar.util import Roller
roller = Roller()

n = "\n"

class Player:
    def __init__(self, race, cls, background):
        self.race = race
        self.cls = cls
        self.background = background
        self.strongscores = self.cls.goodabilities
        self.scores = roller.getscores(
            self.cls.goodabilities,
            str=self.race.scores["str"],
            dex=self.race.scores["dex"],
            con=self.race.scores["con"],
            int=self.race.scores["int"],
            wis=self.race.scores["wis"],
            cha=self.race.scores["cha"]
        )
        self.hp = self.cls.hitdie + self.scores["con"].modifier
        self.armor = 10 + self.scores["dex"].modifier
        self.perception = 10 + self.scores["wis"].modifier + self.cls.proficiency
        self.align = {
        "deeds": roller.choice(self.race.align["deeds"]),
        "order": roller.choice(self.race.align["order"])
        }
        self.personality = {
        "trait": roller.choice(self.background.personality["traits"]),
        "ideal": roller.choice(self.background.personality["ideals"]),
        "bond": roller.choice(self.background.personality["bonds"]),
        "flaw": roller.choice(self.background.personality["flaws"])
        }
        self.lang = list(dict.fromkeys(self.race.lang + self.background.lang))
        self.proficiencies = {
            "armor": self.cls.proficiencies["armor"],
            "weapons": self.cls.proficiencies["weapons"],
            "tools": list(dict.fromkeys(self.cls.proficiencies["tools"] + self.background.tools)),
            "skills": list(dict.fromkeys(self.cls.proficiencies["skills"] + self.background.skills))
        }
        self.gender = roller.choice(["male", "female"])
        if self.race.names["family"] != []:
            self.name = roller.choice(self.race.names[self.gender])+" "+roller.choice(self.race.names["family"])
        else:
            self.name = roller.choice(self.race.names[self.gender])
        self.equipment = self.cls.equipment + self.background.equipment
        self.equipment = "\n- ".join(self.equipment)
        self.features = self.cls.features + self.race.features + [self.background.feature]
        for i, x in enumerate(self.features):
            self.features[i] = "**"+self.features[i][0]+"**. " + self.features[i][1]
        self.features = "\n".join(self.features)
    def __str__(self):
        return f"""**{self.name}**
*{self.background.name} {self.race.name} {self.cls.name}*
Hit Die: 1d{self.cls.hitdie}\tHealth: {self.hp}
Speed: {self.race.speed}\tArmor Class: {self.armor}
STR: {self.scores["str"].score}, {self.scores["str"].strmod}\tINT: {self.scores["int"].score}, {self.scores["int"].strmod}
DEX: {self.scores["dex"].score}, {self.scores["dex"].strmod}\tWIS: {self.scores["wis"].score}, {self.scores["wis"].strmod} ({self.perception})
CON: {self.scores["con"].score}, {self.scores["con"].strmod}\tCHA: {self.scores["cha"].score}, {self.scores["cha"].strmod}
Alignment: {self.align["order"].title()} {self.align["deeds"].title()}
Personality:
- {self.personality["trait"]}
- {self.personality["ideal"]}
- {self.personality["bond"]}
- {self.personality["flaw"]}
Proficiencies:
- Saving Throws:\t{", ".join(self.cls.proficiencies["saving"]).upper()}
- Languages:\t\t{", ".join(self.lang)}
- Armor:\t\t{", ".join(self.proficiencies["armor"])}
- Weapons:\t\t{", ".join(self.proficiencies["weapons"])}
- Tools:\t\t{", ".join(self.proficiencies["tools"])}
- Skills:\t\t{", ".join(self.proficiencies["skills"])}
Equipment:
- {self.equipment}
Features:\n
{self.features}
"""


def getrandchar():
    race = roller.choice(races)()
    if (race.subraces != []):
        race = roller.choice(race.subraces)(race)
    charclass = roller.choice(classes)()
    background = roller.choice(backgrounds)()
    return (race, charclass, background)
