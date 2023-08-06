from dndchar.data import (
    abilityscores,
	skills,
	simpleweapons_melee,
	simpleweapons,
    martialweapons,
    artisanstools,
    instruments,
	clericdomains,
	fighterstyle,
	rangerenimies,
	rangerterrains,
    sorcererorgin
)
from dndchar.util import Roller
roll = Roller()
c = roll.choice
# Stores race attributes
class CharacterClass:
    def __init__(self):
        #CharacterClass.__init__(self)
        self.name = "characterclass"
        self.goodabilities = []
        self.hitdie = 0
        self.proficiency = 0
        self.proficiencies = {
            "armor": [],
            "weapons": [],
            "tools": [],
            "saving": [],
            "skills": []
        }
        self.equipment = []
        self.spellcasting = {
        "cantrips": 0,
        "spellsknown": 0,
        "slots": {1: 0}
        }
        # Level 1 subclasses only
        self.subclasses = []
        # Level 1 features only!
        self.features = []
    def __str__(self):
        return self.name


# Actual Classes
#Barbarian
class Barbarian(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Barbarian"
        self.goodabilities = ["str", "con"]
        self.hitdie = 12
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["light armor","medium armor","shields"],
            "weapons": ["simple weapons","martial weapons"],
            "tools": [],
            "saving": ["str", "con"],
            "skills": roll.sample(["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"], 2)
        }
        self.equipment = [
            c(["a greataxe", c(martialweapons)]),
            c(["two handaxes", c(simpleweapons)]),
            "an explorer's pack",
            "four javelins"
        ]
        self.features = [
        ("Rage", "In battle, you fight with primal ferocity. On your turn, you can enter a rage as a bonus action. While raging, you gain the following benefits if you aren’t wearing heavy armor:\n• You have advantage on Strength checks and Strength saving throws.\n• When you make a melee weapon attack using Strength, you gain a bonus to the damage roll that increases as you gain levels as a barbarian, as shown in the Rage Damage column of the Barbarian table.\n• You have resistance to bludgeoning, piercing, and slashing damage.\nIf you are able to cast spells, you can’t cast them or concentrate on them while raging.\nYour rage lasts for 1 minute. It ends early if you are knocked unconscious or if your turn ends and you haven’t attacked a hostile creature since your last turn or taken damage since then. You can also end your rage on your turn as a bonus action.\nOnce you have raged the number of times shown for your barbarian level in the Rages column of the Barbarian table, you must finish a long rest before you can rage again."),
        ("Unarmored Defense", "While you are not wearing any armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier. You can use a shield and still gain this benefit.")
        ]


#Bard
class Bard(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Bard"
        self.goodabilities = ["cha", "dex"]
        self.hitdie = 8
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["light armor"],
            "weapons": ["simple weapons", "hand crossbows", "longswords", "rapiers", "shortswords"],
            "tools": roll.sample(instruments, 3),
            "saving": ["dex", "cha"],
            "skills": roll.sample(skills, 3)
        }
        self.equipment = [
        c(["a rapier", "a longsword", c([simpleweapons])]),
        c(["a diplomat’s pack", "an entertainer's pack"]),
        c(["lute", c(instruments)]),
        "leather armor",
        "a dagger"
        ]
        self.spellcasting = {
        "cantrips": 2,
        "spellsknown": 4,
        "slots": {1: 2}
        }
        self.features = [
        ("Spellcasting", "Charisma is your spellcasting ability for your bard spells. Your magic comes from the heart and soul you pour into the performance of your music or oration. You use your Charisma whenever a spell refers to your spellcasting ability. In addition, you use your Charisma modifier when setting the saving throw DC for a bard spell you cast and when making an attack roll with one.\nSpell save DC = 8 + your proficiency bonus + your Charisma modifier\nSpell attack modifier = your proficiency bonus + your Charisma modifier\nRitual Casting\nYou can cast any bard spell you know as a ritual if that spell has the ritual tag.\nSpellcasting Focus\nYou can use a musical instrument as a spellcasting focus for your bard spells."),
        ("Bardic Inspiration", "You can inspire others through stirring words or music. To do so, you use a bonus action on your turn to choose one creature other than yourself within 60 feet of you who can hear you. That creature gains one Bardic Inspiration die, a d6.\nOnce within the next 10 minutes, the creature can roll the die and add the number rolled to one ability check, attack roll, or saving throw it makes. The creature can wait until after it rolls the d20 before deciding to use the Bardic Inspiration die, but must decide before the DM says whether the roll succeeds or fails. Once the Bardic Inspiration die is rolled, it is lost. A creature can have only one Bardic Inspiration die at a time.\nYou can use this feature a number of times equal to your Charisma modifier (a minimum of once). You regain any expended uses when you finish a long rest. Your Bardic Inspiration die changes when you reach certain levels in this class. The die becom es a d8 at 5th level, a d 10 at 10th level, and a d l2 at 15th level.")
        ]


#Cleric
class Cleric(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Cleric"
        self.goodabilities = ["wis", "con"]
        self.hitdie = 8
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["light armor", "medium armor", "shields"],
            "weapons": ["All simple weapons"],
            "tools": [],
            "saving": ["wis","cha"],
            "skills": roll.sample(["History", "Insight", "Medicine", "Persuasion", "Religion"], 2)
        }
        self.equipment = [
        "a mace",
        c(["scale mail","leather armor"]),
        c(["a light crossbow and 20 bolts ", c(simpleweapons)]),
        c(["a priest’s pack", "an explorer’s pack"]),
        "a shield",
        "a holy symbol"
        ]
        self.spellcasting = {
        "cantrips": 3,
        "slots": {1: 2}
        }
        self.features = [
        ("Spellcasting", "You prepare the list of cleric spells that are available for you to cast, choosing from the cleric spell list. When you do so, choose a number of cleric spells equal to your Wisdom modifier + your cleric level (minimum of one spell). The spells must be of a level for which you have spell slots.\nFor example, if you are a 3rd-level cleric, you have four 1st-level and two 2nd-level spell slots. With a Wisdom of 16, your list of prepared spells can include six spells of 1st or 2nd level, in any combination. If you prepare the 1st-level spell cure wounds, you can cast it using a 1st-level or 2nd-level slot. Casting the spell doesn’t remove it from your list of prepared spells. You can change your list of prepared spells when you finish a long rest. Preparing a new list o f cleric spells requires time spent in prayer and meditation: at least 1 minute per spell level for each spell on your list.\nSpellcasting Ability\nWisdom is your spellcasting ability for your cleric spells. The power of your spells comes from your devotion to your deity. You use your Wisdom whenever a cleric spell refers to your spellcasting ability. In addition, you use your Wisdom m odifier when setting the saving throw DC for a cleric spell you cast and when making an attack roll with one.\nSpell save DC = 8 + your proficiency bonus + your Wisdom modifier\nSpell attack modifier = your proficiency bonus + your Wisdom modifier\nRitual Casting\nYou can cast a cleric spell as a ritual if that spell has the ritual tag and you have the spell prepared.\nSpellcasting Focus\nYou can use a holy symbol as a spellcasting focus for your cleric spells."),
        ("Divine Domain", "Choose one domain related to your deity: Knowledge, Life, Light, Nature, Tempest, Trickery, or War. Each domain is detailed at the end of the class description, and each one provides examples of gods associated with it. Your choice grants you domain spells and other features when you choose it at 1st level. It also grants you additional ways to use Channel Divinity when you gain that feature at 2nd level, and additional benefits at 6th, 8th, and 17th levels.\nDomain Spells\nEach dom ain has a list of spells—its domain spells— that you gain at the cleric levels noted in the domain description. Once you gain a domain spell, you always have it prepared, and it doesn’t count against the number of spells you can prepare each day.\nIf you have a domain spell that doesn’t appear on the cleric spell list, the spell is nonetheless a cleric spell for you.\nYour Divine Domine is: "+c(clericdomains)+".")
        ]


#Druid
class Druid(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Druid"
        self.goodabilities = ["wis", "con"]
        self.hitdie = 8
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["light armor", "medium armor", "shields"],
            "weapons": ["clubs", "daggers", "darts", "javelins", "maces",
"quarterstaffs", "scimitars", "sickles", "slings", "spears"],
            "tools": ["herbalism kit"],
            "saving": ["int", "wis"],
            "skills": roll.sample(["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"], 2)
        }
        self.equipment = [
        c(["a wooden shield", c(simpleweapons)]),
        c(["a scimitar", c([simpleweapons_melee])]),
        "leather armor",
        "an explorer's pack",
        "a drudic focus"
        ]
        self.spellcasting = {
        "cantrips": 2,
        "slots": {1: 2}
        }
        self.features = [
        ("Spellcasting", "You prepare the list of druid spells that are available for you to cast, choosing from the druid spell list. When you do so, choose a number of druid spells equal to your Wisdom modifier + your druid level (minimum of one spell). The spells must be of a level for which you have spell slots.\nFor example, if you are a 3rd-level druid, you have four 1st-level and two 2nd-level spell slots. With a Wisdom of 16, your list of prepared spells can include six spells of 1st or 2nd level, in any combination. If you prepare the 1st-level spell cure wounds, you can cast it using a 1st-level or 2nd-level slot. Casting the spell doesn’t remove it from your list of prepared spells.\nYou can also change your list of prepared spells when you finish a long rest. Preparing a new list of druid spells requires time spent in prayer and meditation: at least 1 minute per spell level for each spell on your list.\nSpellcasting Ability\nWisdom is your spellcasting ability for your druid spells, since your magic draws upon your devotion and attunement to nature. You use your Wisdom whenever a spell refers to your spellcasting ability. In addition, you use your Wisdom modifier when setting the saving throw DC for a druid spell you cast and when making an attack roll with one.\nSpell save DC = 8 + your proficiency bonus + your Wisdom modifier\nSpell attack modifier = your proficiency bonus + your Wisdom modifier\nRitual Casting\nYou can cast a druid spell as a ritual if that spell has the ritual tag and you have the spell prepared.\nSpellcasting Focus\nYou can use a druidic focus as a spellcasting focus for your druid spells."),
        ("Drudic", "You know Druidic, the secret language of druids. You can speak the language and use it to leave hidden messages. You and others who know this language automatically spot such a message. Others spot the message’s presence with a successful DC 15 Wisdom (Perception) check but can’t decipher it without magic.")
        ]


#Fighter
class Fighter(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Fighter"
        self.goodabilities = ["str", "dex"]
        self.hitdie = 10
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["all armor", "shields"],
            "weapons": ["simple weapons", "martial weapons"],
            "tools": [],
            "saving": ["str", "con"],
            "skills": roll.sample(["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"], 2)
        }
        self.equipment = [
        c(["chain mail","leather, longbow, and 20 arrows"]),
        c(martialweapons),
        c(martialweapons),
        c(["a light crossbow and 20 bolts", "two handaxes"]),
        c(["a dungeoneer’s pack", "an explorer’s pack"])
        ]
        self.features = [
        ("Fighting Style", "You adopt a particular style of fighting as your specialty. Choose one of the following options. You can’t take a Fighting Style option more than once, even if you later get to choose again.\nArchery\nYou gain a +2 bonus to attack rolls you make with ranged weapons.\nDefense\nWhile you are wearing armor, you gain a +1 bonus to AC.\nDueling\nWhen you are wielding a m elee w eapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.\nGreat Weapon Fighting\nWhen you roll a 1 or 2 on a damage die for an attack you make with a melee weapon that you are wielding with two hands, you can reroll the die and must use the new roll, even if the new roll is a 1 or a 2. The weapon must have the two-handed or versatile property for you to gain this benefit.\nProtection\nWhen a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to im pose disadvantage on the attack roll. You must be wielding a shield.\nTwo-Weapon Fighting\nWhen you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack.\nYour Fighting Style is: "+c(fighterstyle)+"."),
        ("Second Wind", "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d 10 + your fighter level.\nOnce you use this feature, you must finish a short or long rest before you can use it again.")
        ]


#Monk
class Monk(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Monk"
        self.goodabilities = ["dex", "wis"]
        self.hitdie = 8
        self.proficiency = 2
        self.proficiencies = {
            "armor": [],
            "weapons": ["simple weapons", "shortswords"],
            "tools": [c([c(instruments), c(artisanstools)])],
            "saving": ["str", "dex"],
            "skills": roll.sample(["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"], 2)
        }
        self.equipment = [
        c(["a shortswords", c(simpleweapons)]),
        c(["a dungeoneer’s pack", "an explorer’s pack"]),
        "10 darts"
        ]
        self.features = [
        ("Unarmored Defense", "Beginning at 1st level, while you are wearing no armor and not wielding a shield, your AC equals 10 + your Dexterity modifier + your Wisdom modifier."),
        ("Martial Arts", "At 1st level, your practice of martial arts gives you mastery of combat styles that use unarmed strikes and monk weapons, which are shortswords and any simple melee weapons that don’t have the two-handed or heavy property.\nYou gain the following benefits while you are unarmed or wielding only monk weapons and you aren’t wearing armor or wielding a shield:\n• You can use Dexterity instead of Strength for the attack and damage rolls of your unarmed strikes and monk weapons.\n• You can roll a d4 in place of the normal damage of your unarmed strike or monk weapon. This die changes as you gain monk levels, as shown in the Martial Arts column of the Monk table.\n• When you use the Attack action with an unarmed strike or a monk weapon on your turn, you can make one unarmed strike as a bonus action. For example, if you take the Attack action and attack with a quarterstaff, you can also make an unarm ed strike as a bonus action, assuming you haven't already taken a bonus action this turn. Certain monasteries use specialized forms of the monk weapons. For example, you might use a club that is two lengths of wood connected by a short chain (called a nunchaku) or a sickle with a shorter, straighter blade (called a kama).")
        ]


#Paladin
class Paladin(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Paladin"
        self.goodabilities = ["str", "cha"]
        self.hitdie = 10
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["all armor", "shields"],
            "weapons": ["simple weapons", "martial weapons"],
            "tools": [],
            "saving": ["wis", "cha"],
            "skills": [roll.sample(["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"])]
        }
        self.equipment = [
        c(martialweapons),
        c(martialweapons),
        c(["five javelins", c(simpleweapons)]),
        c(["a priest’s pack", "an explorer’s pack"]),
        "chain mail",
        "a holy symbol"
        ]
        self.spellcasting = None
        self.features = [
        ("Divine Sense", "The presence of strong evil registers on your senses like a noxious odor, and powerful good rings like heavenly music in your ears. As an action, you can open your awareness to detect such forces. Until the end of your next turn, you know the location of any celestial, fiend, or undead within 60 feet of you that is not behind total cover. You know the type (celestial, fiend, or undead) of any being whose presence you sense, but not its identity. Within the same radius, you also detect the presence of any place or object that has been consecrated or desecrated, as with the hallow spell.\nYou can use this feature a number of times equal to 1 + your Charisma modifier.\nWhen you finish a long rest, you regain all expended uses."),
        ("Lay on Hands", "Your blessed touch can heal wounds. You have a pool of healing power that replenishes when you take a long rest. With that pool, you can restore a total number of hit points equal to your paladin level x 5. As an action, you can touch a creature and draw power from the pool to restore a number of hit points to that creature, up to the maximum amount remaining in your pool.\nAlternatively, you can expend 5 hit points from your pool of healing to cure the target of one disease or neutralize one poison affecting it. You can cure multiple diseases and neutralize multiple poisons with a single use of Lay on Hands, expending hit points separately for each one.\nThis feature has no effect on undead and constructs.")
        ]


#Ranger
class Ranger(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Ranger"
        self.goodabilities = ["dex", "wis"]
        self.hitdie = 10
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["light armor", "medium armor", "shields"],
            "weapons": ["simple weapons", "martial weapons"],
            "tools": [],
            "saving": ["str", "dex"],
            "skills": roll.sample(["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"], 3)
        }
        self.equipment = [
        c(["scale mail", "leather armor"]),
        c(simpleweapons),
        c(simpleweapons),
        c(["a dungeoneer’s pack", "an explorer’s pack"]),
        "A longbow and a quiver of 20 arrows"
        ]
        self.features = [
        ("Favored Enemy", "Beginning at 1st level, you have significant experience studying, tracking, hunting, and even talking to a certain type of enemy.\nChoose a type of favored enemy: aberrations, beasts, celestials, constructs, dragons, elementals, fey, fiends, giants, monstrosities, oozes, plants, or undead. Alternatively, you can select two races of humanoid (such as gnolls and orcs) as favored enemies. You have advantage on Wisdom (Survival) checks to track your favored enemies, as well as on Intelligence checks to recall information about them.\nWhen you gain this feature, you also learn one language of your choice that is spoken by your favored enemies, if they speak one at all.\nYou choose one additional favored enemy, as well as an associated language, at 6th and 14th level. As you gain levels, your choices should reflect the types of monsters you have encountered on your adventures.\nYour Favored Enemy type is: "+c(rangerenimies)+"."),
        ("Natural Explorer", "You are particularly familiar with one type of natural environment and are adept at traveling and surviving in such regions. Choose one type of favored terrain: arctic, coast, desert, forest, grassland, mountain, swamp, or the Underdark. When you make an Intelligence or Wisdom check related to your favored terrain, your proficiency bonus is doubled if you are using a skill that you’re proficient in.\nWhile traveling for an hour or m ore in your favored terrain, you gain the following benefits\n• Difficult terrain doesn’t slow your group’s travel.\n• Your group can’t become lost except by magical means.\n• Even when you are engaged in another activity while traveling (such as foraging, navigating, or tracking), you remain alert to danger.\n• If you are traveling alone, you can move stealthily at a normal pace.\n• When you forage, you find twice as much food as you normally would.\n• While tracking other creatures, you also learn their exact number, their sizes, and how long ago they passed through the area.\nYou choose additional favored terrain types at 6th and 10th level.\nYour Natural Environment is: "+c(rangerterrains)+".")
        ]


#Rouge
class Rouge(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Rouge"
        self.goodabilities = ["dex", "cha"]
        self.hitdie = 8
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["light armor"],
            "weapons": ["simple weapons", "hand crossbows", "longswords", "rapiers", "shortswords"],
            "tools": ["thieves' tools"],
            "saving": ["dex", "int"],
            "skills": roll.sample("Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Perform ance, Persuasion, Sleight of Hand, Stealth".split(", "), 4)
        }
        self.equipment = [
        c(["a rapier", "a shortsword"]),
        c(["a shortbow and quiver of 20 arrows", "a shortsword"]),
        c(["a burglar’s pack", "a dungeoneer’s pack", "an explorer’s pack"]),
        "leather armor",
        "two daggers",
        "thieves' tools"
        ]
        self.features = [
        ("Expretise", "At 1st level, choose two of your skill proficiencies, or one of your skill proficiencies and your proficiency with thieves’ tools. Your proficiency bonus is doubled for any ability check you m ake that uses either of the chosen proficiencies.\nAt 6th level, you can choose two m ore of your proficiencies (in skills or with thieves’ tools) to gain this benefit."),
        ("Sneak Attack", "Beginning at 1st level, you know how to strike subtly and exploit a foe’s distraction. Once per turn, you can deal an extra 1d6 damage to one creature you hit with an attack if you have advantage on the attack roll. The attack must use a finesse or a ranged weapon.\nYou don’t need advantage on the attack roll if another enemy of the target is within 5 feet of it, that enemy isn’t incapacitated, and you don’t have disadvantage on the attack roll.\nThe amount of the extra damage increases as you gain levels in this class, as show n in the Sneak Attack column of the Rogue table."),
        ("Thieves' Cant", "During your rogue training you learned thieves’ cant, a secret mix of dialect, jargon, and code that allows you to hide messages in seemingly normal conversation. Only another creature that knows thieves’ cant understands such messages. It takes four times longer to convey such a message than it does to speak the same idea plainly.\nIn addition, you understand a set of secret signs and symbols used to convey short, simple messages, such as whether an area is dangerous or the territory of a thieves’ guild, whether loot is nearby, or whether the people in an area are easy marks or will provide a safe house for thieves on the run.")
        ]


#Sorcerer
class Sorcerer(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Sorcerer"
        self.goodabilities = ["cha", "con"]
        self.hitdie = 6
        self.proficiency = 2
        self.proficiencies = {
            "armor": [],
            "weapons": "Daggers, darts, slings, quarterstaffs, light crossbows".split(", "),
            "tools": [],
            "saving": ["con", "cha"],
            "skills": roll.sample("Arcana, Deception, Insight, Intimidation, Persuasion, Religion".split(", "), 2)
        }
        self.equipment = [
        c(["a light crossbow and 20 bolts", c(simpleweapons)]),
        c(["a component pouch", "an arcane focus"]),
        c(["a dungeoneer’s pack", "an explorer’s pack"]),
        "two daggers"
        ]
        self.spellcasting = {
        "cantrips": 4,
        "spellsknown": 2,
        "slots": {1: 2}
        }
        self.features = [
        ("Spellcasting", "Charisma is your spellcasting ability for your sorcerer spells, since the power of your magic relies on your ability to project your will into the world. You use your Charisma whenever a spell refers to your spellcasting ability. In addition, you use your Charisma modifier when setting the saving throw DC for a sorcerer spell you cast and when making an attack roll with one.\nSpell save DC = 8 + your proficiency bonus + your Charisma modifier\nSpell attack modifier = your proficiency bonus + your Charisma modifier\nSpellcasting Focus\nYou can use an arcane focus as a spellcasting focus for your sorcerer spells."),
        ("Sorcerous Origin", "Choose a sorcerous origin, which describes the source of your innate magical power. Your choice grants you features when you choose it at 1st level and again at 6th, 14th, and 18th level.\nYour Sorcerous Origin is: "+c(sorcererorgin)+".")
        ]


#Warlock
class Warlock(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Warlock"
        self.goodabilities = ["cha", "con"]
        self.hitdie = 8
        self.proficiency = 2
        self.proficiencies = {
            "armor": ["light armor"],
            "weapons": ["simple weapons"],
            "tools": [],
            "saving": ["wis", "cha"],
            "skills": roll.sample(" Arcana, Deception, History, Intimidation, Investigation, Nature, Religion".split(", "), 2)
        }
        self.equipment = [
        c(["a light crossbow and 20 bolts", c(simpleweapons)]),
        c(["a component pouch", "an arcane focus"]),
        c(["a scholar's pack", "a dungeoneer's pack"]),
        "leather armor",
        c(simpleweapons),
        "two daggers"
        ]
        self.spellcasting = {
        "cantrips": 2,
        "spellsknown": 2,
        "slots": {1: 1}
        }
        self.features = [
        ("Otherworldly Patron", "At 1st level, you have struck a bargain with an otherworldly being of your choice: the Archfey, the Fiend, or the Great Old One, each of which is detailed at the end of the class description. Your choice grants you features at 1st level and again at 6th, 10th, and 14th level."),
        ("Pact Magic", "Charisma is your spellcasting ability for your w arlock spells, so you use your Charisma whenever a spell refers to your spellcasting ability. In addition, you use your Charisma modifier when setting the saving throw DC for a warlock spell you cast and when making an attack roll with one.\nSpell save DC = 8 + your proficiency bonus + your Charisma modifier\nSpell attack modifier = your proficiency bonus + your Charisma modifier\nSpellcasting Focus\nYou can use an arcane focus as a spellcasting focus for your warlock spells.")
        ]


#Wizard
class Wizard(CharacterClass):
    def __init__(self):
        CharacterClass.__init__(self)
        self.name = "Wizard"
        self.goodabilities = ["int","con"]
        self.hitdie = 6
        self.proficiency = 2
        self.proficiencies = {
            "armor": [],
            "weapons": "Daggers, darts, slings, quarterstaffs, light crossbows".split(", "),
            "tools": [],
            "saving": ["int", "wis"],
            "skills": roll.sample("Arcana, History, Insight, Investigation, Medicine, Religion".split(", "), 2)
        }
        self.equipment = [
        c(["a quarterstaff", "a dagger"]),
        c(["a component pouch", "an arcane focus"]),
        c(["a scholar's pack", "a explorer's pack"]),
        "a spellbook"
        ]
        self.spellcasting = {
        "cantrips": 3,
        "slots": {1: 2}
        }
        self.features = [
        ("Spellcasting", "Intelligence is your spellcasting ability for your wizard spells, since you learn your spells through dedicated study and memorization. You use your Intelligence whenever a spell refers to your spellcasting ability. In addition, you use your Intelligence modifier when setting the saving throw DC for a wizard spell you cast and when making an attack roll with one.\nSpell save DC = 8 + your proficiency bonus + your Intelligence modifier\nSpell attack modifier = your proficiency bonus + your intelligence modifier\nRitual Casting\nYou can cast a wizard spell as a ritual if that spell has the ritual tag and you have the spell in your spellbook. You don't need to have the spell prepared.\nSpellcasting Focus\nYou can use an arcane focus (found in chapter 5) as a spellcasting focus for your wizard spells.\nLearning Spells of 1st Level and Higher\nEach time you gain a wizard level, you can add two wizard spells of your choice to your spellbook. Each of these spells must be of a level for which you have spell slots, as shown on the W izard table. On your adventures, you might find other spells that you can add to your spellbook."),
        ("Arcane Recovery", "You have learned to regain some of your magical energy by studying your spellbook. Once per day when you finish a short rest, you can choose expended spell slots to recover. The spell slots can have a combined level that is equal to or less than half your wizard level (rounded up), and none of the slots can be 6th level or higher.\nFor example, if you’re a 4th-level wizard, you can recover up to two levels worth of spell slots. You can recover either a 2nd-level spell slot or two 1st-level spell slots.")
        ]

classes = [Barbarian, Bard, Cleric, Druid, Fighter, Monk, Ranger, Rouge, Sorcerer, Warlock, Wizard]
