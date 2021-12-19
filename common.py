import re, requests

ICONS = {
    3: 'Bypass barriers Act',
    14: 'Agility Up Auto Skill',
    178: 'Seal Act',
    10005: 'Removal Immunity Act',
    192: 'Brilliance Recovery Reduction Act',
    158: 'Poison Damage Act',
    182: 'Burn damage Act',
    184: 'Stun damage Up Act',
    15: 'Agility Down Act',
    186: 'Confusion Damage Act',
    188: 'Freeze damage Act',
    189: 'Blindness Damage Act',
    194: 'Resilience Act',
    195: 'Normal-type Damage Act',
    196: 'Special-type Damage Act',
    197: 'Remove Exit Act',
    16: 'Accuracy Rate Up Act',
    17: 'Accuracy Rate Down Act',
    18: 'Evasion Rate Up Act',
    19: 'Evasion Rate Down Act',
    20: 'Dexterity up Act',
    21: 'Dexterity down Act',
    22: 'Critical Up Act',
    23: 'Critical down Act',
    5: 'Low HP Act',
    26: 'Negate Effects Resistance',
    28: 'HP Regen Act',
    29: 'Brilliance Auto Skill',
    30: 'Normal Barrier Act',
    31: 'Special Barrier Act',
    32: 'Reflect Normal Damage Act',
    33: 'Reflect Special Damage Act',
    34: 'Evasion Act',
    35: 'Perfect Aim Act',
    36: 'Fortitude Act',
    6: 'HP Recovery Act',
    39: 'Effective Element Damage Auto Skill',
    40: 'Climax Act Power Auto Skill',
    44: 'Absorb Act',
    45: 'Counter Heal Act',
    54: 'Poison Act',
    55: 'Burn Act',
    56: 'Provoke Act',
    57: 'Stun Act',
    58: 'Sleep Act',
    59: 'Confusion Act',
    8: 'Act Power up Auto Skill',
    60: 'Stop Act',
    61: 'Freeze Act',
    62: 'Blindness Act',
    65: 'HP Recovery Reduction Act',
    10: 'Defense Up Auto Skill',
    9: 'Act Power Down Act',
    89: 'Brilliance recovery Act',
    91: 'Poison Resistance Auto Skill',
    92: 'Burn Resistance Act',
    93: 'Provoke Resistance Auto Skill',
    94: 'Stun Resistance Auto Skill',
    95: 'Sleep Resistance Auto Skill',
    96: 'Confusion Resistance Auto Skill',
    97: 'Stop Resistance Auto Skill',
    98: 'Freeze Resistance Auto Skill',
    99: 'Blindness Resistance Auto Skill',
    10006: 'Stat buff removal Act',
    11: 'Defense Down Act',
    10007: 'Bonus damage Auto Skill',
    12: 'SpDef up Act',
    150: 'Mark Act',
    13: 'SpDef Down Act',
    151: 'Flip Act',
    152: 'Aggro Act',
    153: 'Aggro Immunity Auto Skill',
    155: 'Exit Evasion Act',
    156: 'Invincible Act',
    157: 'AP Down Act',
    173: 'AP Up act',
    175: 'Mark Resistance Auto Skill',
    1: 'Front enemy damage Act',
    1000: 'Light of Courage Effect',
    10001: 'Enemy group Act',
    10002: 'High Damage Act',
    1001: 'We Are on the Stage (Flower) Effect',
    1002: 'We Are on the Stage (Wind) Effect',
    1003: 'We Are on the Stage (Snow) Effect',
    1004: 'We Are on the Stage (Moon) Effect',
    1005: 'We Are on the Stage (Space) Effect',
    1006: 'We Are on the Stage (Cloud) Effect',
    1007: 'Sunset Tune Act',
    1008: 'Shadow Stupor Act',
    1009: 'Lightning Shade Act',
    1010: 'Ironclad Guard Act',
    1011: 'Boldness Act',
    1012: 'Thunder Effect',
    1013: 'Winning Determination Act',
    1014: 'Concentration (Space) Effect',
    1015: 'Concentration (Wind) Effect',
    1016: 'Concentration (Snow) Effect',
    1017: 'Tears or Mist Act',
    1018: "God of War's Protection Act",
    1019: 'Wild Hope Act',
    1020: 'Roaring Fire Act',
    1021: 'Angelic Smile Act',
    1022: 'Self Trapping Act',
    1023: 'Disaster Hail Act',
    1024: "Death's Kiss Act",
    1025: 'Tragic Music Act',
    111: 'Damage Dealt Up Act',
    114: 'Damage Received Down Act',
    159: 'Seisho Auto Skill A',
    160: 'Rinmeikan Auto Skill A',
    161: 'Frontier Auto Skill A',
    162: 'Siegfeld Auto Skill A',
    163: 'Seisho Auto Skill D',
    164: 'Rinmeikan Auto Skill D',
    165: 'Frontier Auto Skill D',
    166: 'Siegfeld Auto Skill D',
    167: 'Front Position Unit Skill A',
    168: 'Middle Position Unit Skill A',
    169: 'Back Position Unit Skill A',
    170: 'Front Position Unit Skill D',
    171: 'Middle Position Unit Skill D',
    172: 'Back Position Unit Skill D',
    174: 'Stat immunity Act',
    198: 'Perfect Aim High Damage Act',
    199: 'Continuous Damage Immunity Act',
    2: 'Bypass Defense Act',
    10003: '10003 idk its green with kira swirling',
    10004: '10004 idk its green with a large kira and green wings',
    200: 'Flower Defense Down Act',
    201: 'Wind Defense Down Act',
    202: 'Snow Defense Down Act',
    203: 'Moon Defense Down Act',
    204: 'Space Defense Down Act',
    205: 'Cloud Defense Down Act',
    206: 'Dream Defense Down Act',
    207: 'Flower Damage Down Act',
    208: 'Wind Damage Down Act',
    209: 'Snow Damage Down Act',
    210: 'Moon Damage Down Act',
    211: 'Space Damage Down Act',
    212: 'Cloud Damage Down Act',
    213: 'Dream Damage Down Act',
    214: 'Seiran Unit Skill A',
    215: 'Seiran Unit Skill D',
    216: 'Normal Act Type Unit Skill',
    217: 'Special Act Type Unit Skill',
    218: 'Normal Act Type Unit Skill D',
    219: 'Special Act Type Unit Skill D',
    220: 'Climax Act Power Down Act',
    221: 'Lovesickness Act',
    222: 'Brilliance reduction Act',
    223: 'HP Up Auto Skill',
    224: 'HP Down Auto Skill',
    225: 'Self Unit Skill A',
    226: 'Self Unit Skill HP',
    227: '227 idk three explosions with a ring of explosions',
    228: 'Revive Act',
    229: 'Seisho Bonus Damage Act',
    230: 'Rinmeikan Bonus Damage Act',
    231: 'Frontier Bonus Damage Act',
    232: 'Siegfeld Bonus Damage Act',
    233: 'Seiran Bonus Damage Act',
    234: 'Nightmare Act',
    235: 'Positive Effects Immunity Act',
    236: 'Daze Act',
    237: 'Impudence Act',
    238: 'Hope Act',
    239: 'Lovesickness Bonus Damage Act',
    24: '24 idk wow what the hell orange heart with plus',
    240: 'Weak Spot Act',
    25: '25 idk purple heart minus',
    27: '27 idk opposite of NER',
    41: '41 idk shield explosion',
    53: '53 idk damage but invincible',
    66: 'Flower element Unit Skill D',
    67: 'Wind element Unit Skill D',
    68: 'Snow element Unit Skill D',
    69: 'Moon Element Unit Skill D',
    70: 'Space element Unit Skill D',
    71: 'Cloud Element Unit Skill D',
    72: 'Dream Element Unit Skill D',
    73: 'Flower element Unit Skill A',
    74: 'Wind element Unit Skill A',
    75: 'Snow element Unit Skill A',
    76: 'Moon Element Unit Skill',
    77: 'Space element Unit Skill',
    78: 'Cloud element Unit Skill A',
    79: 'Dream Element Unit Skill A',
}

NAMES = { 
    101: "Karen Aijo" ,
    102: "Hikari Kagura",
    103: "Mahiru Tsuyuzaki",
    104: "Claudine Saijo",
    105: "Maya Tendo",
    106: "Junna Hoshimi",
    107: "Nana Daiba",
    108: "Futaba Isurugi",
    109: "Kaoruko Hanayagi",
    201: "Tamao Tomoe",
    202: "Ichie Otonashi",
    203: "Fumi Yumeoji",
    204: "Rui Akikaze",
    205: "Yuyuko Tanaka",
    301: "Aruru Otsuki",
    302: "Misora Kano",
    303: "Lalafin Nonomiya",
    304: "Tsukasa Ebisu",
    305: "Shizuha Kocho",
    401: "Akira Yukishiro",
    402: "Michiru Otori",
    403: "Liu Mei Fan",
    404: "Shiori Yumeoji",
    405: "Yachiyo Tsuruhime",
    501: "Koharu Yanagi",
    502: "Suzu Minase",
    503: "Hisame Honami",
    802: "Elle Nishino",
    803: "Andrew"
}

SCHOOLS = {
    1: "Seisho Music Academy",
    2: "Rinmeikan Girls School",
    3: "Frontier School of Arts",
    4: "Siegfeld Institute of Music",
    5: "Seiran General Art Institute"
}

ATTR = {
    1: "Flower",
    2: "Wind",
    3: "Snow",
    4: "Moon",
    5: "Space",
    6: "Cloud",
    7: "Dream"
}

TYPE = {
    1: "Normal",
    2: "Special"
}

RARITY = {
    2: "Two",
    3: "Three",
    4: "Four"
}

GACHA = {
    "lim": "Premium",
    "bf": "Brilliance Fest",
    "season": "Season"
}

def get_json(url):
    res = requests.get(url).json()
    return res

def get_story(code: str):
    return get_json("https://karth.top/api/adventure/ww/" + code + ".json")

def get_chara_names():
    return get_json("https://karth.top/api/adventure_chara_name.json")

def get_dress(code: str):
    return get_json("https://karth.top/api/dress/" + code + ".json")

def write_line(filename, line: str):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(line + '\n')

def download_img(filename, code, img_type):
    url = "https://cdn.starira.xyz/api/assets/dlc/res/" + img_type + "/cg/" + code + "/image.png"
    img_data = requests.get(url).content
    with open(f'{filename}', 'wb') as handler:
        handler.write(img_data)

def is_naming_limit(name):
    match = re.search(r'\[.*\]', name)
    return match is not None

class Skill:
    iconID = ""
    desc = ""

    def __init__(self, iconID, desc):
        self.iconID = iconID
        self.desc = self.__format_desc(desc)

    def __format_desc(self, desc):
        result = ""
        result = re.sub(r' \[(\d+)/\d+\]\% ', lambda m : m.group(1) + "%", desc)
        result = re.sub(r' \[(\d+)/\d+\]t', lambda m : m.group(1), result)
        result = re.sub(' {2,}', ' ', result)
        result = re.sub(r'(Brilliance|Resistance|DMG|Barrier) (?!Recovery|&).*(%)+(?!&)', 
                        lambda m : m.group(0).replace(m.group(2), ""), result)
        result = re.sub(r'(%) (Brilliance|HP|\w* Barrier)', lambda m : m.group(0).replace(m.group(1), ""), result)

        return result

    def get_info(self):
        return f"|[[File:{ICONS[self.iconID]}.png|30px]]\n|{self.desc}"