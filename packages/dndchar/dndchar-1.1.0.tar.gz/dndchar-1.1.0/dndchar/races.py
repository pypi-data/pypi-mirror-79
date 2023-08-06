from dndchar.data import languages, abilityscores
from dndchar.util import Roller
roll = Roller()
# Stores race attributes
class Race:
    def __init__(self):
        # Sets defualt values for all the race attributes
        self.name = ""
        # Score modifiers
        self.scores = {
        "str": 0,
        "dex": 0,
        "con": 0,
        "int": 0,
        "wis": 0,
        "cha": 0
        }
        # Age (A low and a high value)
        self.age = []
        # Alignment (A dict of probabilities)
        self.align = {
            "deeds": ["netural"], # Good or Evil
            "order": ["netural"]  # Lawful or Chaotic
        }
        # Size
        self.size = "medium"
        # Speed
        self.speed = 0
        # Languages
        self.lang = ["common"]
        # Names
        self.names = {
            "male": "".split(", "),
            "female": "".split(", "),
            "family": "".split(", ")
        }
        # Subraaces
        self.subraces = []
        # Other Features
        self.features = []
    def __str__(self):
        return self.name

# Pass a race and add subrace attributes
class Subrace:
    def __init__(self, race):
        self.name = race.name
        # Score modifiers
        self.scores = {
        "str": race.scores["str"] + 0,
        "dex": race.scores["dex"] + 0,
        "con": race.scores["con"] + 0,
        "int": race.scores["int"] + 0,
        "wis": race.scores["wis"] + 0,
        "cha": race.scores["cha"] + 0
        }
        # Age
        self.age = race.age
        # Alignment
        self.align = race.align
        # Names
        self.names = race.names
        # Size
        self.size = race.size
        # Speed
        self.speed = race.speed
        # Languages
        self.lang = race.lang + []
        # Other Features
        self.features = race.features + []
    def __str__(self):
        return self.name


# Actual Races:
#Dwarf
class Dwarf(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Dwarf"
        self.scores["con"] = 2
        self.age = [20, 300]
        self.align = {
            "deeds": ["good", "netural", "good", "netural", "good"],
            "order": ["lawful", "lawful", "lawful", "netural"]
        }
        self.size = "medium"
        self.speed = 25
        self.lang = ["common","dwarvish"]
        self.names = {
            "male": "Adrik, Alberich, Baern, Barendd, Brottor, Bruenor, Dain, Darrak, Delg, Eberk, Einkil, Fargrim, Flint, Gardain, Harbek, Kildrak, Morgran, Orsik, Oskar, Rangrim, Rurik, Taklinn, Thoradin, Thorin, Tordek, Traubon, Travok, Ulfgar, Veit, Vondal".split(", "),
            "female": "Amber, Artin, Audhild, Bardryn, Dagnal, Diesa, Eldeth, Falkrunn, Finellen, Gunnloda, Gurdis, Helja, Hlin, Kathra, Kristryd, Ilde, Liftrasa, Mardred, Riswynn, Sannl, Torbera, Torgga, Vistra".split(", "),
            "family": "Balderk, Battlehammer, Brawnanvil, Dankil, Fireforge, Frostbeard, Gorunn, Holderhek, Ironfist, Loderr, Lutgehr, Rumnaheim, Strakeln, Torunn, Ungart".split(", ")
        }
        self.subraces = [self.HillDwarf, self.MountainDwarf]
        self.features = [
        ("Darkvision", "Accustomed to life underground, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it w ere dim light. You can’t discern color in darkness, only shades of gray."),
        ("Dwarven Resilience", "You have advantage on saving throws against poison, and you have resistance against poison damage"),
        ("Dwarven Combat Training", "You have proficiency with the battleaxe, handaxe, throwing hammer, and warhammer."),
        ("Tool Proficiency", "You gain proficiency with the artisan’s tools of your choice: smith’s tools, brewer’s supplies, or mason’s tools."),
        ("Stonecunning", "Whenever you make an Intelligence (History) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check, instead of your normal proficiency bonus.")
        ]
    class HillDwarf(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Hill " + race.name
            self.scores["wis"] += 1
            self.features = race.features + [
            ("Dwarven Toughness", "Your hit point maximum increases by 1, and it increases by 1 every time you gain a level.")
            ]
    class MountainDwarf(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Mountain " + race.name
            self.scores["str"] += 2
            self.features = race.features + [
            ("Dwarven Armor Training", "You have proficiency with light and medium armor.")
            ]


#Elf
class Elf(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Elf"
        self.scores["dex"] = 2
        self.age = [80, 730]
        self.align = {
            "deeds": ["good", "good", "netural"],
            "order": ["chaotic", "chaotic", "chaotic", "netural"]
        }
        self.size = "medium"
        self.speed = 30
        self.lang = ["common","elvish"]
        self.names = {
            "male": "Adran, Aelar, Aramil, Arannis, Aust, Beiro, Berrian, Carric , Enialis, Erdan, Erevan, Galinndan, Hadarai, Heian, Himo, Immeral, Ivellios, Laucian, Mindartis, Paelias, Peren, Quarion, Riardon, Rolen, Soveliss, Thamior, Tharivol, Theren, Varis".split(", "),
            "female": "Adrie, Althaea, Anastrianna, Andraste, Antinua, Bethrynna, Birel, Caelynn, Drusilia, Enna, Felosial, Ielenia, Jelenneth, Keyleth, Leshanna, Lia, Meriele, M ialee, Naivara, Quelenna, Quillathe, Sariel, Shanairra, Shava, Silaqui, Theirastra, Thia, Vadania, Valanthe, Xanaphia".split(", "),
            "family": "Amakiir (Gemflower), Amastacia (Starflower), Galanodel (Moonwhisper), Holimion (Diamonddew), Ilphelkiir (Gemblossom), Liadon (Silverfrond), Meliamne (Oakenheel), Nai'lo (Nightbreeze), Siannodel (Moonbrook), Xiloscient (Goldpetal)".split(", ")
        }
        self.subraces = [self.HighElf, self.WoodElf, self.DarkElf]
        self.features = [
        ("Darkvision", "Accustom ed to twilit forests and the night sky, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can’t discern color in darkness, only shades of gray."),
        ("Keen Senses", "You have proficiency in the Perception skill."),
        ("Fey Ancestry", "You have advantage on saving throws against being charmed, and magic can’t put you to sleep."),
        ("Trance", "Elves don’t need to sleep. Instead, they meditate deeply, remaining semiconscious, for 4 hours a day. (The Common word for such meditation is “trance.”) While meditating, you can dream after a fashion; such dreams are actually mental exercises that have become reflexive through years of practice. After resting in this way, you gain the same benefit that a human does from 8 hours of sleep.")
        ]
    class HighElf(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "High " + race.name
            self.scores["int"] += 1
            self.lang = self.lang + [roll.choice(languages)]
            self.features = self.features + [
            ("Elf Weapon Training", "You have proficiency with the longsword, shortsword, shortbow, and longbow."),
            ("Cantrip", "You know one cantrip of your choice from the wizard spell list. Intelligence is your spellcasting ability for it."),
            ]
    class WoodElf(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Wood " + race.name
            self.scores["wis"] += 1
            self.speed = 35
            self.features = self.features + [
            ("Elf Weapon Training", "You have proficiency with the longsword, shortsword, shortbow, and longbow."),
            ("Mask of the Wild", "You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena.")
            ]
    class DarkElf(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Dark " + race.name + " (Drow)"
            self.scores["cha"] += 1
            self.align = {
                "deeds": ["evil", "evil", "netural"],
                "order": self.align["order"]
            }
            self.features = self.features + [
            ("Superior Darkvision", "Your darkvision has a radius of 120 feet."),
            ("Sunlight Sensitivity", "You have disadvantage on attack rolls and on W isdom (Perception) checks that rely on sight when you, the target of your attack, or whatever you are trying to perceive is in direct sunlight."),
            ("Drow Magic", "You know the dancing lights cantrip. When you reach 3rd level, you can cast the faerie fire spell once per day. When you reach 5th level, you can also cast the darkness spell once per day. Charisma is your spellcasting ability for these spells."),
            ("Drow Weapon Training", "You have proficiency with rapiers, shortswords, and hand crossbows.")
            ]


#Halfling
class Halfling(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Halfling"
        self.scores["dex"] = 2
        self.age = [20, 130]
        self.align = {
            "deeds": ["good","good","good","good","netural"],
            "order": ["lawful", "lawful", "netural"]
        }
        self.size = "small"
        self.speed = 25
        self.lang = ["common", "halfling"]
        self.names = {
            "male": "Alton, Ander, Cade, Corrin, Eldon, Errich, Finnan, Garret, Lindal, Lyle, Merric, Milo, Osborn, Perrin, Reed, Roscoe, Wellby".split(", "),
            "female": "Andry, Bree, Callie, Cora, Euphemia, Jillian, Kithri, Lavinia, Lidda, Merla, Nedda, Paela, Portia, Seraphina, Shaena, Trym, Vani, Verna".split(", "),
            "family": "Brushgather, Goodbarrel, Greenbottle, High-hill, Hilltopple, Leagallow, Tealeaf, Thorngage, Tosscobble, Underbough".split(", ")
        }
        self.subraces = [self.LightfootHalfling, self.StoutHalfling]
        self.features = [
        ("Lucky", "When you roll a 1 on an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll."),
        ("Brave", "You have advantage on saving throws against being frightened."),
        ("Halfling Nimbleness", "You can move through the space of any creature that is of a size larger than yours.")
        ]
    class LightfootHalfling(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Lightfoot " + race.name
            self.scores["cha"] += 1
            self.features = self.features + [
            ("Naturally Stealthy", "You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.")
            ]
    class StoutHalfling(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Stout " + race.name
            self.scores["con"] += 1
            self.features = self.features + [
            ("Stout Resilience", "You have advantage on saving throws against poison, and you have resistance against poison damage.")
            ]


#Human
class Human(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Human"
        self.scores = {
        "str": 1,
        "dex": 1,
        "con": 1,
        "int": 1,
        "wis": 1,
        "cha": 1
        }
        self.age = [20,60]
        self.align = {
            "deeds": ["good", "good", "netural", "netural", "evil"],
            "order": ["lawful", "netural", "chaotic"]
        }
        self.size = "medium"
        self.speed = 30
        self.lang = ["common", roll.choice(languages)]
        self.names = {
            "male": "Aseir, Bardeid, Haseid, Khemed, Mehmen, Sudeiman, Zasheir, Darvin, Dorn, Evendur, Gorstag, Grim, Helm, Malark, Morn, Randal, Stedd, Bor, Fodel, Glar, Grigor, Igan, Ivor, Kosef, Mival, Orel, Pavel, Sergor, Ander, Blath, Bran, Frath, Geth, Lander, Luth, Malcer, Stor, Taman, Urth, Aoth, Bareris, Ehput-Ki, Kethoth, Mumed, Ramas, So-Kehur, Thazar-De, Urhur, Borivik, Faurgar, Jandar, Kanithar, Madislak, Ralmevik, Shaumar, Vladislak, An, Chen, Chi, Fai, Jiang, Jun, Lian, Long, Meng, On, Shan, Shui, Wen, Anton, Diero, Marcon, Pieron, Rimardo, Romero, Salazar, Umbero".split(", "),
            "female": "Atala, Ceidil, Hama, Jasmal, Meilil, Seipora, Yasheira, Zasheida, Arveene, Esvele, Jhessail, Kerri, Lureene, Miri, Rowan, Shandri, Tessele, Alethra, Kara, Katernin, Mara, Natali, Olma, Tana, Zora, Amafrey, Betha, Cefrey, Kethra, Mara, Olga, Silifrey, Westra, Arizima, Chathi, Nephis, Nulara, Murithi, Sefris, Thola, Umara, Zolis, Fyevarra, Hulmarra, Immith, Imzel, Navarra, Shevarra, Yuldra, Bai, Chao, Jia, Lei, Mei, Qiao, Shui, Tai, Balama, Dona, Faila, Jalana, Luisa, Marta, Quara, Selise, Vonda".split(", "),
            "family": "Basha, Dumein, Jassan, Khalid, Mostana, Pashar, Rein, Am blecrown, Buckman, Dundragon, Evenwood, Greycastle, Tallstag, Bersk, Chernin, Dotsk, Kulenov, Marsk, Nemetsk, Shemov, Starag, Brightwood, Helder, Hornraven, Lackman, Stormwind, Windrivver, Ankhalab, Anskuld, Fezim, Hahpet, Nathandem, Sepret, Uuthrakt, Chergoba, Dyernina, Iltazyara, Murnyethara, Stayanoga, Ulmokina, Chien, Huang, Kao, Kung, Lao, Ling, Mei, Pin, Shin, Sum, Tan, Wan, Agosto, Astorio, Calabra, Domine, Falone, Marivaldi, Pisacar, Ramondo".split(", ")
        }
        self.subraces = []
        self.features = []



#Dragonborn
class Dragonborn(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Dragonborn"
        self.names = {
            "male": "Arjhan, Balasar, Bharash, Donaar, Ghesh. Heskan, Kriv, Medrash, Mehen, Nadarr, Pandjed, Patrin, Rhogar, Shamash, Shedinn, Tarhun, Torinn".split(", "),
            "female": "Akra, Biri, Daar, Farideh, Harann, Flavilar, Jheri, Kava, Korinn, Mishann, Nala, Perra, Raiann, Sora, Surina, Thava, Uadjit".split(", "),
            "family": "Clethtinthiallor, Daardendrian, Delmirev, Drachedandion, Fenkenkabradon, Kepeshkmolik, Kerrhylon, Kimbatuul, Linxakasendalor, Myastan, Nemmonis, Norixius, Ophinshtalajiir, Prexijandilin, Shestendeliath, Turnuroth, Verthisathurgiesh, Yarjerit".split(", ")
        }
        self.scores["str"] = 2
        self.scores["cha"] = 1
        self.age = [9, 55]
        self.align = {
            "deeds": ["good","good","good","evil"],
            "order": ["lawful","chaotic"]
        }
        self.size = "medium"
        self.speed = 30
        self.lang = ["common", "draconic"]
        self.subraces = []
        self.features = [
        ("Draconic Ancestry", "You have draconic ancestry. Choose one type of dragon from the Draconic Ancestry table. Your breath weapon and damage resistance are determined by the dragon type, as shown in the table."),
        ("Breath Weapon", "You can use your action to exhale destructive energy. Your draconic ancestry determines the size, shape, and damage type of the exhalation. When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level.\nAfter you use your breath weapon, you can’t use it again until you com plete a short or long rest."),
        ("Damage Resistance", "You have resistance to the damage type associated with your draconic ancestry.")
        ]


#Gnome
class Gnome(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Gnome"
        self.names = {
            "male": "Alston, Alvyn, Boddynock, Brocc, Burgell, Dimble, Eldon, Erky, Fonkin, Frug, Gerbo, Gimble, Glim, Jebeddo, Kellen, Nam foodle, Orryn, Roondar, Seebo, Sindri, Warryn, Wrenn, Zook".split(", "),
            "female": "Bimpnottin, Breena, Caramip, Carlin, Donella, Duvamil, Ella, Ellyjobell, Ellywick, Lilli, Loopmottin, Lorilla, Mardnab, Nissa, Nyx, Oda, Orla, Roywyn, Shamil, Tana, Waywocket, Zanna".split(", "),
            "family": "Beren, Daergel, Folkor, Garrick, Nackle, Murnig, Ningel, Raulnor, Scheppen, Tim bers, Turen".split(", "),
            "nicknames": "Aleslosh, Ashhearth, Badger, Cloak, Doublelock, Filchbatter, Fnipper, Ku, Nim, Oneshoe, Pock, Sparklegem, Stumbleduck".split(", ")
        }
        self.scores["int"] = 2
        self.age = [20, 350]
        self.align = {
            "deeds": ["good", "good", "good", "good", "netural"],
            "order": ["chaotic", "chaotic", "netural"]
        }
        self.size = "small"
        self.speed = 25
        self.lang = ["common", "gnomish"]
        self.subraces = [self.ForestGnome, self.RockGnome]
        self.features = [
        ("Gnome Cunning", "You have advantage on all Intelligence, Wisdom, and Charisma saving throws against magic.")
        ]
    class ForestGnome(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Forest " + race.name
            self.scores["dex"] += 1
            self.features = [
            ("Natural Illusionist", "You know the minor illusion cantrip. Intelligence is your spellcasting ability for it."),
            ("Speak with Small Beasts", "Through sounds and gestures, you can communicate simple ideas with Small or smaller beasts. Forest gnomes love animals and often keep squirrels, badgers, rabbits, m oles, woodpeckers, and other creatures as beloved pets.")
            ]
    class RockGnome(Subrace):
        def __init__(self, race):
            Subrace.__init__(self, race)
            self.name = "Rock " + race.name
            self.scores["con"] += 1
            self.features = [
            ("Artificer’s Lore", "Whenever you make an Intelligence (History) check related to magic items, alchemical objects, or technological devices, you can add twice your proficiency bonus, instead of any proficiency bonus you normally apply."),
            ("Tinker", "You have proficiency with artisan’s tools (tinker’s tools). Using those tools, you can spend 1 hour and 10 gp worth of materials to construct a Tiny clockwork device (AC 5, 1 hp). The device ceases to function after 24 hours (unless you spend 1 hour repairing it to keep the device functioning), or when you use your action to dismantle it; at that time, you can reclaim the materials used to create it. You can have up to three such devices active at a time. When you create a device, choose one of the following options:\nClockwork Toy. This toy is a clockwork animal, monster, or person, such as a frog, mouse, bird, dragon, or soldier. When placed on the ground, the toy m oves 5 feet across the ground on each of your turns in a random direction. It makes noises as appropriate to the creature it represents.\nFire Starter. The device produces a miniature flame, which you can use to light a candle, torch, or campfire. Using the device requires your action.\nMusic Box. When opened, this music box plays a single song at a moderate volume. The box stops playing when it reaches the song’s end or when it is closed."),
            ]


#Half-Elf
class HalfElf(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Half Elf"
        self.scores["cha"] = 2
        for i in range(2):
            a = abilityscores.copy()
            a.remove("cha")
            self.scores[roll.choice(a)] += 1
        self.age = [18, 160]
        self.align = {
            "deeds": ["good","good","netural","netural","evil"],
            "order": ["chaotic","chaotic","chaotic","chaotic","chaotic","netural"]
        }
        self.size = "medium"
        self.speed = 30
        self.lang = ["common", roll.choice(languages)]
        self.names = {
            "male": "Aseir, Bardeid, Haseid, Khemed, Mehmen, Sudeiman, Zasheir, Darvin, Dorn, Evendur, Gorstag, Grim, Helm, Malark, Morn, Randal, Stedd, Bor, Fodel, Glar, Grigor, Igan, Ivor, Kosef, Mival, Orel, Pavel, Sergor, Ander, Blath, Bran, Frath, Geth, Lander, Luth, Malcer, Stor, Taman, Urth, Aoth, Bareris, Ehput-Ki, Kethoth, Mumed, Ramas, So-Kehur, Thazar-De, Urhur, Borivik, Faurgar, Jandar, Kanithar, Madislak, Ralmevik, Shaumar, Vladislak, An, Chen, Chi, Fai, Jiang, Jun, Lian, Long, Meng, On, Shan, Shui, Wen, Anton, Diero, Marcon, Pieron, Rimardo, Romero, Salazar, Umbero, Adran, Aelar, Aramil, Arannis, Aust, Beiro, Berrian, Carric , Enialis, Erdan, Erevan, Galinndan, Hadarai, Heian, Himo, Immeral, Ivellios, Laucian, Mindartis, Paelias, Peren, Quarion, Riardon, Rolen, Soveliss, Thamior, Tharivol, Theren, Varis".split(", "),
            "female": "Atala, Ceidil, Hama, Jasmal, Meilil, Seipora, Yasheira, Zasheida, Arveene, Esvele, Jhessail, Kerri, Lureene, Miri, Rowan, Shandri, Tessele, Alethra, Kara, Katernin, Mara, Natali, Olma, Tana, Zora, Amafrey, Betha, Cefrey, Kethra, Mara, Olga, Silifrey, Westra, Arizima, Chathi, Nephis, Nulara, Murithi, Sefris, Thola, Umara, Zolis, Fyevarra, Hulmarra, Immith, Imzel, Navarra, Shevarra, Yuldra, Bai, Chao, Jia, Lei, Mei, Qiao, Shui, Tai, Balama, Dona, Faila, Jalana, Luisa, Marta, Quara, Selise, Vonda, Adrie, Althaea, Anastrianna, Andraste, Antinua, Bethrynna, Birel, Caelynn, Drusilia, Enna, Felosial, Ielenia, Jelenneth, Keyleth, Leshanna, Lia, Meriele, M ialee, Naivara, Quelenna, Quillathe, Sariel, Shanairra, Shava, Silaqui, Theirastra, Thia, Vadania, Valanthe, Xanaphia".split(", "),
            "family": "Amakiir (Gemflower), Amastacia (Starflower), Galanodel (Moonwhisper), Holimion (Diamonddew), Ilphelkiir (Gemblossom), Liadon (Silverfrond), Meliamne (Oakenheel), Nai'lo (Nightbreeze), Siannodel (Moonbrook), Xiloscient (Goldpetal), Basha, Dumein, Jassan, Khalid, Mostana, Pashar, Rein, Am blecrown, Buckman, Dundragon, Evenwood, Greycastle, Tallstag, Bersk, Chernin, Dotsk, Kulenov, Marsk, Nemetsk, Shemov, Starag, Brightwood, Helder, Hornraven, Lackman, Stormwind, Windrivver, Ankhalab, Anskuld, Fezim, Hahpet, Nathandem, Sepret, Uuthrakt, Chergoba, Dyernina, Iltazyara, Murnyethara, Stayanoga, Ulmokina, Chien, Huang, Kao, Kung, Lao, Ling, Mei, Pin, Shin, Sum, Tan, Wan, Agosto, Astorio, Calabra, Domine, Falone, Marivaldi, Pisacar, Ramondo".split(", ")
        }
        self.subraces = []
        self.features = [
        ("Darkvision", "Thanks to your elf blood, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can’t discern color in darkness, only shades of gray."),
        ("Fey Ancestry", "You have advantage on saving throws against being charmed, and magic can’t put you to sleep."),
        ("Skill Versatility", "You gain proficiency in two skills of your choice.")
        ]


#Half-Orc
class HalfOrc(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Half Orc"
        self.scores["str"] = 2
        self.scores["con"] = 1
        self.age = [13, 65]
        self.align = {
            "deeds": ["good","netural","netural","evil"],
            "order": ["chaotic","chaotic","netural"]
        }
        self.size = "medium"
        self.speed = 30
        self.lang = ["common", "orc"]
        self.names = {
            "male": "Dench, Feng, Gell, Henk, Holg, Imsh, Keth, Krusk, Mhurren, Ront, Shump, Thokk".split(", "),
            "female": "Baggi, Emen, Engong, Kansif, Myev, Neega, Ovak, Ownka, Shautha, Sutha, Vola, Volen, Yevelda".split(", "),
            "family": "".split(", ")
        }
        self.subraces = []
        self.features = [
        ("Darkvision","Thanks to your orc blood, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can't discern color in darkness, only shades of gray."),
        ("Menacing", "You gain proficiency in the Intimidation skill."),
        ("Relentless Endurance", "When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead. You can’t use this feature again until you finish a long rest."),
        ("Savage Attacks", "When you score a critical hit with a melee weapon attack, you can roll one of the weapon’s damage dice one additional time and add it to the extra damage of the critical hit.")
        ]


#Tiefling
class Tiefling(Race):
    def __init__(self):
        Race.__init__(self)
        self.name = "Tiefling"
        self.scores["int"] = 1
        self.scores["cha"] = 2
        self.age = [20, 70]
        self.align = {
            "deeds": ["good", "netural","netural","evil"],
            "order": ["chaotic","chaotic","netural","lawful"]
        }
        self.size = "medium"
        self.speed = 30
        self.lang = ["common","infernal"]
        self.names = {
            "male": roll.choice(["Akmenos, Amnon, Barakas, Damakos, Ekemon, Iados, Kairon, Leucis, Melech, Mordai, Morthos, Pelaios, Skamos, Therai".split(", "), "Art, Carrion, Chant, Creed, Despair, Excellence, Fear, Glory, Hope, Ideal, Music, Nowhere, Open, Poetry, Quest, Random, Reverence, Sorrow, Temerity, Torment, Weary".split(", ")]),
            "female": roll.choice(["Akta, Anakis, Bryseis, Criella, Damaia, Ea, Kallista, Lerissa, Makaria, Nemeia, Orianna, Phelaia, Rieta".split(", "), "Art, Carrion, Chant, Creed, Despair, Excellence, Fear, Glory, Hope, Ideal, Music, Nowhere, Open, Poetry, Quest, Random, Reverence, Sorrow, Temerity, Torment, Weary".split(", ")]),
            "family": []
        }
        self.subraces = []
        self.features = [
        ("Darkvision", "Thanks to your infernal heritage, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can’t discern color in darkness, only shades of gray."),
        ("Hellish Resistance", "You have resistance to fire damage."),
        ("Infernal Legacy", "You know the thaumaturgy cantrip. Once you reach 3rd level, you can cast the hellish rebuke spell once per day as a 2nd-level spell. Once you reach 5th level, you can also cast the darkness spell once per day. Charisma is your spellcasting ability for these spells.")
        ]


races = [Dwarf, Elf, Halfling, Human, Dragonborn, Gnome, HalfElf, Tiefling]
