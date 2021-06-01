import logging

from mvc_base import BaseCell, BaseModel


class Cell(BaseCell):
    def __init__(self, x: int, y: int, is_alive=False):
        self._x = x
        self._y = y
        self._is_alive = is_alive

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def is_alive(self) -> bool:
        return self._is_alive


class MemoryState(BaseModel):
    def __init__(self) -> None:
        self.state = {}
        self.mins = [0, 0]
        self.maxs = [0, 0]

    def initialize(self):
        pass

    @property
    def x_range(self):
        return range(self.mins[0] - 1, self.maxs[0] + 2)

    @property
    def y_range(self):
        return range(self.mins[1] - 1, self.maxs[1] + 2)

    def get_cell(self, x, y):
        return Cell(x, y, is_alive=self.state.get((x, y), False))

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
        for x in self.x_range:
            for y in self.y_range:
                if (x, y) not in self.state:
                    yield Cell(x, y, is_alive=False)
