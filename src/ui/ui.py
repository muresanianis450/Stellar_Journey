from src.game.game import Game

class ConsoleUI:

    def __init__(self):
        self.game = Game()

    def run(self):

        while not self.game.game_over:
            self.game.grid.display()
            command = input("Enter fire coordinate (e.g., G1) or type 'cheat' to reveal aliens: ").strip().upper()

            if command == "CHEAT":
                self.game.grid.display(reveal=True)
                continue

            self.game.fire(command)