import pygame
import sys

import pandas as pd

df = pd.read_csv('all_seasons.csv')
names = set(df['player_name'])


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

nba_name(names)
