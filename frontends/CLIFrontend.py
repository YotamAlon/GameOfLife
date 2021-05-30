import logging
from mvc_base import BaseFrontend, BaseModel


class CLIFrontend(BaseFrontend):
    def initialize(self, initial_state: BaseModel) -> None:
        self.view_state = initial_state
        self.get_initial_game_state()

    @staticmethod
    def generate_grid(game_state: BaseModel):
        return [[game_state.get_cell(x, y) for x in game_state.x_range] for y in game_state.y_range]

    def draw(self):
        print('\n'.join(['  '.join(['■' if cell.is_alive else '□' for cell in row])
                         for row in self.generate_grid(self.view_state)]))

    def update(self, state: BaseModel):
        self.view_state = state

    def show(self):
        while True:
            self.draw()
            self.get_next_instruction()

    def get_initial_game_state(self):
        more_input_remains = True
        while more_input_remains:
            self.draw()
            next_input = input('Enter the coordinates for next cell to turn alive (in the format "x,y") '
                               'or nothing to start the game:\n >>> ')
            if len(next_input) > 0:
                try:
                    x, y = next_input.replace(' ', '').split(',')
                    self.controller.update_cell(int(x), int(y), is_alive=True)
                except Exception as e:
                    logging.warning(f'An error occurred while input was being processed: {e}. '
                                    f'Maybe the input "{next_input}" is illegal? ')
                    print('You have entered an illegal input, please try again:')
            else:
                more_input_remains = False

    def get_next_instruction(self):
        next_input = input('Press enter to progress one generation or e to exit')
        if next_input == 'e':
            self.controller.exit()
        self.controller.next()

    def close(self):
        pass