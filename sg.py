import sys, os
from common import NAMES, SCHOOLS, ATTR, TYPE, RARITY, Skill, get_dress, download_img, write_line, ICONS, GACHA

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
    gacha_type = ""
    filename = ""
    code = -1
    
    def __init__(self, code, gacha_type, filename):
        info = get_dress(code)

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
        self.gacha_type = gacha_type
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

    def __get_img(self, code):
        filename = self.__get_full_name() + ".png"
        download_img(filename, code, "dress")
        return f"[[File:{filename}|center|750px]]"

    def __write(self, line: str):
        write_line(self.filename, line)

    def __get_full_name(self):    
        return f"{self.role} {self.chara}"

    def __get_first_name(self):
        name = self.chara.split()[0]
        if name == 'Liu':
            name = 'Meifan'
        return name

    def __get_rarity_word(self):
        return RARITY[self.rarity]
    
    def __get_gacha_type(self):
        return GACHA[self.gacha_type]

    def write_file(self):
        self.__write("{{Quote|{{" + self.__get_first_name() + "|" + self.message + "}}}}")
        self.__write(self.__get_img(self.code)+"\n")
        self.__write("==Details==\n" + \
            '{| class="article-table" style="margin:1em auto 1em auto; clear:both; text-align:center;' + \
                'font-weight:900; width:100%" cellspacing="1" cellpadding="1" border="0"')
        self.__write('!Stage Girl\n|<span style="font-weight: bold; font-size: 20px;" >' + \
            f'[[{self.chara}]]</span> [[{self.__get_full_name()}/Bond Story|【Bond Story】]]\n|-')
        self.__write(f"!School\n|[[{self.school}]]\n|-")
        self.__write(f"!Initial Rarity\n|[[File:{self.__get_rarity_word()}_Star_icon.png|center|90px]]\n|-")
        self.__write(f"!Element\n|[[File:{self.element} Element.png|30px]] {self.element}\n|-")
        self.__write(f"!Position\n|[[File:{self.position} Position.jpg]] {self.position}\n|-")
        self.__write(f"!Act Type\n|[[File:{self.act_type} Act Type.png]] {self.act_type}\n|-")
        self.__write("!Description\n|"+ self.desc + "\n|}")
        self.__write('\n==Acts==\n{| class="article-table" style="margin:1em auto 1em auto;' + \
            'clear:both; text-align:left; font-weight:900; width:100%" cellspacing="1" cellpadding="1" border="0"')
        for act in self.acts:
            self.__write(act.get_info())
        self.__write(self.climax_act.get_info())
        self.__write('! rowspan="3" |Auto Skill')
        for skill in self.auto_skills:
            self.__write(skill.get_info() + "\n|-")
        self.__write(self.unit_skill.get_info())
        self.__write(f"\n==Gallery==\n<tabber>\n3D Model=[[File:{self.__get_full_name()} 3D Model.png|left|300px]]")
        self.__write(f"|-|\nLive2D=[[File:{self.code}_live2d.png|center|300px]]\n</tabber>")
        self.__write(f"[[Category:Cards]]\n[[Category:{self.rarity}✰ Cards]]\n[[Category:{self.element}]]" + \
            f"\n[[Category:{self.act_type} Act Type]]\n[[Category:{self.position} Position]]")
        self.__write(f"[[Category:{self.__get_gacha_type()} Gacha Cards]]")

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
        print("py sg.py dresscode [-o filename] [--lim/bf/season]")
        exit(1)

    code = sys.argv[1]

    filename = "sg.txt"
    gacha_type = ""

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-o":
            filename = sys.argv[i + 1]
        elif '--' in sys.argv[i]:
            gacha_type = sys.argv[i][2:]

    with open(filename, "w", encoding="utf-8") as create:
        pass

    dress = Dress(code, gacha_type, filename)

    dress.write_file()

    os.startfile(filename)