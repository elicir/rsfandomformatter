import re, requests

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

def get_json(url):
    res = requests.get(url).json()
    return res

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
        return f"|[[File: PLACEHOLDER.png|30px]]\n|{self.desc}"