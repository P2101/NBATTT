import pandas as pd
import random

df = pd.read_csv('all_seasons.csv')
df
equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHH', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
 'MIN', 'NJN', 'NOH', 'NOK', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'SEA', 'TOR', 'UTA', 'VAN', 'WAS']
# equipos filtrados --> habría que cambiar el 36 del random
#equipos = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 
 #'MIN', 'NJN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

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

name = input('Introduce el nombre del jugador:  ')
teams = set(df[df['player_name'] == name.title()]['team_abbreviation'])
print(teams)
num1 = int(input('Introduce un número: '))
num2 = int(input('Introduce un número: '))
for team in teams:
    
    if first_r[num1] in teams and second_r[num2] in teams:
        print('correcto')
        break
    else:
        print('incorrecto')
        break