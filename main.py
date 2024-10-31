import numpy as np

def max_matching(matriz_inc):
    """
    Calcula el emparejamiento máximo en un grafo bipartito dado por una matriz de incidencia.

    Parámetros:
    matriz_inc (numpy.ndarray): Matriz de incidencia donde los elementos son 1 si existe arista entre los vértices y 0 si no.

    Retorna:
    tuple: Una lista de pares (x, y) donde x es un vértice del conjunto X y y es un vértice del conjunto Y,
           y el número total de emparejamientos máximos encontrados.
    """
    n, m = matriz_inc.shape
    match_y = [-1] * m  # Arreglo para almacenar las coincidencias de vértices en Y

    def dfs(x, visitado):
        """
        Busca un camino de aumentación usando búsqueda en profundidad (DFS) desde el vértice x.

        Parámetros:
        x (int): El vértice actual del conjunto X.
        visitado (list): Lista que indica si un vértice en Y ha sido visitado durante esta DFS.

        Retorna:
        bool: True si se encontró un camino de aumentación, False de lo contrario.
        """
        for y in range(m):
            # Si existe una arista y el vértice y no ha sido visitado
            if matriz_inc[x][y] == 1 and not visitado[y]:
                visitado[y] = True
                print(f"Intentando expandir camino desde X[{x+1}] hacia Y[{y+1}]")
                # Si y no está emparejado o podemos reasignarlo
                if match_y[y] == -1 or dfs(match_y[y], visitado):
                    print(f"Emparejando X[{x+1}] con Y[{y+1}]")
                    match_y[y] = x
                    return True
                else:
                    print(f"Y[{y+1}] ya está emparejado y no se puede reasignar")
        return False

    max_match = 0
    for x in range(n):
        visitado = [False] * m
        if dfs(x, visitado):
            max_match += 1

    emparejamiento = [(match_y[y], y) for y in range(m) if match_y[y] != -1]
    return emparejamiento, max_match

def matching(matriz_inc):
    """
    Imprime el emparejamiento máximo y el número máximo de emparejamientos
    para la matriz de incidencia dada.

    Parámetros:
    matriz_inc (numpy.ndarray): Matriz de incidencia para la cual se calcula el emparejamiento máximo.
    """
    print(matriz_inc)
    emparejamiento, max_match = max_matching(matriz_inc)
    emparejamiento = np.array(emparejamiento) + 1  # Convertir a 1-indexado
    print("Emparejamiento máximo:\n", emparejamiento)
    print("Número máximo de emparejamientos:", max_match)
    print("\n\n")

# Ejemplo de uso con matrices de incidencia diferentes
matriz_inc1 = np.array([
    [0, 1, 1, 1],
    [0, 1, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 1],
])
matching(matriz_inc1)

matriz_inc2 = np.array([
    [0, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
])
matching(matriz_inc2)

matriz_inc3 = np.array([
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [1, 0, 0, 1, 0],
])
matching(matriz_inc3)



"""import pandas as pd
import numpy as np

def metodo_hungaro(data):
    # Asegurarse de que la matriz es cuadrada agregando filas o columnas de ceros
    if data.shape[0] != data.shape[1]:
        max_dim = max(data.shape)
        data = data.reindex(index=data.index.union([f"Extra_Row_{i}" for i in range(max_dim - data.shape[0])]),
                            columns=data.columns.union([f"Extra_Col_{i}" for i in range(max_dim - data.shape[1])]),
                            fill_value=0)

    print("---Data Original---")
    print(data)

    # Primera iteracion por filas
    data = data.subtract(data.min(axis=1), axis=0)
    print("\n---Primera Iteracion por Filas---\n")
    print(data)

    # Segunda iteracion por columnas
    data = data.subtract(data.min(axis=0), axis=1)
    print("\n---Segunda Iteracion por Columnas---\n")
    print(data)

    # Identificar las intersecciones minimas necesarias automaticamente
    filas_tachadas = set()
    columnas_tachadas = set()
    while len(filas_tachadas) + len(columnas_tachadas) < len(data):
        min_val = np.inf
        min_pos = (None, None)

        # Buscar el menor valor sin tachar
        for i in data.index:
            if i not in filas_tachadas:
                for j in data.columns:
                    if j not in columnas_tachadas and data.at[i, j] < min_val:
                        min_val = data.at[i, j]
                        min_pos = (i, j)

        # Realizar el tachado de filas y columnas
        fila_min, col_min = min_pos
        filas_tachadas.add(fila_min)
        columnas_tachadas.add(col_min)

        # Ajustar la matriz con el valor minimo no tachado
        for i in data.index:
            for j in data.columns:
                if i not in filas_tachadas and j not in columnas_tachadas:
                    data.at[i, j] -= min_val
                elif i in filas_tachadas and j in columnas_tachadas:
                    data.at[i, j] += min_val

    print("\n---Resultado Final---\n")
    print(data)

    # Determinar la asignacion optima
    asignaciones = []
    filas_asignadas = set()
    columnas_asignadas = set()
    for i in data.index:
        for j in data.columns:
            if data.at[i, j] == 0 and i not in filas_asignadas and j not in columnas_asignadas:
                asignaciones.append((i, j, original_data.at[i, j]))
                filas_asignadas.add(i)
                columnas_asignadas.add(j)

    print("\n---Asignacion Optima---\n")
    for fila, columna, costo in asignaciones:
        print(f"Asignar fila {fila} a columna {columna}, costo: {costo}")

# Ejemplo de uso
data = pd.DataFrame({
    'Persona_1': [9, 11, 14, 11, 7],
    'Persona_2': [6, 15, 13, 13, 10],
    'Persona_3': [12, 13, 6, 8, 8],
    'Persona_4': [8, 8, 9, 11, 12],
    'Persona_5': [10, 12, 8, 9, 11]
}, index=['Tarea_1', 'Tarea_2', 'Tarea_3', 'Tarea_4', 'Tarea_5'])

# Guardamos una copia del original para calcular costos
original_data = data.copy()
metodo_hungaro(data)


# Ejemplo de uso
data2 = pd.DataFrame({
    "P1": [82, 83, 69, 92],
    "P2": [77, 37, 49, 92],
    "P3": [11, 69, 5, 86],
    "P4": [8, 9, 98, 23]
}, index=['T1', 'T2', 'T3', 'T4'])

# Guardamos una copia del original para calcular costos
original_data = data2.copy()
metodo_hungaro(data2)
"""