from typing import Iterable
from peewee import IntegerField, Model, SqliteDatabase, fn, DoesNotExist
from mvc_base import BaseCell, BaseModel

db = SqliteDatabase(':memory:')


class Cell(Model, BaseCell):
    X = IntegerField()
    Y = IntegerField()
    state_id = IntegerField()

    class Meta:
        database = db

    def __init__(self, *args, **kwargs):
        if (len(args) == 3 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], bool)) \
                or (len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int)
                    and isinstance(kwargs.get('is_alive'), bool)):
            super().__init__(X=args[0], Y=args[1])
            if (len(args) == 3 and args[2]) or kwargs.get('is_alive'):
                self.save()
        else:
            super().__init__(*args, **kwargs)

    @property
    def x(self) -> int:
        return self.X

    @property
    def y(self) -> int:
        return self.Y

    @property
    def is_alive(self) -> bool:
        return not self.is_dirty()


class SQLiteState(BaseModel):
    def initialize(self):
        db.connect()
        db.create_tables([Cell])

    def get_value(self, cell_field, func, default):
        return Cell.select(func(cell_field)).where(Cell.state_id == id(self)).scalar() or default

    @property
    def x_range(self) -> Iterable[int]:
        return range(self.get_value(Cell.X, fn.MIN, 0), self.get_value(Cell.X, fn.MAX, 0) + 1)

    @property
    def y_range(self) -> Iterable[int]:
        return range(self.get_value(Cell.Y, fn.MIN, 0), self.get_value(Cell.Y, fn.MAX, 0) + 1)

    def get_cell(self, x: int, y: int) -> BaseCell:
        try:
            return Cell.get(X=x, Y=y, state_id=id(self))
        except DoesNotExist:
            return Cell(x, y, is_alive=False)

    def set_cell_life(self, cell: BaseCell, is_alive: bool) -> None:
        if is_alive:
            Cell.replace(X=cell.x, Y=cell.y, state_id=id(self)).execute()
        else:
            Cell.delete().where(X=cell.x, Y=cell.y, state_id=id(self)).execute()

    def get_living_cells(self) -> Iterable[BaseCell]:
        return Cell.select().where(Cell.state_id == id(self))

    def get_living_neighbors(self, cell) -> Iterable[BaseCell]:
        return Cell.select().where(Cell.X.between(cell.x - 1, cell.x + 1), Cell.Y.between(cell.y - 1, cell.y + 1),
                                   Cell.X != cell.x, Cell.Y != cell.y, Cell.state_id == id(self))

    def get_dead_cells(self) -> Iterable[BaseCell]:
        existing_x_y_pairs = {(cell.X, cell.Y) for cell in Cell.select(Cell.X, Cell.Y).where(Cell.state_id == id(self))}
        for x in self.x_range:
            for y in self.y_range:
                if (x, y) not in existing_x_y_pairs:
                    yield Cell(x, y, is_alive=False)
