class Cell(object):
    def __init__(self, x: int, y: int, is_alive=False):
        self.x = x
        self.y = y
        self.is_alive = is_alive

    def __str__(self):
        return f'{self.x}, {self.y}, {"alive" if self.is_alive else "dead"}'

    def set_is_alive(self, is_alive):
        self.is_alive = is_alive


class Grid(object):
    def __init__(self, size: int=10) -> None:
        self.size = size
        self._grid = [[Cell(x, y) for x in range(self.size)] for y in range(self.size)]

    def set_cell_life(self, cell: Cell, is_alive: bool) -> None:
        self._grid[cell.x][cell.y].set_is_alive(is_alive)

    def get_living_cells(self):
        for column in self._grid:
            for cell in column:
                if cell.is_alive:
                    yield cell

    def get_living_neighbors(self, cell):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 and dy != 0:
                    try:
                        if self._grid[cell.x + dx][cell.y + dy].is_alive:
                            yield self._grid[cell.x + dx][cell.y + dy]
                    except IndexError:
                        pass

    def get_dead_cells(self):
        for column in self._grid:
            for cell in column:
                if not cell.is_alive:
                    yield cell


class GameOfLifeEngine(object):
    def __init__(self) -> None:
        self.grid = Grid()

    def calculate_next_game_state(self) -> Grid:
        new_grid = Grid()
        for cell in self.grid.get_living_cells():
            n_neighbors = len(list(self.grid.get_living_neighbors(cell)))
            if 2 <= n_neighbors <= 3:
                new_grid.set_cell_life(cell, is_alive=True)

        for cell in self.grid.get_dead_cells():
            n_neighbors = len(list(self.grid.get_living_neighbors(cell)))
            if n_neighbors == 3:
                new_grid.set_cell_life(cell, is_alive=True)

        return new_grid

    def set_state(self, grid: Grid):
        self.grid = grid