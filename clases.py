# clases.py
import numpy as np
from random import randint
from variables import SHIPS, BOARD_SIZE, WATER, SHIP, HIT, MISS

class Board:
    def __init__(self, player_id):
        self.player_id = player_id
        self.size = BOARD_SIZE
        self.grid = np.full((self.size, self.size), WATER)  # Tablero visible
        self.ship_grid = np.full((self.size, self.size), WATER)  # Tablero oculto con los barcos
        self.ships = []  # Lista de coordenadas de barcos

        # Coloca los barcos en posiciones fijas o aleatorias
        self.place_ships()

    def place_ships(self):
        for ship_name, length in SHIPS.items():
            for _ in range(SHIPS[ship_name]):
                placed = False
                while not placed:
                    placed = self.place_single_ship(length)

    def place_single_ship(self, length):
        direction = randint(0, 3)  # 0 = Norte, 1 = Sur, 2 = Este, 3 = Oeste
        x = randint(0, self.size - 1)
        y = randint(0, self.size - 1)

        coordinates = []
        if direction == 0:  # Norte
            if x - length >= 0:
                coordinates = [(x - i, y) for i in range(length)]
        elif direction == 1:  # Sur
            if x + length < self.size:
                coordinates = [(x + i, y) for i in range(length)]
        elif direction == 2:  # Este
            if y + length < self.size:
                coordinates = [(x, y + i) for i in range(length)]
        else:  # Oeste
            if y - length >= 0:
                coordinates = [(x, y - i) for i in range(length)]

        if all(self.ship_grid[coord[0], coord[1]] == WATER for coord in coordinates):
            for coord in coordinates:
                self.ship_grid[coord[0], coord[1]] = SHIP
            self.ships.append(coordinates)
            return True
        return False

    def shoot(self, x, y):
        # Verificar si ya se ha disparado en la coordenada
        if self.grid[x, y] == HIT or self.grid[x, y] == MISS:
            return "Ya has disparado en esta coordenada. Intenta con otra."
        if self.ship_grid[x, y] == SHIP:
            self.grid[x, y] = HIT
            return "Disparo certero"
        else:
            self.grid[x, y] = MISS
            return "Disparo fallido"

    def display(self): #Muestra el tablero simulando una tabla con un indicador de columna y de fila para indicar las coordenadas
        columnas = "   " + " ".join(f"{i:2}" for i in range(self.size))
        print(columnas)
        print("   " + "-" * (self.size * 3))
        for i, fila in enumerate(self.grid):
            fila_completa = " ".join(f"{cell:2}" for cell in fila)
            print(f"{i:2} | {fila_completa}")

    def display_full_board(self): #Muestra el tablero con la ubicacion de los barcos
        full_board = np.where(self.ship_grid == SHIP, SHIP, self.grid)
        columnas = "   " + " ".join(f"{i:2}" for i in range(self.size))
        print(columnas)
        print("   " + "-" * (self.size * 3))
        for i, fila in enumerate(full_board):
            fila_completa = " ".join(f"{cell:2}" for cell in fila)
            print(f"{i:2} | {fila_completa}")

    def is_sunk(self, ship_coordinates):
        return all(self.grid[x, y] == HIT for x, y in ship_coordinates)
