import sys, os
from common import NAMES, SCHOOLS, ATTR, TYPE, RARITY, Skill, get_json, download_img, ICONS

class Dress:
    chara = ""
    role = ""
    school = ""
    rarity = -1
    element = ""
    position = ""
    act_type = ""
    message = ""
    desc = ""
    acts = []
    climax_act = None
    auto_skills = []
    unit_skill = None
    is_lim = False
    filename = ""
    code = -1
    
    def __init__(self, code, is_lim, filename):
        url = "https://karth.top/api/dress/" + code + ".json"
        info = get_json(url)

        chara_code = info['basicInfo']['character']
        self.chara = NAMES[chara_code]
        self.role = info['basicInfo']['name']['en']
        self.school = SCHOOLS[int(str(chara_code)[0])]
        self.rarity = info['basicInfo']['rarity']
        self.element = ATTR[info['base']['attribute']]
        self.position = info['base']['roleIndex']['role'].capitalize()
        self.act_type = TYPE[info['base']['attackType']]
        self.message = info['basicInfo']['message']['en']
        self.desc = info['basicInfo']['description']['en']
        self.__init_acts(info['act'])
        self.__init_auto_skills(info['skills'])
        self.__init_group_skills(info['groupSkills'])
        self.is_lim = is_lim
        self.filename = filename
        self.code = code

    def __init_acts(self, acts):
        for key in acts:
            act = acts[key]['normalSkill']
            new = Act(act['name']['en'], act['iconID'], act['description']['en'])
            self.acts.append(new)

    def __init_auto_skills(self, skills):
        for key in skills:
            skill = skills[key]
            new = Skill(skill['iconID'], skill['info']['en'])
            self.auto_skills.append(new)

    def __init_group_skills(self, skills):
        climax_act = skills['climaxACT']
        self.climax_act = ClimaxAct(climax_act['name']['en'], climax_act['iconID'], climax_act['description']['en'])

        unit_skill = skills['unitSkill']
        self.unit_skill = UnitSkill(unit_skill['iconID'], unit_skill['info']['en'])

    def get_img(self, code):
        filename = self.get_full_name() + ".png"
        download_img(filename, code, "dress")
        return f"[[File:{filename}|center|750px]]"

    def write_line(self, line: str):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(line + '\n')

    def get_full_name(self):    
        return f"{self.role} {self.chara}"

    def get_first_name(self):
        name = self.chara.split()[0]
        if name == 'Liu':
            name = 'Meifan'
        return name

    def get_rarity_word(self):
        return RARITY[self.rarity]

    def write_file(self):
        self.write_line("{{Quote|{{" + self.get_first_name() + "|" + self.message + "}}}}")
        self.write_line(self.get_img(self.code)+"\n")
        self.write_line("==Details==\n" + \
            '{| class="article-table" style="margin:1em auto 1em auto; clear:both; text-align:center;' + \
                'font-weight:900; width:100%" cellspacing="1" cellpadding="1" border="0"')
        self.write_line('!Stage Girl\n|<span style="font-weight: bold; font-size: 20px;" >' + \
            f'[[{self.chara}]]</span> [[{self.get_full_name()}/Bond Story|【Bond Story】]]\n|-')
        self.write_line(f"!School\n|[[{self.school}]]\n|-")
        self.write_line(f"!Initial Rarity\n|[[File:{self.get_rarity_word()}_Star_icon.png|center|90px]]\n|-")
        self.write_line(f"!Element\n|[[File:{self.element} Element.png|30px]] {self.element}\n|-")
        self.write_line(f"!Position\n|[[File:{self.position} Position.jpg]] {self.position}\n|-")
        self.write_line(f"!Act Type\n|[[File:{self.act_type} Act Type.png]] {self.act_type}\n|-")
        self.write_line("!Description\n|"+ self.desc + "\n|}")
        self.write_line('\n==Acts==\n{| class="article-table" style="margin:1em auto 1em auto;' + \
            'clear:both; text-align:left; font-weight:900; width:100%" cellspacing="1" cellpadding="1" border="0"')
        for act in self.acts:
            self.write_line(act.get_info())
        self.write_line(self.climax_act.get_info())
        self.write_line('! rowspan="3" |Auto Skill')
        for skill in self.auto_skills:
            self.write_line(skill.get_info() + "\n|-")
        self.write_line(self.unit_skill.get_info())
        self.write_line(f"\n==Gallery==\n<tabber>\n3D Model=[[File:{self.get_full_name()} 3D Model.png|left|300px]]")
        self.write_line(f"|-|\nLive2D=[[File:{self.code}_live2d.png|center|300px]]\n</tabber>")
        self.write_line(f"[[Category:Cards]]\n[[Category:{self.rarity}✰ Cards]]\n[[Category:{self.element}]]" + \
            f"\n[[Category:{self.act_type} Act Type]]\n[[Category:{self.position} Position]]")
        if self.is_lim:
            self.write_line("[[Category:Premium Gacha Cards]]")

class UnitSkill(Skill):
    def __init__(self, iconID, desc):
        super().__init__(iconID, desc)

    def get_info(self):
        return "!Unit Skill\n" + super().get_info() + "\n|}"

class Act(Skill):
    name = ""
    
    def __init__(self, name, iconID, desc):
        super().__init__(iconID, desc)
        self.name = name

    def get_info(self):
        return f"!{self.name}\n" + super().get_info() + "\n|-"


class ClimaxAct(Act):
    def __init__(self, name, iconID, desc):
        super().__init__(name, iconID, desc)
    
    def get_info(self):
        return f'!style="background:#FC5252; color:#FFFFFF" |{self.name}\n' + \
        f'|style="background:#FFD1D1" |[[File:{ICONS[self.iconID]}.png|30px]]\n' + \
        f'|style="background:#FFD1D1" |{self.desc}\n|-'


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("py sg.py dresscode [-o filename] [--lim]")
        exit(1)

    code = sys.argv[1]

    filename = "sg.txt"
    is_lim = False

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-o":
            filename = sys.argv[i + 1]
        elif sys.argv[i] == "--lim":
            is_lim = True

    with open(filename, "w", encoding="utf-8") as create:
        pass

    dress = Dress(code, is_lim, filename)

    dress.write_file()

    os.startfile(filename)