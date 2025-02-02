from core import Champion, Shape, Team, Match
from rich import print
from rich.prompt import Prompt
from rich.table import Table
import pickle as pic
import threading as thr
from socket import socket,AF_INET,SOCK_DGRAM
import time

def input_champion(picker: int,
                   champions: dict[Champion],
                   picking: list[str],
                   waiting: list[str],
                   psock: socket,
                   wsock: socket) -> None:

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    print(f'Player {picker} is picking')
    psock.send("Pick a champion: ".encode())
    wsock.send("Opponent is picking.".encode())
    
    while True:
        match psock.recv(1024).decode():
            case name if name not in champions:
                msg = f'The champion {name} is not available. Try again.'
                psock.send(msg.encode())
            case name if name in picking:
                msg = f'{name} is already in your team. Try again.'
                psock.send(msg.encode())
            case name if name in waiting:
                msg = f'{name} is in the enemy team. Try again.'
                psock.send(msg.encode())
            case _:
                picking.append(name)
                pmsg = f'{name} is now on your team.'
                wmsg = f'The opponent picked {name}.'
                print(f'Player {picker} picked {name}')
                psock.send(pmsg.encode())
                wsock.send(wmsg.encode())
                break

def print_champs(champions: dict[Champion]):

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    return available_champs


def main() -> None:
    sock = socket()
    sock.bind(("",5555))
    sock.listen()
    
    while 1:
        print("Waiting for players...")
        p1, _ = sock.accept()
        print("Player 1 connected.")
        p1.send("You are [bold red]Red[/bold red]. Waiting for opponent...\n".encode())
        p2, _ = sock.accept()
        print("Player 2 connected.")
        p2.send("You are [blue]Blue[/blue].\n".encode())
        plrs = [p1,p2]
        welcomemsg = "\nWelcome to [bold yellow]Team Network Tactics[/bold yellow]!\nEach player chooses a champion each turn.\n".encode()
        time.sleep(1)
        for i in plrs:
            i.send(welcomemsg)

        DBsock = socket(AF_INET,SOCK_DGRAM)
        DBsock.sendto(" ".encode(),("tntdb",5555))
        picklechamp = DBsock.recv(4096)
        champions = pic.loads(picklechamp)
        
        pickletable = pic.dumps(print_champs(champions))
        
        for i in plrs:
            i.send(pickletable)

        player1 = []
        player2 = []

        time.sleep(1)
        # Champion selection
        for _ in range(2):
            input_champion(1, champions, player1, player2, p1, p2)
            input_champion(2, champions, player2, player1, p2, p1)

        # Match
        match = Match(
            Team([champions[name] for name in player1]),
            Team([champions[name] for name in player2])
        )
        match.play()

        # Send match results to players
        picklematch = pic.dumps(match)
        for i in plrs:
            i.send(picklematch)
            i.close()
        print("Game finished\n")


if __name__ == '__main__':
    main()
