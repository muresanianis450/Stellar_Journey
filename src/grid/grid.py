import random

import random

class Grid:

    SIZE = 7
    COLUMNS = ["A", "B", "C", "D", "E", "F", "G"]

    def __init__(self):
        self.grid = [[" " for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.earth_position = (3, 3)  # Earth is at the center (row 4, col D)
        self.grid[self.earth_position[0]][self.earth_position[1]] = "E"
        self._asteroids = []
        self._aliens = []

    def is_valid_asteroid_position(self, row, col):
        if (row, col) == self.earth_position:
            return False

        # Check for adjacency
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if (row + dr, col + dc) in self._asteroids:
                    return False

        return True

    def place_asteroids(self, count=8):
        """Places exactly `count` asteroids, ensuring no two are adjacent in row, column, or diagonal."""

        self._asteroids = []  # Reset asteroid list
        available_positions = [
            (r, c) for r in range(self.SIZE) for c in range(self.SIZE) if (r, c) != self.earth_position
        ]
        random.shuffle(available_positions)

        for row, col in available_positions:
            if len(self._asteroids) >= count:
                break
            if self.is_valid_asteroid_position(row, col):
                self._asteroids.append((row, col))
                self.grid[row][col] = "*"

    def place_aliens(self):
        possible_positions = ([(0, col) for col in range(self.SIZE)] +
                              [(self.SIZE - 1, col) for col in range(self.SIZE)] +
                              [(row, 0) for row in range(self.SIZE)] +
                              [(row, self.SIZE - 1) for row in range(self.SIZE)])
        while True:
            self._aliens = random.sample(possible_positions, 2)
            if not (self._aliens[0][0] == self._aliens[1][0] or self._aliens[0][1] == self._aliens[1][1]):
                break

        for alien in self._aliens:
            self.grid[alien[0]][alien[1]] = "X"  # Hidden during actual gameplay

    def display(self, reveal=False):

        header = "    " + "   ".join(self.COLUMNS)
        print(header)
        print("  " + "-" * (self.SIZE * 4 - 1))

        for i in range(self.SIZE):
            row_display = f"{i + 1} |"
            for j in range(self.SIZE):
                if (i, j) in self._aliens and not reveal:
                    row_display += "   |"
                else:
                    row_display += f" {self.grid[i][j]} |"
            print(row_display)
            print("  " + "-" * (self.SIZE * 4 - 1))

        print()

    def get_asteroids(self):
        return self._asteroids

    def get_aliens(self):
        return self._aliens