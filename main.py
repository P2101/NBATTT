import pandas as pd
import random

df = pd.read_csv('all_seasons.csv')
df
equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHH', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
 'MIN', 'NJN', 'NOH', 'NOK', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'SEA', 'TOR', 'UTA', 'VAN', 'WAS']

first_r = []
second_r = []
# CREC QUE POT TORNAR MATEIX NOMBRE 2 VEGADES, REPASSA    
rands = [random.randint(0, 36) for i in range(6) ] # if i not in rands SI FAIG ASO DARRERA, ME TORNA UN DE BUIT, FER FUNCIÓ
count = 0

for i in rands:
    count += 1
    if count <= 3:
        first_r.append(equipos[i])
    else:
        second_r.append(equipos[i])
print(first_r)
print(second_r)

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(row[col] == player for row in board):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def play_tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        name = input('Introduce el nombre del jugador:  ')
        teams = set(df[df['player_name'] == name.title()]['team_abbreviation'])
        print(teams)
        row = int(input(f"Player {current_player}, enter row (0, 1, 2): "))
        col = int(input(f"Player {current_player}, enter column (0, 1, 2): "))
        for team in teams:
            
            if first_r[row] in teams and second_r[col] in teams:
                print('correcto')
                break
                # return True
            else:
                print('incorrecto')
                break
                # return False
        # row = int(input(f"Player {current_player}, enter row (0, 1, 2): "))
        # col = int(input(f"Player {current_player}, enter column (0, 1, 2): "))

        if board[row][col] != " ":
            print("Cell already taken. Try again.")
            continue

        board[row][col] = current_player
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if all(board[i][j] != " " for i in range(3) for j in range(3)):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_tic_tac_toe()
