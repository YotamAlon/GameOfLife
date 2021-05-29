from frontend_base import BaseFrontend
from game_logic import GameOfLifeEngine


class GameOfLifeController(object):
    def __init__(self):
        self.view: BaseFrontend = BaseFrontend()
        self.engine = GameOfLifeEngine()

    def set_frontend(self, frontend: BaseFrontend):
        self.view = frontend

    def run(self):
        grid = self.view.get_initial_game_state()
        self.engine.set_state(grid)

        while True:
            self.view.draw_grid(self.engine.grid)

            instruction = self.view.get_next_instruction()
            if instruction.type == 'exit':
                break
            elif instruction.type == 'next':
                grid = self.engine.calculate_next_game_state()
                self.engine.set_state(grid)
