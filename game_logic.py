import logging
from typing import Type
from mvc_base import BaseModel


class GameOfLifeEngine(object):
    def __init__(self, model_class: Type[BaseModel]):
        self.model_class = model_class

    def calculate_next_game_state(self, state: BaseModel) -> BaseModel:
        new_state = self.model_class()
        for cell in state.get_living_cells():
            neighbors = list(state.get_living_neighbors(cell))
            logging.debug(f'Cell {cell} has neighbors: {neighbors}')
            n_neighbors = len(neighbors)
            if 2 <= n_neighbors <= 3:
                logging.info(f'setting {cell} as alive because it has {n_neighbors} neighbors')
                new_state.set_cell_life(cell, is_alive=True)

        for cell in state.get_dead_cells():
            logging.debug(f'looking at {cell}')
            neighbors = list(state.get_living_neighbors(cell))
            logging.debug(f'Cell {cell} has neighbors: {neighbors}')
            n_neighbors = len(neighbors)
            if n_neighbors == 3:
                logging.info(f'setting {cell} as alive because it has {n_neighbors} neighbors')
                new_state.set_cell_life(cell, is_alive=True)

        return new_state
