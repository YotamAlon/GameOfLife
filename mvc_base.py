from typing import Iterable


class Request(object):
    def __init__(self, type_):
        self.type = type_


class BaseCell(object):
    def __init__(self, x: int, y: int, is_alive: bool):
        raise NotImplementedError()

    @property
    def x(self) -> int:
        raise NotImplementedError()

    @property
    def y(self) -> int:
        raise NotImplementedError()

    @property
    def is_alive(self) -> bool:
        raise NotImplementedError()

    def __str__(self):
        return f'Cell(x={self.x}, y={self.y}, {"alive" if self.is_alive else "dead"})'


class BaseModel(object):
    def initialize(self):
        raise NotImplementedError()

    @property
    def x_range(self) -> Iterable[int]:
        raise NotImplementedError()

    @property
    def y_range(self) -> Iterable[int]:
        raise NotImplementedError()

    def get_cell(self, x: int, y: int) -> BaseCell:
        raise NotImplementedError()

    def set_cell_life(self, cell: BaseCell, is_alive: bool) -> None:
        raise NotImplementedError()

    def get_living_cells(self) -> Iterable[BaseCell]:
        raise NotImplementedError()

    def get_living_neighbors(self, cell) -> Iterable[BaseCell]:
        raise NotImplementedError()

    def get_dead_cells(self) -> Iterable[BaseCell]:
        raise NotImplementedError()


class BaseController(object):
    def next(self):
        """Move to next game state"""
        raise NotImplementedError()

    def update_cell(self, x: int, y: int, is_alive: bool):
        raise NotImplementedError()

    def exit(self) -> None:
        """Close and cleanup"""
        raise NotImplementedError()


class BaseFrontend(object):
    view_state: BaseModel

    def __init__(self, controller: BaseController):
        self.controller = controller

    def show(self) -> None:
        """The main function of the view"""
        raise NotImplementedError()

    def update(self, state: BaseModel) -> None:
        """Update the view state with the latest game state"""
        raise NotImplementedError()

    def initialize(self, initial_state: BaseModel) -> None:
        """Initialze the view"""
        raise NotImplementedError()

    def close(self) -> None:
        """Close and cleanup"""
        raise NotImplementedError()
