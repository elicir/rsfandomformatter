import sys, os

from common import NAMES, RARITY, Skill, get_json, download_img, is_naming_limit

class Equip:
    name = ""
    profile = ""
    charas = []
    rarity = -1
    skill = None
    instant_skill = None
    filename = ""
    code = -1
    
    def __init__(self, code, filename):
        url = "https://karth.top/api/equip/" + code + ".json"
        info = get_json(url)
        self.name = info['basicInfo']['name']['en']
        self.profile = info['basicInfo']['profile']['en']
        self.__init_charas(info['basicInfo']['charas'])
        self.rarity = info['basicInfo']['rarity']
        self.__init_skills(info['skill'], info['activeSkill'])
        self.filename = filename
        self.code = code

    def __init_charas(self, chara_list):
        for code in chara_list:
            self.charas.append(NAMES[code])

    def __init_skills(self, skill, instant_skill):
        if instant_skill == 0:
            self.instant_skill = None
        else:
            cost = (instant_skill['cost'][0], instant_skill['cost'][-1])
            init = (instant_skill['execution']['firstExecutableTurns'][0], instant_skill['execution']['firstExecutableTurns'][-1])
            turns = (instant_skill['execution']['recastTurns'][0], instant_skill['execution']['recastTurns'][-1])
            limit = (instant_skill['execution']['executeLimitCounts'][0], instant_skill['execution']['executeLimitCounts'][-1])
            self.instant_skill = InstantSkill(instant_skill['iconID'], instant_skill['info']['en'], cost, init, turns, limit)
        self.skill = Skill(skill['iconID'], skill['info']['en'])

    def get_names(self):
        result = ""
        for i in range(len(self.charas)):
            result += f"[[{self.charas[i]}]]"
            if i < len(self.charas) - 1:
                result += ", "
        return result
        
    def get_img(self, code):
        filename = self.name + ".png"
        download_img(filename, code, "equip")
        return f"[[File:{filename}|center|750px]]"

    def write_line(self, line: str):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(line + '\n')

    def get_rarity_word(self):
        return RARITY[self.rarity]
    
    def __fix_name(self):
        self.name = self.name.replace("[", "-").replace("]", "-")

    def write_file(self):
        if is_naming_limit(self.name):
            self.write_line("{{NamingLimitNotice|" + self.name + "}}")
            self.__fix_name()
        self.write_line("{{Quote|" + self.profile + "}}")
        self.write_line(self.get_img(self.code)+"\n")
        self.write_line("==Details==\n" + \
            '{| class="article-table" style="margin:1em auto 1em auto; clear:both; text-align:center;' + \
                'font-weight:900; width:100%" cellspacing="1" cellpadding="1" border="0"')
        self.write_line(f'!Rarity\n| colspan="2"|[[File:{self.get_rarity_word()}_Star_icon.png|center|90px]]\n|-')
        self.write_line(f'!Stage Girl(s)\n| colspan="2"|{self.get_names()}\n|-')
        self.write_line("!Auto Skill\n" + self.skill.get_info())
        if self.instant_skill is not None:
            self.write_line("|-\n" + self.instant_skill.get_info())
        self.write_line("|}")

        self.write_line(f"[[Category:Memoirs]]\n[[Category:{self.rarity}✰ Memoirs]]")
        if self.instant_skill is not None:
            self.write_line("[[Category:Instant Skill]]")

class InstantSkill(Skill):
    cost = (0, 0)
    init = (0, 0)
    turns = (0, 0)
    limit = (0, 0)

    def __init__(self, iconID, desc, cost, init, turns, limit):
        super().__init__(iconID, desc)
        self.cost = cost
        self.init = init
        self.turns = turns
        self.limit = limit

    def get_info(self):
        return "!Instant Skill\n" + super().get_info() + \
            f"<br><small>Cost: {self.cost[0]} (MAX - {self.cost[1]})</small><br>" + \
            f"<small>Cooldown: {self.init[0]} turns (MAX - {self.init[1]}) (initial), {self.turns[0]} turns (MAX - {self.turns[1]})</small><br>" + \
                f"<small>Max No. of Uses: {self.limit[0]} (MAX - {self.limit[1]})</small>"


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("py sg.py equipcode [-o filename]")
        exit(1)

    code = sys.argv[1]

    filename = "memoir.txt"

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-o":
            filename = sys.argv[i + 1]

    with open(filename, "w", encoding="utf-8") as create:
        pass

    equip = Equip(code, filename)

    equip.write_file()

    os.startfile(filename)