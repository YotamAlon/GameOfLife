from frontend_base import BaseFrontend, Instruction
from game_logic import Grid, Cell


class TextColor(object):
    base_sequence = '\033[{}m'
    default = white = '0'
    black = '47'

    def paint_text(self, text, color):
        color_code = getattr(self, color, None)
        if color_code is None:
            raise ValueError(f'TextColor does not support {color}')
        return f'{self.base_sequence.format(color_code)}{text}{self.base_sequence.format(self.default)}'


class DebuggingFrontend(BaseFrontend):
    def draw_grid(self, grid: Grid):
        [print(TextColor().paint_text(str(cell), 'black' if cell.is_alive else 'white'))
         for cell in grid.get_living_cells()]

    def get_initial_game_state(self) -> Grid:
        grid = Grid()
        more_input_remains = True
        while more_input_remains:
            self.draw_grid(grid)
            next_input = input('Enter the coordinates for next cell to turn alive (in the format "x,y")'
                               'or nothing to start the game:\n >>> ')
            if len(next_input) > 0:
                try:
                    x, y = next_input.replace(' ', '').split(',')
                    cell = Cell(int(x), int(y), is_alive=True)
                    grid.set_cell_life(cell, is_alive=True)
                except:
                    print('You have entered an illegal input, please try again:')
            else:
                more_input_remains = False

        return grid

    def get_next_instruction(self) -> Instruction:
        try:
            input('Press enter to progress one generation or ctrl + c to exit')
        except KeyboardInterrupt:
            return Instruction(type_='exit')
        return Instruction(type_='next')
