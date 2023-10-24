import os
import pygame
import numpy as np
import time


# Función para choose map number
def choose_map():
    input_valid = False
    while not input_valid:
        maps = [m[3:] for m in os.listdir(os.path.join('..', '..', '..', '..')) if m[0:3]=='map']
        maps.append('random')
        n_map = input(f'Los mapas disponibles son:\n{maps}\nNº de mapa que desea explorar: ')
        if n_map in maps:
            input_valid = True
        else:
            print("La entrada no es un valor valido.")
    file = os.path.join('..', '..', '..', '..', f'map{n_map}', f'map{n_map}.csv') if n_map != 'random' else 'random'
    return file

# Función para volcar estructura de datos para mapa
def dumpMap(charMap):
    for line in charMap:
        print(line)

# Función para, de fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa
def load_map(filename, charMap):
    print(filename)
    if filename == 'random':
        input_valid = False
        while not input_valid:
            w = input('Anchura del mapa random: ')
            h = input('Altura del mapa random: ')
            try:
                w = int(w)
                h = int(h)
                input_valid = True
            except:
                ValueError("Altura y/o anchura no validas (solo valores enteros)")
        charMap = np.random.rand(h,w) # Generate random map of given height and width
        charMap = charMap.round(0) # Round the matrix to be binary (otherwise is float)
        charMap = np.char.mod('%d', charMap) # Convert to string
    else:
        with open(filename) as f:
            line = f.readline()
            while line:
                charLine = line.strip().split(',')
                charMap.append(charLine)
                line = f.readline()
    return charMap

# Función para tomar coords de inicio y fin
def get_start_end_coords(charMap):
    input_valid = False
    while not input_valid:
        print(f'Limites del mapa para el eje X: 0-{len(charMap)-1}\nLimites del mapa para el eje Y: 0-{len(charMap[0])-1}')
        START_X = input('X coordenada de inicio: ')
        START_Y = input('Y coordenada de inicio: ')
        END_X = input('X coordenada de destino: ')
        END_Y = input('Y coordenada de destino: ')
        try:
            # Convert it into integer
            START_X = int(START_X)
            START_Y = int(START_Y)
            END_X = int(END_X)
            END_Y = int(END_Y)
            if 0 <= START_X <= len(charMap)-1 and\
                0 <= START_Y <= len(charMap[0])-1 and\
                0 <= END_X <= len(charMap)-1 and\
                0 <= END_Y <= len(charMap[0])-1:
                input_valid = True
        except ValueError:
            print("Las entradas no son valores enteros.")
    return START_X, START_Y, END_X, END_Y

