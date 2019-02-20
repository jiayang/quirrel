import csv
import random

CARDS = dict()
ICONICS = dict()
LEGENDARIES = dict()
MYTHICS = dict()
RARES = dict()
UNCOMMONS = dict()
COMMONS = dict()

types = {
    'iconic' : ICONICS,
    'legendary' : LEGENDARIES,
    'mythic' : MYTHICS,
    'rare' : RARES,
    'uncommon' : UNCOMMONS,
    'common' : COMMONS
}

with open('data/cards.csv') as f:
    r = csv.DictReader(f, delimiter=',')
    for val in r:
        val['name'].replace('_','\_')
        CARDS[int(val['id'].strip())] = val
        CARDS[val['name'].lower().strip()] = val
        types[val['rarity'].lower().strip()][int(val['id'].strip())] = val

def open_pack(pack):
    cards = []
    if pack == 'Wood':
        #4 commons
        #1 50% uncommon, 25% rare, 17% mythic, 6% legendary, 2% iconic
        for i in range(4):
            cards += [random.choice(list(COMMONS.keys()))]
        n = random.randint(1,100)
        if n > 98:
            cards += [random.choice(list(ICONICS.keys()))]
        elif n > 92:
            cards += [random.choice(list(LEGENDARIES.keys()))]
        elif n > 75:
            cards += [random.choice(list(MYTHICS.keys()))]
        elif n > 50:
            cards += [random.choice(list(RARES.keys()))]
        else:
            cards += [random.choice(list(UNCOMMONS.keys()))]
    if pack == 'Iron':
        #4 commons
        #2 uncommons
        #2 70% rare, 20% mythic, 8% legendary, 2% iconic
        for i in range(4):
            cards += [random.choice(list(COMMONS.keys()))]
        for i in range(2):
            cards += [random.choice(list(UNCOMMONS.keys()))]
        for i in range(2):
            n = random.randint(1,100)
            if n > 98:
                cards += [random.choice(list(ICONICS.keys()))]
            elif n > 90:
                cards += [random.choice(list(LEGENDARIES.keys()))]
            elif n > 70:
                cards += [random.choice(list(MYTHICS.keys()))]
            else:
                cards += [random.choice(list(RARES.keys()))]
    if pack == 'Gold':
        #5 uncommon
        #2 rare
        #3 80% mythic, 15% legendary, 5% iconic
        for i in range(5):
            cards += [random.choice(list(UNCOMMONS.keys()))]
        for i in range(2):
            cards += [random.choice(list(RARES.keys()))]
        for i in range(3):
            n = random.randint(1,100)
            if n > 95:
                cards += [random.choice(list(ICONICS.keys()))]
            elif n > 80:
                cards += [random.choice(list(LEGENDARIES.keys()))]
            else:
                cards += [random.choice(list(MYTHICS.keys()))]
    return [CARDS[card]['id'] for card in cards]





def format(lst):
    new_lst = [format_string(CARDS[int(i)]) for i in lst]
    return new_lst

def format_string(item):
    s = f"{item['name']} | {item['rarity']} | {item['kit']}"
    return s

def name(id):
    if int(id) not in CARDS:
        return None
    return CARDS[int(id)]['name']

def get_card(name):
    if name.lower().strip() not in CARDS:
        return None
    return CARDS[name.lower().strip()]

def setup(bot):
    pass
