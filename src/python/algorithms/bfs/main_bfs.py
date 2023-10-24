#! /usr/bin/env python

"""
# Notactión

## Mapa

En mapa original:

* 0: libre
* 1: ocupado (muro/obstáculo)

Vía código incorporamos:

* 2: visitado
* 3: start
* 4: goal

## Nodo

Nós
* -2: parentId del nodo start
* -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Específico de implementación Python

* Índices empiezan en 0
* charMap
"""

# # Initial values are hard-coded (A nivel mapa)
import os
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

print('EXPLORAR EL MAPA DE MODO ANCHURA')
FILE_NAME = choose_map() 
charMap = [] # Creamos estructura de datos para mapa
charMap = load_map(FILE_NAME, charMap)

# ## A nivel mapa, integramos la info que teníamos de start & end
START_X, START_Y, END_X, END_Y = get_start_end_coords(charMap)
charMap[START_X][START_Y] = '3' # 3: start
charMap[END_X][END_Y] = '4' # 4: goal

# Volcamos mapa por consola

dumpMap(charMap)

# # Grafo búsqueda

# ## Creamos el primer nodo
init = Node(START_X, START_Y, 0, -2)
# init.dump() # comprobar que primer nodo bien

# ## `nodes` contendrá los nodos del grafo

nodes = []
fully_dev_nodes = []

# ## Añadimos el primer nodo a `nodes`

nodes.append(init)

# ## Empieza algoritmo

done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

import pygame
import numpy as np
import time

pygame.init()

width, height = 720, 1280 #len(charMap[0])*70, len(charMap)*70
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption('BFS')
bg = 25,25,25
screen.fill(bg)
nxC, nyC = len(charMap),len(charMap[0])
dimCW = height / nxC
dimCH = width / nyC
image = np.matrix(charMap)

start = time.monotonic()

while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    image = np.matrix(charMap)
    screen.fill(bg)
    explore = [node for node in nodes if node not in fully_dev_nodes]
    print('nodes')
    print([n.myId for n in nodes])
    print('explore')
    print([n.myId for n in explore])
    if len(explore) == 0:
        done = True
        print('Not possible')
    for node in explore:
        node.dump()
        exp = 0
        # up
        tmpX = node.x - 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("up: GOALLLL!!!")
            goalParentId = node.myId  # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("up: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        else:
            exp +=1

        # down
        tmpX = node.x + 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("down: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("down: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        else:
            exp +=1

        # right
        tmpX = node.x
        tmpY = node.y + 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("right: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("right    : mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        else:
            exp +=1

        # left
        tmpX = node.x
        tmpY = node.y - 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("left: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("left: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        else:
            exp +=1

        if exp == 4:
            fully_dev_nodes.append(node)

        # Print everything on screen
        image = np.matrix(charMap)
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
    time.sleep(0.5)


# Display solución hallada
ok = False
end = time.monotonic()
prev_x = END_X
prev_y = END_Y

print(round(end-start, 4))

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
                ok = True
                pygame.display.flip()
time.sleep(10)


