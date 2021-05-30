from typing import List
from game_logic import GameState, Cell


class Instruction(object):
    def __init__(self, type_):
        self.type = type_


class BaseFrontend(object):
    def __init__(self, controller=None):
        self.controller = controller

    def draw(self, living_cells: List[Cell]) -> None:
        raise NotImplementedError()

    def get_initial_game_state(self) -> GameState:
        raise NotImplementedError()

    def get_next_instruction(self) -> Instruction:
        raise NotImplementedError()
