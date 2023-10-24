#! /usr/bin/env python

"""
# Notación

Mapa

En mapa original:
** -2 visitado y malo
* 0: libre
* 1: ocupado (muro/obstáculo)

Vía código incorporamos:

* 2: visitado
* 3: start
* 4: goal

Nodo

N-id
* -2: parentId del nodo start
* -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Específico de implementación Python

* Índices empiezan en 0
* charMap


"""

# Initial values are hard-coded (A nivel mapa)
import os
import pygame
import numpy as np
import time
import sys

sys.path.append('..')
from utils import get_start_end_coords, load_map, dumpMap, choose_map


# Define Node class (A nivel grafo/nodo)
class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))
        
    def check_or_develop(self, charMap, nodes, n_nodes):
        for move in [[-1,0], [0,1], [1,0], [0,-1]]: # up, right, down, left
            tmpX, tmpY = self.x +move[0], self.y +move[1]
            if 0 <= tmpX <= len(charMap)-1 and\
               0 <= tmpY <= len(charMap[0])-1 : # Check its within boundaries
                if( charMap[tmpX][tmpY] == '4' ): # Goal reached
                    print("Ha llegado a su destino!!!")
                    return charMap, nodes, n_nodes, self.myId, True
                elif ( charMap[tmpX][tmpY] == '0' ): # Continue this way
                    print(f"Continuar por {tmpX}, {tmpY}")
                    time.sleep(0.5)
                    n_nodes +=1
                    newNode = Node(tmpX, tmpY, n_nodes, self.myId)
                    charMap[tmpX][tmpY] = '2'
                    nodes.insert(0, newNode)
                    return charMap, nodes, n_nodes, -1, False
        charMap[self.x][self.y] = '-2'
        return charMap, nodes[1:], n_nodes, -1, False # Dump node that was being investigated if no move worked



print('EXPLORAR EL MAPA DE MODO GREEDY/VORAZ')
FILE_NAME = choose_map() 
charMap = [] # Creamos estructura de datos para mapa
charMap = load_map(FILE_NAME, charMap)
START_X, START_Y, END_X, END_Y = get_start_end_coords(charMap)
# A nivel mapa, integramos la info que teníamos de start & end
charMap[START_X][START_Y] = '3' # 3: start
charMap[END_X][END_Y] = '4' # 4: goal

# Grafo búsqueda
init = Node(START_X, START_Y, 0, -2) # Creamos el primer nodo
nodes = [] # `nodes` contendrá los nodos del grafo
n_nodes = 0
nodes.append(init) # Añadimos el primer nodo a `nodes`

ok = False # Visualization purposes

# GREEDY ALGORITHM
done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

################################################################

pygame.init()

width, height = 720, 1280 #len(charMap[0])*70, len(charMap)*70
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption('DFS')
bg = 25,25,25
screen.fill(bg)
nxC, nyC = len(charMap),len(charMap[0])
dimCW = height / nxC
dimCH = width / nyC
image = np.matrix(charMap)

start = time.monotonic()

while not done:
    image = np.matrix(charMap)
    screen.fill(bg)

    if len(nodes) > 0:
        charMap, nodes, n_nodes, goalParentId, done = nodes[0].check_or_develop(charMap, nodes, n_nodes)
    else:
        print('Destino no alcanzable')
        done = True

    # Print everything on screen
    for x in range (0, nxC):
        for y in range (0, nyC):
            # Polygon that defines where you want to paint in the map for each square
            poly = [(x * dimCW, y *dimCH),
                            ((x+1) * dimCW, y *dimCH),
                            ((x+1) * dimCW, (y+1) *dimCH),
                            (x * dimCW, (y+1) *dimCH)]
                    
            if image[x,y] == '0': # Void
                pygame.draw.polygon(screen, (128,128,128), poly, 1)
            elif image[x,y] == '2': # Visited
                pygame.draw.polygon(screen, (250,128,114), poly, 0)
            elif image[x,y] == '-2': # Visited and no good
                pygame.draw.polygon(screen, (130,11,11), poly, 0)
            else:
                pygame.draw.polygon(screen, (255,255,255), poly, 0)

    x,y = START_X,START_Y
    poly = [(x * dimCW, y *dimCH),((x+1) * dimCW, y *dimCH),((x+1) * dimCW, (y+1) *dimCH),(x * dimCW, (y+1) *dimCH)]
    pygame.draw.polygon(screen, (0,255,0), poly, 0)

    x,y = END_X,END_Y
    poly = [(x * dimCW, y *dimCH),((x+1) * dimCW, y *dimCH),((x+1) * dimCW, (y+1) *dimCH),(x * dimCW, (y+1) *dimCH)]
    pygame.draw.polygon(screen, (255,0,0), poly, 0)

    pygame.display.flip()

    if done:
        print(round(time.monotonic()-start, 4))
        # Show result
        print('------------------------------------------------------')
        prev_x = END_X
        prev_y = END_Y
        while not ok:
            for node in nodes:
                if( node.myId == goalParentId ):
                    node.dump()
                    curr_x = node.x
                    curr_y = node.y
                    poly = [((prev_x+0.5)*dimCW, (prev_y+0.5)*dimCH),
                            ((curr_x+0.5)*dimCW, (prev_y+0.5)*dimCH),
                            ((curr_x+0.5)*dimCW, (curr_y+0.5)*dimCH),
                            ((prev_x+0.5)*dimCW, (curr_y+0.5)*dimCH)]
                    pygame.draw.polygon(screen, (0,255,0), poly, 1)
                    prev_x = curr_x
                    prev_y =curr_y
                    goalParentId = node.parentId
                    if( goalParentId == -2):
                        print('------------------------------------------------------')
                        ok = True
                pygame.display.flip()
        time.sleep(10)



