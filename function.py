import pygame
import sys
import pandas as pd

df = pd.read_csv('all_seasons.csv')
names = set(df['player_name'])

pygame.init()

# Configuración del juego
size = 400, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tic Tac Toe')

# Colores
white = 255, 255, 255
black = 0, 0, 0

# Fuente
font = pygame.font.Font(None, 36)

# Cuadro de entrada
input_text = ""
input_box_active = True
input_box_rect = pygame.Rect(50, 400, 200, 30)

# Tablero de Tic Tac Toe
board_state = [['', '', ''],
               ['', '', ''],
               ['', '', '']]

# Jugador actual
current_player = 'X'

# Opciones disponibles en el cuadro de entrada
suggestions = []
selected_suggestion = 0

# Bucle principal
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if input_box_active:
                if event.key == pygame.K_RETURN:
                    if suggestions:
                        # Establece el nombre de la sugerencia seleccionada como el nombre del jugador actual
                        input_text = suggestions[selected_suggestion]
                        input_box_active = False
                        suggestions = []  # Limpia la lista de sugerencias
                    elif input_text:
                        # Establece el nombre ingresado como el nombre del jugador actual
                        current_player = input_text
                        input_text = ""
                        input_box_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_DOWN:
                    selected_suggestion = (selected_suggestion + 1) % len(suggestions)
                elif event.key == pygame.K_UP:
                    selected_suggestion = (selected_suggestion - 1) % len(suggestions)
                else:
                    input_text += event.unicode
                    suggestions = [nombre for nombre in names if nombre.lower().startswith(input_text.lower())]
                    selected_suggestion = 0  # Reinicia la selección de sugerencias al escribir
        elif not input_box_active and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // 133
            clicked_col = mouseX // 133
            if board_state[clicked_row][clicked_col] == '':
                # Marcar la casilla con el nombre del jugador actual
                board_state[clicked_row][clicked_col] = current_player
                # Cambiar al siguiente jugador
                current_player = 'X' if current_player == 'O' else 'O'
                # Reiniciar el cuadro de entrada para el próximo turno
                input_text = ""
                input_box_active = True
                suggestions = []  # Limpia la lista de sugerencias

    # Dibuja el tablero
    screen.fill(white)
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, black, (col * 133, row * 133, 133, 133), 2)
            text_surface = font.render(board_state[row][col], True, black)
            text_rect = text_surface.get_rect(center=(col * 133 + 67, row * 133 + 67))
            screen.blit(text_surface, text_rect)

    # Dibuja el cuadro de entrada
    pygame.draw.rect(screen, black, input_box_rect, 2)
    text_surface = font.render(input_text, True, black)
    width = max(200, text_surface.get_width() + 10)
    input_box_rect.w = width
    screen.blit(text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

    # Dibuja el menú desplegable de sugerencias
    if suggestions:
        for i, suggestion in enumerate(suggestions):
            pygame.draw.rect(screen, white, (50, 430 + i * 30, 200, 30))
            if i == selected_suggestion:
                # Destaca la sugerencia seleccionada
                pygame.draw.rect(screen, (200, 200, 200), (50, 430 + i * 30, 200, 30))
            text_surface = font.render(suggestion, True, black)
            screen.blit(text_surface, (60, 440 + i * 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
