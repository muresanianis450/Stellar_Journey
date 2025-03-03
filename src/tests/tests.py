from src.game.game import Game
from src.grid.grid import Grid

def tests():
    game = Game()

    # Test firing at an empty space
    initial_aliens_count = len(game.grid.get_aliens())
    game.fire("A1")
    assert len(game.grid.get_aliens()) == initial_aliens_count

    # Test firing at an asteroid
    asteroid_position = game.grid.get_asteroids()[0]
    asteroid_coordinate = f"{Grid.COLUMNS[asteroid_position[1]]}{asteroid_position[0] + 1}" #making it a string so the function works properly
    game.fire(asteroid_coordinate)
    assert len(game.grid.get_aliens()) == initial_aliens_count

    alien_position = game.grid.get_aliens()[0]
    alien_coordinate = f"{Grid.COLUMNS[alien_position[1]]}{alien_position[0] + 1}"  # string cause the function requires a str
    game.fire(alien_coordinate)
    assert len(game.grid.get_aliens()) == initial_aliens_count - 1

    # Tests firing at the same alien twice
    game.fire(alien_coordinate)
    assert len(game.grid.get_aliens()) == initial_aliens_count - 1

    # Test game over condition
    for alien in game.grid.get_aliens()[:]:
        alien_coordinate = f"{Grid.COLUMNS[alien[1]]}{alien[0] + 1}"
        game.fire(alien_coordinate)
    assert game.game_over