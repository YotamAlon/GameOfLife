import logging
from frontend_base import BaseFrontend, Instruction
from game_logic import GameState, Cell


class CLIFrontend(BaseFrontend):
    @staticmethod
    def generate_grid(game_state: GameState):
        return [[Cell(x, y, is_alive=game_state.get_cell(x, y).is_alive) for x in game_state.x_range]
                for y in game_state.y_range]

    def draw(self, game_state: GameState):
        print('\n'.join(['  '.join(['■' if cell.is_alive else '□' for cell in row])
                         for row in self.generate_grid(game_state)]))

    def get_initial_game_state(self) -> GameState:
        initial_state = GameState()
        more_input_remains = True
        while more_input_remains:
            self.draw(initial_state)
            next_input = input('Enter the coordinates for next cell to turn alive (in the format "x,y") '
                               'or nothing to start the game:\n >>> ')
            if len(next_input) > 0:
                try:
                    x, y = next_input.replace(' ', '').split(',')
                    cell = Cell(int(x), int(y), is_alive=True)
                    initial_state.set_cell_life(cell, is_alive=True)
                    logging.info(str(list(initial_state.get_living_cells())))
                except:
                    print('You have entered an illegal input, please try again:')
            else:
                more_input_remains = False

        return initial_state

    def get_next_instruction(self) -> Instruction:
        next_input = input('Press enter to progress one generation or e to exit')
        if next_input == 'e':
            return Instruction(type_='exit')
        return Instruction(type_='next')
