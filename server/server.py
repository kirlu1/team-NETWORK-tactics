from core import Champion, Shape, Team, Match
from rich import print
from rich.prompt import Prompt
from rich.table import Table

import threading


def champ_dict_parse(champ_dict: str) -> Champion:
    dic = dict(champ_dict)
    newdic = {}
    for i in dic.values():
        x = i.remove('')
        name, rock, paper, scissors = x.split('|')
        dic[name] = Champion(name, float(rock), float(paper), float(scissors))
    return newdic

