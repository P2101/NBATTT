import sys
import pygame

pygame.init()

size = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('NBA Tic Tac Toe')

white = 255, 255, 255

# Define los colores de los jugadores
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)
FONT_COLOR = (0, 0, 0)

# Fuente para mostrar el ganador
font = pygame.font.Font(None, 36)

# Inicializa una matriz para representar el tablero
board_state = [[None, None, None],
               [None, None, None],
               [None, None, None]]

current_player = "X"  # Jugador actual, empieza con "X"
game_over = False
winner = None

# Función para verificar si hay un ganador
def check_winner(board_state):
    # Verifica filas
    for row in board_state:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    # Verifica columnas
    for col in range(3):
        if board_state[0][col] == board_state[1][col] == board_state[2][col] and board_state[0][col] is not None:
            return board_state[0][col]

    # Verifica diagonales
    if board_state[0][0] == board_state[1][1] == board_state[2][2] and board_state[0][0] is not None:
        return board_state[0][0]
    if board_state[0][2] == board_state[1][1] == board_state[2][0] and board_state[0][2] is not None:
        return board_state[0][2]

    return None

# Función para dibujar el tablero
def draw_board():
    line_width = 15
    line_color = (0, 0, 0)  # Color negro

    # Dibuja un fondo blanco
    screen.fill(white)

    # Dibuja las líneas horizontales y verticales del tablero
    for i in range(1, 3):
        # Líneas horizontales
        pygame.draw.line(screen, line_color, (0, i * size[1] // 3), (size[0], i * size[1] // 3), line_width)
        # Líneas verticales
        pygame.draw.line(screen, line_color, (i * size[0] // 3, 0), (i * size[0] // 3, size[1]), line_width)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Maneja los clics del mouse si el juego no ha terminado
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            clicked_row = mouseY // 200
            clicked_col = mouseX // 200

            if board_state[clicked_row][clicked_col] is None:
                board_state[clicked_row][clicked_col] = current_player
                current_player = "O" if current_player == "X" else "X"

                winner = check_winner(board_state)
                if winner:
                    game_over = True

    # Dibuja el tablero en la pantalla
    draw_board()

    # Dibuja las fichas en el tablero
    for row in range(3):
        for col in range(3):
            if board_state[row][col] == "X":
                pygame.draw.line(screen, PLAYER_X_COLOR, (col * 200, row * 200), ((col + 1) * 200, (row + 1) * 200), 10)
                pygame.draw.line(screen, PLAYER_X_COLOR, ((col + 1) * 200, row * 200), (col * 200, (row + 1) * 200), 10)
            elif board_state[row][col] == "O":
                pygame.draw.circle(screen, PLAYER_O_COLOR, (col * 200 + 100, row * 200 + 100), 80, 10)

    # Muestra el ganador si hay uno
    if game_over:
        if winner:
            text = font.render("¡El jugador " + winner + " ha ganado!", True, FONT_COLOR)
        else:
            text = font.render("¡Empate!", True, FONT_COLOR)

        # Centra el texto en la parte superior de la pantalla
        text_rect = text.get_rect(center=(size[0] // 2, 50))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
