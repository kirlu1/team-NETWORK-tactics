from core import Champion
from socket import socket, AF_INET, SOCK_DGRAM
import pickle as pic


def _parse_champ(champ_text: str) -> Champion:
    name, rock, paper, scissors = champ_text.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))


def from_csv(filename: str) -> dict[str, Champion]:
    champions = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            champ = _parse_champ(line)
            champions[champ.name] = champ
    return champions


def load_some_champs():
    return from_csv('some_champs.txt')

sock = socket(AF_INET,SOCK_DGRAM)

sock.bind(("",5555))

while 1:
    _, source = sock.recvfrom(1)
    print("Sending...")
    load = load_some_champs()
    ans = pic.dumps(load)
    sock.sendto(ans,source)
