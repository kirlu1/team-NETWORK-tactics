from socket import socket
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from core import Champion, Shape, Match, Team
import pickle as pic


def print_match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')

def input_champ(sock: socket):
    prompt = sock.recv(1024).decode()
    if prompt == "Pick a champion: ":
        while 1:
            choice = input(prompt)
            sock.send(choice.encode())
            ans = sock.recv(1024).decode()
            print(ans)
            if ans[-5:] == "team.":
                break
    else:
        print(prompt)
        oppopicked = sock.recv(1024).decode()
        print(oppopicked)
        

sock = socket()
sock.connect(("tntserver",5555))

print(sock.recv(1024).decode())

print(sock.recv(1024).decode())

pickletable = sock.recv(4096)

champions = pic.loads(pickletable)

print(champions)
print("\n")

for _ in range(4):
    input_champ(sock)

print("\n")

match = pic.loads(sock.recv(2048))
print_match_summary(match)

print("\n\nGG")

sock.close()