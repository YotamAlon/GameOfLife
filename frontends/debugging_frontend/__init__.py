from frontend_base import BaseFrontend, Instruction
from game_logic import Grid, Cell


class DebuggingFrontend(BaseFrontend):
    def draw_grid(self, grid: Grid):
        for row in grid._grid:
            print('  '.join(['■' if cell.is_alive else '□' for cell in row]))

    def get_initial_game_state(self) -> Grid:
        grid = Grid()
        more_input_remains = True
        while more_input_remains:
            self.draw_grid(grid)
            next_input = input('Enter the coordinates for next cell to turn alive (in the format "x,y") '
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
        next_input = input('Press enter to progress one generation or e to exit')
        if next_input == 'e':
            return Instruction(type_='exit')
        return Instruction(type_='next')
