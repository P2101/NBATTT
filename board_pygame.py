import sys
import pygame
import pandas as pd
import random
# from inputs import nba_name

df = pd.read_csv('info_players.csv', sep=';')
df

equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
names = set(df['player_name'])

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
# board_state = [[' ', first_r[0], first_r[1], first_r[2]],
#                [second_r[0], None, None, None],
#                [second_r[1], None, None, None],
#                [second_r[2], None, None, None]]

board_state = [[' ', None, None, None],
               [None, None, None, None],
               [None, None, None, None],
               [None, None, None, None]]

def load_and_resize_image(img_path, target_size):
    image = pygame.image.load(img_path)
    return pygame.transform.scale(image, target_size)


for i in range(3):
    # Cargar imágenes dinámicamente para first_r[0], first_r[1], first_r[2]
    img_path = f'teams/{first_r[i]}.png'
    board_state[0][i + 1] = load_and_resize_image(img_path, (140, 140))

for i in range(3):
    # Cargar imágenes dinámicamente para first_r[0], first_r[1], first_r[2]
    img_path = f'teams/{second_r[i]}.png'
    board_state[i + 1][0] = load_and_resize_image(img_path, (140, 140))

current_player = "X"  # Jugador actual, empieza con "X"
game_over = False
winner = None

def nba_name(names):
    pygame.init()

    # Configuración de la pantalla
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption('Input con Sugerencias en Pygame')

    # Colores
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Fuente
    font = pygame.font.Font(None, 36)

    # Nombres permitidos
    nombres_permitidos = names
    # nombres_permitidos = ['LeBron', 'Stephen', 'Kevin', 'Giannis', 'Luka', 'James', 'Nikola']
    user_input = ''
    suggestions = []
    selected_suggestion = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if suggestions:
                        user_input = suggestions[selected_suggestion]
                        if user_input in nombres_permitidos:
                            nombres_permitidos.remove(user_input)  # Elimina el nombre de la lista
                        suggestions = []  # Borra las sugerencias al enviar
                        selected_suggestion = 0  # Reinicia la selección de sugerencias
                    else:
                        if user_input:
                            print("Nombre ingresado:", user_input)
                            if user_input in nombres_permitidos:
                                nombres_permitidos.remove(user_input)  # Elimina el nombre de la lista
                            user_input = ''  # Borra el texto ingresado
                            suggestions = []  # Borra las sugerencias al enviar
                            selected_suggestion = 0  # Reinicia la selección de sugerencias
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                    suggestions = [nombre for nombre in nombres_permitidos if nombre.lower().startswith(user_input.lower())]
                    selected_suggestion = 0  # Reinicia la selección de sugerencias al borrar
                elif event.key == pygame.K_DOWN:  # Flecha hacia abajo para navegar por las sugerencias
                    selected_suggestion = (selected_suggestion + 1) % len(suggestions)
                else:
                    user_input += event.unicode
                    suggestions = [nombre for nombre in nombres_permitidos if nombre.lower().startswith(user_input.lower())]
                    selected_suggestion = 0  # Reinicia la selección de sugerencias al escribir

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, suggestion in enumerate(suggestions):
                    if 50 <= event.pos[0] <= 350 and 100 + i * 30 <= event.pos[1] <= 130 + i * 30:
                        user_input = suggestions[i]
                        if user_input in nombres_permitidos:
                            nombres_permitidos.remove(user_input)  # Elimina el nombre de la lista
                        suggestions = []  # Borra las sugerencias al seleccionar una
                        selected_suggestion = 0  # Reinicia la selección de sugerencias

        # Limpia la pantalla
        screen.fill(white)

        # Dibuja el cuadro de entrada
        pygame.draw.rect(screen, black, (50, 50, 300, 50), 2)

        # Dibuja el texto ingresado
        text_surface = font.render(user_input, True, black)
        screen.blit(text_surface, (60, 60))

        # Dibuja el menú desplegable de sugerencias
        if suggestions:
            for i, suggestion in enumerate(suggestions):
                pygame.draw.rect(screen, white, (50, 100 + i * 30, 300, 30))
                if i == selected_suggestion:
                    # Destaca la sugerencia seleccionada
                    pygame.draw.rect(screen, (200, 200, 200), (50, 100 + i * 30, 300, 30))
                text_surface = font.render(suggestion, True, black)
                screen.blit(text_surface, (60, 110 + i * 30))

        pygame.display.flip()

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

            if isinstance(value, str):  # Si es una cadena de texto
                text = font.render(value, True, FONT_COLOR)
                text_rect = text.get_rect(center=((col * size[0] // 4) + size[0] // 8, (row * size[1] // 4) + 20 + size[1] // 8))
                screen.blit(text, text_rect)
            elif isinstance(value, pygame.Surface):  # Si es una imagen cargada con Pygame
                # Ajusta las coordenadas para posicionar la imagen más arriba a la derecha
                img_x = (col * size[0] // 4) + size[0] // 28
                img_y = (row * size[1] // 4) + 40

                # Ajusta las coordenadas según tus necesidades específicas
                screen.blit(value, (img_x - 5, img_y - 5))
# Función para dibujar el cuadro de entrada
def draw_input_box():
    pygame.draw.rect(screen, (0, 0, 0), (0, size[1] - 50, size[0], 50))
    pygame.draw.rect(screen, white, (10, size[1] - 40, size[0] - 20, 30))
    
draw = False
run = True
input_text = ""
input_box_active = False
input_box_rect = pygame.Rect(10, size[1] - 40, size[0] - 20, 30)

# Variable para almacenar el nombre del jugador
player_name = ""
white = (255, 255, 255)
black = (0, 0, 0)

# Solicita al usuario que ingrese su nombre antes de comenzar el juego
# while not player_name:
#     # Limpia la pantalla
#     screen.fill(white)
    
#     # Dibuja un cuadro de entrada para el nombre del jugador
#     pygame.draw.rect(screen, black, (0, size[1] // 3, size[0], 50))
#     pygame.draw.rect(screen, white, (10, size[1] // 3 + 10, size[0] - 20, 30))
    
#     font = pygame.font.Font(None, 36)
#     text_surface = font.render("Ingresa tu nombre:", True, black)
#     screen.blit(text_surface, (10, size[1] // 3 + 60))
    
#     text_surface = font.render(player_name, True, black)
#     screen.blit(text_surface, (20, size[1] // 3 + 15))
    
#     pygame.display.flip()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RETURN:
#                 player_name = nba_name(names)  # Usa la función nba_name para obtener el nombre ingresado
#             elif event.key == pygame.K_BACKSPACE:
#                 player_name = player_name[:-1]
#             else:
#                 player_name += event.unicode

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
            if event.key == pygame.K_RETURN:
                if input_box_active:
                    # Utiliza la función nba_name() para obtener el nombre ingresado
                    input_text = nba_name(names)
                    input_box_active = False
                    # Establece el nombre ingresado en la casilla del tablero
                    board_state[0][clicked_col] = input_text
                    input_text = ""
                elif not game_over:
                    input_box_active = not input_box_active  # Activa o desactiva el cuadro de entrada
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif input_box_active:
                input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica si se hizo clic en el cuadro de entrada
            if (10 <= event.pos[0] <= size[0] - 10) and (size[1] - 40 <= event.pos[1] <= size[1] - 10):
                input_box_active = not input_box_active

         # Dibuja el cuadro de entrada (si está activo)
        if input_box_active:
            pygame.draw.rect(screen, (0, 0, 0), (10, size[1] - 40, size[0] - 20, 30), 2)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(input_text, True, white)
            screen.blit(text_surface, (20, size[1] - 35))

    # Dibuja el tablero en la pantalla
    draw_board()

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
