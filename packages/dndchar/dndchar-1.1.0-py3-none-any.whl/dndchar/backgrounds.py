from dndchar.data import languages
from dndchar.util import Roller
roll = Roller()

# Stores background attributes
class Background:
    def __init__(self):
        #Background.__init__(self)
        self.name = "Background"
        self.skills = []
        self.lang = []
        self.tools = []
        self.equipment = []
        self.personality = {
        "traits": [],
        "ideals": [],
        "bonds": [],
        "flaws": []
        }
        self.feature = ("name", "description")
    def __str__(self):
        return self.name

# Actual Backgrounds
#Acolyte
class Acolyte(Background):
    def __init__(self):
        Background.__init__(self)
        self.name = "Acolyte"
        self.skills = ["Insight", "Religion"]
        self.lang = roll.sample(languages, 2)
        self.equipment = [
        "a holy symbol",
        "a prayer book or prayer wheel",
        "5 sticks of incense",
        "vestments",
        "a set of common clothes",
        "a belt pouch containing 15 gp"
        ]
        self.personality = {
        "traits": ["I idolize a particular hero of my faith, and constantly refer to that person’s deeds and example.", "I can find common ground between the fiercest enemies, empathizing with them and always working toward peace.", "I see omens in every event and action. The gods try to speak to us, we just need to listen.", "Nothing can shake my optimistic attitude.", "I quote (or misquote) sacred texts and proverbs in almost every situation.", roll.choice(["I am tolerant of other faiths and respect the worship of other gods.", "I am intolerant of other faiths and condemn the worship of other gods."]), "I've enjoyed fine food, drink, and high society among my temple’s elite. Rough living grates on me.", "I’ve spent so long in the temple that I have little practical experience dealing with people in the outside world."],
        "ideals": ["**Tradition.** The ancient traditions of worship and sacrifice must be preserved and upheld. (Lawful)", "**Charity.** I always try to help those in need, no matter what the personal cost. (Good)", "**Change.** We must help bring about the changes the gods are constantly working in the world. (Chaotic)", "**Power.** I hope to one day rise to the top of my faith’s religious hierarchy. (Lawful)", "**Faith.** I trust that my deity will guide my actions, I have faith that if I work hard, things will go well. (Lawful)", "**Aspiration.** I seek to prove myself worthy of my god’s favor by matching my actions against his or her teachings. (Any)",],
        "bonds": ["I would die to recover an ancient relic of my faith that was lost long ago.", "I will someday get revenge on the corrupt temple hierarchy who branded me a heretic.", "I owe my life to the priest who took me in when my parents died.", "Everything I do is for the common people.", "I will do anything to protect the temple where I served.", "I seek to preserve a sacred text that my enemies consider heretical and seek to destroy."],
        "flaws": ["I judge others harshly, and myself even more severely.", "I put too much trust in those who wield power within my temple’s hierarchy.", "My piety sometimes leads me to blindly trust those that profess faith in my god.", "I am inflexible in my thinking.", "I am suspicious of strangers and expect the worst of them.", "Once I pick a goal, I become obsessed with it to the detriment of everything else in my life."]
        }
        self.feature = ("Shelter of the Faithful", "As an acolyte, you command the respect of those who share your faith, and you can perform the religious ceremonies of your deity. You and your adventuring companions can expect to receive free healing and care at a temple, shrine, or other established presence of your faith, though you must provide any material components needed for spells. Those who share your religion will support you (but only you) at a modest lifestyle.", "You might also have ties to a specific temple dedicated to your chosen deity or pantheon, and you have a residence there. This could be the temple where you used to serve, if you remain on good terms with it, or a temple where you have found a new hom e. W hile near your temple, you can call upon the priests for assistance, provided the assistance you ask for is not hazardous and you remain in good standing with your temple.")


#Charlatan
class Charlatan(Background):
    def __init__(self):
        Background.__init__(self)
        self.name = "Charlatan"
        self.skills = ["Deception", "Sleight of Hand"]
        self.tools = ["disguise kit", "forgery kit"]
        self.equipment = ["a set of fine clothes", "a disguise kit", "tools of the con of your choice (ten stoppered bottles filled with colored liquid, a set of weighted dice, a deck of marked cards or a signet ring of an imaginary duke)", "a belt pouch containing 15 gp"]
        self.personality = {
        "traits": ["I fall in and out of love easily, and am always pursuing someone.", "I have a joke for every occasion, especially occasions where humor is inappropriate.", "Flattery is my preferred trick for getting what I want.", "I’m a born gambler who can't resist taking a risk for a potential payoff.", "I lie about almost everything, even when there’s no good reason to.", "Sarcasm and insults are my weapons of choice.", "I keep multiple holy symbols on me and invoke whatever deity might come in useful at any given moment.", "I pocket anything I see that might have some value."],
        "ideals": ["**Independence.** I am a free spirit— no one tells me what to do. (Chaotic)", "**Fairness.** I never target people who can’t afford to lose a few coins. (Lawful)", "**Charity.** I distribute the money I acquire to the people who really need it. (Good)", "**Creativity.** I never run the same con twice. (Chaotic)", "**Friendship.** Material goods come and go. Bonds of friendship last forever. (Good)", "**Aspiration.** I’m determined to make something of myself. (Any)"],
        "bonds": ["I fleeced the wrong person and must work to ensure that this individual never crosses paths with me or those I care about.", "I owe everything to my mentor— a horrible person who’s probably rotting in jail somewhere.", "Somewhere out there, I have a child who doesn’t know me. I’m making the world better for him or her.", "I come from a noble family, and one day I’ll reclaim my lands and title from those who stole them from me.", "A powerful person killed someone I love. Some day soon, I’ll have my revenge.", "I swindled and ruined a person who didn’t deserve it. I seek to atone for my misdeeds but might never be able to forgive myself."],
        "flaws": ["I can’t resist a pretty face.", "I'm always in debt. I spend my ill-gotten gains on decadent luxuries faster than I bring them in.", "I’m convinced that no one could ever fool me the way I fool others.", "I’m too greedy for my own good. I can’t resist taking a risk if there’s money involved.", "I can’t resist swindling people who are more powerful than me.", "I hate to admit it and will hate myself for it, but I'll run and preserve my own hide if the going gets tough."]
        }
        self.feature = ("False Identity", "You have created a second identity that includes documentation, established acquaintances, and disguises that allow you to assume that persona. Additionally, you can forge documents including official papers and personal letters, as long as you have seen an example of the kind of document or the handwriting you are trying to copy.")


backgrounds = [Acolyte, Charlatan]
