import logging
from mvc_base import BaseFrontend, Request
from game_logic import GameState, Cell


class CLIFrontend(BaseFrontend):
    def initialize(self) -> None:
        self.view_state = GameState()
        self.get_initial_game_state()

        request = Request(type_='update_state')
        request.state = self.view_state
        self.controller.handle_request(request)

    @staticmethod
    def generate_grid(game_state: GameState):
        return [[Cell(x, y, is_alive=game_state.get_cell(x, y).is_alive) for x in game_state.x_range]
                for y in game_state.y_range]

    def draw(self):
        print('\n'.join(['  '.join(['■' if cell.is_alive else '□' for cell in row])
                         for row in self.generate_grid(self.view_state)]))

    def update(self, state: GameState):
        self.view_state = state

    def show(self):
        while True:
            self.draw()
            request = self.get_next_instruction()
            self.controller.handle_request(request)

    def get_initial_game_state(self):
        more_input_remains = True
        while more_input_remains:
            self.draw()
            next_input = input('Enter the coordinates for next cell to turn alive (in the format "x,y") '
                               'or nothing to start the game:\n >>> ')
            if len(next_input) > 0:
                try:
                    x, y = next_input.replace(' ', '').split(',')
                    cell = Cell(int(x), int(y), is_alive=True)
                    self.view_state.set_cell_life(cell, is_alive=True)
                    logging.info(str(list(self.view_state.get_living_cells())))
                except Exception as e:
                    logging.warning(f'An error occurred while input was being processed: {e}. '
                                    f'Maybe the input "{next_input}" is illegal? ')
                    print('You have entered an illegal input, please try again:')
            else:
                more_input_remains = False

    @staticmethod
    def get_next_instruction() -> Request:
        next_input = input('Press enter to progress one generation or e to exit')
        if next_input == 'e':
            return Request(type_='exit')
        return Request(type_='next')

    def close(self):
        pass
