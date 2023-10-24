# Búsqueda en mapas
Autora: Silvia Romero Azpitarte
NIA: 100505917
<hr>

## Cómo instalar / ejecutar
```sh
pip install -r requirements.txt
```
Una vez instalados los requisitos se puede ejecutar el código escribiendo el comando:
```sh
cd dfs
python3 main_dfs.py # Para el codigo en profundidad
```
o
```sh
cd bfs
python3 main_bfs.py # Para el codigo en anchura
```

## DFS/greedy/voraz/en profundidad
Las mejoras incorporadas en el algoritmo greedy, a parte de la modificación del código BFS para que sea DFS han sido:
- Control de errores
- Selección del mapa por comando
- Generación de mapas aleatorios
- Visualización de la búsqueda en el mapa en tiempo de ejecución
- Selección del punto de origen y destino por comando
- Mejora del código BFS para que las comparaciones temporales sean más realistas
- Temporizadores para la comparación con el tiempo en BFS
- Intento de implementación de SE(2) para que pueda girar el robot. (No me ha salido pero el código está en `main_dfs_se2.py`, donde intenté familiarizarme con el código).


## BFS/en anchura
Las mejoras incorporadas en anchura comprenden la incorporación de una interfaz gráfica para ver mejor cómo se extiende la búsqueda por el mapa.
Asimismo, se han incorporado unos temporizadores para poder hacer la comparativa de tiempo de ejecución entre las aproximaciones BFS y DFS.
Se ha mejorado la estructura del código para no volver a explorar nodos que estén completamente desarrollados

## Resultados
Los resultados de los temporizadores y la comparativa de ejecución se muestran en el excel: `ComparativaTemporal.csv`. Tal y como se aprecia, BFS tarda menos pero ocuparía más espacio en memoria, al tener desarrollados todos los nodos en todo momento conforme se avanza por el mapa. Además, como se aprecia en la carpeta de `imgs`, BFS siempre devuelve el camino más óptimo, mientras que DFS resuelve una solución a fuerza bruta.