import pygame
import sys
import pandas as pd
import random

df = pd.read_csv('all_seasons.csv')
names = set(df['player_name'])

equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
names = set(df['player_name'])

first_r = []
second_r = []   
rands = random.sample(range(30), 6)
count = 0

for i in rands:
    count += 1
    if count <= 3:
        first_r.append(equipos[i])
    else:
        second_r.append(equipos[i])

pygame.init()

# Game Configuration
size = 600, 760
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tic Tac Toe')

# Colors
white = 255, 255, 255
black = 0, 0, 0

# Font
font = pygame.font.Font(None, 36)

# Input Box
input_text = ""
input_box_active = True
input_box_rect = pygame.Rect(50, 650, 500, 30)

# Tic Tac Toe Board (4x4)
board_state = [[' ', '', '', ''],
               ['', '', '', ''],
               ['', '', '', ''],
               ['', '', '', '']]

def load_and_resize_image(img_path, target_size):
    image = pygame.image.load(img_path)
    return pygame.transform.scale(image, target_size)

def draw_image(image, rect):
    if image:
        screen.blit(image, rect)

for i in range(3):
    # Load and resize images for first_r[0], first_r[1], first_r[2]
    img_path = f'teams/{first_r[i]}.png'
    board_state[0][i + 1] = load_and_resize_image(img_path, (140, 140))

for i in range(3):
    # Load and resize images for second_r[0], second_r[1], second_r[2]
    img_path = f'teams/{second_r[i]}.png'
    board_state[i + 1][0] = load_and_resize_image(img_path, (140, 140))

# Current Player
current_player = 'X'

# Suggestions
suggestions = []
selected_suggestion = 0

# Function to check for a winner or draw
def check_winner():
    winner = None

    # Check rows and columns (excluding first row and column)
    for i in range(1, 4):
        if all(board_state[i][j] == current_player for j in range(1, 4)):
            winner = current_player
        if all(board_state[j][i] == current_player for j in range(1, 4)):
            winner = current_player

    # Check diagonals (excluding first row and column)
    if all(board_state[i][i] == current_player for i in range(1, 4)):
        winner = current_player
    if all(board_state[i][4 - i] == current_player for i in range(1, 4)):
        winner = current_player

    return winner

def check_player(name):
    teams = set(df[df['player_name'] == name]['team_abbreviation'])
    print(teams)
    return teams

# Main Game Loop
run = True
invalid_move_message = None
invalid_move_timer = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if input_box_active:
                if event.key == pygame.K_RETURN:
                    if suggestions:
                        input_text = suggestions[selected_suggestion]
                        input_box_active = False
                        suggestions = []  # Clear suggestions list
                    elif input_text:
                        current_player = input_text
                        input_text = ""
                        input_box_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_b:
                    # Si se presiona la tecla "B", borra la selección actual
                    input_text = ""
                elif event.key == pygame.K_DOWN:
                    selected_suggestion = (selected_suggestion + 1) % len(suggestions)
                elif event.key == pygame.K_UP:
                    selected_suggestion = (selected_suggestion - 1) % len(suggestions)
                else:
                    input_text += event.unicode
                    suggestions = [nombre for nombre in names if nombre.lower().startswith(input_text.lower())]
                    selected_suggestion = 0  # Reset suggestion selection when typing
            else:
                # Si la caja de entrada no está activa, permitir escribir un nuevo nombre
                input_box_active = True
                input_text += event.unicode
                suggestions = [nombre for nombre in names if nombre.lower().startswith(input_text.lower())]
                selected_suggestion = 0  # Reset suggestion selection when typing

        elif not input_box_active and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            # Verificar si hizo clic en la caja de entrada
            if input_box_rect.collidepoint(mouseX, mouseY):
                input_text = ""  # Borrar texto si hizo clic en la caja de entrada
            else:
                clicked_row = mouseY // 150
                clicked_col = mouseX // 150

                # Ignore clicks in the first row and first column
                if 0 < clicked_row < 4 and 0 < clicked_col < 4 and board_state[clicked_row][clicked_col] == '':
                    # Obtener los nombres de los equipos en las casillas correspondientes
                    team1 = first_r[clicked_col-1]
                    team2 = second_r[clicked_row-1]

                    print(f"Team 1: {team1}")
                    print(f"Team 2: {team2}")
                    print(f"Input Text: {input_text}")

                    # Verificar si el jugador seleccionado está entre los dos equipos
                    player_teams = check_player(input_text)
                    if team1 in player_teams and team2 in player_teams:
                        print("Valid move!")
                        board_state[clicked_row][clicked_col] = current_player
                        winner = check_winner()
                        if winner:
                            print(f"Player {winner} wins!")
                            run = False
                        elif all(all(cell != '' for cell in row[1:]) for row in board_state[1:]):
                            print("It's a draw!")
                            run = False

                        current_player = 'X' if current_player == 'O' else 'O'
                        input_text = ""
                        input_box_active = True
                        suggestions = []
                    else:
                        print("Invalid move!")
                        invalid_move_message = "Invalid move!"
                        invalid_move_timer = 270  # 3 segundos a 60 fps
                        current_player = 'X' if current_player == 'O' else 'O'
                        input_text = ""
                        input_box_active = True
                        suggestions = []

    # Draw the Board
    screen.fill(white)
    for row in range(4):
        for col in range(4):
            pygame.draw.rect(screen, black, (col * 150, row * 150, 150, 150), 2)
            if isinstance(board_state[row][col], pygame.Surface):
                draw_image(board_state[row][col], (col * 150 + 5, row * 150 + 5))
            else:
                text_surface = font.render(str(board_state[row][col]), True, black)
                text_rect = text_surface.get_rect(center=(col * 150 + 75, row * 150 + 75))
                screen.blit(text_surface, text_rect)

    # Draw the Input Box
    pygame.draw.rect(screen, black, input_box_rect, 2)
    text_surface = font.render(input_text, True, black)
    width = max(500, text_surface.get_width() + 10)
    input_box_rect.w = width
    screen.blit(text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

    # Draw Suggestions
    if suggestions:
        for i, suggestion in enumerate(suggestions):
            pygame.draw.rect(screen, white, (50, 680 + i * 30, 500, 30))
            if i == selected_suggestion:
                pygame.draw.rect(screen, (200, 200, 200), (50, 680 + i * 30, 500, 30))
            text_surface = font.render(suggestion, True, black)
            screen.blit(text_surface, (60, 690 + i * 30))

    # Draw Invalid Move Message
    if invalid_move_message:
        pygame.draw.rect(screen, (255, 0, 0), (0, 0, size[0], 30))
        text_surface = font.render(invalid_move_message, True, white)
        screen.blit(text_surface, (10, 5))
        invalid_move_timer -= 1
        if invalid_move_timer <= 0:
            invalid_move_message = None

    pygame.display.flip()

pygame.quit()
sys.exit()
