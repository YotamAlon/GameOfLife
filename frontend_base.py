from game_logic import Grid


class Instruction(object):
    def __init__(self, type_):
        self.type = type_


class BaseFrontend(object):
    def __init__(self, controller=None):
        self.controller = controller

    def draw_grid(self, living_cells):
        raise NotImplementedError()

    def get_initial_game_state(self) -> Grid:
        raise NotImplementedError()

    def get_next_instruction(self) -> Instruction:
        raise NotImplementedError()
