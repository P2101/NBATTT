import pandas as pd
import random

df = pd.read_csv('all_seasons.csv')
df
# equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHH', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
#  'MIN', 'NJN', 'NOH', 'NOK', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'SEA', 'TOR', 'UTA', 'VAN', 'WAS']
equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

first_r = []
second_r = []   
rands = random.sample(range(30), 6) # if i not in rands SI FAIG ASO DARRERA, ME TORNA UN DE BUIT, FER FUNCIÓ
# rands = [random.randint(0, 36) for i in range(6) ] # if i not in rands SI FAIG ASO DARRERA, ME TORNA UN DE BUIT, FER FUNCIÓ
count = 0

for i in rands:
    count += 1
    if count <= 3:
        first_r.append(equipos[i])
    else:
        second_r.append(equipos[i])


def print_board(board):
    # Print column header
    print('  ', (' | '.join(first_r))) # row
    print('-----------------')

    # Print the board
    for i, row in enumerate(board):
        print(second_r[i], end=' | ') # column
        for element in row:
            print(element, end=' | ')
        print('\n-----------------')

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

def check_player():
    name = input('Introduce el nombre del jugador:  ')
    teams = set(df[df['player_name'] == name.title()]['team_abbreviation'])
    print(teams)
    return teams
    
def play_tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        teams = check_player()
        
        while True:
            try:
                row = int(input(f'Player {current_player} enter the row number (1-3): ')) - 1
                col = int(input(f'Player {current_player} enter the column number (1-3): ')) - 1

                # posar un if si està bé però ocupat que passi o si falla amb es jugador triat
                if 0 <= row < 3 and 0 <= col < 3:
                    break
                else:
                    print('Invalid input. Row and column numbers must be between 1 and 3.')
            except ValueError:
                print('Invalid input. Please enter a valid number.')
                
        if board[row][col] != " ":
            print("Cell already taken. Try again.")
            continue

        if all(board[i][j] != " " for i in range(3) for j in range(3)):
            print_board(board)
            print("It's a draw!")
            break     
        
        if first_r[row] in teams and second_r[col] in teams:
            board[row][col] = current_player
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
        else:
            print('Datos incorrectos')
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    play_tic_tac_toe()
