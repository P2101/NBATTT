import sys
import pygame
import pandas as pd
import random

df = pd.read_csv('info_players.csv', sep=';')
df

equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

first_r = []
second_r = []   
rands = random.sample(range(30), 6) # if i not in rands SI FAIG ASO DARRERA, ME TORNA UN DE BUIT, FER FUNCIÓ
count = 0

for i in rands:
    count += 1
    if count <= 3:
        first_r.append(equipos[i])
    else:
        second_r.append(equipos[i])
pygame.init()

size = 700, 750
screen = pygame.display.set_mode(size)
pygame.display.set_caption('NBA Tic Tac Toe')

white = 255, 255, 255

# Define los colores de los jugadores
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)
FONT_COLOR = (10, 10, 10)

# Fuente para mostrar el ganador
font = pygame.font.Font(None, 46)

# Inicializa una matriz para representar el tablero 4x4
board_state = [[' ', first_r[0], first_r[1], first_r[2]],
               [second_r[0], None, None, None],
               [second_r[1], None, None, None],
               [second_r[2], None, None, None]]

current_player = "X"  # Jugador actual, empieza con "X"
game_over = False
winner = None

# Función para verificar si hay un ganador
def check_winner(board_state):
    # Verifica filas
    for row in range(1, len(board_state)):
        if all(board_state[row][col] == current_player for col in range(1, len(board_state))):
            return current_player

    # Verifica columnas
    for col in range(4):
        if all(board_state[row][col] == current_player for row in range(1, len(board_state))):
            return current_player

    # Verifica diagonales
    if all(board_state[i][i] == current_player for i in range(1, len(board_state))) or all(board_state[i][len(board_state) - i] == current_player for i in range(1, len(board_state))):
        return current_player

    return None

# Función para dibujar el tablero
def draw_board():
    line_width = 15
    line_color = (0, 0, 0)  # Color negro

    # Dibuja un fondo blanco
    screen.fill(white)

    # Dibuja una línea de título sobre el juego
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, size[0], 20))

    # Dibuja las líneas horizontales y verticales del tablero
    for i in range(1, 5):
        # Líneas horizontales
        pygame.draw.line(screen, line_color, (0, i * size[1] // 4), (size[0], i * size[1] // 4), line_width)
        # Líneas verticales
        pygame.draw.line(screen, line_color, (i * size[0] // 4, 40), (i * size[0] // 4, size[1]), line_width)

    # Dibuja los valores en cada casilla
    for row in range(len(board_state)):
        for col in range(4):
            value = board_state[row][col]
            text = font.render(value, True, FONT_COLOR)
            text_rect = text.get_rect(center=((col * size[0] // 4) + size[0] // 8, (row * size[1] // 4) + 20 + size[1] // 8))
            screen.blit(text, text_rect)

# Función para dibujar el cuadro de entrada
def draw_input_box():
    pygame.draw.rect(screen, (0, 0, 0), (0, size[1] - 50, size[0], 50))
    pygame.draw.rect(screen, white, (10, size[1] - 40, size[0] - 20, 30))
    
draw = False
run = True
input_text = ""
input_box_active = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            clicked_row = (mouseY - 40) // (size[1] // 4)
            clicked_col = mouseX // (size[0] // 4)

            if board_state[clicked_row][clicked_col] is None:
                board_state[clicked_row][clicked_col] = current_player

                winner = check_winner(board_state)
                if not winner and all(all(cell is not None for cell in row) for row in board_state[1:]):
                    draw = True
                elif winner:
                    game_over = True
                else:
                    current_player = "O" if current_player == "X" else "X"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and input_box_active:
                # Guarda el texto ingresado y lo muestra en la casilla correspondiente
                input_box_active = False
                board_state[0][clicked_col] = input_text
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif input_box_active:
                input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica si se hizo clic en el cuadro de entrada
            if (10 <= event.pos[0] <= size[0] - 10) and (size[1] - 40 <= event.pos[1] <= size[1] - 10):
                input_box_active = not input_box_active

    # Dibuja el tablero en la pantalla
    draw_board()

    # Dibuja el cuadro de entrada
    draw_input_box()
    if input_box_active:
        pygame.draw.rect(screen, (0, 0, 0), (10, size[1] - 40, size[0] - 20, 30), 2)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(input_text, True, white)
        screen.blit(text_surface, (20, size[1] - 35))

    # Muestra el ganador si hay uno
    if draw:
        text = font.render("¡Empate!", True, FONT_COLOR)
        text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2.2))
        screen.blit(text, text_rect)

    if game_over:
        if winner:
            text = font.render("¡El jugador " + winner + " ha ganado!", True, FONT_COLOR)
        else:
            text = font.render("¡Empate!", True, FONT_COLOR)

        # Centra el texto en la parte superior de la pantalla
        text_rect = text.get_rect(center=(size[0] // 2.2, 80))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
