import sys
from typing import Type
from mvc_base import BaseFrontend, BaseController, BaseModel
from game_logic import GameOfLifeEngine


class GameOfLifeController(BaseController):
    def __init__(self, model: Type[BaseModel], view: Type[BaseFrontend]):
        self.view = view(self)
        self.model = model()
        self.engine = GameOfLifeEngine(model)

    def set_state(self, model: BaseModel) -> None:
        self.model = model

    def update_cell(self, x: int, y: int, is_alive: bool):
        cell = self.model.get_cell(x, y)
        self.model.set_cell_life(cell, is_alive=is_alive)
        self.view.update(self.model)

    def next(self):
        game_state = self.engine.calculate_next_game_state(self.model)
        self.set_state(game_state)
        self.view.update(game_state)

    def initialize(self):
        self.model.initialize()
        self.view.initialize(self.model)
        self.view.show()

    def exit(self):
        self.view.close()
        sys.exit()
