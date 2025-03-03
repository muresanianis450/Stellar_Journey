import random
from src.grid.grid import Grid

class Game:

    def __init__(self):
        self.grid = Grid()
        self.grid.place_asteroids()
        self.grid.place_aliens()
        self.game_over = False

    def parse_coordinate(self, coordinate):

        """Converts user input (e.g., 'B3') into (row, col) indexes."""
        if len(coordinate) < 2 or coordinate[0] not in self.grid.COLUMNS:
            return None, None

        col = self.grid.COLUMNS.index(coordinate[0])
        try:
            row = int(coordinate[1:]) - 1  # Convert to 0-indexed row
            if row < 0 or row >= self.grid.SIZE:
                return None, None
            return row, col
        except ValueError:
            return None, None

    def fire(self, coordinate):
        """
        Fires at the given coordinate on the grid.
        :param coordinate: str - The coordinate to fire at, in the format 'A1' to 'G7'.
        """
        row, col = self.parse_coordinate(coordinate)

        if row is None or col is None:
            print("Invalid input. Use format: B3")
            return

        # If it hit asteroid
        if (row, col) in self.grid.get_asteroids():
            print("🪨You hit an asteroid! Try again.")
            return

        # If it hit alien
        if (row, col) in self.grid.get_aliens():
            print(f"🔥 Hit! Alien ship at {coordinate} destroyed.")
            self.grid.get_aliens().remove((row, col))
            self.grid.grid[row][col] = "-"  # Mark hit
            if not self.grid.get_aliens():
                print("All alien ships destroyed. You won! 🎉")
                self.game_over = True
                return
        else:
            print("❌Miss! Alien ships are moving.")

        self.move_aliens()
        # Update grid with new alien positions
        for alien in self.grid.get_aliens():
            self.grid.grid[alien[0]][alien[1]] = "X"

            # Check if an alien is adjacent to Earth
            if self.is_adjacent_to_earth(alien):
                print("An alien ship reached Earth. Game Over! 😭")
                self.game_over = True
                return

    def teleport_to_same_distance(self, position):

        row, col = position
        earth_row, earth_col = self.grid.earth_position
        distance = abs(row - earth_row) + abs(col - earth_col)

        possible_positions = [
            (r, c) for r in range(self.grid.SIZE) for c in range(self.grid.SIZE)
            if self.grid.grid[r][c] == " " and abs(r - earth_row) + abs(c - earth_col) == distance
        ]

        if possible_positions:
            return random.choice(possible_positions)
        else:
            return position  # If no valid position found, stay in the same place

    def move_closer(self, position):
        row, col = position
        earth_row, earth_col = self.grid.earth_position

        if row < earth_row:
            row += 1
        elif row > earth_row:
            row -= 1
        if col < earth_col:
            col += 1
        elif col > earth_col:
            col -= 1

        return row, col

    def move_aliens(self):
        """Moves the alien ships either closer to Earth or teleports to an empty square at the same distance."""
        new_positions = []

        # Clear old positions from grid
        for alien in self.grid.get_aliens():
            self.grid.grid[alien[0]][alien[1]] = " "  # Clear old position

        for alien in self.grid.get_aliens():
            if random.random() < 0.5:  # 50% chance to move closer
                new_pos = self.move_closer(alien)
            else:  # 50% chance to teleport to an empty square at the same distance
                new_pos = self.teleport_to_same_distance(alien)
            new_positions.append(new_pos)

        self.grid._aliens = new_positions

    def is_adjacent_to_earth(self, position):
        """Checks if there is an alien which is adjacent to earth"""
        row, col = position
        earth_row, earth_col = self.grid.earth_position
        return abs(row - earth_row) <= 1 and abs(col - earth_col) <= 1