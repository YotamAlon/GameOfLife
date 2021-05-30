import logging


class Cell(object):
    def __init__(self, x: int, y: int, is_alive=False):
        self.x = x
        self.y = y
        self.is_alive = is_alive

    def __str__(self):
        return f'Cell(x={self.x}, y={self.y}, {"alive" if self.is_alive else "dead"})'

    def __repr__(self):
        return str(self)

    def set_is_alive(self, is_alive):
        self.is_alive = is_alive


class GameState(object):
    def __init__(self) -> None:
        self.state = {}
        self.mins = [0, 0]
        self.maxs = [0, 0]

    def set_cell_life(self, cell: Cell, is_alive: bool) -> None:
        self.maxs = [max(self.maxs[0], cell.x), max(self.maxs[1], cell.y)]
        self.mins = [min(self.mins[0], cell.x), min(self.mins[1], cell.y)]
        logging.debug(f'self.maxs, self.mins: {self.maxs}, {self.mins}')
        if is_alive:
            self.state[(cell.x, cell.y)] = True
        else:
            del self.state[(cell.x, cell.y)]

    def get_living_cells(self):
        for x, y in self.state:
            yield Cell(x, y, is_alive=True)

    def get_living_neighbors(self, cell):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue

                try:
                    if self.state.get((cell.x + dx, cell.y + dy), False):
                        yield Cell(cell.x + dx, cell.y + dy, is_alive=True)
                except IndexError:
                    pass

    def get_dead_cells(self):
        for x in range(self.mins[0], self.maxs[0] + 2):
            for y in range(self.mins[1], self.maxs[1] + 2):
                if (x, y) not in self.state:
                    yield Cell(x, y, is_alive=False)


class GameOfLifeEngine(object):
    def __init__(self) -> None:
        self.state = GameState()

    def calculate_next_game_state(self) -> GameState:
        new_state = GameState()
        for cell in self.state.get_living_cells():

            neighbors = list(self.state.get_living_neighbors(cell))
            logging.debug(f'Cell {cell} has neighbors: {neighbors}')
            n_neighbors = len(neighbors)
            if 2 <= n_neighbors <= 3:
                logging.info(f'setting {cell} as alive because it has {n_neighbors} neighbors')
                new_state.set_cell_life(cell, is_alive=True)

        for cell in self.state.get_dead_cells():
            logging.debug(f'looking at {cell}')
            neighbors = list(self.state.get_living_neighbors(cell))
            logging.debug(f'Cell {cell} has neighbors: {neighbors}')
            n_neighbors = len(neighbors)
            if n_neighbors == 3:
                logging.info(f'setting {cell} as alive because it has {n_neighbors} neighbors')
                new_state.set_cell_life(cell, is_alive=True)

        return new_state

    def set_state(self, state: GameState):
        self.state = state
